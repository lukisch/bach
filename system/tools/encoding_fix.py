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
encoding_fix.py - Zentraler Encoding-Sanitizer fuer BACH
=========================================================

Repariert Mojibake (doppelt/dreifach kodiertes UTF-8) das durch
Windows cp1252/latin-1 Fehlinterpretation entsteht.

Typisches Muster:
  "ue" (U+00FC) → UTF-8 \xc3\xbc → als cp1252 gelesen → "Ã¼"

Verwendung:
    from tools.encoding_fix import sanitize_outbound
    clean = sanitize_outbound("WÃ¼rge")  # → "Würge"

Registriert als BACH Tool: bach tools search encoding
Version: 1.0.0
Erstellt: 2026-02-13
"""


def sanitize_outbound(text: str) -> str:
    """Repariert Mojibake (doppelt/dreifach kodiertes UTF-8).

    Erkennt und repariert das Muster:
      UTF-8 Bytes → gelesen als Latin-1/cp1252 → nochmal als UTF-8 gespeichert

    Sicher: Korrekt kodierter Text wird NICHT veraendert.
    Idempotent: Mehrfacher Aufruf aendert nichts am Ergebnis.

    Args:
        text: Potenziell korrupter String

    Returns:
        Reparierter String (oder Original wenn nicht korrupt)
    """
    if not isinstance(text, str) or not text:
        return text or ""

    # Schnell-Check: Wenn keine typischen Mojibake-Marker vorhanden, nichts tun
    # \xc3 = Ã in Latin-1 (erster Byte von 2-Byte UTF-8 Sequenzen)
    if '\xc3' not in text and '\xc2' not in text and '\xc4' not in text and '\xc5' not in text:
        return text

    # Bis zu 3 Reparatur-Runden (fuer dreifach-kodierte Strings)
    result = text
    for _ in range(3):
        try:
            candidate = result.encode('cp1252').decode('utf-8')
            if candidate == result:
                break  # Keine Aenderung mehr → fertig
            # Validierung: Reparierter Text sollte weniger Bytes brauchen
            if len(candidate.encode('utf-8')) < len(result.encode('utf-8')):
                result = candidate
            else:
                break
        except (UnicodeDecodeError, UnicodeEncodeError):
            break  # Nicht (weiter) reparierbar

    return result


def sanitize_subprocess_output(raw_bytes: bytes) -> str:
    """Dekodiert subprocess-Output mit UTF-8/cp1252 Fallback.

    Fuer Claude CLI und andere Node.js-Prozesse auf Windows,
    die je nach Konfiguration UTF-8 oder cp1252 ausgeben.

    Args:
        raw_bytes: Rohe Bytes vom subprocess stdout/stderr

    Returns:
        Korrekt dekodierter String
    """
    if not raw_bytes:
        return ""

    # Versuch 1: UTF-8 (bevorzugt)
    try:
        return raw_bytes.decode('utf-8')
    except UnicodeDecodeError:
        pass

    # Versuch 2: cp1252 (Windows-Fallback)
    try:
        return raw_bytes.decode('cp1252')
    except UnicodeDecodeError:
        pass

    # Versuch 3: UTF-8 mit Replacement (Notfall)
    return raw_bytes.decode('utf-8', errors='replace')


# CLI-Interface fuer Tests
if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])
        fixed = sanitize_outbound(text)
        if fixed != text:
            print(f"KORRUPT: {repr(text)}")
            print(f"REPARIERT: {repr(fixed)}")
            print(f"ANZEIGE: {fixed}")
        else:
            print(f"OK: {text}")
    else:
        # Selbst-Test
        tests = [
            ("WÃ¼rge", "Würge"),
            ("gelÃ¶scht", "gelöscht"),
            ("SÃ¤ckingen", "Säckingen"),
            ("kÃ¼mmere", "kümmere"),
            ("Hallo Welt", "Hallo Welt"),  # Nicht veraendern
            ("ÃƒÂ¼ber", "über"),  # Dreifach
        ]
        ok = 0
        for inp, expected in tests:
            result = sanitize_outbound(inp)
            status = "OK" if result == expected else "FAIL"
            if status == "OK":
                ok += 1
            print(f"  [{status}] {repr(inp)} → {repr(result)} (erwartet: {repr(expected)})")
        print(f"\n{ok}/{len(tests)} Tests bestanden")
