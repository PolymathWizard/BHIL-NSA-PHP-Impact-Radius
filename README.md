<!-- markdownlint-disable MD033 MD041 -->
<div align="center">

<img src="assets/exhibits/00-blast-radius-cover.png" alt="PHP2Shell: The Blast Radius Assessment" width="100%">

# BHIL &middot; NSA PHP Impact Radius

### A defensive intelligence toolkit and briefing for the NSA PHP advisory of October 21, 2026

**`CVE-2026-109618`** &nbsp;&middot;&nbsp; **`CVE-2026-109619`** &nbsp;&middot;&nbsp; codename **PHP2Shell**

[![Release](https://img.shields.io/badge/release-v1.0.0-1B4FD8?style=flat-square)](https://github.com/PolymathWizard/BHIL-NSA-PHP-Impact-Radius/releases)
[![CVSS](https://img.shields.io/badge/CVSS_v4.0-9.2_critical-8A2331?style=flat-square)](docs/01-advisory-deconstruction.md)
[![Python](https://img.shields.io/badge/python-3.8%2B_stdlib_only-1B4FD8?style=flat-square)](tools/)
[![Data current](https://img.shields.io/badge/data-2026--10--21-1B4FD8?style=flat-square)](data/affected_versions.json)
[![Code](https://img.shields.io/badge/code-MIT-1B4FD8?style=flat-square)](LICENSE)
[![Content](https://img.shields.io/badge/content-CC_BY_4.0-1B4FD8?style=flat-square)](LICENSE)

### [▶ &nbsp;Open the live scroll briefing](https://barryhurd.com/project/php2shell-blast-radius-deploy.html)

<sub>Barry Hurd Intelligence Lab &nbsp;&middot;&nbsp; Human-Directed. AI-Enabled. Commercially Tested.</sub>

</div>

---

Two memory-safety flaws in the PHP engine put roughly **24 million live sites** one
unauthenticated request from compromise. This repository turns a terse government advisory into
something a defender can act on in the next seventy-two hours: **tooling** to find out whether
your PHP is exposed, a **machine-readable data layer**, a full **written briefing** with eight
exhibit-grade visuals, a **curated resource directory**, and a **data-driven scroll site**.

> [!IMPORTANT]
> **Defensive by design.** This repository is for assessing and remediating systems *you
> operate*. It contains no exploit or proof-of-concept code, nothing that triggers
> CVE-2026-109618 / 109619, and no scanning or probing of third-party systems. See
> [the scope note](tools/README.md#scope--read-this-first).

---

## By the numbers

| The weapon | The exposure | The clock |
|---|---|---|
| **2** critical CVEs, both **CVSS 9.2** | **24,429,280** live PHP sites | CVE IDs leaked **Oct 20, ~15:00 UTC** |
| Class **CWE-824**, unauthenticated RCE | **9,218,655** in the U.S. (37.7%) | Cloudflare WAF live **03:02 UTC** |
| Affects **every release since PHP 5.4** | **~8.5M** on versions with no upstream fix | Attack traffic seen **07:43 UTC** |
| Fixed in **4** builds only | **~3.2M** of those U.S.-hosted | Coordinated release **14:00 UTC** |
| Heartbleed-style memory leak, no RCE needed | **883,717** hosts still on PHP 8.1 or older | Patch to n-day in **hours, not weeks** |

**Fixed builds (the only safe versions):** `8.5.12` &middot; `8.4.27` &middot; `8.3.36` &middot; `8.2.35`.
Everything below these on a supported branch, and every end-of-life branch, is exposed.

---

## Quick start

```bash
# Is this host's PHP exposed?
python3 tools/php_patch_check.py --local

# Check one version string
python3 tools/php_patch_check.py 8.3.20
#   -> VULNERABLE - PATCH NOW   branch 8.3 - fixed in 8.3.36

# Triage a whole inventory (CSV with a php_version column)
python3 tools/php_patch_check.py --inventory data/inventory.example.csv

# Full read-only posture check (version, SAPI, php.ini stopgaps)
bash tools/check_local.sh
```

No dependencies: Python 3.8+ standard library and POSIX shell. The tools send no network
traffic and change nothing. Exit codes make them CI-friendly (`0` safe, `1` patch available,
`2` no upstream fix, `3` error), so you can gate a pipeline on fleet patch status:

```bash
python3 tools/php_patch_check.py --inventory fleet.csv >/dev/null || echo "unpatched PHP in fleet"
```

Full tool reference: [tools/README.md](tools/README.md). One-page cheat sheet:
[docs/QUICKREF.md](docs/QUICKREF.md). Every key figure with its source: [docs/METRICS.md](docs/METRICS.md).

---

## The briefing, in eight exhibits

The full assessment runs across the documents in [`docs/`](docs/) and the companion brief in
[`brief/`](brief/). Each exhibit below is a standalone BHIL intelligence plate; the full-size
gallery is in [docs/EXHIBITS.md](docs/EXHIBITS.md).

### 1 &middot; The weapon

<img src="assets/exhibits/01-nsa-advisory.png" alt="Deconstructing the NSA Advisory" width="100%">

Engine-level, pre-authentication RCE plus a Heartbleed-style memory leak. The NSA release names
no CVE and runs five sentences; the technical record comes from PHP, CISA, CERT-EU, NCSC, and
vendor research. Every web-serving SAPI is in scope (php-fpm, mod_php, php-cgi, FrankenPHP,
LiteSpeed), and application quality is no defense.
&rarr; [docs/01-advisory-deconstruction.md](docs/01-advisory-deconstruction.md)

<img src="assets/exhibits/02-kill-chain.png" alt="PHP2Shell Kill Chain" width="100%">

One unauthenticated multipart POST reaches the engine before any application code runs, drives a
fatal error, and turns a half-initialized heap into remote code execution or a direct memory
leak of passwords, tokens, and TLS keys.

### 2 &middot; The race

<img src="assets/exhibits/03-disclosure-race.png" alt="The 36-Hour Disclosure Race" width="100%">

This is not a classic zero-day. It is a leaked-before-patch vulnerability that became an n-day
within hours. Cloudflare reports attack traffic six hours before the coordinated release.
Telemetry conflicts, and is unverified vendor data in motion.
&rarr; [docs/01-advisory-deconstruction.md](docs/01-advisory-deconstruction.md#exploitation-status--contested-and-moving)

### 3 &middot; The target field

<img src="assets/exhibits/04-exposure-paradox.png" alt="The Exposure Paradox" width="100%">

Value concentrates in fewer than 2,700 high-tier sites; volume sits in a 23.6 million-site long
tail that is where botnet capacity and DDoS staging come from. The tiers overlap and must never
be summed. &rarr; [docs/02-exposure-matrix.md](docs/02-exposure-matrix.md)

<img src="assets/exhibits/05-version-mix.png" alt="Version Mix and the No-Fix Population" width="100%">

About one live PHP site in three (roughly 8.5 million) runs a version that will never receive an
upstream fix. Distro packages may carry a backport without bumping the version number, so verify
against your vendor advisory, not the number alone.

### 4 &middot; The damages

<img src="assets/exhibits/06-loss-scenarios.png" alt="Modeled Loss Scenarios" width="100%">

A 10% breach rate across the 1,155 sites earning $100M+ models to about $1.3B on IBM's U.S.
breach-cost basis; 24 hours offline across that tier is roughly $316M at the revenue floor.
These are illustrative exposure models, not forecasts.
&rarr; [docs/03-economic-impact.md](docs/03-economic-impact.md)

### 5 &middot; The defense

<img src="assets/exhibits/07-triage-protocol.png" alt="The 72-Hour Triage Protocol" width="100%">

A three-phase protocol mapped to the NSA and CISA directives: Identify and Isolate, Mitigate,
then Patch and Verify. The checker in [`tools/`](tools/) produces the Phase 1 triage list.
&rarr; [docs/04-remediation-roadmap.md](docs/04-remediation-roadmap.md) &middot;
[docs/05-legacy-strategy.md](docs/05-legacy-strategy.md)

> [!WARNING]
> **Assume breach for the exposure window.** Any host that was internet-reachable and unpatched
> after October 20 should be treated as potentially compromised: hunt webshells and persistence,
> and rotate database credentials, API keys, session secrets, and TLS keys. The memory-disclosure
> path harvests them without RCE.

### Appendix &middot; Evidence and sources

<img src="assets/exhibits/08-caveats-sources.png" alt="Evidence, Caveats, and Source Register" width="100%">

Confidence, caveats, and the full Admiralty-graded source register. `TLP:CLEAR`, built entirely
from public reporting. &rarr; [docs/news-and-resources.md](docs/news-and-resources.md)

---

## Repository layout

```
BHIL-NSA-PHP-Impact-Radius/
├── tools/                      Defensive tooling (see tools/README.md)
│   ├── php_patch_check.py       Version to patch/isolate verdict; single, --local, --inventory
│   └── check_local.sh           Read-only version + php.ini posture check
├── data/                       Single source of truth (JSON/CSV)
│   ├── affected_versions.json   Branch to fixed-build to verdict matrix (tools read this)
│   ├── mitigations.json         php.ini stopgaps, edge rules, detection signals
│   ├── exposure_matrix.csv      BuiltWith exposure tiers
│   ├── sources.json             Source register (Admiralty-graded)
│   └── inventory.example.csv    Template for --inventory
├── docs/                       The briefing
│   ├── 01-advisory-deconstruction.md
│   ├── 02-exposure-matrix.md
│   ├── 03-economic-impact.md
│   ├── 04-remediation-roadmap.md
│   ├── 05-legacy-strategy.md
│   ├── news-and-resources.md    Best-in-class coverage + primary sources
│   ├── EXHIBITS.md              Full-size visual gallery (the 8 plates)
│   ├── METRICS.md               Every key figure with its source
│   └── QUICKREF.md              One-page responder cheat sheet
├── assets/exhibits/            The 8 BHIL intelligence plates (PNG)
├── site/
│   └── index.html               The data-driven scroll briefing
└── brief/                       Companion BHIL intelligence brief (DOCX + PDF)
```

---

## Keeping it current

As PHP ships new patch releases, update `fixed_build` in
[data/affected_versions.json](data/affected_versions.json). Both the tools and the docs read
from it, and the quality gate in [`.github/workflows/`](.github/workflows/) will re-run the tool
self-checks. Watch the
[CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) for either CVE;
a listing changes the urgency. Monitoring guidance is in
[docs/news-and-resources.md](docs/news-and-resources.md).

## Sources and handling

`TLP:CLEAR`. Built entirely from public reporting. Every source is named in
[data/sources.json](data/sources.json) and [docs/news-and-resources.md](docs/news-and-resources.md),
graded on the Admiralty scale. Verify anything that would change an operational decision against
the primary sources.

## License

Dual license, the BHIL standard: **[MIT](LICENSE)** for code and schemas, **CC BY 4.0** for the
written content and exhibits. Offered as-is for defensive use.

---

<div align="center">
<sub><b>Barry Hurd Intelligence Lab</b> &nbsp;&middot;&nbsp; REF PHP2SHELL-001 &nbsp;&middot;&nbsp; Human-Directed. AI-Enabled. Commercially Tested.</sub><br>
<sub><a href="https://barryhurd.com/project/php2shell-blast-radius-deploy.html">Live scroll briefing</a> &nbsp;&middot;&nbsp; <a href="https://barryhurd.com">barryhurd.com</a></sub>
</div>
