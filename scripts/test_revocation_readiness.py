from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_revocation_readiness import assess_readiness


class RevocationReadinessTests(unittest.TestCase):
    def setUp(self):
        self.revoked = datetime(2026, 10, 25, 22, 30, tzinfo=timezone.utc)
        self.now = self.revoked + timedelta(minutes=11)
        self.receipt = {
            "assignmentGetStatus": 404,
            "directQueryStatus": 403,
            "nativeConnectionPrincipalVerified": True,
            "freshConversationVerified": True,
            "revocationVerifiedAtUtc": self.revoked.isoformat(),
            "nativeConnectionAuthenticationVerifiedAtUtc": (self.revoked + timedelta(minutes=10)).isoformat(),
            "directQueryVerifiedAtUtc": (self.revoked + timedelta(minutes=10, seconds=10)).isoformat(),
            "freshConversationVerifiedAtUtc": (self.revoked + timedelta(minutes=10, seconds=20)).isoformat(),
        }

    def test_exact_threshold_is_only_preflight_not_acceptance(self):
        result = assess_readiness(self.receipt, self.now)
        self.assertEqual(result["minimumPropagationSeconds"], 600)
        self.assertTrue(result["receiptValidationOnly"])
        for field in ("nativeAcceptancePassed", "effectiveNativeRequestPrincipalEstablished",
                      "historicalFailureReclassified"):
            self.assertFalse(result[field])

    def test_one_second_before_threshold_is_rejected(self):
        self.receipt["nativeConnectionAuthenticationVerifiedAtUtc"] = (
            self.revoked + timedelta(seconds=599)).isoformat()
        with self.assertRaisesRegex(ValueError, "at least 600 seconds"):
            assess_readiness(self.receipt, self.now)

    def test_old_connection_signin_cannot_certify_post_removal_authentication(self):
        self.receipt["nativeConnectionAuthenticationVerifiedAtUtc"] = (
            self.revoked - timedelta(minutes=4)).isoformat()
        with self.assertRaisesRegex(ValueError, "not after the deletion intent"):
            assess_readiness(self.receipt, self.now)

    def test_missing_verified_completion_does_not_fall_back_to_intent(self):
        self.receipt["revocationIntentAtUtc"] = self.receipt.pop("revocationVerifiedAtUtc")
        with self.assertRaisesRegex(ValueError, "revocationVerifiedAtUtc"):
            assess_readiness(self.receipt, self.now)

    def test_missing_controls_and_wrong_statuses_are_rejected(self):
        for field, invalid in (
            ("assignmentGetStatus", 200), ("directQueryStatus", 200),
            ("nativeConnectionPrincipalVerified", "true"), ("freshConversationVerified", False),
        ):
            with self.subTest(field=field):
                receipt = dict(self.receipt, **{field: invalid})
                with self.assertRaises(ValueError):
                    assess_readiness(receipt, self.now)

    def test_invalid_naive_and_future_timestamps_are_rejected(self):
        for invalid in ("not-a-date", "2026-10-25T22:30:00", None,
                        (self.now + timedelta(seconds=1)).isoformat()):
            with self.subTest(value=invalid):
                receipt = dict(self.receipt, revocationVerifiedAtUtc=invalid)
                with self.assertRaises(ValueError):
                    assess_readiness(receipt, self.now)

    def test_stale_direct_denial_and_old_conversation_are_rejected(self):
        for field in ("directQueryVerifiedAtUtc", "freshConversationVerifiedAtUtc"):
            with self.subTest(field=field):
                receipt = dict(self.receipt, **{field: self.revoked.isoformat()})
                with self.assertRaisesRegex(ValueError, "then verify the fresh conversation"):
                    assess_readiness(receipt, self.now)

    def test_preflight_freshness_accepts_120_seconds_but_rejects_121(self):
        queried = datetime.fromisoformat(self.receipt["directQueryVerifiedAtUtc"])
        assess_readiness(self.receipt, queried + timedelta(seconds=120))
        with self.assertRaisesRegex(ValueError, "at most 120 seconds old"):
            assess_readiness(self.receipt, queried + timedelta(seconds=121))

    def test_cli_invalid_receipt_exits_nonzero_without_success_json(self):
        script = Path(__file__).with_name("check_revocation_readiness.py")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "invalid.json"
            path.write_text(json.dumps({"revocationIntentAtUtc": self.revoked.isoformat()}), encoding="utf-8")
            result = subprocess.run([sys.executable, str(script), str(path)],
                                    capture_output=True, text=True, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("independent assignment GET", result.stderr)
        self.assertEqual(result.stdout, "")


if __name__ == "__main__":
    unittest.main()
