#!/usr/bin/env bash
# selftest.sh - verify the checker and data layer. Run locally or in CI.
# No dependencies beyond Python 3 standard library.
set -u
cd "$(dirname "$0")/.."
fail=0
chk() { # chk <description> <expected-exit> <args...>
  local desc="$1" want="$2"; shift 2
  python3 tools/php_patch_check.py "$@" >/dev/null 2>&1
  local got=$?
  if [ "$got" = "$want" ]; then printf 'ok    %s (exit %s)\n' "$desc" "$got"
  else printf 'FAIL  %s (want %s, got %s)\n' "$desc" "$want" "$got"; fail=1; fi
}

echo "== version verdict exit codes =="
chk "8.4.27 is safe"                 0 8.4.27
chk "8.3.20 needs patch"             1 8.3.20
chk "8.1.29 has no upstream fix"     2 8.1.29
chk "5.6.40 is abandoned"            2 5.6.40
chk "example inventory worst=abandoned" 2 --inventory data/inventory.example.csv

echo "== data layer =="
python3 - <<'PY'
import json, glob, sys
ok = True
for f in glob.glob("data/*.json"):
    try: json.load(open(f))
    except Exception as e: print("FAIL  %s: %s" % (f, e)); ok = False
    else: print("ok    %s parses" % f)
sys.exit(0 if ok else 1)
PY
[ $? -ne 0 ] && fail=1

echo
if [ "$fail" = 0 ]; then echo "ALL CHECKS PASSED"; else echo "SELFTEST FAILED"; fi
exit $fail
