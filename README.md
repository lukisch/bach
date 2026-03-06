<p align="center">
  <img src="ellmos-logo.jpg" alt="ellmos logo" width="300">
</p>

# ellmos BACH - Text-Based Operating System for LLMs

*The stream that unites everything.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-green)
![Version](https://img.shields.io/badge/Version-v3.7.0--waterfall-orange)
![Status](https://img.shields.io/badge/Status-Production--Ready-brightgreen)

**Version:** v3.7.0-waterfall

## Overview

**BACH** is a text-based operating system that empowers Large Language Models (LLMs) to work autonomously, learn, and self-organize. Part of the **ellmos** family (Extra Large Language Model Operating Systems), BACH provides comprehensive infrastructure for task management, knowledge management, automation, and LLM orchestration.

### Key Features

- **109+ Handlers** - Full CLI and API coverage of all system functions
- **373+ Tools** - Extensive tool library for file processing, analysis, and automation
- **932+ Skills** - Reusable workflows and templates
- **54 Protocol Workflows** - Pre-built process workflows
- **Knowledge Store** - Lessons, Facts, and Multi-Level Memory System
- **Agent CLI** - `bach agent start/stop/list` for direct agent control
- **Prompt System** - Central prompt management with board system and versioning
- **SharedMemory Bus** - Multi-agent coordination with conflict detection and decay
- **USMC Bridge** - United Shared Memory Communication for cross-agent communication
- **llmauto Chains** - Claude prompts as chain steps with `bach://` URL resolution

## Installation

```bash
# Clone the repository
git clone https://github.com/lukisch/bach.git
cd bach

# Install dependencies
pip install -r requirements.txt

# Initialize BACH
python system/setup.py
```

## MCP Servers (Claude Code Integration)

BACH provides two MCP servers for integration with Claude Code, Cursor, and other IDEs:

```bash
# Install and configure MCP servers (recommended)
python system/bach.py setup mcp

# Or manually via npm:
npm install -g bach-codecommander-mcp bach-filecommander-mcp
```

- **[bach-codecommander-mcp](https://www.npmjs.com/package/bach-codecommander-mcp)** - Code analysis and refactoring tools
- **[bach-filecommander-mcp](https://www.npmjs.com/package/bach-filecommander-mcp)** - File management and batch operations

## Quick Start

```bash
# Start BACH
python bach.py --startup

# Create a task
python bach.py task add "Analyze project structure"

# Manage agents
python bach.py agent list
python bach.py agent start bueroassistent

# Manage prompts
python bach.py prompt list
python bach.py prompt add "My Prompt" --content "..."

# Check scheduler status
python bach.py scheduler status

# Shut down BACH
python bach.py --shutdown
```

## Core Components

### 1. Task Management
Full GTD system with prioritization, deadlines, tags, and context tracking.

### 2. Knowledge System
Structured memory system with Facts, Lessons, and automatic consolidation (5 memory types).

### 3. Agent Framework
Boss agents orchestrate experts for complex tasks. The Agent CLI allows direct starting, stopping, and listing of agents via `bach agent`.

<p align="center">
  <img src="sketch_bach_boss_agents.jpg" alt="BACH Boss Agents" width="600"><br>
  <i>The 5 Boss Agents: ati, officeassistant, finance-assistant, health-assistant, personal-assistant</i>
</p>

<p align="center">
  <img src="sketch_fachexperten_en_new.jpg" alt="BACH Experts" width="600"><br>
  <i>14 specialized Experts working under their Boss Agents</i>
</p>

### 4. Prompt System
Central management of prompt templates with board collections and full versioning (`bach prompt`).

### 5. Bridge System
Connector framework for external services (Telegram, Email, WhatsApp, etc.) and USMC Bridge for cross-agent communication.

### 6. Automation
SchedulerService for time-based jobs (chains, tasks, scripts) and event-driven workflows via the hook framework.

### 7. SharedMemory
Multi-agent coordination with context generation, conflict detection, decay, and delta queries.

### 8. llmauto Integration
Chain steps as LLM prompts with `bach://` URL resolution for dynamic context embedding.

## The ellmos Family

All ellmos projects follow a water metaphor -- from a spring to a full stream:

| Tier | Project | Description | Repository |
|------|---------|-------------|------------|
| 1 | **USMC** | United Shared Memory Client -- the spring (shared memory only) | [github.com/lukisch/usmc](https://github.com/lukisch/usmc) |
| 2 | **Rinnsal** | The trickle -- USMC + llmauto (LLM orchestration), extremely compact | [github.com/lukisch/rinnsal](https://github.com/lukisch/rinnsal) |
| 3 | **BACH** | The stream that unites everything -- 109+ handlers, 932+ skills, agents, GUI, bridge | [github.com/lukisch/bach](https://github.com/lukisch/bach) |

## Documentation

- **[Quickstart Guide](QUICKSTART.md)** - Get your first workflow running in 5 minutes
- **[User Manual](BACH_USER_MANUAL.md)** - Complete handbook
- **[Skills Catalog](SKILLS.md)** - All available skills
- **[Agents Catalog](AGENTS.md)** - All available agents and experts
- **[Workflows](WORKFLOWS.md)** - 54 protocol workflows
- **[SKILL.md](SKILL.md)** - LLM operating instructions (for Claude, Gemini, Ollama)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Support

- **Issues:** [GitHub Issues](https://github.com/lukisch/bach/issues)
- **Discussions:** [GitHub Discussions](https://github.com/lukisch/bach/discussions)

---

## Deutsche Version

BACH ist ein textbasiertes Betriebssystem, das Large Language Models (LLMs) befaehigt, eigenstaendig zu arbeiten, zu lernen und sich zu organisieren.

Die vollstaendige deutsche Dokumentation findest du hier: **[README.de.md](README.de.md)**

---

*ellmos BACH v3.7.0-waterfall - Text-Based Operating System for LLMs*
