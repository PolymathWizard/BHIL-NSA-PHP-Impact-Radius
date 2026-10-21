# 03 · Economic & Strategic Impact

> Priced against the benchmarks boards already trust — and the NSA's own fallback order.
> **These are illustrative exposure models, not forecasts.**

## What an RCE on a commerce backend yields

Code execution as the web-server user typically gives an attacker five things:

1. Application config — database credentials and payment-gateway keys (the NSA "direct path").
2. The power to rewrite checkout templates and JavaScript — the Magecart skimming precondition.
3. Bulk extraction of customer and order data.
4. A pivot point for ransomware deployment.
5. Via the memory-disclosure path, session tokens and secrets **even where RCE fails**.

## Benchmarks applied to the 1,155 $100M+ sites

| Loss vector | Benchmark | Modeled exposure |
|---|---|---|
| Data breach | IBM 2026 U.S. average **$11.5M** (global $4.99M) | 5% of tier (58 sites) ≈ **$0.66B**; 10% (116) ≈ **$1.33B**; full-tier ceiling ≈ $13.3B |
| Ransomware | Coveware Q2 2026: avg payment **$1.88M**, median $150K; avg recovery $1.7M ex-ransom | ≈ $1.85M–$3.6M per incident before notification/legal |
| Mandated downtime | Revenue floor of $100M/yr ≈ $11,400/hour; ITIC: 41% of firms price an hour at $1M–$5M+ | 24h offline across all 1,155 ≈ **$316M at the floor** |
| Magecart / regulatory | British Airways: proposed £183.39M GDPR fine (£20M final), ~429,612 people, 11-day skimmer | Fines scale with turnover (GDPR up to 4%); PCI costs on top |

## The board math

The **downtime** figure is the number executives should stare at. The official mitigation for
unpatchable systems is going offline, so delay converts directly into lost revenue — and the
revenue-floor figure is the *minimum*; ITIC's cross-industry rates run two orders of magnitude
higher. The expected cost of a two-to-four-hour controlled maintenance window is trivial next
to a single breach. **Authorize the emergency change window today.**

For the 3,120-site $10M+ tier the same logic holds with one twist: thinner security teams and
heavier reliance on agencies and managed hosts make **patch latency**, not exploit difficulty,
the dominant risk factor.

## The "zombie PHP" problem

The ~79M expired sites are not live attack surface (a site that no longer resolves cannot be
exploited) but they are evidence: deployment without decommissioning is the same behavior that
produced today's unpatched estate, and dangling DNS, forgotten staging subdomains, and
never-deprovisioned hosting accounts resurface on their own.

The ~23.6M **live** long-tail sites are the systemic risk. A third or more can only be
protected by migration or isolation — abandonware owners will do neither. One toolchain works
across WordPress, Joomla, Drupal, and custom code alike.

**The precedent:** CVE-2024-4577 (the previous PHP-CGI RCE) was weaponized by TellYouThePass
ransomware within ~2 days of its June 2024 patch; seven months later GreyNoise still logged
1,089 unique IPs attempting it, with 79 public exploits circulating. Expect PHP2Shell-derived
infections to persist for years.

## The U.S. domestic concentration

Two in five of the world's live PHP sites are U.S.-hosted. That concentrates: **attack
surface** (~3.2M U.S. sites on no-fix versions), **cost** (IBM's U.S. average runs ~2.3× the
global figure), and **public-sector exposure** (CISA warns PHP "is often a component of other
software and prevalence may not be directly observable" — inventories are almost certainly
incomplete).

*Benchmark sources: IBM Cost of a Data Breach 2026, Coveware Q2 2026, ITIC, UK ICO, GreyNoise,
Cisco Talos. See [news-and-resources.md](news-and-resources.md).*
