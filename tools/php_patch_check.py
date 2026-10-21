#!/usr/bin/env python3
"""
php_patch_check.py — PHP2Shell patch-status checker
===================================================

Determines whether a PHP version is exposed to PHP2Shell
(CVE-2026-109618 / CVE-2026-109619) and what to do about it.

This is a DEFENSIVE asset-inventory tool. It compares version strings against
the published fixed-build matrix (data/affected_versions.json). It contains no
exploit code, sends no network traffic, and does nothing to any remote system.
It answers one question about hosts you already run: "patch, backport, or pull
the plug?"

Usage
-----
  # one version string
  php_patch_check.py 8.3.20

  # the PHP on this machine (runs `php -v`)
  php_patch_check.py --local

  # a whole inventory (CSV with a `php_version` column; see data/inventory.example.csv)
  php_patch_check.py --inventory hosts.csv
  php_patch_check.py --inventory hosts.csv --format csv  > triage.csv
  php_patch_check.py --inventory hosts.csv --format json > triage.json

  # machine-readable single check
  php_patch_check.py 8.1.29 --json

Exit codes (useful in CI / cron gates)
--------------------------------------
  0  all checked versions SAFE
  1  at least one VULNERABLE — patch available (supported branch)
  2  at least one VULNERABLE — no upstream fix / abandoned (EOL)
  3  usage or data error

Update the fixed builds in data/affected_versions.json as PHP ships new patch
releases; this tool trusts that file.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.normpath(os.path.join(HERE, "..", "data", "affected_versions.json"))

# severity -> process exit code contribution
SEVERITY_EXIT = {0: 0, 1: 1, 2: 2, 3: 2}


# ----------------------------------------------------------------------------- data
def load_matrix(path=DATA):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            return json.load(fh)
    except (OSError, ValueError) as exc:
        sys.stderr.write("error: cannot read version matrix %s: %s\n" % (path, exc))
        sys.exit(3)


# --------------------------------------------------------------------------- parsing
VERSION_RE = re.compile(r"(\d+)\.(\d+)(?:\.(\d+))?")
# a distro/custom package suffix means the number may be a backport target
DISTRO_SUFFIX_RE = re.compile(r"\d+\.\d+\.\d+[-+~].+")


def parse_version(raw):
    """Return (major, minor, patch, had_suffix) or None if unparseable."""
    if raw is None:
        return None
    s = str(raw).strip()
    # tolerate 'PHP 8.3.20 (cli)...' and bare '8.3.20'
    m = VERSION_RE.search(s)
    if not m:
        return None
    major = int(m.group(1))
    minor = int(m.group(2))
    patch = int(m.group(3)) if m.group(3) is not None else 0
    had_suffix = bool(DISTRO_SUFFIX_RE.search(s))
    return (major, minor, patch, had_suffix)


def branch_key(major, minor):
    return "%d.%d" % (major, minor)


def cmp_tuple(a, b):
    return (a > b) - (a < b)


# -------------------------------------------------------------------------- classify
def classify(raw_version, matrix):
    """Return a verdict dict for one version string."""
    verdicts = matrix["verdicts"]
    parsed = parse_version(raw_version)
    result = {
        "input": raw_version,
        "version": None,
        "branch": None,
        "branch_status": None,
        "fixed_build": None,
        "verdict": "unknown",
        "severity": verdicts["unknown"]["severity"],
        "label": verdicts["unknown"]["label"],
        "action": "Version could not be parsed. Treat as exposed until verified.",
        "note": None,
    }
    if not parsed:
        return result

    major, minor, patch, had_suffix = parsed
    result["version"] = "%d.%d.%d" % (major, minor, patch)
    bkey = branch_key(major, minor)
    result["branch"] = bkey

    branch = next((b for b in matrix["branches"] if b["branch"] == bkey), None)
    if branch is None:
        # unknown branch (e.g. a future 8.6 or an exotic build): be conservative
        result["note"] = "Branch %s is not in the matrix." % bkey
        v = verdicts["unknown"]
        result.update(verdict="unknown", severity=v["severity"], label=v["label"],
                      action="Unknown branch — confirm against php.net and treat as exposed until verified.")
        return result

    result["branch_status"] = branch["status"]
    result["fixed_build"] = branch["fixed_build"]

    # Supported branch with a fixed build -> version arithmetic
    if branch["fixed_build"]:
        fb = parse_version(branch["fixed_build"])
        is_at_or_above = cmp_tuple((major, minor, patch), fb[:3]) >= 0
        if is_at_or_above:
            # distro suffix at/above the number is fine (and often backported lower too)
            v = verdicts["safe"]
            result.update(verdict="safe", severity=v["severity"], label=v["label"],
                          action="At or above the fixed build. Confirm workers were restarted after upgrade.")
            return result
        # below the fixed build
        if had_suffix:
            # distro package below the upstream number MAY still carry a backport
            v = verdicts["verify-vendor"]
            result.update(verdict="verify-vendor", severity=v["severity"], label=v["label"],
                          action=("Distro/custom package below upstream %s. The fix may be backported "
                                  "without bumping the number — confirm against your vendor's security "
                                  "advisory before trusting the version alone." % branch["fixed_build"]))
            result["note"] = "Package suffix detected; upstream arithmetic is not authoritative for distro builds."
            return result
        v = verdicts["patch-available"]
        result.update(verdict="patch-available", severity=v["severity"], label=v["label"],
                      action=branch["action"])
        return result

    # EOL branch -> no upstream fix; severity by backport availability
    vkey = branch["verdict_if_below"]
    v = verdicts.get(vkey, verdicts["unknown"])
    result.update(verdict=vkey, severity=v["severity"], label=v["label"], action=branch["action"])
    return result


# ---------------------------------------------------------------------------- inputs
def read_local_version():
    """Run `php -v` on this host and return the raw first line, or None."""
    try:
        out = subprocess.check_output(["php", "-v"], stderr=subprocess.STDOUT, timeout=10)
        return out.decode("utf-8", "replace").splitlines()[0]
    except FileNotFoundError:
        sys.stderr.write("error: `php` not found on PATH. Pass a version string instead.\n")
        return None
    except (subprocess.SubprocessError, IndexError) as exc:
        sys.stderr.write("error: could not run `php -v`: %s\n" % exc)
        return None


def read_inventory(path):
    """Yield dict rows from an inventory CSV that has a php_version column."""
    try:
        with open(path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames or "php_version" not in reader.fieldnames:
                sys.stderr.write("error: inventory CSV needs a 'php_version' column. "
                                 "See data/inventory.example.csv.\n")
                sys.exit(3)
            for row in reader:
                yield row
    except OSError as exc:
        sys.stderr.write("error: cannot read inventory %s: %s\n" % (path, exc))
        sys.exit(3)


# --------------------------------------------------------------------------- display
RESET, BOLD, DIM = "\033[0m", "\033[1m", "\033[2m"
COLOR = {0: "\033[32m", 1: "\033[33m", 2: "\033[31m", 3: "\033[31m"}  # green / amber / red


def tty():
    return sys.stdout.isatty() and os.environ.get("NO_COLOR") is None


def paint(text, sev):
    if not tty():
        return text
    return "%s%s%s" % (COLOR.get(sev, ""), text, RESET)


def print_one(r):
    sev = r["severity"]
    head = paint("%-28s" % r["label"], sev)
    ver = r["version"] or r["input"]
    print("%s %s%s%s" % (head, BOLD if tty() else "", ver, RESET if tty() else ""))
    meta = "  branch %s" % (r["branch"] or "?")
    if r["branch_status"]:
        meta += " · %s" % r["branch_status"]
    if r["fixed_build"]:
        meta += " · fixed in %s" % r["fixed_build"]
    print(paint(meta, sev) if not tty() else (DIM + meta + RESET))
    print("  → %s" % r["action"])
    if r["note"]:
        print((DIM + "  i %s" % r["note"] + RESET) if tty() else "  i %s" % r["note"])
    print()


def rank_rows(rows):
    # worst first, then by host/version for stable ordering
    return sorted(rows, key=lambda x: (-x["_result"]["severity"], x.get("host", ""), x["_result"]["input"]))


def print_inventory_table(rows):
    rows = rank_rows(rows)
    counts = {}
    print("%-26s %-11s %-30s %s" % ("HOST", "VERSION", "VERDICT", "ACTION"))
    print("-" * 110)
    for row in rows:
        r = row["_result"]
        counts[r["severity"]] = counts.get(r["severity"], 0) + 1
        host = (row.get("host") or "-")[:26]
        ver = (r["version"] or r["input"] or "-")[:11]
        label = r["label"][:30]
        action = r["action"]
        line = "%-26s %-11s %-30s %s" % (host, ver, label, action)
        print(paint(line, r["severity"]) if tty() else line)
    print("-" * 110)
    summary = "  SAFE %d   PATCH-NOW %d   NO-UPSTREAM-FIX %d   ABANDONED %d" % (
        counts.get(0, 0), counts.get(1, 0), counts.get(2, 0), counts.get(3, 0))
    print(summary)


# ------------------------------------------------------------------------------ main
def main(argv=None):
    p = argparse.ArgumentParser(
        description="PHP2Shell patch-status checker (defensive; CVE-2026-109618 / 109619).",
        epilog="Exit codes: 0 safe · 1 patch-available · 2 no-upstream-fix/abandoned · 3 error.")
    p.add_argument("version", nargs="?", help="a PHP version string, e.g. 8.3.20")
    p.add_argument("--local", action="store_true", help="check the PHP on this host (runs `php -v`)")
    p.add_argument("--inventory", metavar="CSV", help="check an inventory CSV with a php_version column")
    p.add_argument("--format", choices=["table", "json", "csv"], default="table",
                   help="output format for --inventory (default: table)")
    p.add_argument("--json", action="store_true", help="JSON output for a single/local check")
    p.add_argument("--data", metavar="JSON", default=DATA, help="path to affected_versions.json")
    args = p.parse_args(argv)

    matrix = load_matrix(args.data)

    # ---- inventory mode
    if args.inventory:
        rows = []
        for row in read_inventory(args.inventory):
            row["_result"] = classify(row.get("php_version"), matrix)
            rows.append(row)
        if not rows:
            sys.stderr.write("error: no rows in inventory.\n")
            return 3
        worst = max(r["_result"]["severity"] for r in rows)
        if args.format == "json":
            out = [{"host": r.get("host"), **{k: v for k, v in r["_result"].items()}} for r in rank_rows(rows)]
            print(json.dumps(out, indent=2))
        elif args.format == "csv":
            w = csv.writer(sys.stdout)
            w.writerow(["host", "version", "branch", "branch_status", "verdict", "severity", "action"])
            for row in rank_rows(rows):
                r = row["_result"]
                w.writerow([row.get("host", ""), r["version"] or r["input"], r["branch"],
                            r["branch_status"], r["verdict"], r["severity"], r["action"]])
        else:
            print_inventory_table(rows)
        return SEVERITY_EXIT.get(worst, 2)

    # ---- single / local mode
    raw = args.version
    if args.local:
        raw = read_local_version()
        if raw is None:
            return 3
    if not raw:
        p.print_help()
        return 3

    result = classify(raw, matrix)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print()
        print_one(result)
    return SEVERITY_EXIT.get(result["severity"], 2)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
    except BrokenPipeError:
        # downstream closed the pipe (e.g. `| head`); exit quietly
        try:
            sys.stdout.close()
        except Exception:
            pass
        os.close(os.open(os.devnull, os.O_WRONLY))
        sys.exit(0)
