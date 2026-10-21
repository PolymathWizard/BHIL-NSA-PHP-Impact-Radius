# 02 · Quantifying the Threat Landscape

> BuiltWith's census turns a technical advisory into a map of who is standing in the open.

## The blast radius

BuiltWith tracks **24,429,280 live PHP sites**, **9,218,655** of them hosted in the United
States (~37.7%), plus ~79 million expired/historic PHP sites. Because the flaw is in the
engine, the practical blast radius is the entire live installed base until each host is
verified patched.

## Four risk profiles

- **High-visibility properties** — top-ranked media, SaaS, government and enterprise sites,
  often fingerprinted on subdomains or inner pages. Reach and a perimeter foothold.
- **Revenue-bearing enterprises** — PHP sitting beside payment flows and internal networks.
  The ransomware and extortion target set.
- **Transactional commerce** — Magento/Adobe Commerce, WooCommerce, Shopware are all PHP.
  Sansec: these stores "are exposed even when their own code is clean."
- **The long tail** — millions of agency-built, hobbyist and abandoned sites whose patching
  depends entirely on the hosting provider.

## The Exposure Matrix

Machine-readable in [`../data/exposure_matrix.csv`](../data/exposure_matrix.csv).

| Exposure Category | Risk Tier | Volume of Sites | Primary Risk Profile / Motivation for Attackers |
|---|---|---:|---|
| **Traffic / Reach** | Top 10k | 1,362 | High-profile defacement, massive malware distribution (watering-hole attacks). |
| | Top 100k | 13,440 | Significant brand damage, high-value data exfiltration. |
| **Sales Revenue** | $100m+ | 1,155 | Prime targets for targeted ransomware, corporate espionage, massive financial extortion. |
| | $10m+ | 3,120 | Highly lucrative targets for financial data theft and ransomware. |
| **E-Commerce (SKUs)** | 100k+ SKUs | 102 | Enterprise e-commerce; extreme risk of Magecart card skimming and customer-data breaches. |
| | 10k+ SKUs | 3,949 | Large retail operations; high risk of business disruption and inventory manipulation. |
| **Long-Tail / Zombie** | Outside Top 1m | ~23.6 Million | Massive botnets, DDoS staging, crypto-mining — often unmaintained "abandonware." |

## Reading the matrix

- **The high-value tiers are tiny.** Top-10k, $100M+ and 100k-SKU together total fewer than
  2,700 sites (~0.01% of the population) yet carry most of the per-incident economic loss.
- **The long tail carries the systemic risk.** At ~96.6% of live sites by count, it is where
  botnet capacity and DDoS staging come from. Compromise even 1% → ~236,000 servers.
- **The top-tier count is a floor.** BuiltWith fingerprints the primary property; W3Techs
  finds PHP on 59.7% of top-10k sites with a known server-side language. True top-site exposure
  likely runs several times the 1,362 shown.
- **Tiers overlap** — views of one population, never additive. Never sum them.

## The unpatchable third

W3Techs' version census: **65.2%** of PHP sites on PHP 8, **27.0%** on PHP 7, **7.8%** on PHP
5/4. Applied to the live count, roughly **8.5 million sites** — about 3.2M of them U.S.-hosted
— run versions with **no upstream fix**. Host telemetry agrees: Mallory counted 883,717
internet-facing hosts (59% of those disclosing a version) still advertising PHP ≤ 8.1 on
Oct 20.

*Measurement sources: BuiltWith Trends, W3Techs. See [news-and-resources.md](news-and-resources.md).
Figures are snapshots; sources measure different things (fingerprinted sites vs. version share
vs. hosts) and should not be combined arithmetically.*
