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
FinancialProof - Sentiment Analyse
NLP-basierte Stimmungsanalyse von News und Social Media
"""
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Any, List, Optional
import re

from ..base import (
    BaseAnalyzer, AnalysisResult, AnalysisParameters,
    AnalysisCategory, AnalysisTimeframe
)
from ..registry import AnalysisRegistry


@AnalysisRegistry.register
class SentimentAnalyzer(BaseAnalyzer):
    """Sentiment-Analyse für Aktien/Assets."""

    name = "sentiment"
    display_name = "Sentiment & News Analyse"
    category = AnalysisCategory.NLP
    description = "Analysiert Nachrichten und Social Media für Marktstimmung"
    estimated_duration = 15
    min_data_points = 1

    supported_timeframes = [AnalysisTimeframe.SHORT]

    POSITIVE_WORDS = {
        'buy', 'bullish', 'upgrade', 'growth', 'profit', 'gain', 'surge',
        'rally', 'breakthrough', 'beat', 'exceed', 'record', 'strong',
        'positive', 'optimistic', 'outperform', 'winner', 'success',
        'momentum', 'breakout', 'opportunity', 'kaufen', 'stark', 'wachstum',
        'gewinn', 'durchbruch', 'erfolg', 'positiv', 'chancen'
    }

    NEGATIVE_WORDS = {
        'sell', 'bearish', 'downgrade', 'loss', 'decline', 'drop', 'crash',
        'fall', 'miss', 'weak', 'negative', 'warning', 'risk', 'concern',
        'underperform', 'loser', 'failure', 'bankruptcy', 'fraud', 'lawsuit',
        'verkaufen', 'schwach', 'verlust', 'risiko', 'warnung', 'absturz',
        'krise', 'pleite', 'negativ'
    }

    @classmethod
    def get_parameter_schema(cls) -> Dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "include_news": {"type": "boolean", "default": True},
                "max_articles": {"type": "integer", "default": 20, "minimum": 5, "maximum": 50}
            }
        }

    async def analyze(self, params: AnalysisParameters) -> AnalysisResult:
        symbol = params.symbol
        self.set_progress(10)

        try:
            include_news = params.custom_params.get('include_news', True)
            max_articles = params.custom_params.get('max_articles', 20)

            self.set_progress(20)
            articles = self._fetch_news(symbol, max_articles) if include_news else []

            self.set_progress(40)
            if not articles:
                return AnalysisResult(
                    analysis_type=self.name, symbol=symbol, timestamp=datetime.now(),
                    summary="Keine Nachrichten gefunden für Sentiment-Analyse.",
                    confidence=0.3, data={'articles_analyzed': 0}, warnings=["Keine News verfügbar"]
                )

            self.set_progress(60)
            analyzed_articles = self._analyze_articles(articles)

            self.set_progress(80)
            metrics = self._aggregate_sentiment(analyzed_articles)
            result = self._build_result(symbol, analyzed_articles, metrics)

            self.set_progress(100)
            return result
        except Exception as e:
            return self.create_empty_result(self.name, symbol, str(e))

    def _fetch_news(self, symbol: str, limit: int) -> List[Dict]:
        try:
            import yfinance as yf
            ticker = yf.Ticker(symbol)
            news = ticker.news
            if not news:
                return []
            return [{
                'title': item.get('title', ''),
                'publisher': item.get('publisher', 'Unknown'),
                'link': item.get('link', ''),
                'published': item.get('providerPublishTime', 0),
                'type': item.get('type', 'news')
            } for item in news[:limit]]
        except Exception:
            return []

    def _analyze_articles(self, articles: List[Dict]) -> List[Dict]:
        analyzed = []
        for article in articles:
            title = article['title']
            sentiment_score = self._simple_sentiment(title)
            analyzed.append({
                **article,
                'sentiment_score': sentiment_score,
                'sentiment_label': self._score_to_label(sentiment_score)
            })
        return analyzed

    def _simple_sentiment(self, text: str) -> float:
        text_lower = text.lower()
        words = re.findall(r'\w+', text_lower)
        positive_count = sum(1 for w in words if w in self.POSITIVE_WORDS)
        negative_count = sum(1 for w in words if w in self.NEGATIVE_WORDS)
        total = positive_count + negative_count
        return (positive_count - negative_count) / total if total > 0 else 0.0

    def _score_to_label(self, score: float) -> str:
        if score > 0.3:
            return "positiv"
        elif score < -0.3:
            return "negativ"
        return "neutral"

    def _aggregate_sentiment(self, articles: List[Dict]) -> Dict:
        if not articles:
            return {'average': 0, 'positive_pct': 0, 'negative_pct': 0}
        scores = [a['sentiment_score'] for a in articles]
        positive = sum(1 for s in scores if s > 0.3)
        negative = sum(1 for s in scores if s < -0.3)
        neutral = len(scores) - positive - negative
        return {
            'average': np.mean(scores), 'median': np.median(scores), 'std': np.std(scores),
            'positive_count': positive, 'negative_count': negative, 'neutral_count': neutral,
            'positive_pct': positive / len(scores) * 100,
            'negative_pct': negative / len(scores) * 100,
            'neutral_pct': neutral / len(scores) * 100,
            'total_articles': len(scores)
        }

    def _build_result(self, symbol: str, articles: List[Dict], metrics: Dict) -> AnalysisResult:
        avg_sentiment = metrics['average']
        if avg_sentiment > 0.3:
            overall, recommendation, emoji = "bullish", "buy", "🐂"
        elif avg_sentiment < -0.3:
            overall, recommendation, emoji = "bearish", "sell", "🐻"
        else:
            overall, recommendation, emoji = "neutral", "hold", "😐"

        confidence = min(0.85, 0.5 + abs(avg_sentiment) * 0.1 + (0.2 if metrics['std'] < 0.3 else 0))

        summary = (
            f"Marktstimmung {emoji}: {overall.upper()} "
            f"(Score: {avg_sentiment:.2f}). "
            f"Analysiert: {metrics['total_articles']} Artikel."
        )

        warnings = []
        if metrics['std'] > 0.5:
            warnings.append("Hohe Varianz im Sentiment")
        if metrics['total_articles'] < 5:
            warnings.append("Wenige Artikel analysiert")

        return AnalysisResult(
            analysis_type=self.name, symbol=symbol, timestamp=datetime.now(),
            summary=summary, confidence=confidence,
            data={
                'overall_sentiment': overall, 'average_score': avg_sentiment,
                'median_score': metrics['median'], 'std_deviation': metrics['std'],
                'positive_count': metrics['positive_count'],
                'negative_count': metrics['negative_count'],
                'total_articles': metrics['total_articles']
            },
            signals=[{
                'type': recommendation, 'indicator': 'Sentiment',
                'description': f'Marktstimmung: {overall}', 'confidence': confidence
            }],
            recommendation=recommendation, warnings=warnings
        )
