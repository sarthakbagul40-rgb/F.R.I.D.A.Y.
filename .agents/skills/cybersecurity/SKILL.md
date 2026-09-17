---
name: cybersecurity-sentinel
description: 818 MITRE ATT&CK and NIST CSF 2.0 mapped cybersecurity skills for code auditing, secrets scanning, and endpoint hardening.
---

# Cybersecurity Sentinel (Anthropic Cyber Skills Protocol)

On-demand security intelligence, vulnerability scanning, secrets discovery, and MITRE-mapped defense for F.R.I.D.A.Y. OS 10.0.

## When to Activate
Activate ONLY when Boss explicitly asks for:
- "Scan this repo for vulnerabilities"
- "Check for leaked API keys or passwords"
- "Audit my code for security flaws"
- "Perform a MITRE / OWASP security check"
- "Hardening audit on open ports and system configs"

## Core Inspection Domains
1. **Secrets & Credentials (CWE-798)**:
   - Scan files for unencrypted JWT tokens, Stripe/OpenAI/GitHub keys, AWS secret credentials, and database passwords.
   - Verify `.env` is listed in `.gitignore`.
2. **Injection Attacks (CWE-89, CWE-78)**:
   - Check SQL queries for parameterization.
   - Detect raw `shell=True` or `os.system()` with unsanitized user inputs.
3. **Dependency CVE Auditing**:
   - Check `requirements.txt` and `package.json` for known vulnerabilities using local pip/npm audit tools.
4. **Network & Port Surface**:
   - Verify local web servers bind to `localhost` (`127.0.0.1`) rather than public `0.0.0.0` unless explicitly intended.
