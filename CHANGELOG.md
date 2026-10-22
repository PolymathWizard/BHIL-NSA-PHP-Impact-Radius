# Changelog

All notable changes to this repository are recorded here.

## [1.0.0] - 2026-10-21

Initial release: BHIL NSA PHP Impact Radius.

### Added
- `tools/php_patch_check.py` - PHP2Shell patch-status checker (single version, `--local`,
  `--inventory` batch; table/JSON/CSV output; distro-backport awareness; CI exit codes).
- `tools/check_local.sh` - read-only version and `php.ini` posture check.
- `data/affected_versions.json` - branch to fixed-build to verdict matrix (source of truth).
- `data/mitigations.json` - `php.ini` stopgaps, edge rules, detection signals.
- `data/exposure_matrix.csv` - BuiltWith exposure tiers.
- `data/sources.json` - Admiralty-graded source register.
- `data/inventory.example.csv` - inventory template.
- `docs/` - advisory deconstruction, exposure matrix, economic impact, remediation roadmap,
  legacy strategy, and a curated news/resources directory.
- `docs/EXHIBITS.md`, `docs/METRICS.md`, `docs/QUICKREF.md` - visual gallery, full metrics
  reference, and a one-page responder cheat sheet.
- `assets/exhibits/` - eight BHIL intelligence plates (PNG) embedded through the README and docs.
- A full visual README with cover plate, status badges, and a by-the-numbers summary.
- `site/index.html` - data-driven scrollytelling briefing. Live at
  https://barryhurd.com/project/php2shell-blast-radius-deploy.html
- `brief/` - companion BHIL intelligence brief (DOCX + PDF).
- `.github/workflows/quality-gate.yml` and `scripts/selftest.sh` - dash gate, tool self-test,
  byte-compile.

### Data snapshot
- Fixed builds current as of 2026-10-21: 8.5.12, 8.4.27, 8.3.36, 8.2.35.
- Update `data/affected_versions.json` as PHP ships new patch releases.
