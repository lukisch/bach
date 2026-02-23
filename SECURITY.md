# Security Policy

## Reporting a Vulnerability

If you find a security vulnerability in BACH, please report it responsibly:

1. **Do NOT open a public issue**
2. **Use GitHub's [private vulnerability reporting](https://github.com/lukisch/bach/security/advisories/new)**
3. Include: description, steps to reproduce, potential impact

### How to Report

1. Go to: https://github.com/lukisch/bach/security/advisories/new
2. Fill out the form (title, description, severity, affected versions)
3. Submit privately (not visible to public until disclosed)

We will respond as soon as possible.

## Scope

BACH runs locally. The main attack surface is:
- Bridge/Connector endpoints (Telegram, Discord, etc.)
- GUI web server (FastAPI, localhost only by default)
- File system access (bach.db, user data)
- MCP server (localhost only)

## Response

As a solo project, response times may vary. Critical issues will be
prioritized. Please allow reasonable time before public disclosure.
