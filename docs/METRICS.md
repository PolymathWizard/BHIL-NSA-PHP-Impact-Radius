# Key Metrics

Every headline figure in this assessment, with its source and a note on how to read it. Figures
are snapshots as of 2026-10-21. Sources are graded on the Admiralty scale in
[data/sources.json](../data/sources.json).

> Measurement sources count different things (fingerprinted sites, version share, hosts) and must
> not be combined arithmetically. The exposure tiers overlap and must not be summed.

## The vulnerability

| Metric | Value | Source / note |
|---|---|---|
| CVEs | CVE-2026-109618, CVE-2026-109619 | PHP project GHSA advisories |
| CVSS v4.0 | 9.2 (both), Critical | CNA score; pre-release 10.0 and 9.4 figures were wrong |
| Vector | `AV:N/AC:H/AT:P/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N` | Network, no auth, no user interaction |
| Weakness class | CWE-824 (access of uninitialized pointer) | Unauthenticated RCE + memory disclosure |
| First affected version | PHP 5.4 | Wiz; every release in roughly the last decade |
| Fixed builds | 8.5.12, 8.4.27, 8.3.36, 8.2.35 | php.net release announcements |

## The exposed population

| Metric | Value | Source / note |
|---|---|---|
| Live PHP sites (global) | 24,429,280 | BuiltWith Trends |
| Live PHP sites (U.S.) | 9,218,655 (37.7%) | BuiltWith; largest single-country share |
| Expired/historic PHP sites | ~79 million | BuiltWith; not live attack surface, but evidence of decommissioning failure |
| Sites with no upstream fix | ~8.5 million (about one in three) | W3Techs version share applied to BuiltWith live count |
| No-fix sites, U.S.-hosted | ~3.2 million | Same basis |
| Hosts on PHP 8.1 or older | 883,717 (59% of those disclosing a version) | Host-level scan, 2026-10-20 |

## Version distribution (live PHP sites)

| Branch family | Share | Fix status |
|---|---|---|
| PHP 8.x | 65.2% | Fixed builds exist; upgrade and restart workers |
| PHP 7.x | 27.0% | End of life; 7.4 source-only backport, older nothing |
| PHP 5.x / 4.x | 7.8% | Abandoned; no fix will ship |

Source: W3Techs version census, 2026-10-21.

## The exposure matrix

| Exposure category | Risk tier | Sites | Prime target |
|---|---|---:|:---:|
| Traffic / Reach | Top 10k | 1,362 | yes |
| Traffic / Reach | Top 100k | 13,440 | |
| Sales Revenue | $100m+ | 1,155 | yes |
| Sales Revenue | $10m+ | 3,120 | |
| E-Commerce (SKUs) | 100k+ SKUs | 102 | yes |
| E-Commerce (SKUs) | 10k+ SKUs | 3,949 | |
| Long-Tail / Zombie | Outside top 1m | ~23,600,000 | |

Fewer than 2,700 sites across the three prime-target tiers carry most of the per-incident loss.
The long tail is about 96.6% of live sites by count. Machine-readable in
[data/exposure_matrix.csv](../data/exposure_matrix.csv). The Top-10k count is a floor: W3Techs
finds PHP on 59.7% of top-10k sites with a known server-side language.

## The economic model (illustrative, not forecasts)

| Metric | Value | Source / note |
|---|---|---|
| Average U.S. data breach | $11.5M | IBM Cost of a Data Breach 2026 |
| Average global data breach | $4.99M | IBM 2026 |
| Average ransomware payment | $1.88M (median $150K) | Coveware Q2 2026; mean skewed by outliers |
| Average ransomware recovery | $1.7M (excluding ransom) | Sophos |
| 10% breach, $100M+ tier (116 sites) | ~$1.3B | 116 x IBM U.S. average |
| 5% breach, $100M+ tier (58 sites) | ~$0.66B | Same basis |
| Full-tier ceiling (1,155 sites) | ~$13.3B | Theoretical maximum |
| 24h offline, full $100M+ tier | ~$316M at the revenue floor | $100M/yr implies ~$11,400/hour; ITIC puts an hour at $1M to $5M+ for 41% of firms |
| British Airways skimming fine | £183.39M proposed, £20M final | UK ICO; ~429,612 people, 11-day skimmer |

## The clock (October 2026, UTC)

| Time | Event |
|---|---|
| Oct 20, ~15:00 | CVE identifiers leak |
| Oct 21, 03:02 | Cloudflare WAF rules live |
| Oct 21, 07:43 | Cloudflare observes attack traffic (before release) |
| Oct 21, 14:00 | Coordinated release: PHP fixes, NSA, CISA, CERT-EU, NCSC |
| Oct 21, 14:19 | watchTowr reports active exploitation attempts |

## The precedent

| Metric | Value | Source / note |
|---|---|---|
| Prior PHP-CGI RCE | CVE-2024-4577 | The nearest comparison |
| Time to weaponization | ~2 days after patch | TellYouThePass ransomware, June 2024 |
| Still-active scanning | 1,089 unique IPs, 79 public exploits | GreyNoise, January 2025, seven months later |

The takeaway: PHP2Shell-derived infections should be expected to persist for years, especially
across the unpatchable long tail.
