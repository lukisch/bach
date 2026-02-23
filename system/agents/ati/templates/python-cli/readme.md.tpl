# ${project_name}

${description}

## Installation

```bash
pip install -e .
```

## Usage

```bash
python -m ${project_name} --help
```

## Structure

```
${project_name}/
├── src/${project_name}/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   └── core/
├── tests/
├── docs/
├── _modules/        # BACH wiederverwendbare Module
├── _policies/       # BACH Policies
├── CHANGELOG.md
└── README.md
```

## Development

```bash
# Tests
pytest

# Lint
ruff check .
```

## License

MIT

---
*Generated with ATI Project Bootstrapper*
