#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright (c) 2026 Lukas Geiger

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
Tool: call_graph
Version: 1.0.0
Author: BACH Team
Created: 2026-02-06

Dependency-Mapping und Call-Graph-Visualisierung fuer BACH v2.
Erzeugt Mermaid-Diagramme als .md Dateien.

Usage:
    python call_graph.py <view> [--filter <pattern>]
    Views: imports, skills, cli, tools, help, full, status
"""
__version__ = "1.0.0"

import ast
import re
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field

SYSTEM_ROOT = Path(__file__).parent.parent
HUB_DIR = SYSTEM_ROOT / "hub"
TOOLS_DIR = SYSTEM_ROOT / "tools"
SKILLS_DIR = SYSTEM_ROOT / "skills"
HELP_DIR = SYSTEM_ROOT / "help"
OUTPUT_DIR = SYSTEM_ROOT / "data" / "graphs"

SKIP_DIRS = {"_archive", "_archive_handlers", "__pycache__", ".git", "node_modules"}
STDLIB = {"os", "sys", "re", "json", "sqlite3", "pathlib", "datetime", "typing",
          "subprocess", "shutil", "hashlib", "time", "math", "collections",
          "dataclasses", "abc", "argparse", "importlib", "traceback", "signal",
          "threading", "copy", "io", "csv", "xml", "urllib", "http", "email",
          "functools", "itertools", "contextlib", "tempfile", "glob", "fnmatch",
          "textwrap", "string", "struct", "codecs", "unicodedata", "logging",
          "warnings", "inspect", "ast", "base64", "uuid", "socket", "zipfile"}


def _san(raw: str) -> str:
    """Sanitize string to valid Mermaid node ID."""
    return re.sub(r'[^a-zA-Z0-9_]', '_', raw)


def _q(label: str) -> str:
    """Quote label for Mermaid."""
    return f'"{label}"' if any(c in label for c in '-./\\()[] ') else label


# ---- Data Structures ----

@dataclass
class Node:
    id: str; label: str; kind: str

@dataclass
class Edge:
    src: str; dst: str; label: str = ""

@dataclass
class Graph:
    title: str = ""
    nodes: Dict[str, Node] = field(default_factory=dict)
    edges: List[Edge] = field(default_factory=list)

    def add(self, id: str, label: str, kind: str):
        if id not in self.nodes:
            self.nodes[id] = Node(id=id, label=label, kind=kind)

    def edge(self, src: str, dst: str, label: str = ""):
        self.edges.append(Edge(src=src, dst=dst, label=label))

    def merge(self, other: 'Graph'):
        self.nodes.update(other.nodes)
        self.edges.extend(other.edges)


# ---- Import Scanner (AST) ----

def scan_imports(base_dir: Path, prefix: str = "") -> Graph:
    """Scanne alle .py Dateien und extrahiere interne Imports."""
    g = Graph(title="Python Import Graph")
    for py in sorted(base_dir.rglob("*.py")):
        if any(s in py.parts for s in SKIP_DIRS):
            continue
        rel = py.relative_to(SYSTEM_ROOT)
        mod_id = _san(str(rel.with_suffix('')))
        mod_label = str(rel.with_suffix('')).replace('\\', '/')

        # Typ bestimmen
        kind = "tool"
        if "hub" in py.parts: kind = "handler"
        elif "_agents" in py.parts: kind = "agent"
        elif "_experts" in py.parts: kind = "expert"
        elif "_services" in py.parts: kind = "service"

        try:
            source = py.read_text(encoding='utf-8', errors='replace')
            tree = ast.parse(source, filename=str(py))
        except (SyntaxError, UnicodeDecodeError):
            continue

        imports = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                mod = node.module
                if node.level > 0:  # Relative import
                    pkg = str(rel.parent).replace('\\', '.').replace('/', '.')
                    mod = f"{pkg}.{mod}" if mod else pkg
                imports.add(mod.split('.')[0] if '.' in mod else mod)
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split('.')[0])

        # Dynamische Imports erkennen
        for m in re.finditer(r'import_module\([f"\']([^"\'{}]+)', source):
            imports.add(m.group(1).split('.')[0])

        # Nur interne Imports behalten
        internal = {i for i in imports if i in ("hub", "tools", "skills", "gui")
                     and i not in STDLIB}

        if internal or prefix == "":
            g.add(mod_id, mod_label, kind)

        for imp in internal:
            target_id = _san(imp)
            g.add(target_id, imp, "handler" if imp == "hub" else "tool")
            g.edge(mod_id, target_id)

    return g


# ---- SKILL.md Scanner ----

def _parse_skill_yaml(path: Path) -> Dict:
    """Parst YAML-Frontmatter aus SKILL.md (ohne PyYAML)."""
    try:
        text = path.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return {}
    m = re.match(r'^---\s*\n(.*?)\n---', text, re.DOTALL)
    if not m:
        return {}
    yaml = m.group(1)
    result = {}
    for key in ("name", "type", "version"):
        km = re.search(rf'^{key}:\s*(.+)$', yaml, re.MULTILINE)
        if km:
            result[key] = km.group(1).strip()
    for section in ("dependencies", "orchestrates"):
        sm = re.search(rf'^{section}:\s*\n((?:\s+\w[\w-]*:.*\n?)*)', yaml, re.MULTILINE)
        if sm:
            result[section] = {}
            for sl in sm.group(1).split('\n'):
                slm = re.match(r'\s+([\w-]+):\s*\[([^\]]*)\]', sl)
                if slm:
                    items = [x.strip() for x in slm.group(2).split(',') if x.strip()]
                    result[section][slm.group(1)] = items
    return result


def scan_skills() -> Graph:
    """Scannt SKILL.md Dateien und baut Skills-Dependency-Graph."""
    g = Graph(title="Skills Dependency Graph")
    skill_dirs = [
        (SKILLS_DIR / "_agents", "agent"),
        (SKILLS_DIR / "_experts", "expert"),
    ]
    for base, kind in skill_dirs:
        if not base.exists():
            continue
        for d in sorted(base.iterdir()):
            if not d.is_dir() or d.name.startswith('_'):
                continue
            skill_id = _san(d.name)
            g.add(skill_id, d.name, kind)

            sm = d / "SKILL.md"
            if sm.exists():
                meta = _parse_skill_yaml(sm)
                deps = meta.get("dependencies", {})
                for t in deps.get("tools", []):
                    tid = _san(t.replace('.py', ''))
                    g.add(tid, t, "tool")
                    g.edge(skill_id, tid)
                for s in deps.get("services", []):
                    sid = _san(s)
                    g.add(sid, s, "service")
                    g.edge(skill_id, sid)
                for w in deps.get("workflows", []):
                    wid = _san(w.replace('.md', ''))
                    g.add(wid, w, "workflow")
                    g.edge(skill_id, wid)
                orch = meta.get("orchestrates", {})
                for e in orch.get("experts", []):
                    eid = _san(e)
                    g.add(eid, e, "expert")
                    g.edge(skill_id, eid, "orchestrates")
                for s in orch.get("services", []):
                    sid = _san(s)
                    g.add(sid, s, "service")
                    g.edge(skill_id, sid, "orchestrates")

    # Workflows als Nodes
    wf_dir = SKILLS_DIR / "workflows"
    if wf_dir.exists():
        for wf in sorted(wf_dir.glob("*.md")):
            wid = _san(wf.stem)
            g.add(wid, wf.name, "workflow")

    # Services
    svc_dir = HUB_DIR / "_services"
    if svc_dir.exists():
        for sd in sorted(svc_dir.iterdir()):
            if sd.is_dir() and not sd.name.startswith('_'):
                sid = _san(f"svc_{sd.name}")
                g.add(sid, sd.name, "service")
    return g


# ---- CLI Reach Scanner ----

def scan_cli() -> Graph:
    """Parst bach.py handler-map und zeigt CLI-Reichweite."""
    g = Graph(title="CLI Reach Graph")
    bach_py = SYSTEM_ROOT / "bach.py"
    if not bach_py.exists():
        return g

    source = bach_py.read_text(encoding='utf-8', errors='replace')
    g.add("bach_py", "bach.py", "cli")

    # Handler-Map extrahieren: "name": lambda: _import_handler("module", "Class")
    for m in re.finditer(
        r'"(\w+)":\s*lambda:\s*_import_handler\("(\w+)",\s*"(\w+)"\)', source
    ):
        cmd, module, cls = m.group(1), m.group(2), m.group(3)
        hid = _san(f"h_{cmd}")
        g.add(hid, cmd, "handler")
        g.edge("bach_py", hid)

        # Handler-Datei scannen fuer tiefere Abhaengigkeiten
        handler_file = HUB_DIR / f"{module}.py"
        if handler_file.exists():
            _scan_handler_reach(g, hid, handler_file)

    return g


def _scan_handler_reach(g: Graph, handler_id: str, handler_file: Path):
    """Scannt einen Handler nach Service/Tool/Skill-Imports."""
    try:
        source = handler_file.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return

    # from tools.X import / from skills._experts.X import
    for m in re.finditer(r'from\s+(tools|skills)[.\w]*\.(\w+)\s+import', source):
        pkg, mod = m.group(1), m.group(2)
        kind = "tool" if pkg == "tools" else "expert"
        tid = _san(f"{pkg}_{mod}")
        g.add(tid, mod, kind)
        g.edge(handler_id, tid)

    # from ._services.X import / _services/X/
    for m in re.finditer(r'_services[/\\.](\w+)', source):
        svc = m.group(1)
        sid = _san(f"svc_{svc}")
        g.add(sid, svc, "service")
        g.edge(handler_id, sid)


# ---- Skills-over-Tools View ----

def scan_skill_tools() -> Graph:
    """Skills als Startpunkte die ueber Tools regieren."""
    g = Graph(title="Skills-to-Tools Governance")
    skill_dirs = [
        (SKILLS_DIR / "_agents", "agent"),
        (SKILLS_DIR / "_experts", "expert"),
    ]
    for base, kind in skill_dirs:
        if not base.exists():
            continue
        for d in sorted(base.iterdir()):
            if not d.is_dir() or d.name.startswith('_'):
                continue
            skill_id = _san(d.name)

            # Spezifische Tools im Skill-Ordner
            specific = list(d.glob("*.py"))
            if not specific and not (d / "SKILL.md").exists():
                continue
            g.add(skill_id, d.name, kind)
            for py in specific:
                if py.name.startswith('_'):
                    continue
                tid = _san(f"spec_{py.stem}")
                g.add(tid, py.name, "tool")
                g.edge(skill_id, tid, "owns")

            # Allgemeine Tools aus SKILL.md dependencies
            sm = d / "SKILL.md"
            if sm.exists():
                meta = _parse_skill_yaml(sm)
                for t in meta.get("dependencies", {}).get("tools", []):
                    tid = _san(f"gen_{t.replace('.py', '')}")
                    g.add(tid, t, "tool")
                    g.edge(skill_id, tid, "uses")
    return g


# ---- Help/Wiki to Skills Mapping ----

def scan_help_skills() -> Graph:
    """Verbindet Help/Wiki-Eintraege mit Skills/Handlern."""
    g = Graph(title="Help/Wiki to Skills Mapping")

    # Help-Dateien scannen
    if HELP_DIR.exists():
        for hf in sorted(HELP_DIR.glob("*.txt")):
            hid = _san(f"help_{hf.stem}")
            g.add(hid, hf.stem, "workflow")  # Help als workflow-Farbe

            # Handler-Name = Help-Dateiname?
            handler_file = HUB_DIR / f"{hf.stem}.py"
            if handler_file.exists():
                tid = _san(f"h_{hf.stem}")
                g.add(tid, hf.stem, "handler")
                g.edge(hid, tid, "documents")

        # Wiki-Eintraege
        wiki_dir = HELP_DIR / "wiki"
        if wiki_dir.exists():
            for wf in sorted(wiki_dir.rglob("*.txt")):
                rel = wf.relative_to(wiki_dir)
                wid = _san(f"wiki_{wf.stem}")
                cat = rel.parent.name if rel.parent.name != "wiki" else "allgemein"
                g.add(wid, f"{cat}/{wf.stem}" if cat != "allgemein" else wf.stem, "partner")

                # Skill-Referenz aus Dateiname oder Inhalt erkennen
                try:
                    content = wf.read_text(encoding='utf-8', errors='replace')[:2000]
                except Exception:
                    continue
                # Suche nach bach --handler oder skill-namen
                for m in re.finditer(r'bach\s+--?(\w+)', content):
                    cmd = m.group(1)
                    if (HUB_DIR / f"{cmd}.py").exists():
                        tid = _san(f"h_{cmd}")
                        g.add(tid, cmd, "handler")
                        g.edge(wid, tid, "references")

        # Tool-Help
        tool_help = HELP_DIR / "tools"
        if tool_help.exists():
            for tf in sorted(tool_help.glob("*.txt")):
                thid = _san(f"thelp_{tf.stem}")
                g.add(thid, tf.stem, "workflow")
                # Passendes Tool?
                for tool_py in TOOLS_DIR.glob(f"*{tf.stem}*.py"):
                    tid = _san(f"t_{tool_py.stem}")
                    g.add(tid, tool_py.stem, "tool")
                    g.edge(thid, tid, "documents")
                    break
    return g


# ---- Mermaid Renderer ----

STYLES = {
    "cli":      ("fill:#E53935,stroke:#B71C1C,color:#fff", "[[{}]]"),
    "handler":  ("fill:#2196F3,stroke:#1565C0,color:#fff", "([{}])"),
    "tool":     ("fill:#FFC107,stroke:#FF8F00,color:#000", "[/{}/]"),
    "agent":    ("fill:#42A5F5,stroke:#1E88E5,color:#fff", "{{{{{}}}}}"),
    "expert":   ("fill:#66BB6A,stroke:#388E3C,color:#fff", "([{}])"),
    "service":  ("fill:#FF7043,stroke:#D84315,color:#fff", "[({})]"),
    "workflow":  ("fill:#BDBDBD,stroke:#757575,color:#000", "[{}]"),
    "partner":  ("fill:#AB47BC,stroke:#7B1FA2,color:#fff", "(({}))"),
}


def render_mermaid(graph: Graph, direction: str = "TD",
                   filter_pat: Optional[str] = None) -> str:
    """Rendert Graph als Mermaid-Markdown."""
    if filter_pat:
        keep = {nid for nid, n in graph.nodes.items()
                if filter_pat.lower() in n.label.lower()}
        # Auch verbundene Nodes behalten
        for e in graph.edges:
            if e.src in keep: keep.add(e.dst)
            if e.dst in keep: keep.add(e.src)
        graph.nodes = {k: v for k, v in graph.nodes.items() if k in keep}
        graph.edges = [e for e in graph.edges
                       if e.src in graph.nodes and e.dst in graph.nodes]

    lines = [f"# {graph.title}", "", f"Generiert: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
             f"Nodes: {len(graph.nodes)} | Edges: {len(graph.edges)}", "",
             "## Legende", "",
             "| Form | Typ | Farbe |",
             "|------|-----|-------|",
             "| Doppel-Rect | CLI | Rot |",
             "| Stadium | Handler/Expert | Blau/Gruen |",
             "| Parallelogramm | Tool | Gelb |",
             "| Hexagon | Agent | Hellblau |",
             "| Zylinder | Service | Orange |",
             "| Rechteck | Workflow/Help | Grau |",
             "| Kreis | Wiki/Partner | Lila |", "",
             "## Graph", "", "```mermaid", f"graph {direction}"]

    # Nodes nach Kind gruppieren
    by_kind: Dict[str, List[Node]] = {}
    for n in graph.nodes.values():
        by_kind.setdefault(n.kind, []).append(n)

    for kind, nodes in sorted(by_kind.items()):
        if len(nodes) > 3:
            lines.append(f"    subgraph {kind.upper()}")
            for n in sorted(nodes, key=lambda x: x.label):
                shape = STYLES.get(n.kind, STYLES["tool"])[1]
                lines.append(f"        {n.id}{shape.format(_q(n.label))}")
            lines.append("    end")
        else:
            for n in nodes:
                shape = STYLES.get(n.kind, STYLES["tool"])[1]
                lines.append(f"    {n.id}{shape.format(_q(n.label))}")

    # Edges
    for e in graph.edges:
        if e.src in graph.nodes and e.dst in graph.nodes:
            if e.label:
                lines.append(f"    {e.src} -->|{e.label}| {e.dst}")
            else:
                lines.append(f"    {e.src} --> {e.dst}")

    # Style classes
    lines.append("")
    for kind, (style, _) in STYLES.items():
        lines.append(f"    classDef {kind} {style}")
    for kind, nodes in by_kind.items():
        if nodes:
            ids = ",".join(n.id for n in nodes)
            lines.append(f"    class {ids} {kind}")

    lines.extend(["```", ""])
    return "\n".join(lines)


# ---- Orchestrator ----

def generate_view(view: str, filter_pat: Optional[str] = None) -> str:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if view == "status":
        return _status()

    builders = {
        "imports": lambda: scan_imports(SYSTEM_ROOT),
        "skills":  scan_skills,
        "cli":     scan_cli,
        "tools":   scan_skill_tools,
        "help":    scan_help_skills,
    }

    if view == "full":
        g = Graph(title="BACH v2 - Full System Map")
        for name, builder in builders.items():
            if name != "imports":  # imports zu gross fuer full
                g.merge(builder())
        direction = "LR"
    elif view in builders:
        g = builders[view]()
        direction = "LR" if view in ("cli", "tools") else "TD"
    else:
        return f"[FEHLER] Unbekannte Ansicht: {view}\nVerfuegbar: imports, skills, cli, tools, help, full, status"

    md = render_mermaid(g, direction, filter_pat)
    out = OUTPUT_DIR / f"graph_{view}.md"
    out.write_text(md, encoding='utf-8')
    return f"[OK] {out.relative_to(SYSTEM_ROOT)}\n     {len(g.nodes)} Nodes, {len(g.edges)} Edges"


def _status() -> str:
    py_hub = len(list(HUB_DIR.glob("*.py"))) if HUB_DIR.exists() else 0
    py_tools = len(list(TOOLS_DIR.glob("*.py"))) if TOOLS_DIR.exists() else 0
    agents = len([d for d in (SKILLS_DIR / "_agents").iterdir()
                  if d.is_dir() and not d.name.startswith('_')]) if (SKILLS_DIR / "_agents").exists() else 0
    experts = len([d for d in (SKILLS_DIR / "_experts").iterdir()
                   if d.is_dir() and not d.name.startswith('_')]) if (SKILLS_DIR / "_experts").exists() else 0
    services = len([d for d in (HUB_DIR / "_services").iterdir()
                    if d.is_dir()]) if (HUB_DIR / "_services").exists() else 0
    workflows = len(list((SKILLS_DIR / "workflows").glob("*.md"))) if (SKILLS_DIR / "workflows").exists() else 0
    helps = len(list(HELP_DIR.glob("*.txt"))) if HELP_DIR.exists() else 0
    wikis = len(list((HELP_DIR / "wiki").rglob("*.txt"))) if (HELP_DIR / "wiki").exists() else 0

    existing = [f.name for f in OUTPUT_DIR.glob("graph_*.md")] if OUTPUT_DIR.exists() else []

    return "\n".join([
        "BACH v2 System Map",
        "=" * 40,
        f"  Handler:     {py_hub:>4} (.py in hub/)",
        f"  Tools:       {py_tools:>4} (.py in tools/)",
        f"  Agents:      {agents:>4} (agents/)",
        f"  Experts:     {experts:>4} (agents/_experts/)",
        f"  Services:    {services:>4} (hub/_services/)",
        f"  Workflows:   {workflows:>4} (skills/workflows/)",
        f"  Help:        {helps:>4} (docs/docs/docs/help/*.txt)",
        f"  Wiki:        {wikis:>4} (wiki/)",
        "",
        f"Generierte Graphen: {', '.join(existing) if existing else 'keine'}",
        f"Output: data/graphs/",
        "",
        "Views:",
        "  bach map imports          Python-Import-Graph",
        "  bach map skills           Skills/Agents/Experts Abhaengigkeiten",
        "  bach map cli              CLI-Reichweite ab bach.py",
        "  bach map tools            Skills regieren ueber Tools",
        "  bach map help             Help/Wiki zu Skills Mapping",
        "  bach map full             Alles kombiniert",
        "  bach map status           Diese Uebersicht",
        "  --filter <muster>         Graph filtern",
    ])


def main():
    args = sys.argv[1:]
    view = args[0] if args else "status"
    filt = None
    for i, a in enumerate(args):
        if a in ("--filter", "-f") and i + 1 < len(args):
            filt = args[i + 1]
    print(generate_view(view, filt))
    return 0


if __name__ == "__main__":
    sys.exit(main())
