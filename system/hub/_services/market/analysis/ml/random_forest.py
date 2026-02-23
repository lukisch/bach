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
FinancialProof - Random Forest Trend-Klassifikation
Machine Learning Modell zur Vorhersage der Kursrichtung
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Tuple

from ..base import (
    BaseAnalyzer, AnalysisResult, AnalysisParameters,
    AnalysisCategory, AnalysisTimeframe
)
from ..registry import AnalysisRegistry


@AnalysisRegistry.register
class RandomForestAnalyzer(BaseAnalyzer):
    """
    Random Forest Klassifikator für Trend-Vorhersage.
    """

    name = "random_forest"
    display_name = "KI Trend-Vorhersage (Random Forest)"
    category = AnalysisCategory.ML
    description = "Machine Learning Modell zur Vorhersage der nächsten Kursbewegung"
    estimated_duration = 20
    min_data_points = 100

    supported_timeframes = [
        AnalysisTimeframe.SHORT
    ]

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "n_estimators": {
                    "type": "integer",
                    "default": 100,
                    "minimum": 50,
                    "maximum": 500,
                    "description": "Anzahl der Entscheidungsbäume"
                },
                "test_size": {
                    "type": "number",
                    "default": 0.2,
                    "minimum": 0.1,
                    "maximum": 0.3,
                    "description": "Anteil der Testdaten"
                },
                "prediction_days": {
                    "type": "integer",
                    "default": 1,
                    "minimum": 1,
                    "maximum": 5,
                    "description": "Vorhersage-Horizont in Tagen"
                }
            }
        }

    async def analyze(self, params: AnalysisParameters) -> AnalysisResult:
        """Führt die Random Forest Analyse durch"""
        symbol = params.symbol
        data = params.data

        errors = self.validate_data(data)
        if errors:
            return self.create_empty_result(self.name, symbol, errors[0])

        self.set_progress(10)

        try:
            n_estimators = params.custom_params.get('n_estimators', 100)
            test_size = params.custom_params.get('test_size', 0.2)
            pred_days = params.custom_params.get('prediction_days', 1)

            self.set_progress(20)
            X, y, feature_names = self._prepare_features(data, pred_days)

            if len(X) < 50:
                return self.create_empty_result(
                    self.name, symbol,
                    "Zu wenig Daten nach Feature-Engineering"
                )

            self.set_progress(40)

            model, metrics, importance = self._train_model(
                X, y, feature_names, n_estimators, test_size
            )

            self.set_progress(70)

            prediction, probability = self._predict(model, X)

            self.set_progress(90)

            result = self._build_result(
                symbol, data, prediction, probability,
                metrics, importance, feature_names, pred_days
            )

            self.set_progress(100)
            return result

        except ImportError as e:
            return self.create_empty_result(
                self.name, symbol,
                f"scikit-learn nicht installiert: {e}"
            )
        except Exception as e:
            return self.create_empty_result(self.name, symbol, str(e))

    def _prepare_features(
        self,
        df: pd.DataFrame,
        prediction_days: int
    ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Erstellt Features für das ML-Modell."""
        data = df.copy()

        data['returns'] = data['Close'].pct_change()
        data['log_returns'] = np.log(data['Close'] / data['Close'].shift(1))

        data['high_low_ratio'] = data['High'] / data['Low']
        data['close_open_ratio'] = data['Close'] / data['Open']

        data['volume_ma5'] = data['Volume'].rolling(5).mean()
        data['volume_ma20'] = data['Volume'].rolling(20).mean()
        data['volume_ratio'] = data['Volume'] / data['volume_ma20']

        data['roc_5'] = data['Close'].pct_change(5)
        data['roc_10'] = data['Close'].pct_change(10)
        data['roc_20'] = data['Close'].pct_change(20)

        data['volatility_5'] = data['returns'].rolling(5).std()
        data['volatility_20'] = data['returns'].rolling(20).std()

        data['sma_5'] = data['Close'].rolling(5).mean()
        data['sma_20'] = data['Close'].rolling(20).mean()
        data['sma_50'] = data['Close'].rolling(50).mean()

        data['price_sma5_ratio'] = data['Close'] / data['sma_5']
        data['price_sma20_ratio'] = data['Close'] / data['sma_20']
        data['sma5_sma20_ratio'] = data['sma_5'] / data['sma_20']

        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        data['rsi'] = 100 - (100 / (1 + gain / loss.replace(0, 0.0001)))

        data['target'] = (data['Close'].shift(-prediction_days) > data['Close']).astype(int)

        feature_cols = [
            'returns', 'high_low_ratio', 'close_open_ratio',
            'volume_ratio', 'roc_5', 'roc_10', 'roc_20',
            'volatility_5', 'volatility_20',
            'price_sma5_ratio', 'price_sma20_ratio', 'sma5_sma20_ratio',
            'rsi'
        ]

        data = data.dropna()

        X = data[feature_cols].iloc[:-prediction_days].values
        y = data['target'].iloc[:-prediction_days].values

        return X, y, feature_cols

    def _train_model(
        self,
        X: np.ndarray,
        y: np.ndarray,
        feature_names: List[str],
        n_estimators: int,
        test_size: float
    ) -> Tuple[Any, Dict, Dict]:
        """Trainiert das Random Forest Modell"""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

        split_idx = int(len(X) * (1 - test_size))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            min_samples_split=10,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)

        metrics = {
            'accuracy': accuracy_score(y_test, y_pred),
            'precision': precision_score(y_test, y_pred, zero_division=0),
            'recall': recall_score(y_test, y_pred, zero_division=0),
            'f1': f1_score(y_test, y_pred, zero_division=0),
            'train_samples': len(X_train),
            'test_samples': len(X_test)
        }

        importance = dict(zip(feature_names, model.feature_importances_))
        importance = dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))

        return model, metrics, importance

    def _predict(self, model, X: np.ndarray) -> Tuple[int, float]:
        """Macht Vorhersage für den aktuellsten Datenpunkt"""
        last_row = X[-1:].reshape(1, -1)
        prediction = model.predict(last_row)[0]
        probability = model.predict_proba(last_row)[0][prediction]
        return prediction, probability

    def _build_result(
        self,
        symbol: str,
        data: pd.DataFrame,
        prediction: int,
        probability: float,
        metrics: Dict,
        importance: Dict,
        feature_names: List[str],
        pred_days: int
    ) -> AnalysisResult:
        """Baut das Analyse-Ergebnis zusammen"""
        current_price = data['Close'].iloc[-1]
        direction = "steigend" if prediction == 1 else "fallend"
        direction_emoji = "📈" if prediction == 1 else "📉"

        if prediction == 1 and probability > 0.6:
            recommendation = "buy"
        elif prediction == 0 and probability > 0.6:
            recommendation = "sell"
        else:
            recommendation = "hold"

        confidence = (metrics['accuracy'] * 0.5) + (probability * 0.5)

        summary = (
            f"KI-Prognose {direction_emoji}: Kurs {direction} in {pred_days} Tag(en) "
            f"(Wahrscheinlichkeit: {probability*100:.1f}%). "
            f"Modell-Genauigkeit: {metrics['accuracy']*100:.1f}%."
        )

        warnings = []
        if metrics['accuracy'] < 0.55:
            warnings.append(
                "Warnung: Modell-Genauigkeit unter 55% - "
                "Vorhersage wenig zuverlässig."
            )
        if probability < 0.55:
            warnings.append(
                f"Geringe Konfidenz ({probability*100:.1f}%) - "
                "Signal ist unsicher."
            )

        return AnalysisResult(
            analysis_type=self.name,
            symbol=symbol,
            timestamp=datetime.now(),
            summary=summary,
            confidence=confidence,
            data={
                'current_price': current_price,
                'prediction': int(prediction),
                'prediction_label': direction,
                'probability': probability,
                'prediction_days': pred_days,
                'accuracy': metrics['accuracy'],
                'precision': metrics['precision'],
                'recall': metrics['recall'],
                'f1_score': metrics['f1'],
                'train_samples': metrics['train_samples'],
                'test_samples': metrics['test_samples'],
                'feature_importance': importance
            },
            signals=[{
                'type': 'buy' if prediction == 1 else 'sell',
                'indicator': 'Random Forest',
                'description': f'KI-Prognose: {direction} ({probability*100:.1f}%)',
                'confidence': probability
            }],
            recommendation=recommendation,
            warnings=warnings
        )
