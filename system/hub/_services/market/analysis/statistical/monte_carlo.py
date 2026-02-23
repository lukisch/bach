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
FinancialProof - Monte-Carlo-Simulation
Risiko-Analyse mit Value at Risk (VaR) und Szenario-Simulationen
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass

from ..base import (
    BaseAnalyzer, AnalysisResult, AnalysisParameters,
    AnalysisCategory, AnalysisTimeframe
)
from ..registry import AnalysisRegistry


@dataclass
class SimulationResult:
    """Ergebnis einer einzelnen Simulation"""
    final_prices: np.ndarray
    paths: np.ndarray
    var_95: float
    var_99: float
    cvar_95: float  # Conditional VaR (Expected Shortfall)
    expected_return: float
    probability_profit: float


@AnalysisRegistry.register
class MonteCarloAnalyzer(BaseAnalyzer):
    """
    Monte-Carlo-Simulation für Risikoanalyse.

    Simuliert tausende möglicher Zukunftsszenarien basierend auf
    historischer Volatilität und Drift.
    """

    name = "monte_carlo"
    display_name = "Monte-Carlo-Simulation"
    category = AnalysisCategory.STATISTICAL
    description = "Berechnet Value at Risk (VaR) und simuliert Zukunftsszenarien"
    estimated_duration = 15
    min_data_points = 30

    supported_timeframes = [
        AnalysisTimeframe.SHORT,
        AnalysisTimeframe.MEDIUM
    ]

    # Standardparameter
    DEFAULT_SIMULATIONS = 10000
    DEFAULT_DAYS = {
        AnalysisTimeframe.SHORT: 5,
        AnalysisTimeframe.MEDIUM: 21  # 1 Monat Trading-Tage
    }

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "timeframe": {
                    "type": "string",
                    "enum": ["short", "medium"],
                    "default": "short",
                    "description": "Simulationshorizont"
                },
                "num_simulations": {
                    "type": "integer",
                    "default": 10000,
                    "minimum": 1000,
                    "maximum": 100000,
                    "description": "Anzahl der Simulationen"
                },
                "investment_amount": {
                    "type": "number",
                    "default": 10000,
                    "description": "Investitionsbetrag für VaR-Berechnung"
                }
            }
        }

    async def analyze(self, params: AnalysisParameters) -> AnalysisResult:
        """Führt die Monte-Carlo-Simulation durch"""
        symbol = params.symbol
        data = params.data
        timeframe = params.timeframe

        errors = self.validate_data(data)
        if errors:
            return self.create_empty_result(self.name, symbol, errors[0])

        self.set_progress(10)

        try:
            close = data['Close'].dropna()

            # Parameter
            num_sims = params.custom_params.get('num_simulations', self.DEFAULT_SIMULATIONS)
            days = self.DEFAULT_DAYS.get(timeframe, 5)
            investment = params.custom_params.get('investment_amount', 10000)

            self.set_progress(20)

            # Historische Renditen berechnen
            returns = self.calculate_log_returns(close)
            mu = returns.mean()  # Drift
            sigma = returns.std()  # Volatilität

            self.set_progress(40)

            # Simulation durchführen
            sim_result = self._run_simulation(
                close.iloc[-1], mu, sigma, days, num_sims
            )

            self.set_progress(80)

            # Ergebnis aufbereiten
            result = self._build_result(
                symbol, close, sim_result, investment, days, timeframe
            )

            self.set_progress(100)
            return result

        except Exception as e:
            return self.create_empty_result(self.name, symbol, str(e))

    def _run_simulation(
        self,
        start_price: float,
        mu: float,
        sigma: float,
        days: int,
        num_simulations: int
    ) -> SimulationResult:
        """
        Führt die Monte-Carlo-Simulation durch.

        Verwendet Geometric Brownian Motion (GBM).
        """
        np.random.seed(42)  # Für Reproduzierbarkeit

        # Zeit-Inkrement
        dt = 1  # 1 Tag

        # Pfade simulieren
        # dS = S * (mu*dt + sigma*sqrt(dt)*Z)
        random_walks = np.random.standard_normal((num_simulations, days))

        # GBM Pfade
        drift = (mu - 0.5 * sigma**2) * dt
        diffusion = sigma * np.sqrt(dt) * random_walks

        # Kumulative Returns
        cumulative = np.cumsum(drift + diffusion, axis=1)

        # Preispfade
        paths = start_price * np.exp(cumulative)

        # Finale Preise
        final_prices = paths[:, -1]

        # Renditen
        returns = (final_prices - start_price) / start_price

        # VaR Berechnung (Verluste als negative Zahlen)
        var_95 = np.percentile(returns, 5)  # 5% Quantil = 95% VaR
        var_99 = np.percentile(returns, 1)  # 1% Quantil = 99% VaR

        # CVaR (Expected Shortfall) - durchschnittlicher Verlust wenn VaR überschritten
        cvar_95 = returns[returns <= var_95].mean()

        # Erwartete Rendite
        expected_return = returns.mean()

        # Wahrscheinlichkeit für Gewinn
        probability_profit = (returns > 0).mean()

        return SimulationResult(
            final_prices=final_prices,
            paths=paths,
            var_95=var_95,
            var_99=var_99,
            cvar_95=cvar_95,
            expected_return=expected_return,
            probability_profit=probability_profit
        )

    def _build_result(
        self,
        symbol: str,
        historical: pd.Series,
        sim_result: SimulationResult,
        investment: float,
        days: int,
        timeframe: AnalysisTimeframe
    ) -> AnalysisResult:
        """Baut das Analyse-Ergebnis zusammen"""
        current_price = historical.iloc[-1]

        # VaR in absoluten Beträgen
        var_95_amount = investment * abs(sim_result.var_95)
        var_99_amount = investment * abs(sim_result.var_99)

        # Konfidenz basierend auf Gewinnwahrscheinlichkeit
        confidence = sim_result.probability_profit

        # Recommendation basierend auf Risiko/Rendite
        if sim_result.expected_return > 0.02 and sim_result.var_95 > -0.05:
            recommendation = "buy"
            risk_level = "niedrig"
        elif sim_result.var_95 < -0.10:
            recommendation = "sell"
            risk_level = "hoch"
        else:
            recommendation = "hold"
            risk_level = "mittel"

        summary = (
            f"Monte-Carlo-Simulation ({sim_result.paths.shape[0]:,} Szenarien, {days} Tage): "
            f"Gewinnwahrscheinlichkeit {sim_result.probability_profit*100:.1f}%. "
            f"VaR (95%): {sim_result.var_95*100:.1f}% "
            f"(€{var_95_amount:.0f} bei €{investment:,.0f} Investment). "
            f"Risiko: {risk_level}."
        )

        # Perzentile für Chart
        percentiles = [5, 25, 50, 75, 95]
        percentile_paths = np.percentile(sim_result.paths, percentiles, axis=0)

        # Chart-Daten
        last_date = historical.index[-1]
        forecast_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=days,
            freq='B'
        )

        chart_data = pd.DataFrame({
            'date': forecast_dates,
            'p5': percentile_paths[0],
            'p25': percentile_paths[1],
            'p50': percentile_paths[2],
            'p75': percentile_paths[3],
            'p95': percentile_paths[4]
        })

        # Verteilung der Endpreise
        price_bins = np.histogram(sim_result.final_prices, bins=50)

        return AnalysisResult(
            analysis_type=self.name,
            symbol=symbol,
            timestamp=datetime.now(),
            summary=summary,
            confidence=confidence,
            data={
                'current_price': current_price,
                'var_95_percent': sim_result.var_95 * 100,
                'var_99_percent': sim_result.var_99 * 100,
                'var_95_amount': var_95_amount,
                'var_99_amount': var_99_amount,
                'cvar_95_percent': sim_result.cvar_95 * 100,
                'expected_return_percent': sim_result.expected_return * 100,
                'probability_profit': sim_result.probability_profit * 100,
                'num_simulations': len(sim_result.final_prices),
                'simulation_days': days,
                'investment_amount': investment,
                'risk_level': risk_level,
                'median_final_price': np.median(sim_result.final_prices),
                'mean_final_price': np.mean(sim_result.final_prices)
            },
            predictions={
                'percentile_5': percentile_paths[0].tolist(),
                'percentile_25': percentile_paths[1].tolist(),
                'percentile_50': percentile_paths[2].tolist(),
                'percentile_75': percentile_paths[3].tolist(),
                'percentile_95': percentile_paths[4].tolist(),
                'dates': [d.isoformat() for d in forecast_dates],
                'price_distribution': {
                    'bins': price_bins[1].tolist(),
                    'counts': price_bins[0].tolist()
                }
            },
            signals=[{
                'type': recommendation,
                'indicator': 'Monte Carlo VaR',
                'description': f'Risiko-Level: {risk_level}, VaR(95%): {sim_result.var_95*100:.1f}%',
                'confidence': confidence
            }],
            recommendation=recommendation,
            chart_data=chart_data,
            warnings=self._get_warnings(sim_result)
        )

    def _get_warnings(self, sim_result: SimulationResult) -> List[str]:
        """Generiert Warnungen basierend auf Simulationsergebnissen"""
        warnings = []

        if sim_result.var_95 < -0.10:
            warnings.append(
                "Hohes Verlustrisiko: 5% Chance auf über 10% Verlust"
            )

        if sim_result.var_99 < -0.20:
            warnings.append(
                "Extremes Tail-Risiko: 1% Chance auf über 20% Verlust"
            )

        if sim_result.probability_profit < 0.45:
            warnings.append(
                "Geringe Gewinnwahrscheinlichkeit unter 45%"
            )

        return warnings
