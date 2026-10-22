# Contributing

Thanks for helping keep this defensive toolkit accurate.

## What's welcome

- **Version-data updates.** When PHP ships a new patch release on a branch, update
  `fixed_build` in [`data/affected_versions.json`](data/affected_versions.json). Open a
  *Version data update* issue (there's a template) or a PR.
- **Distro-backport notes.** Mappings of distro package versions that carry the fix help the
  `VERIFY WITH VENDOR` guidance.
- **Source/link fixes.** Dead links or better primary sources in
  [`data/sources.json`](data/sources.json) / [`docs/news-and-resources.md`](docs/news-and-resources.md).
- **Tool robustness.** Parsing edge cases, output formats, test coverage.

## What will be declined

This is a defensive repository. Pull requests that add exploit or proof-of-concept code,
anything that triggers CVE-2026-109618 / CVE-2026-109619, remote scanners/probers for systems
you don't own, or target-discovery tooling will be closed. Keep contributions focused on
assessing and remediating systems the operator controls.

## Ground rules for the tools

- Standard library only (Python 3.8+) - no third-party dependencies.
- No network calls and no state changes in the core tools.
- Keep [`data/affected_versions.json`](data/affected_versions.json) the single source of truth;
  don't hard-code version numbers in the scripts.

## Verifying a change

```bash
python3 tools/php_patch_check.py 8.3.20      # expect: VULNERABLE - PATCH NOW, exit 1
python3 tools/php_patch_check.py 8.4.27      # expect: SAFE, exit 0
python3 tools/php_patch_check.py 5.6.40      # expect: VULNERABLE - ABANDONED, exit 2
python3 tools/php_patch_check.py --inventory data/inventory.example.csv
```
