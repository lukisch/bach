#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
"""Tests for PIZZA v3.4.0 - Agent Portability + New Modules

Some agents (research_agent, plan_agent) overwrite sys.stdout on import
with io.TextIOWrapper for Windows encoding fixes. We prevent this by
temporarily faking sys.platform during import so the win32 guard is skipped.
"""
import pytest
import sys
import os
import json
import tempfile
from pathlib import Path

# Add system to path
_SYSTEM_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(_SYSTEM_DIR))
sys.path.insert(0, str(_SYSTEM_DIR / "tools" / "agents"))
sys.path.insert(0, str(_SYSTEM_DIR / "hub"))


def _import_without_stdout_hack(module_name):
    """Import a module while preventing sys.stdout overwrite.

    Agents like research_agent.py do:
        if sys.platform == 'win32':
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, ...)
    This destroys pytest's capture buffer. We fake platform during import.
    """
    original_platform = sys.platform
    sys.platform = "linux_fake_for_test"
    try:
        mod = __import__(module_name)
    finally:
        sys.platform = original_platform
    return mod


# Pre-import modules safely
try:
    from portable_base import PortableAgent, BACH_AVAILABLE
    _PORTABLE_AVAILABLE = True
except ImportError:
    _PORTABLE_AVAILABLE = False

try:
    _research_mod = _import_without_stdout_hack("research_agent")
    _RESEARCH_AVAILABLE = True
except ImportError:
    _RESEARCH_AVAILABLE = False

try:
    _entwickler_mod = _import_without_stdout_hack("entwickler_agent")
    _ENTWICKLER_AVAILABLE = True
except ImportError:
    _ENTWICKLER_AVAILABLE = False

try:
    _plan_mod = _import_without_stdout_hack("plan_agent")
    _PLAN_AVAILABLE = True
except ImportError:
    _PLAN_AVAILABLE = False

try:
    from reminder_injector import ReminderInjector
    _REMINDER_AVAILABLE = True
except ImportError:
    _REMINDER_AVAILABLE = False

try:
    from meta_feedback_injector import MetaFeedbackInjector, DEFAULT_PATTERNS
    _META_FB_AVAILABLE = True
except ImportError:
    _META_FB_AVAILABLE = False


# ============================================================
# 1. Portability Tests (portable_base.py)
# ============================================================

class TestPortableBase:
    """Tests fuer portable_base.py"""

    @pytest.mark.skipif(not _PORTABLE_AVAILABLE, reason="portable_base not available")
    def test_portable_base_import(self):
        """Import PortableAgent, verify BACH_AVAILABLE flag exists."""
        assert isinstance(BACH_AVAILABLE, bool)
        assert hasattr(PortableAgent, "AGENT_NAME")
        assert hasattr(PortableAgent, "VERSION")

    @pytest.mark.skipif(not _PORTABLE_AVAILABLE, reason="portable_base not available")
    def test_portable_base_standalone_config(self):
        """Create a PortableAgent subclass, verify standalone_config_template() returns dict."""

        class DummyAgent(PortableAgent):
            AGENT_NAME = "DummyTestAgent"
            VERSION = "0.0.1"

            def run(self, **kwargs):
                return {"ok": True}

            def status(self):
                return {"agent": self.AGENT_NAME}

            def config(self):
                return self._config

            def standalone_config_template(self):
                return {"agent": self.AGENT_NAME, "test": True}

        agent = DummyAgent()
        cfg = agent.standalone_config_template()
        assert isinstance(cfg, dict)
        assert cfg["agent"] == "DummyTestAgent"
        assert cfg["test"] is True


class TestResearchAgentStandalone:
    """Tests fuer ResearchAgent Standalone-Betrieb."""

    @pytest.mark.skipif(not _RESEARCH_AVAILABLE, reason="ResearchAgent not available")
    def test_research_agent_standalone(self):
        """Import ResearchAgent, call status(), verify no crash."""
        agent = _research_mod.ResearchAgent()
        st = agent.status()
        assert isinstance(st, dict)
        assert "version" in st
        assert st.get("version") == "2.0.0"

    @pytest.mark.skipif(not _RESEARCH_AVAILABLE, reason="ResearchAgent not available")
    def test_research_agent_config(self):
        """Verify ResearchAgent standalone_config_template returns expected keys."""
        agent = _research_mod.ResearchAgent()
        cfg = agent.standalone_config_template()
        assert isinstance(cfg, dict)
        assert "agent" in cfg
        assert cfg["agent"] == "ResearchAgent"


class TestEntwicklerAgentStandalone:
    """Tests fuer EntwicklerAgent Standalone-Betrieb."""

    @pytest.mark.skipif(not _ENTWICKLER_AVAILABLE, reason="EntwicklerAgent not available")
    def test_entwickler_agent_standalone(self):
        """Import EntwicklerAgent, call status_report(), verify no crash."""
        agent = _entwickler_mod.EntwicklerAgent()
        report = agent.status_report()
        assert isinstance(report, str)
        assert "ENTWICKLER-AGENT" in report

    @pytest.mark.skipif(not _ENTWICKLER_AVAILABLE, reason="EntwicklerAgent not available")
    def test_entwickler_agent_status_dict(self):
        """Verify EntwicklerAgent status() returns dict with expected keys."""
        agent = _entwickler_mod.EntwicklerAgent()
        st = agent.status()
        assert isinstance(st, dict)
        assert "agent" in st
        assert st["agent"] == "EntwicklerAgent"
        assert "bach_available" in st


class TestPlanAgent:
    """Tests fuer PlanAgent."""

    @pytest.mark.skipif(not _PLAN_AVAILABLE, reason="PlanAgent not available")
    def test_plan_agent_create_plan(self):
        """Import PlanAgent, create a plan, verify JSON structure."""
        agent = _plan_mod.PlanAgent()
        plan = agent.create_plan(
            title="Test-Plan",
            goal="Testplan fuer PIZZA v3.4.0",
            steps=[
                {"title": "Schritt 1", "description": "Erster Schritt"},
                {"title": "Schritt 2", "description": "Zweiter Schritt",
                 "dependencies": ["step-0"]},
            ],
        )
        assert isinstance(plan, dict)
        assert "id" in plan
        assert plan["title"] == "Test-Plan"
        assert plan["status"] == "draft"
        assert len(plan["steps"]) == 2
        assert plan["steps"][0]["id"] == "step-0"
        assert plan["steps"][1]["dependencies"] == ["step-0"]

        # Cleanup
        plan_path = Path(agent._plan_path(plan["id"]))
        if plan_path.exists():
            plan_path.unlink()

    @pytest.mark.skipif(not _PLAN_AVAILABLE, reason="PlanAgent not available")
    def test_plan_agent_add_step(self):
        """Create plan, add step, verify dependency handling."""
        agent = _plan_mod.PlanAgent()
        plan = agent.create_plan(title="Step-Test", goal="Testen")
        plan_id = plan["id"]

        step = agent.add_step(
            plan_id,
            title="Neuer Schritt",
            description="Dynamisch hinzugefuegt",
            dependencies=["step-0"],
        )
        assert step["id"] == "step-0"  # First step added
        assert step["title"] == "Neuer Schritt"
        assert step["dependencies"] == ["step-0"]

        # Verify plan was updated
        updated = agent.get_plan(plan_id)
        assert len(updated["steps"]) == 1

        # Cleanup
        plan_path = Path(agent._plan_path(plan_id))
        if plan_path.exists():
            plan_path.unlink()

    @pytest.mark.skipif(not _PLAN_AVAILABLE, reason="PlanAgent not available")
    def test_plan_agent_status(self):
        """Verify PlanAgent status() returns expected structure."""
        agent = _plan_mod.PlanAgent()
        st = agent.status()
        assert isinstance(st, dict)
        assert st["agent"] == "PlanAgent"
        assert "plans_total" in st


# ============================================================
# 2. Injector Tests
# ============================================================

class TestReminderInjector:
    """Tests fuer reminder_injector.py"""

    @pytest.mark.skipif(not _REMINDER_AVAILABLE, reason="ReminderInjector not available")
    def test_reminder_injector_create(self):
        """Create ReminderInjector with temp JSON fallback, add reminder, verify."""
        with tempfile.TemporaryDirectory() as tmp:
            injector = ReminderInjector(base_path=tmp)
            result = injector.add_reminder(
                "Teste immer auf Deutsch",
                trigger_condition="always",
                priority=1,
            )
            assert isinstance(result, dict)
            assert result["message"] == "Teste immer auf Deutsch"
            assert result["trigger_condition"] == "always"
            assert "id" in result

    @pytest.mark.skipif(not _REMINDER_AVAILABLE, reason="ReminderInjector not available")
    def test_reminder_injector_inject(self):
        """Add 'always' reminder, call inject(), verify prompt contains reminder."""
        with tempfile.TemporaryDirectory() as tmp:
            injector = ReminderInjector(base_path=tmp)
            injector.add_reminder("Deutsch antworten", trigger_condition="always")

            result = injector.inject("Hallo Welt", context={})
            assert "Deutsch antworten" in result
            assert "[BACH-REMINDERS]" in result
            assert "Hallo Welt" in result

    @pytest.mark.skipif(not _REMINDER_AVAILABLE, reason="ReminderInjector not available")
    def test_reminder_injector_invalid_trigger(self):
        """Verify invalid trigger raises ValueError."""
        with tempfile.TemporaryDirectory() as tmp:
            injector = ReminderInjector(base_path=tmp)
            with pytest.raises(ValueError, match="Ungueltiger Trigger"):
                injector.add_reminder("test", trigger_condition="invalid_type")


class TestMetaFeedbackInjector:
    """Tests fuer meta_feedback_injector.py"""

    @pytest.mark.skipif(not _META_FB_AVAILABLE, reason="MetaFeedbackInjector not available")
    def test_meta_feedback_injector_create(self):
        """Create MetaFeedbackInjector, verify default patterns loaded."""
        with tempfile.TemporaryDirectory() as tmp:
            injector = MetaFeedbackInjector(base_path=tmp)
            patterns = injector._list_patterns(active_only=False)
            assert isinstance(patterns, list)
            assert len(patterns) >= 3  # 3 DEFAULT_PATTERNS

    @pytest.mark.skipif(not _META_FB_AVAILABLE, reason="MetaFeedbackInjector not available")
    def test_meta_feedback_check(self):
        """Check a response containing emojis, verify pattern detected."""
        with tempfile.TemporaryDirectory() as tmp:
            injector = MetaFeedbackInjector(base_path=tmp)
            matches = injector.check_response("Hier ist das Ergebnis \U0001F600")
            assert isinstance(matches, list)
            assert len(matches) >= 1
            corrections = [m["correction"] for m in matches]
            assert any("Emoji" in c for c in corrections)

    @pytest.mark.skipif(not _META_FB_AVAILABLE, reason="MetaFeedbackInjector not available")
    def test_meta_feedback_inject_corrections(self):
        """Verify inject_corrections adds block when patterns have hits."""
        with tempfile.TemporaryDirectory() as tmp:
            injector = MetaFeedbackInjector(base_path=tmp)
            # First trigger a pattern to set frequency > 0
            injector.check_response("Sure, here is the answer \U0001F600")
            # Now inject should add the correction block
            result = injector.inject_corrections("Teste prompt")
            assert "[BACH-META-FEEDBACK]" in result
            assert "Teste prompt" in result


# ============================================================
# 3. Bridge Server Tests
# ============================================================

class TestBridgeServer:
    """Tests fuer Bridge Server (server_api + config)."""

    def test_server_api_import(self):
        """Import server_api module (skip if FastAPI not installed)."""
        bridge_dir = _SYSTEM_DIR / "hub" / "_services" / "claude_bridge"
        if str(bridge_dir) not in sys.path:
            sys.path.insert(0, str(bridge_dir))

        try:
            import server_api
            assert hasattr(server_api, "HAS_FASTAPI")
        except ImportError:
            pytest.skip("server_api konnte nicht importiert werden")

    def test_bridge_config_has_mode(self):
        """Read config.json, verify 'mode' and 'server' fields exist."""
        config_path = (
            _SYSTEM_DIR / "hub" / "_services" / "claude_bridge" / "config.json"
        )
        if not config_path.exists():
            pytest.skip(f"Bridge config nicht gefunden: {config_path}")

        with open(config_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)

        assert "mode" in cfg, "config.json hat kein 'mode' Feld"
        assert "server" in cfg, "config.json hat kein 'server' Feld"
        assert "host" in cfg["server"]
        assert "port" in cfg["server"]


# ============================================================
# 4. llmauto Tests
# ============================================================

class TestLlmauto:
    """Tests fuer llmauto Module."""

    def test_llmauto_config_bach_available(self):
        """Import llmauto config, verify BACH_AVAILABLE is bool."""
        import importlib.util
        config_path = _SYSTEM_DIR / "tools" / "llmauto" / "core" / "config.py"
        if not config_path.exists():
            pytest.skip(f"llmauto config.py nicht gefunden: {config_path}")

        spec = importlib.util.spec_from_file_location(
            "llmauto_core_config", str(config_path)
        )
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            pytest.skip(f"llmauto config import fehlgeschlagen: {e}")

        assert hasattr(mod, "BACH_AVAILABLE")
        assert isinstance(mod.BACH_AVAILABLE, bool)

    def test_llmauto_pyproject_exists(self):
        """Verify pyproject.toml exists and has correct entry point."""
        pyproject = _SYSTEM_DIR / "tools" / "llmauto" / "pyproject.toml"
        assert pyproject.exists(), f"pyproject.toml nicht gefunden: {pyproject}"

        content = pyproject.read_text(encoding="utf-8")
        assert 'llmauto = "llmauto.llmauto:main"' in content

    def test_swarm_chains_valid_json(self):
        """Load swarm_haiku_3.json and swarm_haiku_research.json, verify valid JSON."""
        chains_dir = _SYSTEM_DIR / "tools" / "llmauto" / "chains"

        for name in ("swarm_haiku_3.json", "swarm_haiku_research.json"):
            chain_path = chains_dir / name
            assert chain_path.exists(), f"Chain-Datei nicht gefunden: {chain_path}"

            with open(chain_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            assert isinstance(data, dict), f"{name} ist kein JSON-Objekt"
            assert "chain_name" in data, f"{name} hat kein 'chain_name'"
            assert "links" in data, f"{name} hat kein 'links'"
            assert "mode" in data, f"{name} hat kein 'mode'"
            assert len(data["links"]) > 0, f"{name} hat keine Links"
