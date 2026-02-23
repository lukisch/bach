#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Distribution Module - Minimal Version v1.0.0

Wiederverwendbares Modul aus BACH extrahiert fuer:
- Tier-Klassifizierung (Kernel, Core, Extension, UserData)
- Siegel-System (Datei-Hashes fuer Integritaet)
- Versions-Parsing

Kann in beliebige Projekte injiziert werden.

Quelle: BACH tools/distribution_system.py (1185 Zeilen -> 150 Zeilen)
Datum: 2026-01-22
"""

import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


class TierClassifier:
    """Klassifiziert Dateien nach Tier-System."""
    
    TIERS = {
        'kernel': {
            'id': 1,
            'patterns': ['__init__.py', 'core/', 'main.py', 'cli.py'],
            'description': 'Unveraenderbare Kernkomponenten'
        },
        'core': {
            'id': 2,
            'patterns': ['src/', 'lib/', 'handlers/'],
            'description': 'Zentrale Komponenten'
        },
        'extension': {
            'id': 3,
            'patterns': ['plugins/', 'modules/', 'extensions/'],
            'description': 'Erweiterbare Komponenten'
        },
        'userdata': {
            'id': 4,
            'patterns': ['data/', 'user/', 'config/', '_memory/'],
            'description': 'Benutzerdaten und Konfiguration'
        }
    }
    
    def classify(self, path: Path) -> str:
        """Klassifiziert eine Datei nach Tier."""
        path_str = str(path).replace('\\', '/')
        
        for tier_name, tier_info in self.TIERS.items():
            for pattern in tier_info['patterns']:
                if pattern in path_str or path_str.endswith(pattern):
                    return tier_name
        
        return 'extension'  # Default
    
    def get_tier_id(self, tier_name: str) -> int:
        """Gibt die numerische Tier-ID zurueck."""
        return self.TIERS.get(tier_name, {}).get('id', 3)


class SiegelManager:
    """Verwaltet Datei-Siegel (Hashes) fuer Integritaetspruefung."""
    
    def __init__(self, project_root: Path):
        self.root = project_root
        self.siegel_file = project_root / '_data' / 'siegel.json'
    
    def compute_hash(self, file_path: Path) -> str:
        """Berechnet SHA-256 Hash einer Datei."""
        if not file_path.exists():
            return ''
        
        sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    
    def create_siegel(self, files: List[Path]) -> Dict[str, str]:
        """Erstellt Siegel fuer mehrere Dateien."""
        return {
            str(f.relative_to(self.root)): self.compute_hash(f)
            for f in files if f.exists()
        }
    
    def verify_siegel(self, siegel: Dict[str, str]) -> Dict[str, str]:
        """Prueft Siegel und gibt Differenzen zurueck."""
        diff = {}
        for rel_path, expected_hash in siegel.items():
            file_path = self.root / rel_path
            actual_hash = self.compute_hash(file_path)
            
            if actual_hash != expected_hash:
                if not file_path.exists():
                    diff[rel_path] = 'missing'
                else:
                    diff[rel_path] = 'modified'
        
        return diff
    
    def save_siegel(self, siegel: Dict[str, str]):
        """Speichert Siegel in JSON-Datei."""
        self.siegel_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.siegel_file, 'w', encoding='utf-8') as f:
            json.dump({
                'created': datetime.now().isoformat(),
                'files': siegel
            }, f, indent=2)
    
    def load_siegel(self) -> Optional[Dict[str, str]]:
        """Laedt Siegel aus JSON-Datei."""
        if not self.siegel_file.exists():
            return None
        
        with open(self.siegel_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('files', {})


class VersionParser:
    """Parst und validiert Versionsnummern."""
    
    SOURCES = ['release', 'dev', 'learn', 'evo', 'user', 'fork']
    
    @staticmethod
    def parse(version_str: str) -> Dict:
        """Parst Version wie '1.2.3-dev' in Komponenten."""
        parts = version_str.split('-')
        version_parts = parts[0].split('.')
        
        return {
            'major': int(version_parts[0]) if len(version_parts) > 0 else 0,
            'minor': int(version_parts[1]) if len(version_parts) > 1 else 0,
            'patch': int(version_parts[2]) if len(version_parts) > 2 else 0,
            'source': parts[1] if len(parts) > 1 else 'release'
        }
    
    @staticmethod
    def format(major: int, minor: int, patch: int, source: str = 'release') -> str:
        """Formatiert Version zurueck zu String."""
        version = f"{major}.{minor}.{patch}"
        if source != 'release':
            version += f"-{source}"
        return version
    
    @staticmethod
    def bump(version_str: str, level: str = 'patch') -> str:
        """Erhoeht Version um ein Level (major/minor/patch)."""
        parsed = VersionParser.parse(version_str)
        
        if level == 'major':
            parsed['major'] += 1
            parsed['minor'] = 0
            parsed['patch'] = 0
        elif level == 'minor':
            parsed['minor'] += 1
            parsed['patch'] = 0
        else:  # patch
            parsed['patch'] += 1
        
        return VersionParser.format(
            parsed['major'], parsed['minor'], parsed['patch'], parsed['source']
        )


# Convenience Functions
def classify_file(path: Path) -> str:
    """Klassifiziert eine Datei nach Tier."""
    return TierClassifier().classify(path)


def compute_file_hash(file_path: Path) -> str:
    """Berechnet SHA-256 Hash einer Datei."""
    return SiegelManager(file_path.parent).compute_hash(file_path)


def bump_version(version: str, level: str = 'patch') -> str:
    """Erhoeht Version um ein Level."""
    return VersionParser.bump(version, level)


if __name__ == '__main__':
    # Test
    print("Distribution Module - Minimal Version")
    print(f"Tiers: {list(TierClassifier.TIERS.keys())}")
    print(f"Version bump: 1.2.3 -> {bump_version('1.2.3')}")
    print(f"Version bump minor: 1.2.3 -> {bump_version('1.2.3', 'minor')}")
