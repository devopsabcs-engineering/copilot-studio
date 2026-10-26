"""Reject premature permission-removal tests without claiming native acceptance."""

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path


MINIMUM_PROPAGATION_SECONDS = 600
MAXIMUM_PREFLIGHT_AGE_SECONDS = 120


def assess_readiness(receipt: dict, now: datetime) -> dict:
    if now.utcoffset() is None:
        raise ValueError("The assessment time must include a UTC offset.")
    if receipt.get("assignmentGetStatus") != 404:
        raise ValueError("An independent assignment GET must confirm HTTP 404.")
    if receipt.get("directQueryStatus") != 403:
        raise ValueError("The direct data query must confirm HTTP 403.")
    if receipt.get("nativeConnectionPrincipalVerified") is not True:
        raise ValueError("The native connection's authenticated principal must be verified.")
    if receipt.get("freshConversationVerified") is not True:
        raise ValueError("A fresh native conversation must be independently verified.")

    def timestamp(key: str) -> datetime:
        value = receipt.get(key)
        if not isinstance(value, str):
            raise ValueError(f"{key} must be an ISO 8601 timestamp with a UTC offset.")
        try:
            result = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"{key} is not a valid ISO 8601 timestamp.") from error
        if result.utcoffset() is None or result > now:
            raise ValueError(f"{key} must include a UTC offset and cannot be in the future.")
        return result

    revoked = timestamp("revocationVerifiedAtUtc")
    authenticated = timestamp("nativeConnectionAuthenticationVerifiedAtUtc")
    queried = timestamp("directQueryVerifiedAtUtc")
    conversation = timestamp("freshConversationVerifiedAtUtc")
    earliest = revoked + timedelta(seconds=MINIMUM_PROPAGATION_SECONDS)
    if authenticated < earliest:
        raise ValueError(
            "Native connection authentication must be verified at least 600 seconds "
            "after independently confirmed revocation, not after the deletion intent."
        )
    if not authenticated <= queried <= conversation <= now:
        raise ValueError(
            "Verify direct denial after connection authentication, then verify the fresh conversation."
        )
    if (now - queried).total_seconds() > MAXIMUM_PREFLIGHT_AGE_SECONDS:
        raise ValueError("Direct denial and fresh conversation verification must be at most 120 seconds old.")
    return {
        "status": "READY_FOR_SEPARATE_NATIVE_TEST_NOT_ACCEPTANCE",
        "minimumPropagationSeconds": MINIMUM_PROPAGATION_SECONDS,
        "maximumPreflightAgeSeconds": MAXIMUM_PREFLIGHT_AGE_SECONDS,
        "secondsSinceVerifiedRevocation": (now - revoked).total_seconds(),
        "receiptValidationOnly": True,
        "effectiveNativeRequestPrincipalEstablished": False,
        "nativeAcceptancePassed": False,
        "historicalFailureReclassified": False,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("receipt", type=Path, help="Private independently collected preflight JSON.")
    args = parser.parse_args()
    try:
        receipt = json.loads(args.receipt.read_text(encoding="utf-8"))
        if not isinstance(receipt, dict):
            raise ValueError("The receipt must be a JSON object.")
        result = assess_readiness(receipt, datetime.now(timezone.utc))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
