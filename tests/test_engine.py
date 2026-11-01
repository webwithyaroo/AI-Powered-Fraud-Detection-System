from datetime import datetime, timedelta
import unittest

from fraud_detection import RealTimeFraudDetectionEngine, Transaction


class RealTimeFraudDetectionEngineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = RealTimeFraudDetectionEngine()
        self.base_time = datetime(2026, 1, 1, 10, 0, 0)

    def _tx(self, txn_id: str, amount: float, country: str = "US", mcc: str = "groceries") -> Transaction:
        return Transaction(
            transaction_id=txn_id,
            account_id="acct-1",
            amount=amount,
            country=country,
            merchant_category=mcc,
            timestamp=self.base_time + timedelta(minutes=int(amount) % 60),
        )

    def test_low_risk_transaction_is_approved(self) -> None:
        result = self.engine.process(self._tx("t1", 50))

        self.assertEqual(result["decision"], "approve")
        self.assertLess(result["risk_score"], 40)

    def test_unusual_amount_and_risky_context_is_blocked(self) -> None:
        self.engine.process(self._tx("history-1", 100))
        self.engine.process(self._tx("history-2", 120))
        result = self.engine.process(self._tx("t2", 5_000, country="NG", mcc="cryptocurrency"))

        self.assertEqual(result["decision"], "block")
        self.assertGreaterEqual(result["risk_score"], 75)

    def test_medium_risk_transaction_goes_to_review(self) -> None:
        self.engine.process(self._tx("history-1", 100))
        self.engine.process(self._tx("history-2", 90))
        result = self.engine.process(self._tx("t3", 600, mcc="money_transfer"))

        self.assertEqual(result["decision"], "review")
        self.assertGreaterEqual(result["risk_score"], 40)
        self.assertLess(result["risk_score"], 75)


if __name__ == "__main__":
    unittest.main()
