# News & Resources - PHP2Shell

<img src="../assets/exhibits/08-caveats-sources.png" alt="Evidence, Caveats, and Source Register" width="100%">

Best-in-class resources for tracking PHP2Shell (CVE-2026-109618 / CVE-2026-109619) and PHP
vulnerabilities generally. Ordered the way a defender should actually use them: authoritative
first, then deep technical analysis, then live exploitation status, then ongoing journalism.
Reliability grades use the Admiralty scale (A1 = reliable, confirmed → C3 = fairly reliable,
possibly true). Machine-readable version in [`../data/sources.json`](../data/sources.json).

> Check the **primary** sources before acting. Vendor telemetry and press are useful for
> situational awareness but are secondary to the advisories and the official fixed builds.

---

## 1. Primary & authoritative - check these first

| Source | What it gives you | Grade |
|---|---|---|
| **NSA** - [NSA Advisory: PHP Updates](https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4630238/nsa-advisory-php-updates/) | The advisory that started it: patch or take offline. | A1 |
| **CISA** - [Critical Vulnerabilities in PHP Require Immediate Patching](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching) | The operational directives (inventory, prioritize, isolate, monitor). | A1 |
| **PHP project** - [GHSA-w8hw-w9fx-j79w](https://github.com/php/php-src/security/advisories/GHSA-w8hw-w9fx-j79w) · [GHSA-6wmf-4rv5-p3rp](https://github.com/php/php-src/security/advisories/GHSA-6wmf-4rv5-p3rp) | Root cause, affected versions, the fixed builds. | A1 |
| **PHP release announcements** - [php.net/archive](https://www.php.net/archive/) | Confirms 8.5.12 / 8.4.27 / 8.3.36 / 8.2.35 and future patch releases. | A1 |
| **CERT-EU** - [Security Advisory 2026-018](https://cert.europa.eu/publications/security-advisories/2026-018) | EU coordination view; notes embedded-PHP exposure. | A1 |
| **UK NCSC** - [Critical security issue affecting PHP](https://www.ncsc.gov.uk/news/critical-security-issue-affecting-php) | UK guidance. | A2 |
| **The PHP Foundation** - [security release post](https://thephp.foundation/blog/2026/10/21/todays-php-security-release-and-how-were-strengthening-php-security/) | The disclosure story and the funding/structural context. | A2 |
| **NVD** - [search CVE-2026-109618](https://nvd.nist.gov/vuln/search/results?query=CVE-2026-109618) · [CVE-2026-109619](https://nvd.nist.gov/vuln/search/results?query=CVE-2026-109619) | Canonical CVE records, CVSS, CPE, references. | A1 |

## 2. Deep technical analysis - understand the mechanism

| Source | Angle | Grade |
|---|---|---|
| **Wiz Research** - [PHP2Shell - PHP RCE](https://www.wiz.io/blog/php2shell-php-rce) | The definitive teardown: four bug instances, pre-auth RCE demo, the AI-acceleration finding. | B2 |
| **Sansec** - [PHP2Shell](https://sansec.io/research/php2shell) | Commerce / Magento exposure; the "clean code is still exposed" point. | B2 |
| **Cloudflare** - [WAF protection](https://blog.cloudflare.com/php-vulnerabilities-waf-protection/) | Edge-rule guidance + earliest attack-traffic telemetry. | B2 |
| **Tenable** - [PHP2Shell FAQ](https://www.tenable.com/blog/php2shell-cve-2026-109618-cve-2026-109619-frequently-asked-questions-about-critical-php-remote) | Clear FAQ; corrects the bad CVSS numbers. | B2 |
| **Rapid7** - [ETR analysis](https://www.rapid7.com/blog/post/etr-cve-2026-109618-and-cve-2026-109619-critical-unauthenticated-remote-code-execution-in-php/) | Emergent-threat response + detection. | B2 |
| **Qualys** - [critical security release note](https://blog.qualys.com/vulnerabilities-threat-research/2026/10/20/php-announces-critical-security-release-for-two-vulnerabilities) | Detection QIDs. | B2 |

## 3. Live exploitation status - is it being used *right now*?

| Source | Use it to… | Grade |
|---|---|---|
| **CISA KEV Catalog** - [Known Exploited Vulnerabilities](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) | See if either CVE is confirmed exploited (and gets a federal remediation deadline). | A1 |
| **GreyNoise** - [viz.greynoise.io](https://viz.greynoise.io/) | Watch internet-wide scanning/exploitation by CVE and by tag. | B2 |
| **Shadowserver** - [dashboard](https://dashboard.shadowserver.org/) | Track the vulnerable/exposed population over time. | B2 |
| **SANS Internet Storm Center** - [isc.sans.edu](https://isc.sans.edu/) | Handler diaries, honeypot hits, early IOCs. | B2 |
| **Cloudflare Radar** - [radar.cloudflare.com](https://radar.cloudflare.com/) | Macro attack-traffic trends. | B3 |

## 4. Best-in-class security journalism - ongoing coverage

| Outlet | Why it's here | Grade |
|---|---|---|
| **BleepingComputer** - [/news/security](https://www.bleepingcomputer.com/news/security/) | Fast, accurate breaking coverage with IOCs. | B2 |
| **The Hacker News** - [thehackernews.com](https://thehackernews.com/) | High-volume, timely. | B2 |
| **SecurityWeek** - [securityweek.com](https://www.securityweek.com/) | Enterprise/threat-intel depth. | B2 |
| **Ars Technica - Security** - [arstechnica.com/security](https://arstechnica.com/security/) | Careful, technical explainers. | B2 |
| **Dark Reading** - [darkreading.com](https://www.darkreading.com/) | Defender / CISO audience. | B2 |
| **The Record** - [therecord.media](https://therecord.media/) | Recorded Future's newsroom; nation-state context. | B2 |
| **Risky Business** - [risky.biz](https://risky.biz/) | Weekly analysis podcast/newsletter; signal over noise. | B2 |
| **Help Net Security** - [helpnetsecurity.com](https://www.helpnetsecurity.com/) | Vendor-advisory roundups. | B2 |
| **The Register - Security** - [theregister.com/security](https://www.theregister.com/security/) | Skeptical, well-sourced. | B2 |

## 5. Scanner & detection references (defensive)

- **Your vulnerability scanner's plugin for these CVEs** - Tenable (Nessus), Qualys, Rapid7
  (InsightVM) all shipped authenticated checks on release day. Prefer authenticated scanning;
  banner-only checks miss distro backports (see the distro caveat in [`../tools/README.md`](../tools/README.md)).
- **NCSC-NL php2shell repository** - community list of third-party products that embed PHP
  (so you can find PHP that isn't advertised as PHP): search GitHub for `NCSC-NL/php2shell`.
- **This repo's checker** - [`../tools/php_patch_check.py`](../tools/php_patch_check.py) for
  version-status triage of an inventory you already have.

---

## How to monitor this going forward

1. **Watch the KEV catalog** for CVE-2026-109618 / 109619 - a listing changes the urgency and,
   for US federal agencies, imposes a deadline.
2. **Subscribe to the PHP release feed** ([php.net](https://www.php.net/)) so you catch the
   next patch release on your branch and can update [`../data/affected_versions.json`](../data/affected_versions.json).
3. **Set a GreyNoise tag alert** for the CVEs to know when opportunistic mass scanning starts.
4. **Follow two or three of the journalism outlets above** - not all nine. Signal, not volume.

*Grades and notes are reference material, not instructions. Verify anything that would change
an operational decision against the primary sources.*
