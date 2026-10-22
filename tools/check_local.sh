#!/usr/bin/env bash
# check_local.sh - read-only PHP2Shell posture check for a host you run.
#
# Reports: PHP version + SAPI, whether this host is on a fixed build, and the
# state of the four stopgap php.ini settings. It changes NOTHING and contacts
# no network. Pair it with php_patch_check.py for the authoritative verdict.
#
# Usage:  ./check_local.sh
set -u

here="$(cd "$(dirname "$0")" && pwd)"
bold=""; dim=""; red=""; grn=""; amb=""; rst=""
if [ -t 1 ] && [ -z "${NO_COLOR:-}" ]; then
  bold=$'\033[1m'; dim=$'\033[2m'; red=$'\033[31m'; grn=$'\033[32m'; amb=$'\033[33m'; rst=$'\033[0m'
fi

say()  { printf '%s\n' "$*"; }
head() { printf '\n%s== %s ==%s\n' "$bold" "$1" "$rst"; }

if ! command -v php >/dev/null 2>&1; then
  say "${red}php not found on PATH.${rst} Run this on a host that has the PHP CLI, or pass a version"
  say "string to php_patch_check.py directly. Note: the CLI version may differ from the FPM/web"
  say "version - always verify the web SAPI from an actual web request, not just the CLI."
  exit 3
fi

head "Version & SAPI"
ver_line="$(php -v 2>&1 | head -n1)"
ver="$(printf '%s' "$ver_line" | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -n1)"
sapi="$(php -r 'echo PHP_SAPI;' 2>/dev/null)"
say "  CLI reports : ${bold}${ver_line}${rst}"
say "  SAPI (CLI)  : ${sapi:-unknown}"
say "  ${dim}Reminder: the web server runs its own SAPI (fpm/apache2handler/litespeed).${rst}"
say "  ${dim}Verify the web version from a request, e.g. a locked-down phpinfo() page, not the CLI.${rst}"

# authoritative verdict via the Python checker, if present
if command -v python3 >/dev/null 2>&1 && [ -f "$here/php_patch_check.py" ]; then
  head "Patch verdict"
  python3 "$here/php_patch_check.py" "$ver" 2>/dev/null | sed 's/^/  /'
fi

head "Stopgap php.ini posture (advisory only - patching is the fix)"
get() { php -r "echo ini_get('$1');" 2>/dev/null; }

check() {
  # $1 label  $2 ini_key  $3 good-test  $4 good-msg  $5 warn-msg
  local label="$1" key="$2" val
  val="$(get "$key")"
  printf '  %-34s %s\n' "$label" "current: ${val:-<empty>}"
}

upe="$(get session.upload_progress.enabled)"
if [ "$upe" = "0" ] || [ "$upe" = "" ]; then
  printf '  %-34s %sOK%s  (%s)\n' "session.upload_progress.enabled" "$grn" "$rst" "${upe:-0 / off}"
else
  printf '  %-34s %sOPEN%s (=%s)  set to 0 to close the CVE-2026-109619 path\n' "session.upload_progress.enabled" "$amb" "$rst" "$upe"
fi

ml="$(get memory_limit)"
printf '  %-34s current: %s   %s\n' "memory_limit" "${ml:-?}" "${dim}(-1 removes the OOM trigger ONLY with a cgroup/container cap)${rst}"

pms="$(get post_max_size)"
printf '  %-34s current: %s   %s\n' "post_max_size" "${pms:-?}" "${dim}(a low value shrinks the multipart window)${rst}"

feb="$(get fatal_error_backtraces)"
if [ -n "$feb" ]; then
  printf '  %-34s current: %s   %s\n' "fatal_error_backtraces (8.5)" "$feb" "${dim}(0 closes the 8.5 backtrace path)${rst}"
fi

head "Next"
say "  1. If the verdict above is not SAFE, upgrade to the fixed build and ${bold}restart every worker${rst}."
say "  2. Stopgaps buy hours, not weeks. php.net: they 'do not make an installation safe.'"
say "  3. If this host was internet-reachable and unpatched after 2026-10-20, treat it as"
say "     potentially compromised: hunt webshells and rotate DB creds, API keys, session"
say "     secrets, and TLS keys (the memory-disclosure path leaks them without RCE)."
say ""
