# Changelog

All notable changes to this repository are recorded here.

## [1.0.0] — 2026-10-21

Initial release.

### Added
- `tools/php_patch_check.py` — PHP2Shell patch-status checker (single version, `--local`,
  `--inventory` batch; table/JSON/CSV output; distro-backport awareness; CI exit codes).
- `tools/check_local.sh` — read-only version + `php.ini` posture check.
- `data/affected_versions.json` — branch → fixed-build → verdict matrix (source of truth).
- `data/mitigations.json` — `php.ini` stopgaps, edge rules, detection signals.
- `data/exposure_matrix.csv` — BuiltWith exposure tiers.
- `data/sources.json` — Admiralty-graded source register.
- `data/inventory.example.csv` — inventory template.
- `docs/` — advisory deconstruction, exposure matrix, economic impact, remediation roadmap,
  legacy strategy, and a curated news/resources directory.
- `site/index.html` — data-driven scrollytelling briefing.
- `brief/` — companion BHIL intelligence brief (DOCX + PDF).

### Data snapshot
- Fixed builds current as of 2026-10-21: **8.5.12 / 8.4.27 / 8.3.36 / 8.2.35**.
- Update `data/affected_versions.json` as PHP ships new patch releases.
