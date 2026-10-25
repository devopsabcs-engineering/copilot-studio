"""Exercise the vendor identity-construction boundary that failed in hosting."""
import importlib.util
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from azure.ai.agentserver.activity._m365_bridge import _build_outbound_claims
from microsoft_agents.hosting.core import ClaimsIdentity

from evidence import EvidenceError, Record, render_evidence
from retrieval import VerifiedAnswer


class ActivityCompatibilityTests(unittest.TestCase):
    def test_hosted_bridge_preserves_authenticated_bot_identity(self):
        bot_id = "00000000-0000-0000-0000-000000000001"
        identity = _build_outbound_claims(
            ClaimsIdentity, digital_worker=False, is_hosted=True, bot_app_id=bot_id,
        )
        self.assertIsInstance(identity, ClaimsIdentity)
        self.assertFalse(identity.allow_anonymous)
        self.assertEqual(identity.get_app_id(), bot_id)


class ActivityTransportTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.corpus = {
            "fp-fixture": Record(
                "fp-fixture", "fraud-patterns-ks", "fraud-patterns", "Fixture", "Exact."
            ),
        }
        self.expected = render_evidence({"record_ids": ["fp-fixture"]}, self.corpus)

    async def deliver(self, answer_mock):
        spec = importlib.util.spec_from_file_location(
            "activity_transport_fixture", Path(__file__).with_name("main.py"),
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("Cannot load the Activity entry point for the transport test")
        module = importlib.util.module_from_spec(spec)
        with patch.dict("os.environ", {
            "OTEL_SDK_DISABLED": "true", "FOUNDRY_HOSTING_ENVIRONMENT": "",
            "FOUNDRY_AGENT_INSTANCE_CLIENT_ID": "",
        }), patch("dotenv.load_dotenv"), patch("urllib.request.urlopen"), patch(
            "evidence.load_corpus", return_value=self.corpus,
        ), patch("retrieval.answer", answer_mock):
            spec.loader.exec_module(module)
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=module.host), base_url="http://testserver",
            ) as client:
                response = await client.post("/activity/messages", json={
                    "type": "message", "id": "fixture-message", "text": "Fixture question",
                    "channelId": "emulator", "deliveryMode": "expectReplies",
                    "serviceUrl": "http://testserver",
                    "from": {"id": "fixture-user"}, "recipient": {"id": "fixture-bot"},
                    "conversation": {"id": "fixture-conversation"},
                })
        self.assertEqual(response.status_code, 200, response.text)
        answer_mock.assert_awaited_once_with("Fixture question", self.corpus)
        return response.json()["activities"]

    async def test_real_local_adapter_delivers_rendered_evidence_unchanged(self):
        activities = await self.deliver(AsyncMock(return_value=VerifiedAnswer(
            self.expected, ("fp-fixture",), "fixture-retrieval", "fixture-selection",
        )))
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]["text"], self.expected)

    async def test_real_local_adapter_reports_validation_failure_without_evidence(self):
        activities = await self.deliver(AsyncMock(side_effect=EvidenceError("Fixture rejection")))
        self.assertEqual(len(activities), 1)
        self.assertRegex(activities[0]["text"], (
            r"^Source verification or delivery failed\. No unverified answer was delivered\. "
            r"Reference: [0-9a-f-]{36}$"
        ))

    async def test_real_local_adapter_delivers_abstention_unchanged(self):
        text = "Cannot determine from configured sources."
        activities = await self.deliver(AsyncMock(return_value=VerifiedAnswer(
            text, (), "fixture-retrieval", None,
        )))
        self.assertEqual(len(activities), 1)
        self.assertEqual(activities[0]["text"], text)
