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
BACH Market Service - Zentrale API für Agenten-Zugriff

Version: 1.0.0
Erstellt: 2026-01-25
Task: PORT_006 / Task #412

Nutzung:
    from skills._services.market import MarketService
    
    market = MarketService()
    price = market.get_price("AAPL")
    market.watchlist.add("NVDA")
"""
from typing import Optional, Dict, List, Any


# Custom Exceptions
class MarketError(Exception):
    """Basis-Exception für Market-Service."""
    pass


class SymbolNotFound(MarketError):
    """Symbol existiert nicht."""
    pass


class APIRateLimited(MarketError):
    """yfinance Rate-Limit erreicht."""
    pass


class NetworkError(MarketError):
    """Verbindungsproblem."""
    pass


class WatchlistAPI:
    """Watchlist-Operationen für Agenten."""
    
    def __init__(self, db):
        self._db = db
    
    def add(self, symbol: str, name: str = "", asset_type: str = "stock") -> bool:
        """Symbol zur Watchlist hinzufügen."""
        try:
            self._db.add_watchlist_item(symbol=symbol, name=name, asset_type=asset_type)
            return True
        except Exception:
            return False
    
    def remove(self, symbol: str) -> bool:
        """Symbol aus Watchlist entfernen."""
        try:
            self._db.remove_watchlist_item(symbol)
            return True
        except Exception:
            return False
    
    def list(self) -> List[str]:
        """Alle Symbole in der Watchlist."""
        items = self._db.get_watchlist()
        return [item.symbol for item in items]
    
    def list_detailed(self) -> List[Dict]:
        """Watchlist mit Details."""
        items = self._db.get_watchlist()
        return [{"symbol": i.symbol, "name": i.name, "type": i.asset_type} for i in items]


class MarketService:
    """
    Zentraler Service für Agent-Zugriff auf Marktdaten.
    
    Singleton-Pattern: Nur eine Instanz pro Python-Prozess.
    """
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if self._initialized:
            return
        
        # Lazy imports um Zirkularität zu vermeiden
        from .data_provider import DataProvider
        from .database import Database
        
        self._provider = DataProvider()
        self._db = Database()
        self.watchlist = WatchlistAPI(self._db)
        self._initialized = True
    
    def get_stock(self, symbol: str, period: str = "1mo", interval: str = "1d") -> Optional[Dict]:
        """
        Holt Aktiendaten für Symbol.
        
        Args:
            symbol: Ticker-Symbol (z.B. "AAPL", "NVDA")
            period: Zeitraum ("1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "max")
            interval: Intervall ("1m", "5m", "15m", "1h", "1d", "1wk", "1mo")
        
        Returns:
            Dict mit OHLCV-Daten oder None bei Fehler
        """
        try:
            df = self._provider.get_market_data(symbol, period=period, interval=interval)
            if df is None or df.empty:
                return None
            
            return {
                "symbol": symbol,
                "period": period,
                "interval": interval,
                "open": df["Open"].tolist(),
                "high": df["High"].tolist(),
                "low": df["Low"].tolist(),
                "close": df["Close"].tolist(),
                "volume": df["Volume"].tolist(),
                "dates": df.index.strftime("%Y-%m-%d").tolist()
            }
        except Exception as e:
            raise MarketError(f"Fehler beim Abrufen von {symbol}: {e}")
    
    def get_price(self, symbol: str) -> Optional[float]:
        """
        Aktueller Preis eines Symbols.
        
        Args:
            symbol: Ticker-Symbol
        
        Returns:
            Aktueller Schlusskurs oder None
        """
        try:
            df = self._provider.get_market_data(symbol, period="1d", interval="1m")
            if df is None or df.empty:
                return None
            return float(df["Close"].iloc[-1])
        except Exception:
            return None
    
    def get_info(self, symbol: str) -> Optional[Dict]:
        """
        Unternehmens-Informationen.
        
        Args:
            symbol: Ticker-Symbol
        
        Returns:
            Dict mit Firmeninfos oder None
        """
        try:
            return self._provider.get_company_info(symbol)
        except Exception:
            return None
    
    def analyze(self, symbol: str, metrics: List[str] = None) -> Dict:
        """
        Führt Analyse mit gewählten Metriken durch.
        
        Args:
            symbol: Ticker-Symbol
            metrics: Liste von Metriken ["basic", "rsi", "macd", "sma", "bollinger"]
        
        Returns:
            Dict mit Analyse-Ergebnissen
        """
        metrics = metrics or ["basic"]
        
        try:
            from .analysis.registry import AnalysisRegistry
            registry = AnalysisRegistry()
            return registry.run_analysis(symbol, metrics)
        except ImportError:
            # Fallback wenn AnalysisRegistry nicht verfügbar
            return self._basic_analysis(symbol)
        except Exception as e:
            return {"error": str(e), "symbol": symbol}
    
    def _basic_analysis(self, symbol: str) -> Dict:
        """Einfache Analyse ohne Registry."""
        data = self.get_stock(symbol, period="1mo")
        if not data:
            return {"error": "Keine Daten verfügbar", "symbol": symbol}
        
        closes = data["close"]
        return {
            "symbol": symbol,
            "current_price": closes[-1] if closes else None,
            "change_1d": ((closes[-1] / closes[-2]) - 1) * 100 if len(closes) >= 2 else None,
            "high_1mo": max(closes) if closes else None,
            "low_1mo": min(closes) if closes else None,
            "avg_1mo": sum(closes) / len(closes) if closes else None
        }


# Convenience-Exports
__all__ = [
    'MarketService',
    'WatchlistAPI',
    'MarketError',
    'SymbolNotFound',
    'APIRateLimited',
    'NetworkError'
]
