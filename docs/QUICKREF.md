# Responder Quick Reference

One page for the first seventy-two hours. Full roadmap:
[04-remediation-roadmap.md](04-remediation-roadmap.md). Live briefing:
[barryhurd.com](https://barryhurd.com/project/php2shell-blast-radius-deploy.html).

## Am I exposed?

```bash
python3 tools/php_patch_check.py --local          # this host
python3 tools/php_patch_check.py 8.3.20           # one version
python3 tools/php_patch_check.py --inventory f.csv # a fleet
```

## Safe builds (upgrade targets)

| Branch | Fixed build | Status |
|---|---|---|
| 8.5 | `8.5.12` | Active support |
| 8.4 | `8.4.27` | Active support |
| 8.3 | `8.3.36` | Security-only |
| 8.2 | `8.2.35` | Security-only, EOL 2026-12-31 |
| 8.1 / 8.0 / 7.4 | backport only | End of life: backport, or isolate; migrate |
| 7.3 and older / 5.x | none, ever | Isolate or take offline; migrate |

## Verdict to action

| Verdict | Do this |
|---|---|
| SAFE | Confirm every worker was restarted after upgrade. |
| VULNERABLE - PATCH NOW | Upgrade to the fixed build, restart workers. |
| VULNERABLE - NO UPSTREAM FIX | Take a vendor/LTS/source backport, or isolate; migrate. |
| VULNERABLE - ABANDONED | Isolate or take offline (NSA fallback); migrate off. |
| VERIFY WITH VENDOR | Distro build below the number: check your vendor advisory, the fix may be backported. |

## php.ini stopgaps (buy hours, not weeks)

Set at pool level, not `ini_set()`, then restart every worker:

```ini
session.upload_progress.enabled = 0        ; closes the CVE-2026-109619 path
memory_limit = -1                          ; only with a cgroup/container cap, never RLIMIT
post_max_size = 8M                         ; shrink the multipart window
fatal_error_backtraces = 0                 ; PHP 8.5 only
```

Also: enable your WAF's PHP2Shell ruleset, and reject `multipart/form-data` where feasible. PHP
states these "do not make an installation safe."

## The three phases

1. **Identify and Isolate (H+0 to 12).** Inventory from running processes, not banners. Rank
   internet-facing mod_php first, then payment and auth systems. Isolate what cannot patch today.
2. **Mitigate (H+0 to 24).** WAF rules, block multipart, apply the php.ini set together, restart
   workers. Watch for php-fpm spawning shells, oversized PHPSESSID cookies, new .php files.
3. **Patch and Verify (H+0 to 72).** Upgrade, restart everything, verify from a web request not
   the CLI, then assume-breach hunt and rotate all secrets for the exposure window.

## The standing assumption

Any host that was internet-reachable and unpatched after **October 20** should be treated as
potentially compromised. Rotate database credentials, API keys, session secrets, and TLS keys:
the memory-disclosure path leaks them without RCE.

## Detection signals

- php-fpm / php-cgi / httpd / apache2 spawning a shell, interpreter, or download tool
- Bursts of multipart POSTs followed by memory_limit errors or HTTP 500s
- Oversized or malformed PHPSESSID response cookies
- Unexplained worker churn, new .php files, new cron jobs, users, or SSH keys

## When in doubt

Check the [CISA KEV catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog) and
[GreyNoise](https://viz.greynoise.io/) for current exploitation status. More sources in
[news-and-resources.md](news-and-resources.md).
