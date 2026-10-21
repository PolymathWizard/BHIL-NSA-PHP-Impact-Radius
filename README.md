<!-- markdownlint-disable MD033 MD041 -->
<div align="center">

# PHP2Shell — The Blast Radius

**A defensive intelligence toolkit and briefing for the NSA PHP advisory of October 21, 2026**
(`CVE-2026-109618` · `CVE-2026-109619`)

*Two memory-safety flaws in the PHP engine put ~24 million live sites one unauthenticated
request from compromise. This repo helps you find out whether yours is one of them — and what
to do in the next seventy-two hours.*

`Human-Directed. AI-Enabled. Commercially Tested.` — Barry Hurd Intelligence Lab

</div>

---

## What this is

A single place that turns a terse government advisory into something a defender can act on:

- **Tools** that tell you whether a given PHP build is exposed and what to do about it —
  version triage for a single host, this host, or a whole inventory.
- **A machine-readable data layer** (fixed-build matrix, mitigations, exposure tiers, sources)
  the tools and docs both read from.
- **A written briefing** — advisory deconstruction, exposure matrix, economic model, and a
  phased remediation roadmap.
- **Curated, best-in-class resources** for tracking this CVE pair and PHP vulnerabilities
  generally.
- **A scrollytelling site** that presents the whole story as a data-driven web experience.

### Scope — defensive by design

This repository is for assessing and remediating **systems you operate**. It contains **no
exploit or proof-of-concept code**, nothing that triggers CVE-2026-109618 / 109619, and no
scanning or probing of systems you don't own. Contributions that add any of those will be
declined. See [`tools/README.md`](tools/README.md#scope--read-this-first).

---

## Quick start

```bash
# Is this host's PHP exposed?
python3 tools/php_patch_check.py --local

# Check one version string
python3 tools/php_patch_check.py 8.3.20

# Triage a whole inventory (CSV with a php_version column)
python3 tools/php_patch_check.py --inventory data/inventory.example.csv

# Full read-only posture check (version + SAPI + php.ini stopgaps)
bash tools/check_local.sh
```

No dependencies — Python 3.8+ standard library and POSIX shell. The tools send no network
traffic and change nothing. Exit codes make them CI-friendly: `0` safe · `1` patch available ·
`2` no upstream fix · `3` error.

```bash
# fail a pipeline if any host in the fleet is unpatched
python3 tools/php_patch_check.py --inventory fleet.csv >/dev/null || exit 1
```

---

## Repository layout

```
php2shell-blast-radius/
├── tools/                     Defensive tooling (see tools/README.md)
│   ├── php_patch_check.py      Version → patch/isolate verdict; single, --local, --inventory
│   └── check_local.sh          Read-only version + php.ini posture check
├── data/                      Single source of truth (JSON/CSV)
│   ├── affected_versions.json  Branch → fixed-build → verdict matrix (tools read this)
│   ├── mitigations.json        php.ini stopgaps, edge rules, detection signals
│   ├── exposure_matrix.csv     BuiltWith exposure tiers
│   ├── sources.json            Source register (Admiralty-graded)
│   └── inventory.example.csv   Template for --inventory
├── docs/                      The briefing
│   ├── 01-advisory-deconstruction.md
│   ├── 02-exposure-matrix.md
│   ├── 03-economic-impact.md
│   ├── 04-remediation-roadmap.md
│   ├── 05-legacy-strategy.md
│   └── news-and-resources.md   Best-in-class coverage + primary sources
├── site/
│   └── index.html              The data-driven scroll briefing (open in a browser)
└── brief/                      Companion BHIL intelligence brief (DOCX + PDF)
```

---

## The briefing, in one screen

- **The weapon** — engine-level, pre-authentication RCE plus a Heartbleed-style memory leak.
  Every release since PHP 5.4 is affected; fixed only in **8.5.12 / 8.4.27 / 8.3.36 / 8.2.35**.
  → [docs/01](docs/01-advisory-deconstruction.md)
- **The target field** — ~24.4M live PHP sites (~9.2M U.S.); ~8.5M on versions that will never
  get an upstream fix; value concentrated in <2,700 high-tier sites, volume in 23.6M long-tail.
  → [docs/02](docs/02-exposure-matrix.md)
- **The damages** — a 10% breach rate in the $100M+ tier models to ~$1.3B; 24h offline across
  that tier ≈ $316M at the revenue floor. *Illustrative models, not forecasts.*
  → [docs/03](docs/03-economic-impact.md)
- **The defense** — a 72-hour, three-phase protocol (Identify & Isolate → Mitigate → Patch &
  Verify) mapped to the NSA and CISA directives. → [docs/04](docs/04-remediation-roadmap.md)

---

## Keeping it current

As PHP ships new patch releases, update `fixed_build` in
[`data/affected_versions.json`](data/affected_versions.json) — tools and docs both read it.
Watch the [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) for
either CVE; a listing changes the urgency. Monitoring guidance is in
[docs/news-and-resources.md](docs/news-and-resources.md).

## Analytic caveats

- **The NSA release is thin** (no CVEs, versions, or indicators); the technical record here
  comes from PHP, CISA, CERT-EU, NCSC, and vendor research, and a promised NSA follow-up may
  change recommended controls.
- **Exploitation telemetry conflicts** and is unverified vendor data in motion as of Oct 21.
- **The economic figures are illustrative exposure models, not forecasts** — breach rates are
  assumptions; IBM figures average across breach types; downtime uses revenue floors.
- **Measurement sources count different things** (fingerprinted sites vs. version share vs.
  hosts) and must not be combined arithmetically; the exposure tiers overlap and must not be
  summed.
- **Some circulating numbers are wrong** — "70% of the internet" is W3Techs' share of sites
  with a known server-side language; pre-release claims of CVSS 10.0 were incorrect (it is 9.2).

## Sources & handling

`TLP:CLEAR` — built entirely from public reporting. Every source is named in
[`data/sources.json`](data/sources.json) and [docs/news-and-resources.md](docs/news-and-resources.md),
graded on the Admiralty scale. Verify anything that would change an operational decision against
the primary sources.

## License

[MIT](LICENSE). The data and documentation are offered as-is for defensive use; verify against
primary sources before acting.

---

<div align="center">
<sub><b>Barry Hurd Intelligence Lab</b> — Human-Directed. AI-Enabled. Commercially Tested. ·
REF PHP2SHELL-001</sub>
</div>
