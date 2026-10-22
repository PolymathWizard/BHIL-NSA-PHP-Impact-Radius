# Tools

Defensive PHP2Shell tooling. These answer one question about **hosts you run**:
*patch, backport, or take offline?* They read version strings and local config and
compare them against the published fixed-build matrix.

### Scope - read this first

- ✅ **In scope:** checking the PHP version and `php.ini` posture of systems you operate;
  triaging an inventory you already have; gating CI on patch status.
- ❌ **Not in scope, not included:** exploit or proof-of-concept code, anything that
  triggers CVE-2026-109618 / CVE-2026-109619, remote scanning or probing of systems you
  don't own, or internet-wide target discovery. This repository contains none of that and
  will not accept contributions that add it.

The tools send **no network traffic** and make **no changes**. They are safe to run in
production and in CI.

---

## `php_patch_check.py`

Python 3.8+, standard library only. Reads [`../data/affected_versions.json`](../data/affected_versions.json).

```bash
# one version
./php_patch_check.py 8.3.20

# the PHP on this host (runs `php -v`)
./php_patch_check.py --local

# a whole inventory (CSV with a php_version column)
./php_patch_check.py --inventory ../data/inventory.example.csv
./php_patch_check.py --inventory hosts.csv --format csv  > triage.csv
./php_patch_check.py --inventory hosts.csv --format json > triage.json

# machine-readable single check
./php_patch_check.py 8.1.29 --json
```

**Verdicts**

| Verdict | Meaning |
|---|---|
| `SAFE` | At/above the fixed build on a supported branch. Confirm workers were restarted. |
| `VULNERABLE - PATCH NOW` | Supported branch below the fixed build. Upgrade + restart. |
| `VULNERABLE - NO UPSTREAM FIX` | EOL branch (8.1/8.0/7.4): backport or isolate; migrate. |
| `VULNERABLE - ABANDONED` | EOL branch with no backport (7.3 and older, 5.x): isolate/offline; migrate. |
| `VERIFY WITH VENDOR` | Distro package below the upstream number - the fix may be **backported** without bumping the number. Confirm against your distro's advisory. |
| `UNKNOWN - TREAT AS EXPOSED` | Unparseable or unknown branch. Treat as exposed. |

**Exit codes** (for cron / CI gates): `0` all safe · `1` patch available · `2` no upstream
fix / abandoned · `3` usage or data error.

```bash
# fail a pipeline if any host is unpatched
./php_patch_check.py --inventory hosts.csv >/dev/null || echo "unpatched PHP in fleet"
```

### The distro caveat (why `VERIFY WITH VENDOR` exists)

Debian, Ubuntu, RHEL, Alma and others **backport** security fixes into their packaged PHP
without changing the upstream version number - a Debian `8.3.20-1+deb12u2` may already carry
the PHP2Shell fix even though `8.3.20 < 8.3.36`. Upstream version arithmetic lies about
distro builds. When the tool sees a package suffix below the fixed build it returns
`VERIFY WITH VENDOR` rather than a false `VULNERABLE`, and points you to your vendor's
advisory. Always confirm distro builds there, not by the number alone.

### The CLI-vs-web caveat

`php -v` reports the **CLI** build. Your web server runs its own SAPI (php-fpm,
apache2handler, litespeed) which can be a different version with a different `php.ini`.
Verify the web version from an actual web request, not just the CLI.

---

## `check_local.sh`

Read-only posture check for a host you run: prints the version + SAPI, pulls the
authoritative verdict from `php_patch_check.py`, and reports the state of the four stopgap
`php.ini` settings from [`../data/mitigations.json`](../data/mitigations.json). Changes
nothing, contacts nothing.

```bash
./check_local.sh
```

---

## Keeping the data current

As PHP ships new patch releases on each branch, update `fixed_build` in
[`../data/affected_versions.json`](../data/affected_versions.json) - both tools and the docs
read from it. Open a *Version data update* issue if you spot a stale build.
