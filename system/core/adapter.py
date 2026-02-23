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
Handler Adapter - Bridge zwischen Legacy und New-Style Handlern
================================================================
Konvertiert alte handle(op, args_list, dry_run) -> Tuple
zu neuer API handle(op, ParsedArgs) -> Result.
"""

from .base import Result, ParsedArgs


class HandlerAdapter:
    """Wraps einen Legacy-Handler fuer die neue API.

    Legacy-Signatur:
        handler.handle(operation: str, args: List[str], dry_run: bool = False) -> Tuple[bool, str]

    Neue Signatur:
        adapter.handle(operation: str, args: ParsedArgs) -> Result
    """

    def __init__(self, legacy_handler):
        self._handler = legacy_handler

    @property
    def profile_name(self) -> str:
        return self._handler.profile_name

    @property
    def target_file(self):
        return getattr(self._handler, 'target_file', None)

    def get_operations(self) -> dict:
        return self._handler.get_operations()

    def handle(self, operation: str, args: ParsedArgs) -> Result:
        """Ruft Legacy-Handler auf und konvertiert Ergebnis."""
        # ParsedArgs -> List[str] fuer Legacy
        if isinstance(args, ParsedArgs):
            args_list = args.to_list()
            dry_run = args.get("dry-run", False) or args.get("dry_run", False)
        elif isinstance(args, list):
            args_list = args
            dry_run = "--dry-run" in args
        else:
            args_list = []
            dry_run = False

        try:
            result = self._handler.handle(operation, args_list, dry_run=dry_run)

            # Tuple[bool, str] -> Result
            if isinstance(result, tuple) and len(result) >= 2:
                return Result(success=result[0], message=result[1])

            # Falls schon ein Result
            if hasattr(result, 'success') and hasattr(result, 'message'):
                return result

            # Fallback
            return Result(True, str(result) if result else "OK")

        except TypeError:
            # Manche Handler akzeptieren kein dry_run
            try:
                result = self._handler.handle(operation, args_list)
                if isinstance(result, tuple) and len(result) >= 2:
                    return Result(success=result[0], message=result[1])
                return Result(True, str(result) if result else "OK")
            except Exception as e:
                return Result(False, f"Fehler: {e}")
        except Exception as e:
            return Result(False, f"Fehler: {e}")

    def __getattr__(self, name):
        """Proxy fuer alle anderen Attribute des Legacy-Handlers."""
        return getattr(self._handler, name)
