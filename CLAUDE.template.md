# BACH Project Instructions

<!-- BACH:START - Automatically generated, do not edit manually -->

*Generated: (automatically populated on first start)*

## System Settings

**SECURITY**
- `secrets_file_path`: ~/.bach/bach_secrets.json

**BEHAVIOR**
- `auto_backup_days`: 30
- `default_retention_days`: 30
- `timeout_checkpoint_minutes`: 10

**INTEGRATION**
- `integration.claude-code.claude_md_path`: (automatically set)

## BACH Lessons (Top 10)

*No lessons stored yet. BACH learns from your sessions.*

<!-- BACH:END -->

## Development Workflow (Single Installation Model, since v3.3.0)

### Changing Code
```bash
# Develop directly in the Git repo
cd /path/to/BACH
# CORE changes: git add + commit + push
git add system/hub/neuer_handler.py
git commit -m "feat: new handler"
git push origin main
```

### User Data is Protected

The `.gitignore` protects:
- `bach.db` and all runtime data
- `user/` directory (personal data)
- Credentials and API keys
- Generated documentation (MEMORY.md, USER.md, SKILLS.md, etc.)

<!--
  NOTE: This file is a template.
  BACH overwrites the BACH:START/END block automatically with real data.
  Variants: OLLAMA.md, GEMINI.md (same structure, different LLM instructions)
-->

---
🇩🇪 [Deutsche Version](CLAUDE.template.de.md)
