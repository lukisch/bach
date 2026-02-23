#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: MIT
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
BACH Routing Service v1.0
==========================
Berechnet Routen via OSRM (Open Source Routing Machine).
Kein API-Key erforderlich – oeffentliche OSRM-Instanz.

Features:
  - Auto + Fahrrad + Fuss (car/bike/foot)
  - Distanz + Geschaetzte Fahrzeit
  - Zwischen zwei Koordinatenpaaren

Nutzung (Library):
    from hub._services.routing.routing_service import get_route, get_route_text
    result = get_route(start=(47.761, 8.079), end=(47.994, 7.849))
    text   = get_route_text(start=(47.761, 8.079), end=(47.994, 7.849), mode="car")

Nutzung (CLI):
    python routing_service.py 47.761 8.079 47.994 7.849
    python routing_service.py 47.761 8.079 47.994 7.849 bike

Wichtig: OSRM-Oeffentliche API hat Rate-Limits.
         Fuer produktive Nutzung eigene Instanz oder Nominatim+OSRM kombinieren.

Autor: BACH System
Datum: 2026-02-18
"""

import json
import os
import sys
import urllib.request
import urllib.error
from typing import Optional, Tuple

# OSRM oeffentliche Server
OSRM_SERVERS = {
    "car":  "https://router.project-osrm.org/route/v1/driving",
    "bike": "https://router.project-osrm.org/route/v1/cycling",
    "foot": "https://router.project-osrm.org/route/v1/foot",
}

MODE_LABELS = {
    "car":  "Auto",
    "bike": "Fahrrad",
    "foot": "zu Fuss",
}

MODE_ICONS = {
    "car":  "🚗",
    "bike": "🚲",
    "foot": "🚶",
}


def get_route(
    start: Tuple[float, float],
    end:   Tuple[float, float],
    mode:  str = "car",
) -> Optional[dict]:
    """
    Berechnet Route zwischen zwei Koordinatenpaaren.

    Args:
        start: (lat, lon) Startpunkt
        end:   (lat, lon) Zielpunkt
        mode:  "car" | "bike" | "foot"

    Returns:
        dict mit: distance_km, duration_min, duration_h_min,
                  start_coords, end_coords, mode
        oder dict mit "error" bei Fehler.
    """
    if mode not in OSRM_SERVERS:
        return {"error": f"Ungueltiger Modus: {mode}. Erlaubt: car, bike, foot"}

    # OSRM erwartet lon,lat (nicht lat,lon!)
    start_lat, start_lon = start
    end_lat, end_lon = end

    coords = f"{start_lon:.6f},{start_lat:.6f};{end_lon:.6f},{end_lat:.6f}"
    url = f"{OSRM_SERVERS[mode]}/{coords}?overview=false&steps=false"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BACH-Routing-Service/1.0 (github.com/lukisch/bach)"},
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.URLError as e:
        return {"error": f"Netzwerkfehler: {e}"}
    except Exception as e:
        return {"error": f"Fehler: {e}"}

    if data.get("code") != "Ok":
        return {"error": f"OSRM-Fehler: {data.get('code', '?')} – {data.get('message', '')}"}

    try:
        route = data["routes"][0]
        dist_m = route["distance"]
        dur_s  = route["duration"]

        dist_km   = dist_m / 1000
        dur_min   = int(dur_s / 60)
        dur_h     = dur_min // 60
        dur_m_rem = dur_min % 60

        if dur_h > 0:
            dur_str = f"{dur_h}h {dur_m_rem}min"
        else:
            dur_str = f"{dur_min} min"

        return {
            "distance_km":   round(dist_km, 1),
            "duration_min":  dur_min,
            "duration_str":  dur_str,
            "start_coords":  start,
            "end_coords":    end,
            "mode":          mode,
            "mode_label":    MODE_LABELS.get(mode, mode),
            "mode_icon":     MODE_ICONS.get(mode, ""),
        }

    except (KeyError, IndexError, ValueError) as e:
        return {"error": f"Parse-Fehler: {e}"}


def get_route_text(
    start: Tuple[float, float],
    end:   Tuple[float, float],
    mode:  str = "car",
    start_name: str = "",
    end_name:   str = "",
) -> str:
    """
    Gibt einen lesbaren Routen-String zurueck (fuer Claude-Prompt-Injektion).

    Beispiel:
        🚗 Route (Auto): Hamburg → Berlin
        Distanz: 48.3 km | Fahrzeit: ~42 min
    """
    r = get_route(start, end, mode)
    if not r or "error" in r:
        err = r.get("error", "unbekannt") if r else "Timeout"
        return f"[Routing: nicht verfuegbar – {err}]"

    icon = r["mode_icon"]
    label = r["mode_label"]
    start_str = start_name if start_name else f"{start[0]:.4f}°N, {start[1]:.4f}°E"
    end_str   = end_name   if end_name   else f"{end[0]:.4f}°N, {end[1]:.4f}°E"

    return (
        f"{icon} Route ({label}): {start_str} → {end_str}\n"
        f"Distanz: {r['distance_km']} km | Fahrzeit: ~{r['duration_str']}"
    )


def geocode_place(place_name: str) -> Optional[Tuple[float, float]]:
    """
    Sucht Koordinaten fuer einen Ortsnamen via Nominatim (OpenStreetMap).
    Hilfreich wenn nur ein Ortsname bekannt ist.

    Returns:
        (lat, lon) Tuple oder None bei Fehler.
    """
    encoded = urllib.parse.quote(place_name)
    url = f"https://nominatim.openstreetmap.org/search?q={encoded}&format=json&limit=1"

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "BACH-Routing-Service/1.0 (github.com/lukisch/bach)"},
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            results = json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None

    if results:
        try:
            return float(results[0]["lat"]), float(results[0]["lon"])
        except (KeyError, ValueError):
            return None
    return None


def main():
    """CLI: python routing_service.py <start_lat> <start_lon> <end_lat> <end_lon> [mode]"""
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    if len(sys.argv) < 5:
        print("Nutzung: python routing_service.py <start_lat> <start_lon> <end_lat> <end_lon> [car|bike|foot]")
        print("Beispiel: python routing_service.py 47.761 8.079 47.994 7.849 car")
        sys.exit(1)

    try:
        start = (float(sys.argv[1]), float(sys.argv[2]))
        end   = (float(sys.argv[3]), float(sys.argv[4]))
    except ValueError as e:
        print(f"Ungueltige Koordinaten: {e}")
        sys.exit(1)

    mode = sys.argv[5] if len(sys.argv) > 5 else "car"

    text = get_route_text(start, end, mode)
    print(text)


if __name__ == "__main__":
    import urllib.parse
    main()
else:
    import urllib.parse
