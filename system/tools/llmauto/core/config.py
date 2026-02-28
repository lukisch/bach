"""
llmauto.core.config -- Konfigurationsmanagement
=================================================
Laedt, validiert und speichert Chain-Configs und globale Einstellungen.
"""
import json
import os
from pathlib import Path
from copy import deepcopy

BASE_DIR = Path(__file__).parent.parent

# Bekannte User-Home-Pfade
_KNOWN_USER_HOMES = [
    "C:\\Users\\User\\",
]
_ACTUAL_HOME = str(Path.home()) + os.sep  # z.B. "C:\Users\YourUsername\"


DEFAULT_GLOBAL_CONFIG = {
    "default_model": "claude-sonnet-4-6",
    "default_permission_mode": "dontAsk",
    "default_allowed_tools": ["Read", "Edit", "Write", "Bash", "Glob", "Grep"],
    "default_timeout_seconds": 1800,
    "telegram": {
        "enabled": False,
        "bot_token_env": "LLMAUTO_TELEGRAM_BOT_TOKEN",
        "chat_id": "",
    }
}


DEFAULT_CHAIN_CONFIG = {
    "chain_name": "",
    "description": "",
    "mode": "loop",
    "max_rounds": 100,
    "runtime_hours": 0,
    "deadline": "",
    "max_consecutive_blocks": 5,
    "links": [],
    "prompts": {},
    "task_pools": {},
}


DEFAULT_LINK = {
    "name": "",
    "role": "worker",
    "model": None,
    "fallback_model": None,
    "prompt": "",
    "task_pool": "",
    "telegram_update": False,
    "until_full": False,
    "description": "",
}


def load_global_config():
    """Laedt die globale Konfiguration."""
    config_file = BASE_DIR / "config.json"
    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            user_config = json.load(f)
        config = deepcopy(DEFAULT_GLOBAL_CONFIG)
        config.update(user_config)
        return config
    return deepcopy(DEFAULT_GLOBAL_CONFIG)


def save_global_config(config):
    """Speichert die globale Konfiguration."""
    config_file = BASE_DIR / "config.json"
    with open(config_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def _normalize_paths(obj):
    """Ersetzt bekannte User-Home-Pfade durch den aktuellen.

    Damit funktionieren Chain-Configs auf allen Systemen unabhaengig vom Username.
    und Laptop (C:\\Users\\User) ohne Anpassung.
    """
    if isinstance(obj, str):
        for known in _KNOWN_USER_HOMES:
            if known in obj and known != _ACTUAL_HOME:
                obj = obj.replace(known, _ACTUAL_HOME)
        return obj
    elif isinstance(obj, dict):
        return {k: _normalize_paths(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_normalize_paths(item) for item in obj]
    return obj


def load_chain(name):
    """Laedt eine gespeicherte Chain-Config."""
    chain_file = BASE_DIR / "chains" / f"{name}.json"
    if not chain_file.exists():
        raise FileNotFoundError(f"Kette '{name}' nicht gefunden: {chain_file}")
    with open(chain_file, "r", encoding="utf-8") as f:
        chain = json.load(f)
    # Pfade an aktuelles System anpassen
    chain = _normalize_paths(chain)
    # Defaults anwenden
    config = deepcopy(DEFAULT_CHAIN_CONFIG)
    config.update(chain)
    return config


def save_chain(name, config):
    """Speichert eine Chain-Config."""
    chains_dir = BASE_DIR / "chains"
    chains_dir.mkdir(exist_ok=True)
    chain_file = chains_dir / f"{name}.json"
    with open(chain_file, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4, ensure_ascii=False)


def list_chains():
    """Listet alle gespeicherten Ketten."""
    chains_dir = BASE_DIR / "chains"
    if not chains_dir.exists():
        return []
    return [f.stem for f in chains_dir.glob("*.json")]


def new_link(**kwargs):
    """Erstellt ein neues Kettenglied mit Defaults."""
    link = deepcopy(DEFAULT_LINK)
    link.update(kwargs)
    return link
