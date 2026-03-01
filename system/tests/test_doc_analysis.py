#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests fuer Document Analysis Tools (INT06)

Testet: dedup_scanner.py + privacy_classifier.py
Direkter Import ohne Package __init__ (OCR-Dependency vermeiden).
"""

import importlib.util
import sys
import pytest
from pathlib import Path

BACH_ROOT = Path(__file__).parent.parent


def _load_module(name: str, filename: str):
    """Laedt Modul direkt ohne Package __init__."""
    path = BACH_ROOT / "hub" / "_services" / "document" / filename
    spec = importlib.util.spec_from_file_location(name, str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


dedup_mod = _load_module("dedup_scanner", "dedup_scanner.py")
privacy_mod = _load_module("privacy_classifier", "privacy_classifier.py")

DedupScanner = dedup_mod.DedupScanner
sha256_file = dedup_mod.sha256_file
_fmt_size = dedup_mod._fmt_size

PrivacyClassifier = privacy_mod.PrivacyClassifier
AMPEL_ROT = privacy_mod.AMPEL_ROT
AMPEL_GELB = privacy_mod.AMPEL_GELB
AMPEL_GRUEN = privacy_mod.AMPEL_GRUEN


# ================================================================
# DEDUP SCANNER
# ================================================================

class TestSHA256:
    def test_consistent_hash(self, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("hello world")
        h1 = sha256_file(f)
        h2 = sha256_file(f)
        assert h1 == h2
        assert len(h1) == 64  # SHA256 hex length

    def test_different_content(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("content A")
        f2.write_text("content B")
        assert sha256_file(f1) != sha256_file(f2)

    def test_same_content(self, tmp_path):
        f1 = tmp_path / "a.txt"
        f2 = tmp_path / "b.txt"
        f1.write_text("same content")
        f2.write_text("same content")
        assert sha256_file(f1) == sha256_file(f2)


class TestDedupScanner:
    def test_no_duplicates(self, tmp_path):
        (tmp_path / "a.txt").write_text("unique A")
        (tmp_path / "b.txt").write_text("unique B")
        scanner = DedupScanner()
        result = scanner.scan(tmp_path)
        assert result["total_files"] == 2
        assert result["unique_hashes"] == 2
        assert len(result["duplicate_groups"]) == 0
        assert result["wasted_bytes"] == 0

    def test_with_duplicates(self, tmp_path):
        (tmp_path / "a.txt").write_text("duplicate")
        (tmp_path / "b.txt").write_text("duplicate")
        (tmp_path / "c.txt").write_text("unique")
        scanner = DedupScanner()
        result = scanner.scan(tmp_path)
        assert result["total_files"] == 3
        assert result["unique_hashes"] == 2
        assert len(result["duplicate_groups"]) == 1
        assert result["duplicate_groups"][0]["count"] == 2

    def test_recursive(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.txt").write_text("dup")
        (sub / "b.txt").write_text("dup")
        scanner = DedupScanner()
        result = scanner.scan(tmp_path, recursive=True)
        assert len(result["duplicate_groups"]) == 1

    def test_non_recursive(self, tmp_path):
        sub = tmp_path / "sub"
        sub.mkdir()
        (tmp_path / "a.txt").write_text("dup")
        (sub / "b.txt").write_text("dup")
        scanner = DedupScanner()
        result = scanner.scan(tmp_path, recursive=False)
        assert result["total_files"] == 1  # nur a.txt
        assert len(result["duplicate_groups"]) == 0

    def test_min_size(self, tmp_path):
        (tmp_path / "small.txt").write_text("x")
        (tmp_path / "big.txt").write_text("x" * 1000)
        scanner = DedupScanner(min_size=100)
        result = scanner.scan(tmp_path)
        assert result["total_files"] == 1  # nur big.txt

    def test_single_file(self, tmp_path):
        f = tmp_path / "single.txt"
        f.write_text("content")
        scanner = DedupScanner()
        result = scanner.scan(f)
        assert result["total_files"] == 1

    def test_invalid_path(self):
        scanner = DedupScanner()
        with pytest.raises(ValueError):
            scanner.scan(Path("/nonexistent/path"))

    def test_format_report(self, tmp_path):
        (tmp_path / "a.txt").write_text("dup content")
        (tmp_path / "b.txt").write_text("dup content")
        scanner = DedupScanner()
        result = scanner.scan(tmp_path)
        report = scanner.format_report(result)
        assert "DUPLIKAT-SCAN" in report
        assert "x2" in report


class TestFmtSize:
    def test_bytes(self):
        assert _fmt_size(500) == "500 B"

    def test_kb(self):
        assert "KB" in _fmt_size(2048)

    def test_mb(self):
        assert "MB" in _fmt_size(5 * 1024 * 1024)

    def test_gb(self):
        assert "GB" in _fmt_size(3 * 1024 ** 3)


# ================================================================
# PRIVACY CLASSIFIER
# ================================================================

class TestPrivacyClassifier:
    @pytest.fixture
    def classifier(self):
        return PrivacyClassifier()

    def test_iban_rot(self, classifier):
        r = classifier.classify_text("IBAN: DE89 3704 0044 0532 0130 00")
        assert r["ampel"] == AMPEL_ROT
        assert any(f["pattern"] == "IBAN (DE)" for f in r["findings"])

    def test_steuernummer_rot(self, classifier):
        r = classifier.classify_text("Steuernr 12/345/67890")
        assert r["ampel"] == AMPEL_ROT

    def test_gesundheit_rot(self, classifier):
        r = classifier.classify_text("Diagnose: Diabetes Typ 2, Medikament: Metformin")
        assert r["ampel"] == AMPEL_ROT
        assert any(f["pattern"] == "Gesundheitsdaten" for f in r["findings"])

    def test_email_gelb(self, classifier):
        r = classifier.classify_text("Kontakt: test@example.com")
        assert r["ampel"] == AMPEL_GELB

    def test_telefon_gelb(self, classifier):
        r = classifier.classify_text("Tel: +49 170 1234567")
        assert r["ampel"] == AMPEL_GELB

    def test_geburtsdatum_gelb(self, classifier):
        r = classifier.classify_text("geb. 15.03.1990")
        assert r["ampel"] == AMPEL_GELB

    def test_clean_gruen(self, classifier):
        r = classifier.classify_text("Dies ist ein normaler Text.")
        assert r["ampel"] == AMPEL_GRUEN
        assert len(r["findings"]) == 0

    def test_rot_overrides_gelb(self, classifier):
        r = classifier.classify_text("IBAN: DE89370400440532013000, Email: a@b.com")
        assert r["ampel"] == AMPEL_ROT  # ROT hat Vorrang

    def test_classify_file(self, classifier, tmp_path):
        f = tmp_path / "test.txt"
        f.write_text("IBAN: DE89 3704 0044 0532 0130 00")
        r = classifier.classify_file(f)
        assert r["ampel"] == AMPEL_ROT
        assert r["error"] is None

    def test_classify_file_not_text(self, classifier, tmp_path):
        f = tmp_path / "image.png"
        f.write_bytes(b"\x89PNG")
        r = classifier.classify_file(f)
        assert r["error"] == "Kein Textformat"

    def test_scan_directory(self, classifier, tmp_path):
        (tmp_path / "clean.txt").write_text("Normal text")
        (tmp_path / "sensitive.txt").write_text("IBAN: DE89 3704 0044 0532 0130 00")
        (tmp_path / "internal.txt").write_text("Tel: +49 170 1234567")
        result = classifier.scan_directory(tmp_path)
        assert result["rot"] == 1
        assert result["gelb"] == 1
        assert result["gruen"] == 1

    def test_format_report(self, classifier, tmp_path):
        (tmp_path / "test.txt").write_text("Diagnose: Test")
        result = classifier.scan_directory(tmp_path)
        report = classifier.format_report(result)
        assert "DATENSCHUTZ-SCAN" in report
