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
FinancialProof - Data Provider Modul
Wrapper für yfinance mit Caching und Fehlerbehandlung

Migriert von Streamlit: 2026-01-25
- @st.cache_data durch TTL-aware Cache-Decorator ersetzt
- Keine GUI-Abhängigkeiten mehr (BACH PORT_004)
"""
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Any, Tuple, Callable
from functools import wraps
import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import config


def ttl_cache(ttl_seconds: int = 300, maxsize: int = 128):
    """
    Time-to-live Cache Decorator (Ersatz für @st.cache_data)
    
    Args:
        ttl_seconds: Cache-Lebenszeit in Sekunden
        maxsize: Maximale Cache-Größe
    """
    def decorator(func: Callable):
        cache = {}
        timestamps = {}
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Cache-Key aus Argumenten erstellen
            key = str(args) + str(sorted(kwargs.items()))
            current_time = time.time()
            
            # Prüfen ob im Cache und noch gültig
            if key in cache and key in timestamps:
                if current_time - timestamps[key] < ttl_seconds:
                    return cache[key]
            
            # Alten Cache aufräumen wenn zu groß
            if len(cache) >= maxsize:
                # Älteste Einträge entfernen
                oldest_keys = sorted(timestamps.keys(), key=lambda k: timestamps[k])[:maxsize/4]
                for old_key in oldest_keys:
                    cache.pop(old_key, None)
                    timestamps.pop(old_key, None)
            
            # Neuen Wert berechnen und cachen
            result = func(*args, **kwargs)
            cache[key] = result
            timestamps[key] = current_time
            return result
        
        # Cache-Kontrollfunktionen
        wrapper.cache_clear = lambda: (cache.clear(), timestamps.clear())
        wrapper.cache_info = lambda: {"size": len(cache), "maxsize": maxsize, "ttl": ttl_seconds}
        
        return wrapper
    return decorator


class DataProvider:
    """Zentraler Daten-Provider für Marktdaten"""

    # Asset-Typen mit typischen Suffixen
    ASSET_TYPES = {
        "stock": "",
        "etf": "",
        "fund": "",
        "crypto": "-USD",
        "forex": "=X",
        "index": "^"
    }

    # Bekannte Indizes
    KNOWN_INDICES = {
        "DAX": "^GDAXI",
        "DOW": "^DJI",
        "S&P500": "^GSPC",
        "NASDAQ": "^IXIC",
        "FTSE": "^FTSE",
        "NIKKEI": "^N225"
    }

    @staticmethod
    @ttl_cache(ttl_seconds=config.CACHE_TTL_MARKET_DATA)
    def get_market_data(
        ticker: str,
        period: str = "1y",
        interval: str = "1d"
    ) -> Optional[pd.DataFrame]:
        """
        Lädt OHLCV-Marktdaten für ein Symbol.

        Args:
            ticker: Das Symbol (z.B. "AAPL", "BTC-USD", "^GDAXI")
            period: Zeitraum ("1mo", "3mo", "6mo", "1y", "2y", "5y", "max")
            interval: Intervall ("1m", "5m", "15m", "1h", "1d", "1wk", "1mo")

        Returns:
            DataFrame mit Open, High, Low, Close, Volume oder None
        """
        try:
            df = yf.download(
                ticker,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True
            )

            if df.empty:
                return None

            # Spaltennamen normalisieren (für Multi-Ticker Fälle)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)

            # Sicherstellen dass alle benötigten Spalten da sind
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in df.columns:
                    return None

            # NaN-Werte am Anfang/Ende entfernen
            df = df.dropna()

            return df

        except Exception as e:
            print(f"Fehler beim Laden der Daten für {ticker}: {e}")
            return None

    @staticmethod
    @ttl_cache(ttl_seconds=config.CACHE_TTL_TICKER_INFO)
    def get_ticker_info(ticker: str) -> Dict[str, Any]:
        """
        Lädt Metadaten für ein Symbol (Name, Sektor, etc.)

        Args:
            ticker: Das Symbol

        Returns:
            Dictionary mit Ticker-Informationen
        """
        try:
            t = yf.Ticker(ticker)
            info = t.info
            return info if info else {}
        except Exception:
            return {}

    @staticmethod
    @ttl_cache(ttl_seconds=config.CACHE_TTL_NEWS)
    def get_news(ticker: str, limit: int = 10) -> List[Dict]:
        """
        Lädt News für ein Symbol von yfinance.

        Args:
            ticker: Das Symbol
            limit: Maximale Anzahl News

        Returns:
            Liste von News-Dictionaries
        """
        try:
            t = yf.Ticker(ticker)
            news = t.news
            if news:
                return news[:limit]
            return []
        except Exception:
            return []

    @staticmethod
    def get_current_price(ticker: str) -> Optional[Tuple[float, float, float]]:
        """
        Holt den aktuellen Preis und Änderung.

        Args:
            ticker: Das Symbol

        Returns:
            Tuple (aktueller_preis, änderung, änderung_prozent) oder None
        """
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) >= 2:
                current = hist['Close'].iloc[-1]
                previous = hist['Close'].iloc[-2]
                change = current - previous
                change_pct = (change / previous) * 100
                return (current, change, change_pct)
            elif len(hist) == 1:
                return (hist['Close'].iloc[-1], 0, 0)
            return None
        except Exception:
            return None

    @staticmethod
    @ttl_cache(ttl_seconds=config.CACHE_TTL_MARKET_DATA)
    def get_multiple_tickers(
        tickers: List[str],
        period: str = "1y",
        interval: str = "1d"
    ) -> Dict[str, pd.DataFrame]:
        """
        Lädt Daten für mehrere Ticker gleichzeitig.

        Args:
            tickers: Liste von Symbolen
            period: Zeitraum
            interval: Intervall

        Returns:
            Dictionary {ticker: DataFrame}
        """
        result = {}
        try:
            data = yf.download(
                tickers,
                period=period,
                interval=interval,
                progress=False,
                auto_adjust=True,
                group_by='ticker'
            )

            if isinstance(data.columns, pd.MultiIndex):
                for ticker in tickers:
                    if ticker in data.columns.get_level_values(0):
                        df = data[ticker].dropna()
                        if not df.empty:
                            result[ticker] = df
            else:
                # Nur ein Ticker, keine MultiIndex
                if not data.empty:
                    result[tickers[0]] = data.dropna()

        except Exception as e:
            print(f"Fehler beim Laden mehrerer Ticker: {e}")

        return result

    @staticmethod
    def search_ticker(query: str, limit: int = 10) -> List[Dict]:
        """
        Sucht nach Symbolen basierend auf einem Suchbegriff.

        Args:
            query: Suchbegriff (Name oder Symbol)
            limit: Maximale Anzahl Ergebnisse

        Returns:
            Liste von {symbol, name, type} Dictionaries
        """
        try:
            # yfinance hat keine native Suchfunktion,
            # daher verwenden wir die Ticker-Info als Workaround
            t = yf.Ticker(query.upper())
            info = t.info

            if info and 'symbol' in info:
                return [{
                    'symbol': info.get('symbol', query.upper()),
                    'name': info.get('longName', info.get('shortName', query)),
                    'type': info.get('quoteType', 'EQUITY').lower(),
                    'exchange': info.get('exchange', 'Unknown')
                }]
            return []
        except Exception:
            return []

    @staticmethod
    def validate_ticker(ticker: str) -> bool:
        """
        Prüft ob ein Ticker gültig ist.

        Args:
            ticker: Das zu prüfende Symbol

        Returns:
            True wenn gültig, False sonst
        """
        try:
            data = yf.download(ticker, period="5d", progress=False)
            return not data.empty
        except Exception:
            return False

    @staticmethod
    def get_asset_type(ticker: str) -> str:
        """
        Ermittelt den Asset-Typ basierend auf dem Symbol.

        Args:
            ticker: Das Symbol

        Returns:
            Asset-Typ ('stock', 'etf', 'crypto', 'index', etc.)
        """
        ticker = ticker.upper()

        # Indizes
        if ticker.startswith('^'):
            return 'index'

        # Krypto
        if ticker.endswith('-USD') or ticker.endswith('-EUR'):
            return 'crypto'

        # Forex
        if ticker.endswith('=X'):
            return 'forex'

        # Versuche Info abzurufen
        try:
            info = DataProvider.get_ticker_info(ticker)
            quote_type = info.get('quoteType', '').upper()
            if quote_type == 'ETF':
                return 'etf'
            elif quote_type == 'MUTUALFUND':
                return 'fund'
            elif quote_type == 'CRYPTOCURRENCY':
                return 'crypto'
            elif quote_type == 'INDEX':
                return 'index'
        except Exception:
            pass

        return 'stock'

    @staticmethod
    def get_financials(ticker: str) -> Dict[str, pd.DataFrame]:
        """
        Lädt Finanzberichte für eine Aktie.

        Args:
            ticker: Das Symbol

        Returns:
            Dictionary mit 'income', 'balance', 'cashflow' DataFrames
        """
        try:
            t = yf.Ticker(ticker)
            return {
                'income': t.income_stmt,
                'balance': t.balance_sheet,
                'cashflow': t.cashflow
            }
        except Exception:
            return {}

    @staticmethod
    def get_dividends(ticker: str) -> pd.Series:
        """
        Lädt Dividenden-Historie.

        Args:
            ticker: Das Symbol

        Returns:
            Series mit Dividenden-Daten
        """
        try:
            t = yf.Ticker(ticker)
            return t.dividends
        except Exception:
            return pd.Series()

    @staticmethod
    def get_recommendations(ticker: str) -> pd.DataFrame:
        """
        Lädt Analysten-Empfehlungen.

        Args:
            ticker: Das Symbol

        Returns:
            DataFrame mit Empfehlungen
        """
        try:
            t = yf.Ticker(ticker)
            rec = t.recommendations
            return rec if rec is not None else pd.DataFrame()
        except Exception:
            return pd.DataFrame()


class MarketOverview:
    """Gibt einen Überblick über wichtige Marktindizes"""

    MAIN_INDICES = [
        ("^GDAXI", "DAX", "Frankfurt"),
        ("^GSPC", "S&P 500", "New York"),
        ("^DJI", "Dow Jones", "New York"),
        ("^IXIC", "NASDAQ", "New York"),
        ("^FTSE", "FTSE 100", "London"),
        ("^N225", "Nikkei 225", "Tokyo")
    ]

    @staticmethod
    @ttl_cache(ttl_seconds=300)  # 5 Minuten Cache
    def get_indices_overview() -> List[Dict]:
        """
        Holt aktuelle Daten für die Hauptindizes.

        Returns:
            Liste von Dicts mit Index-Daten
        """
        results = []
        for symbol, name, exchange in MarketOverview.MAIN_INDICES:
            try:
                price_data = DataProvider.get_current_price(symbol)
                if price_data:
                    current, change, change_pct = price_data
                    results.append({
                        'symbol': symbol,
                        'name': name,
                        'exchange': exchange,
                        'price': current,
                        'change': change,
                        'change_pct': change_pct
                    })
            except Exception:
                continue
        return results
