from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class Transaction:
    transaction_id: str
    account_id: str
    amount: float
    country: str
    merchant_category: str
    timestamp: datetime


class FeatureStore:
    """In-memory feature store for account-level transaction history."""

    def __init__(self) -> None:
        self._transactions_by_account: Dict[str, List[Transaction]] = {}

    def append(self, transaction: Transaction) -> None:
        self._transactions_by_account.setdefault(transaction.account_id, []).append(transaction)

    def get_account_transactions(self, account_id: str) -> List[Transaction]:
        return self._transactions_by_account.get(account_id, [])


class AnomalyDetector:
    """Rule-based anomaly detector representing a lightweight ML signal layer."""

    def __init__(self, high_value_amount: float = 10_000.0) -> None:
        self.high_value_amount = high_value_amount

    def score(self, transaction: Transaction, history: List[Transaction]) -> float:
        if not history:
            return 0.2 if transaction.amount >= self.high_value_amount else 0.0

        avg_amount = sum(t.amount for t in history) / len(history)
        max_amount = max(t.amount for t in history)

        score = 0.0
        if transaction.amount >= self.high_value_amount:
            score += 0.5
        if transaction.amount > max_amount * 3:
            score += 0.3
        if avg_amount > 0 and transaction.amount > avg_amount * 5:
            score += 0.2
        return min(score, 1.0)


class RiskScorer:
    """Automated risk scoring that combines anomaly and business risk features."""

    HIGH_RISK_COUNTRIES = {"NG", "KP", "IR"}
    HIGH_RISK_MCC = {"gambling", "cryptocurrency", "money_transfer"}

    def score(self, transaction: Transaction, anomaly_score: float) -> float:
        score = anomaly_score * 80

        if transaction.country in self.HIGH_RISK_COUNTRIES:
            score += 20
        if transaction.merchant_category in self.HIGH_RISK_MCC:
            score += 15

        return min(score, 100.0)


class RealTimeFraudDetectionEngine:
    """Monitors transactions in real time and classifies fraud risk."""

    def __init__(
        self,
        feature_store: FeatureStore | None = None,
        anomaly_detector: AnomalyDetector | None = None,
        risk_scorer: RiskScorer | None = None,
        block_threshold: float = 75.0,
        review_threshold: float = 40.0,
    ) -> None:
        self.feature_store = feature_store or FeatureStore()
        self.anomaly_detector = anomaly_detector or AnomalyDetector()
        self.risk_scorer = risk_scorer or RiskScorer()
        self.block_threshold = block_threshold
        self.review_threshold = review_threshold

    def process(self, transaction: Transaction) -> Dict[str, float | str]:
        history = self.feature_store.get_account_transactions(transaction.account_id)
        anomaly_score = self.anomaly_detector.score(transaction, history)
        risk_score = self.risk_scorer.score(transaction, anomaly_score)

        if risk_score >= self.block_threshold:
            decision = "block"
        elif risk_score >= self.review_threshold:
            decision = "review"
        else:
            decision = "approve"

        self.feature_store.append(transaction)
        return {
            "transaction_id": transaction.transaction_id,
            "anomaly_score": round(anomaly_score, 4),
            "risk_score": round(risk_score, 2),
            "decision": decision,
        }
