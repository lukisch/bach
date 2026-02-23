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
FinancialProof - Mean Reversion Analyse
Identifiziert Rückkehr-Potenzial zum historischen Mittelwert
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any
from scipy import stats

from ..base import (
    BaseAnalyzer, AnalysisResult, AnalysisParameters,
    AnalysisCategory, AnalysisTimeframe
)
from ..registry import AnalysisRegistry


@AnalysisRegistry.register
class MeanReversionAnalyzer(BaseAnalyzer):
    """
    Mean Reversion Analyse.

    Basiert auf der Annahme, dass Preise langfristig zu ihrem
    historischen Durchschnitt zurückkehren.
    """

    name = "mean_reversion"
    display_name = "Mean Reversion Prüfung"
    category = AnalysisCategory.STATISTICAL
    description = "Prüft ob der Kurs zum historischen Mittelwert zurückkehren könnte"
    estimated_duration = 10
    min_data_points = 50

    supported_timeframes = [
        AnalysisTimeframe.SHORT,
        AnalysisTimeframe.MEDIUM
    ]

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "lookback_period": {
                    "type": "integer",
                    "default": 60,
                    "minimum": 20,
                    "maximum": 252,
                    "description": "Anzahl der Tage für Mittelwert-Berechnung"
                },
                "z_score_threshold": {
                    "type": "number",
                    "default": 2.0,
                    "minimum": 1.0,
                    "maximum": 3.0,
                    "description": "Z-Score Schwelle für Signal"
                }
            }
        }

    async def analyze(self, params: AnalysisParameters) -> AnalysisResult:
        """Führt die Mean Reversion Analyse durch"""
        symbol = params.symbol
        data = params.data

        errors = self.validate_data(data)
        if errors:
            return self.create_empty_result(self.name, symbol, errors[0])

        self.set_progress(10)

        try:
            close = data['Close'].dropna()

            # Parameter
            lookback = params.custom_params.get('lookback_period', 60)
            z_threshold = params.custom_params.get('z_score_threshold', 2.0)

            self.set_progress(30)

            # Berechnung der Mean Reversion Metriken
            metrics = self._calculate_metrics(close, lookback)

            self.set_progress(60)

            # Stationaritätstest (ADF)
            is_stationary, adf_pvalue = self._test_stationarity(close)

            self.set_progress(80)

            # Half-Life berechnen (Zeit bis zur Rückkehr)
            half_life = self._calculate_half_life(close)

            # Ergebnis zusammenstellen
            result = self._build_result(
                symbol, close, metrics, is_stationary,
                adf_pvalue, half_life, z_threshold, lookback
            )

            self.set_progress(100)
            return result

        except Exception as e:
            return self.create_empty_result(self.name, symbol, str(e))

    def _calculate_metrics(self, prices: pd.Series, lookback: int) -> Dict:
        """Berechnet Mean Reversion Metriken"""
        current_price = prices.iloc[-1]

        # Verschiedene Durchschnitte
        mean_short = prices.iloc[-lookback:].mean()
        mean_long = prices.mean()

        # Z-Score (wie weit vom Mittelwert entfernt)
        std = prices.iloc[-lookback:].std()
        z_score = (current_price - mean_short) / std if std > 0 else 0

        # Distanz zum Mittelwert in Prozent
        distance_pct = ((current_price - mean_short) / mean_short) * 100

        # Bollinger %B (Position innerhalb der Bänder)
        upper = mean_short + 2 * std
        lower = mean_short - 2 * std
        pct_b = (current_price - lower) / (upper - lower) if (upper - lower) > 0 else 0.5

        return {
            'current_price': current_price,
            'mean_short': mean_short,
            'mean_long': mean_long,
            'std': std,
            'z_score': z_score,
            'distance_pct': distance_pct,
            'pct_b': pct_b,
            'upper_band': upper,
            'lower_band': lower
        }

    def _test_stationarity(self, prices: pd.Series) -> tuple:
        """
        Augmented Dickey-Fuller Test für Stationarität.
        Stationäre Serien neigen stärker zur Mean Reversion.
        """
        try:
            from statsmodels.tsa.stattools import adfuller
            result = adfuller(prices.values, autolag='AIC')
            return result[1] < 0.05, result[1]  # p-value < 0.05 = stationär
        except ImportError:
            # Fallback: Einfache Heuristik
            returns = prices.pct_change().dropna()
            # Wenn Varianz der Renditen relativ konstant -> pseudo-stationär
            var_first = returns.iloc[:len(returns)/2].var()
            var_second = returns.iloc[len(returns)/2:].var()
            ratio = var_first / var_second if var_second > 0 else 1
            is_stable = 0.5 < ratio < 2.0
            return is_stable, 0.1 if is_stable else 0.5
        except Exception:
            return False, 1.0

    def _calculate_half_life(self, prices: pd.Series) -> float:
        """
        Berechnet die Half-Life der Mean Reversion.
        Dies ist die erwartete Zeit (in Tagen), bis der Preis
        zur Hälfte zum Mittelwert zurückgekehrt ist.
        """
        try:
            # Ornstein-Uhlenbeck Ansatz
            lagged = prices.shift(1).dropna()
            delta = (prices - lagged).dropna()

            # Regression: delta = theta * (mu - P_t-1)
            # Vereinfacht: delta = a + b * P_t-1
            if len(lagged) < 10:
                return 30  # Default

            # Lineare Regression
            lagged_aligned = lagged.iloc[1:]
            delta_aligned = delta.iloc[1:]

            slope, intercept, r_value, p_value, std_err = stats.linregress(
                lagged_aligned.values, delta_aligned.values
            )

            if slope >= 0:
                # Keine Mean Reversion (Trend)
                return np.inf

            # Half-Life = -ln(2) / ln(1 + slope)
            # Bei kleinem slope: ~ -ln(2) / slope
            half_life = -np.log(2) / slope

            return max(1, min(half_life, 365))  # Clamp zwischen 1 Tag und 1 Jahr

        except Exception:
            return 30  # Default: 30 Tage

    def _build_result(
        self,
        symbol: str,
        prices: pd.Series,
        metrics: Dict,
        is_stationary: bool,
        adf_pvalue: float,
        half_life: float,
        z_threshold: float,
        lookback: int
    ) -> AnalysisResult:
        """Baut das Analyse-Ergebnis zusammen"""
        z_score = metrics['z_score']
        distance = metrics['distance_pct']

        # Bestimme Signal basierend auf Z-Score
        if z_score < -z_threshold:
            signal_type = "buy"
            signal_desc = "Stark unterbewertet - Rückkehr zum Mittelwert erwartet"
            recommendation = "buy"
        elif z_score > z_threshold:
            signal_type = "sell"
            signal_desc = "Stark überbewertet - Korrektur zum Mittelwert erwartet"
            recommendation = "sell"
        else:
            signal_type = "hold"
            signal_desc = "Nahe am Mittelwert - kein klares Reversion-Signal"
            recommendation = "hold"

        # Konfidenz basierend auf Stationarität und Z-Score
        base_confidence = 0.5 if is_stationary else 0.3
        z_boost = min(0.3, abs(z_score) / 10)
        confidence = min(0.85, base_confidence + z_boost)

        # Mean Reversion Stärke
        if is_stationary and half_life < 30:
            mr_strength = "stark"
        elif is_stationary or half_life < 60:
            mr_strength = "moderat"
        else:
            mr_strength = "schwach"

        summary = (
            f"Mean Reversion Analyse: Z-Score {z_score:.2f} "
            f"(Distanz: {distance:+.1f}% vom {lookback}T-Mittel). "
            f"Half-Life: {half_life:.0f} Tage. "
            f"Reversion-Tendenz: {mr_strength}."
        )

        # Chart-Daten für Visualisierung
        chart_data = pd.DataFrame({
            'price': prices.iloc[-lookback:],
            'mean': [metrics['mean_short']] * lookback,
            'upper': [metrics['upper_band']] * lookback,
            'lower': [metrics['lower_band']] * lookback
        }, index=prices.iloc[-lookback:].index)

        warnings = []
        if not is_stationary:
            warnings.append(
                "Warnung: Serie erscheint nicht stationär (ADF p={:.3f}). "
                "Mean Reversion weniger zuverlässig.".format(adf_pvalue)
            )
        if half_life > 90:
            warnings.append(
                f"Lange Half-Life ({half_life:.0f} Tage) - "
                "Reversion kann lange dauern."
            )

        return AnalysisResult(
            analysis_type=self.name,
            symbol=symbol,
            timestamp=datetime.now(),
            summary=summary,
            confidence=confidence,
            data={
                'current_price': metrics['current_price'],
                'mean_price': metrics['mean_short'],
                'z_score': z_score,
                'distance_percent': distance,
                'half_life_days': half_life,
                'is_stationary': is_stationary,
                'adf_pvalue': adf_pvalue,
                'lookback_period': lookback,
                'pct_b': metrics['pct_b'],
                'upper_band': metrics['upper_band'],
                'lower_band': metrics['lower_band'],
                'reversion_strength': mr_strength
            },
            signals=[{
                'type': signal_type,
                'indicator': 'Mean Reversion',
                'description': signal_desc,
                'z_score': z_score,
                'target_price': metrics['mean_short'],
                'confidence': confidence
            }],
            recommendation=recommendation,
            chart_data=chart_data,
            warnings=warnings
        )
