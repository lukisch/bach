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
Base Types - Foundation fuer alle Handler
==========================================
Result, ParsedArgs, OpDef - einheitliche Typen fuer CLI und Library.
"""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class Result:
    """Einheitliches Ergebnis eines Handler-Aufrufs."""
    success: bool
    message: str
    data: Any = None

    def __iter__(self):
        """Kompatibilitaet mit (success, message) Tuple-Pattern."""
        yield self.success
        yield self.message

    def __bool__(self):
        return self.success


@dataclass
class ParsedArgs:
    """Geparste Argumente fuer einen Handler-Aufruf."""
    positional: list = field(default_factory=list)
    options: dict = field(default_factory=dict)
    flags: set = field(default_factory=set)

    def get(self, key: str, default: Any = None) -> Any:
        """Holt Option oder Flag."""
        if key in self.flags:
            return True
        return self.options.get(key, default)

    @property
    def first(self) -> Optional[str]:
        """Erstes positionales Argument."""
        return self.positional[0] if self.positional else None

    @property
    def rest(self) -> list:
        """Alle positonalen Argumente ab dem zweiten."""
        return self.positional[1:]

    def to_list(self) -> list:
        """Konvertiert zurueck in flache Argument-Liste (fuer Legacy-Handler)."""
        result = list(self.positional)
        for key, value in self.options.items():
            result.append(f"--{key}")
            result.append(str(value))
        for flag in self.flags:
            result.append(f"--{flag}")
        return result


@dataclass
class OpDef:
    """Definition einer Handler-Operation."""
    args: list = field(default_factory=list)
    opts: dict = field(default_factory=dict)
    flags: list = field(default_factory=list)
    help: str = ""


def parse_args(raw_args: list, op_def: OpDef = None) -> ParsedArgs:
    """Parst rohe Argument-Liste in ParsedArgs."""
    positional = []
    options = {}
    flags = set()

    i = 0
    while i < len(raw_args):
        arg = raw_args[i]
        if arg.startswith("--"):
            if "=" in arg:
                key, value = arg[2:].split("=", 1)
                options[key] = value
            else:
                key = arg[2:]
                if op_def and key in (op_def.flags or []):
                    flags.add(key)
                elif i + 1 < len(raw_args) and not raw_args[i + 1].startswith("--"):
                    options[key] = raw_args[i + 1]
                    i += 1
                else:
                    flags.add(key)
        else:
            positional.append(arg)
        i += 1

    return ParsedArgs(positional=positional, options=options, flags=flags)
