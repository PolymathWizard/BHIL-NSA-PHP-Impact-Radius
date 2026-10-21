# 05 · The Legacy-Code Challenge

> For business-critical applications on PHP 5.x or 7.x there is no upstream fix, and a rushed
> version jump can break revenue. Handle it in this order of preference.

### 1. Contain first, migrate second
Never leave legacy PHP directly internet-exposed. Put it behind a reverse proxy or WAF that
strips multipart requests and enforces strict request-size, field-count and nesting limits.
Restrict to authenticated users or a VPN where the business allows, and segment the host so a
compromise cannot reach core databases or the domain. This is what "fully mitigated" realistically
means for code that cannot be patched.

### 2. Buy time with supported backports
For 7.4 / 8.0 / 8.1, use PHP's source-only backports or a commercial LTS / distribution vendor's
patched build. Treat this as a bridge with a **hard expiry date**, not a destination. PHP 8.2
itself reaches end of life on **December 31, 2026**.

### 3. Run a time-boxed compatibility sprint
Use static analysis and compatibility tooling (e.g. PHPCompatibility rule sets) plus AI-assisted
refactoring to move to PHP 8.4 / 8.5. The same AI acceleration that weaponized PHP2Shell also
cuts migration effort. Test with production-like traffic replays before cutover.

### 4. Strangler-fig the remainder
Where full migration is infeasible within a quarter, put new endpoints on a supported runtime
and progressively route traffic away from the legacy core. Decommission what's left.

### 5. Make it a governance decision
Every legacy system that stays online unpatched needs a **recorded risk acceptance**: owner,
compensating controls, review date — with the economic arithmetic from
[03-economic-impact.md](03-economic-impact.md) beside it. The case almost always favors funded
migration over carrying an unauthenticated pre-auth RCE.

---

**Strategic note for vendors and policymakers.** The PHP Foundation acknowledges these fixes
stalled for months because of a "structural failure," and that PHP security "still depends on a
small group of foundation-funded developers." Organizations whose revenue rides on PHP should
treat funding that capacity as risk reduction, not charity.
