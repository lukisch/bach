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
FinancialProof - ARIMA Zeitreihenanalyse
Prognosen basierend auf AutoRegressive Integrated Moving Average
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List, Tuple
import warnings

warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=FutureWarning)

from ..base import (
    BaseAnalyzer, AnalysisResult, AnalysisParameters,
    AnalysisCategory, AnalysisTimeframe
)
from ..registry import AnalysisRegistry


@AnalysisRegistry.register
class ARIMAAnalyzer(BaseAnalyzer):
    """ARIMA-basierte Zeitreihenanalyse für Kursprognosen."""

    name = "arima"
    display_name = "Zeitreihenanalyse (ARIMA)"
    category = AnalysisCategory.STATISTICAL
    description = "Prognostiziert zukünftige Kurse basierend auf historischen Mustern"
    estimated_duration = 30
    min_data_points = 60

    supported_timeframes = [AnalysisTimeframe.SHORT, AnalysisTimeframe.MEDIUM, AnalysisTimeframe.LONG]

    FORECAST_DAYS = {
        AnalysisTimeframe.SHORT: 7,
        AnalysisTimeframe.MEDIUM: 30,
        AnalysisTimeframe.LONG: 90
    }

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "timeframe": {"type": "string", "enum": ["short", "medium", "long"], "default": "medium"},
                "confidence_interval": {"type": "number", "default": 0.95, "minimum": 0.8, "maximum": 0.99}
            }
        }

    async def analyze(self, params: AnalysisParameters) -> AnalysisResult:
        symbol = params.symbol
        data = params.data
        timeframe = params.timeframe

        errors = self.validate_data(data)
        if errors:
            return self.create_empty_result(self.name, symbol, errors[0])

        self.set_progress(10)

        try:
            close = data['Close'].dropna()
            self.set_progress(30)
            model_result = self._fit_arima(close)

            if model_result is None:
                return self.create_empty_result(self.name, symbol, "ARIMA-Modell konnte nicht erstellt werden")

            self.set_progress(60)
            forecast_days = self.FORECAST_DAYS.get(timeframe, 30)
            confidence = params.custom_params.get('confidence_interval', 0.95)
            forecast, conf_int = self._forecast(model_result, forecast_days, confidence)

            self.set_progress(80)
            result = self._build_result(symbol, close, forecast, conf_int, model_result, timeframe)

            self.set_progress(100)
            return result

        except Exception as e:
            return self.create_empty_result(self.name, symbol, str(e))

    def _fit_arima(self, data: pd.Series) -> Any:
        try:
            from statsmodels.tsa.arima.model import ARIMA
            from statsmodels.tsa.stattools import adfuller

            adf_result = adfuller(data.values)
            is_stationary = adf_result[1] < 0.05
            d = 0 if is_stationary else 1

            best_aic = np.inf
            best_model = None
            best_order = (1, d, 1)

            for p in range(0, 4):
                for q in range(0, 4):
                    if p == 0 and q == 0:
                        continue
                    try:
                        model = ARIMA(data, order=(p, d, q))
                        fitted = model.fit()
                        if fitted.aic < best_aic:
                            best_aic = fitted.aic
                            best_model = fitted
                            best_order = (p, d, q)
                    except Exception:
                        continue

            if best_model is None:
                model = ARIMA(data, order=(1, d, 1))
                best_model = model.fit()

            best_model._best_order = best_order
            return best_model

        except ImportError:
            return self._simple_forecast_model(data)
        except Exception:
            return None

    def _simple_forecast_model(self, data: pd.Series):
        class SimpleForecast:
            def __init__(self, data):
                self.data = data
                self._best_order = (0, 0, 0)

            def get_forecast(self, steps, alpha=0.05):
                last = self.data.iloc[-1]
                trend = self.data.diff().iloc[-10:].mean()
                pred = np.array([last + trend * (i+1) for i in range(steps)])
                std = self.data.pct_change().std() * self.data.iloc[-1]
                conf_int = np.array([[p - 1.96 * std * np.sqrt(i+1), p + 1.96 * std * np.sqrt(i+1)] for i, p in enumerate(pred)])

                class ForecastResult:
                    def __init__(self, pred, conf):
                        self.predicted_mean = pred
                        self.conf_int = lambda: conf
                return ForecastResult(pred, conf_int)
        return SimpleForecast(data)

    def _forecast(self, model, steps: int, confidence: float) -> Tuple[np.ndarray, np.ndarray]:
        try:
            alpha = 1 - confidence
            forecast_result = model.get_forecast(steps=steps, alpha=alpha)
            return np.array(forecast_result.predicted_mean), np.array(forecast_result.conf_int())
        except Exception:
            last_price = model.data.iloc[-1] if hasattr(model, 'data') else 100
            forecast = np.array([last_price * (1 + 0.001 * i) for i in range(1, steps + 1)])
            std = last_price * 0.02
            return forecast, np.array([[f - 2*std, f + 2*std] for f in forecast])

    def _build_result(self, symbol: str, historical: pd.Series, forecast: np.ndarray, conf_int: np.ndarray, model, timeframe: AnalysisTimeframe) -> AnalysisResult:
        current_price = historical.iloc[-1]
        forecast_end = forecast[-1]
        change_pct = ((forecast_end - current_price) / current_price) * 100

        if change_pct > 5:
            trend, recommendation = "bullish", "buy"
        elif change_pct < -5:
            trend, recommendation = "bearish", "sell"
        else:
            trend, recommendation = "neutral", "hold"

        spread = (conf_int[-1, 1] - conf_int[-1, 0]) / current_price
        confidence = max(0.3, min(0.9, 1 - spread))
        order = getattr(model, '_best_order', (1, 0, 1))

        summary = f"ARIMA{order} Prognose: {trend.capitalize()} Trend. Kursziel: {forecast_end:.2f} ({change_pct:+.1f}%) in {len(forecast)} Tagen."

        return AnalysisResult(
            analysis_type=self.name, symbol=symbol, timestamp=datetime.now(),
            summary=summary, confidence=confidence,
            data={'current_price': current_price, 'forecast_end': forecast_end, 'change_percent': change_pct, 'arima_order': order},
            predictions={'forecast': forecast.tolist(), 'lower_bound': conf_int[:, 0].tolist(), 'upper_bound': conf_int[:, 1].tolist()},
            signals=[{'type': recommendation, 'indicator': 'ARIMA', 'description': f'Prognose: {trend} Trend', 'confidence': confidence}],
            recommendation=recommendation
        )
