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
FinancialProof - Analyse Basis-Modul
Abstrakte Basisklasse für alle Analyse-Algorithmen
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
from datetime import datetime
import pandas as pd
import numpy as np


class AnalysisCategory(str, Enum):
    """Kategorien von Analysen"""
    STATISTICAL = "statistical"
    CORRELATION = "correlation"
    ML = "ml"
    NLP = "nlp"
    RESEARCH = "research"


class AnalysisTimeframe(str, Enum):
    """Zeithorizonte für Prognosen"""
    SHORT = "short"        # 1-7 Tage
    MEDIUM = "medium"      # 1-4 Wochen
    LONG = "long"          # 1-6 Monate
    VERY_LONG = "very_long"  # > 6 Monate


@dataclass
class AnalysisResult:
    """Ergebnis einer Analyse"""
    analysis_type: str
    symbol: str
    timestamp: datetime
    summary: str
    confidence: float  # 0-1

    # Detaillierte Daten
    data: Dict[str, Any] = field(default_factory=dict)

    # Signale und Empfehlungen
    signals: List[Dict] = field(default_factory=list)
    recommendation: str = "hold"  # buy, sell, hold

    # Prognosen
    predictions: Dict[str, Any] = field(default_factory=dict)

    # Visualisierungsdaten (für Charts)
    chart_data: Optional[pd.DataFrame] = None

    # Fehler/Warnungen
    warnings: List[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class AnalysisParameters:
    """Parameter für eine Analyse"""
    symbol: str
    data: pd.DataFrame
    timeframe: AnalysisTimeframe = AnalysisTimeframe.MEDIUM
    custom_params: Dict[str, Any] = field(default_factory=dict)


class BaseAnalyzer(ABC):
    """
    Abstrakte Basisklasse für alle Analyse-Algorithmen.

    Jeder Analyzer muss diese Klasse erweitern und die
    abstrakten Methoden implementieren.
    """

    # Klassen-Attribute (müssen von Subklassen überschrieben werden)
    name: str = "base"
    display_name: str = "Basis-Analyse"
    category: AnalysisCategory = AnalysisCategory.STATISTICAL
    description: str = "Abstrakte Basisklasse"

    # Geschätzte Dauer in Sekunden
    estimated_duration: int = 10

    # Unterstützte Zeithorizonte
    supported_timeframes: List[AnalysisTimeframe] = [
        AnalysisTimeframe.SHORT,
        AnalysisTimeframe.MEDIUM,
        AnalysisTimeframe.LONG
    ]

    # Erforderliche Mindestdatenmenge (in Tagen)
    min_data_points: int = 30

    def __init__(self):
        self._progress: int = 0
        self._status: str = "idle"
        self._cancel_requested: bool = False

    @abstractmethod
    async def analyze(self, params: AnalysisParameters) -> AnalysisResult:
        """
        Führt die Analyse durch.

        Args:
            params: AnalysisParameters mit Symbol, Daten und Einstellungen

        Returns:
            AnalysisResult mit allen Ergebnissen
        """
        pass

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Any]:
        """
        Gibt das JSON-Schema für die Parameter zurück.

        Überschreiben für spezifische Parameter.
        """
        return {
            "type": "object",
            "properties": {
                "timeframe": {
                    "type": "string",
                    "enum": [t.value for t in cls.supported_timeframes],
                    "default": AnalysisTimeframe.MEDIUM.value,
                    "description": "Zeithorizont für die Analyse"
                }
            }
        }

    @classmethod
    def get_info(cls) -> Dict[str, Any]:
        """Gibt Informationen über den Analyzer zurück"""
        return {
            "name": cls.name,
            "display_name": cls.display_name,
            "category": cls.category.value,
            "description": cls.description,
            "estimated_duration": cls.estimated_duration,
            "supported_timeframes": [t.value for t in cls.supported_timeframes],
            "min_data_points": cls.min_data_points,
            "parameters": cls.get_parameter_schema()
        }

    def validate_data(self, data: pd.DataFrame) -> List[str]:
        """
        Validiert die Eingabedaten.

        Returns:
            Liste von Fehlermeldungen (leer wenn valide)
        """
        errors = []

        if data is None or data.empty:
            errors.append("Keine Daten vorhanden")
            return errors

        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing = [col for col in required_columns if col not in data.columns]
        if missing:
            errors.append(f"Fehlende Spalten: {', '.join(missing)}")

        if len(data) < self.min_data_points:
            errors.append(
                f"Zu wenig Datenpunkte: {len(data)} vorhanden, "
                f"{self.min_data_points} benötigt"
            )

        if data['Close'].isnull().sum() > len(data) * 0.1:
            errors.append("Zu viele fehlende Werte in den Kursdaten")

        return errors

    def set_progress(self, progress: int):
        """Setzt den Fortschritt (0-100)"""
        self._progress = min(100, max(0, progress))

    def get_progress(self) -> int:
        """Gibt den aktuellen Fortschritt zurück"""
        return self._progress

    def request_cancel(self):
        """Fordert Abbruch der Analyse an"""
        self._cancel_requested = True

    def is_cancel_requested(self) -> bool:
        """Prüft ob Abbruch angefordert wurde"""
        return self._cancel_requested

    def reset(self):
        """Setzt den Analyzer zurück"""
        self._progress = 0
        self._status = "idle"
        self._cancel_requested = False

    # ===== HILFSMETHODEN FÜR SUBKLASSEN =====

    @staticmethod
    def calculate_returns(prices: pd.Series) -> pd.Series:
        """Berechnet prozentuale Renditen"""
        return prices.pct_change().dropna()

    @staticmethod
    def calculate_log_returns(prices: pd.Series) -> pd.Series:
        """Berechnet logarithmische Renditen"""
        return np.log(prices / prices.shift(1)).dropna()

    @staticmethod
    def calculate_volatility(prices: pd.Series, window: int = 20) -> float:
        """Berechnet annualisierte Volatilität"""
        returns = prices.pct_change().dropna()
        return returns.std() * np.sqrt(252)

    @staticmethod
    def calculate_sharpe_ratio(
        prices: pd.Series,
        risk_free_rate: float = 0.02
    ) -> float:
        """Berechnet die Sharpe Ratio"""
        returns = prices.pct_change().dropna()
        excess_returns = returns.mean() * 252 - risk_free_rate
        volatility = returns.std() * np.sqrt(252)
        if volatility == 0:
            return 0
        return excess_returns / volatility

    @staticmethod
    def create_empty_result(
        analysis_type: str,
        symbol: str,
        error: str
    ) -> AnalysisResult:
        """Erstellt ein leeres Ergebnis mit Fehlermeldung"""
        return AnalysisResult(
            analysis_type=analysis_type,
            symbol=symbol,
            timestamp=datetime.now(),
            summary="Analyse konnte nicht durchgeführt werden",
            confidence=0.0,
            error=error
        )


class MethodSelector:
    """
    Regelbasierte Auswahl der besten Analyse-Methoden.

    Kann später durch ML ersetzt werden.
    """

    def __init__(self):
        self._ml_selector = None  # Placeholder für ML-Modell

    def select_methods(
        self,
        data: pd.DataFrame,
        available_methods: List[str]
    ) -> List[str]:
        """
        Wählt automatisch die besten Methoden basierend auf Marktdaten.

        Args:
            data: OHLCV DataFrame
            available_methods: Liste verfügbarer Methoden-Namen

        Returns:
            Liste der empfohlenen Methoden
        """
        if self._ml_selector is not None:
            return self._ml_selector.predict(data, available_methods)

        # Regelbasierte Auswahl
        methods = []
        close = data['Close']

        volatility = self._calc_volatility(close)
        trend_strength = self._calc_trend_strength(close)
        data_points = len(data)

        # Regel 1: Immer Sentiment für aktuelle Stimmung
        if "sentiment" in available_methods:
            methods.append("sentiment")

        # Regel 2: Hohe Volatilität -> Monte Carlo für Risikoanalyse
        if volatility > 0.3 and "monte_carlo" in available_methods:
            methods.append("monte_carlo")

        # Regel 3: Starker Trend -> ARIMA für Trendprognose
        if trend_strength > 0.6 and "arima" in available_methods:
            methods.append("arima")

        # Regel 4: Seitwärtsmarkt -> Mean Reversion
        if trend_strength < 0.3 and "mean_reversion" in available_methods:
            methods.append("mean_reversion")

        # Regel 5: Genug Daten für ML -> Neural Network
        if data_points > 200 and "neural_network" in available_methods:
            methods.append("neural_network")

        # Regel 6: Korrelationsanalyse immer nützlich für Diversifikation
        if "correlation" in available_methods:
            methods.append("correlation")

        # Mindestens eine Methode zurückgeben
        if not methods and available_methods:
            methods.append(available_methods[0])

        return methods

    def _calc_volatility(self, close: pd.Series) -> float:
        """Berechnet normalisierte Volatilität (0-1 Skala)"""
        returns = close.pct_change().dropna()
        vol = returns.std() * np.sqrt(252)
        # Normalisieren (typische Aktien: 0.1-0.5 p.a.)
        return min(1.0, vol / 0.5)

    def _calc_trend_strength(self, close: pd.Series) -> float:
        """
        Berechnet Trendstärke (0-1).
        Basiert auf ADX-ähnlicher Logik.
        """
        if len(close) < 20:
            return 0.5

        # Einfache Trend-Messung: Steigung der Regression
        x = np.arange(len(close))
        slope, _ = np.polyfit(x, close, 1)

        # Normalisieren relativ zur Preisspanne
        price_range = close.max() - close.min()
        if price_range == 0:
            return 0.5

        normalized_slope = abs(slope * len(close)) / price_range
        return min(1.0, normalized_slope)

    def set_ml_model(self, model):
        """Setzt ein ML-Modell für die Methodenauswahl"""
        self._ml_selector = model


# Globale Instanz
method_selector = MethodSelector()
