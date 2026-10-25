"""Exercise the actual MCP HTTP protocol and signed Entra-token verification."""
import asyncio
from dataclasses import replace
import json
import os
import time
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch

from azure.core.exceptions import AzureError
from cryptography.hazmat.primitives.asymmetric import rsa
import jwt
from starlette.testclient import TestClient

from evidence import EvidenceError, NOTEBOOK_SHA256, NOTEBOOK_URL, Record, render_evidence
from mcp_auth import EVIDENCE_SCOPE, EntraSettings, EntraTokenVerifier
from mcp_server import configured_server, create_app, create_server
from retrieval import VerifiedAnswer


TENANT = "11111111-1111-4111-8111-111111111111"
AUDIENCE = "22222222-2222-4222-8222-222222222222"
CLIENT = "33333333-3333-4333-8333-333333333333"
USER = "44444444-4444-4444-8444-444444444444"
SETTINGS = EntraSettings(
    TENANT, AUDIENCE, frozenset({CLIENT}), frozenset({USER}),
    "https://evidence.example.test/mcp",
)


class MCPTransportTests(unittest.TestCase):
    def setUp(self):
        self.corpus = {
            "rc-fixture": Record(
                "rc-fixture", "regulatory-compliance-ks", "regulatory-compliance",
                "Fixture", "Exact conditional evidence.",
            ),
        }
        self.result = VerifiedAnswer(
            render_evidence({"record_ids": ["rc-fixture"]}, self.corpus),
            ("rc-fixture",), "fixture-retrieval", "fixture-selection",
        )

    def request(self, answer_mock, method, params, *, host="127.0.0.1", entra=None,
                headers=None):
        server = create_server(self.corpus, host=host, entra=entra)
        with patch("mcp_server.retrieval.answer", answer_mock), TestClient(
            create_app(server), base_url="http://127.0.0.1",
            headers={"Accept": "application/json, text/event-stream"},
        ) as client:
            initialization = client.post("/mcp", json={
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                           "clientInfo": {"name": "fixture-client", "version": "1"}},
            }, headers=headers)
            if initialization.status_code != 200:
                return initialization
            self.assertIn("protocolVersion", initialization.json()["result"])
            return client.post("/mcp", json={
                "jsonrpc": "2.0", "id": 2, "method": method, "params": params,
            }, headers=headers)

    def call(self, answer_mock, arguments):
        response = self.request(answer_mock, "tools/call", {
            "name": "retrieve_verified_workshop_evidence", "arguments": arguments,
        })
        self.assertEqual(response.status_code, 200, response.text)
        return response.json()["result"]

    def test_tool_discovery_has_typed_evidence_output(self):
        answer_mock = AsyncMock()
        response = self.request(answer_mock, "tools/list", {})
        self.assertEqual(response.status_code, 200, response.text)
        tools = response.json()["result"]["tools"]
        self.assertEqual(len(tools), 1)
        self.assertEqual(tools[0]["name"], "retrieve_verified_workshop_evidence")
        self.assertEqual(tools[0]["inputSchema"]["required"], ["question"])
        output = tools[0]["outputSchema"]
        self.assertFalse(output["additionalProperties"])
        self.assertIn("records", output["required"])
        self.assertIn("publisher_sha256", output["required"])
        answer_mock.assert_not_awaited()

    def test_returns_exact_text_records_and_correlated_provenance(self):
        answer_mock = AsyncMock(return_value=self.result)
        result = self.call(answer_mock, {"question": "  Original question  "})
        self.assertFalse(result["isError"])
        data = result["structuredContent"]
        self.assertEqual(data, {
            "text": self.result.text, "record_ids": ["rc-fixture"],
            "records": [{
                "record_id": "rc-fixture", "source": "regulatory-compliance-ks",
                "index": "regulatory-compliance", "title": "Fixture",
                "content": "Exact conditional evidence.",
            }],
            "retrieval_response_id": "fixture-retrieval",
            "selection_response_id": "fixture-selection",
            "publisher_url": NOTEBOOK_URL, "publisher_sha256": NOTEBOOK_SHA256,
        })
        self.assertEqual(json.loads(result["content"][0]["text"]), data)
        answer_mock.assert_awaited_once_with("  Original question  ", self.corpus)

    def test_abstention_is_explicit_success_with_empty_records(self):
        result = self.call(AsyncMock(return_value=VerifiedAnswer(
            "Cannot determine from configured sources.", (), "fixture-retrieval", None,
        )), {"question": "Unrelated question"})
        self.assertFalse(result["isError"])
        self.assertEqual(result["structuredContent"]["records"], [])
        self.assertEqual(result["structuredContent"]["record_ids"], [])
        self.assertIsNone(result["structuredContent"]["selection_response_id"])
        self.assertEqual(result["structuredContent"]["text"],
                         "Cannot determine from configured sources.")

    def test_invalid_questions_do_not_invoke_retrieval(self):
        for arguments in ({}, {"question": 12}, {"question": None},
                          {"question": " \n"}, {"question": "x" * 12001}):
            with self.subTest(arguments_type=type(arguments.get("question")).__name__):
                answer_mock = AsyncMock()
                result = self.call(answer_mock, arguments)
                self.assertTrue(result["isError"])
                self.assertNotIn("structuredContent", result)
                answer_mock.assert_not_awaited()

    def test_question_length_limit_is_inclusive(self):
        question = "\U0001f600" * 12000
        answer_mock = AsyncMock(return_value=self.result)
        result = self.call(answer_mock, {"question": question})
        self.assertFalse(result["isError"])
        answer_mock.assert_awaited_once_with(question, self.corpus)

    def test_failures_never_return_partial_evidence_or_abstention(self):
        for error, code in (
            (EvidenceError("private verification detail"), "source_verification_failed"),
            (TimeoutError("private timeout detail"), "retrieval_timed_out"),
            (AzureError("private upstream detail"), "retrieval_failed"),
        ):
            with self.subTest(code=code):
                result = self.call(AsyncMock(side_effect=error), {"question": "Question"})
                self.assertTrue(result["isError"])
                self.assertNotIn("structuredContent", result)
                text = result["content"][0]["text"]
                self.assertIn(code, text)
                self.assertRegex(text, r"Reference: [0-9a-f-]{36}")
                self.assertNotIn("private", text)
                self.assertNotIn("Cannot determine", text)

    def test_rejects_modified_rendering_and_unknown_selected_records(self):
        for answer in (
            replace(self.result, text='A generated "quotation".'),
            replace(self.result, record_ids=("unknown",)),
            replace(self.result, record_ids=("rc-fixture", "rc-fixture")),
            replace(self.result, retrieval_response_id=""),
            replace(self.result, selection_response_id=None),
        ):
            with self.subTest(record_ids=answer.record_ids):
                result = self.call(AsyncMock(return_value=answer), {"question": "Question"})
                self.assertTrue(result["isError"])
                self.assertNotIn("structuredContent", result)
                self.assertIn("source_verification_failed", result["content"][0]["text"])

    def test_http_body_limit_and_dns_rebinding_protection(self):
        server = create_server(self.corpus)
        with TestClient(create_app(server), base_url="http://127.0.0.1") as client:
            initialization = json.dumps({
                "jsonrpc": "2.0", "id": 1, "method": "initialize",
                "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                           "clientInfo": {"name": "body-limit-fixture", "version": "1"}},
            }).encode()
            response = client.post(
                "/mcp", content=initialization + b" " * (150000 - len(initialization)),
                headers={"Content-Type": "application/json",
                         "Accept": "application/json, text/event-stream"},
            )
            self.assertEqual(response.status_code, 200, response.text)
            for kwargs, status in (
                ({"content": b"x" * 150001,
                  "headers": {"Content-Type": "application/json"}}, 413),
                ({"json": {}, "headers": {"Host": "attacker.example"}}, 421),
                ({"json": {}, "headers": {"Origin": "https://attacker.example"}}, 403),
            ):
                with self.subTest(status=status):
                    response = client.post("/mcp", **kwargs)
                    self.assertEqual(response.status_code, status, response.text)

    def test_malformed_and_parser_limit_bodies_are_rejected_before_retrieval(self):
        server = create_server(self.corpus)
        answer_mock = AsyncMock()
        with patch("mcp_server.retrieval.answer", answer_mock), TestClient(
            create_app(server), base_url="http://127.0.0.1",
        ) as client:
            depth = 10000
            for body in (b"{", b"\xff", b"[" * depth + b"]" * depth,
                         b'{"id":' + b"1" * 5000 + b"}"):
                with self.subTest(length=len(body)):
                    response = client.post(
                        "/mcp", content=body, headers={"Content-Type": "application/json"},
                    )
                    self.assertEqual(response.status_code, 400, response.text)
                    self.assertEqual(response.json()["error"]["code"], -32700)
                    self.assertNotIn("result", response.json())
        answer_mock.assert_not_awaited()

    def test_missing_and_untrusted_bearer_are_denied_before_retrieval(self):
        answer_mock = AsyncMock()
        with patch("jwt.PyJWKClient.get_signing_key_from_jwt",
                   side_effect=jwt.PyJWKClientError("fixture")):
            for headers in ({}, {"Authorization": "Bearer invalid-token"}):
                response = self.request(
                    answer_mock, "tools/list", {}, host="0.0.0.0",
                    entra=SETTINGS, headers=headers,
                )
                self.assertEqual(response.status_code, 401, response.text)
        answer_mock.assert_not_awaited()

    def test_nonloopback_requires_complete_authentication_configuration(self):
        with self.assertRaisesRegex(ValueError, "require explicit Entra"):
            create_server(self.corpus, host="0.0.0.0")
        with patch.dict(os.environ, {"WORKSHOP_MCP_TENANT_ID": TENANT}, clear=True):
            with self.assertRaisesRegex(ValueError, "All five"):
                configured_server(self.corpus)
        for url in ("http://evidence.example/mcp", "https://evidence.example/other",
                    "https://user:password@evidence.example/mcp",
                    "https://evidence.example/mcp?extra=1"):
            with self.subTest(url=url), self.assertRaises(ValueError):
                replace(SETTINGS, resource_url=url)
        with self.assertRaises(ValueError):
            replace(SETTINGS, client_ids=frozenset())

    def test_signed_authorized_token_reaches_tool_over_http(self):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        now = int(time.time())
        token = jwt.encode({
            "iss": SETTINGS.issuer, "aud": AUDIENCE, "tid": TENANT, "azp": CLIENT,
            "oid": USER, "scp": EVIDENCE_SCOPE, "iat": now, "nbf": now - 1, "exp": now + 600,
        }, private_key, algorithm="RS256")
        answer_mock = AsyncMock(return_value=self.result)
        with patch("jwt.PyJWKClient.get_signing_key_from_jwt",
                   return_value=SimpleNamespace(key=private_key.public_key())):
            response = self.request(
                answer_mock, "tools/call",
                {"name": "retrieve_verified_workshop_evidence", "arguments": {"question": "Question"}},
                host="0.0.0.0", entra=SETTINGS,
                headers={"Authorization": f"Bearer {token}"},
            )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json()["result"]["structuredContent"]["text"], self.result.text)
        answer_mock.assert_awaited_once_with("Question", self.corpus)


class EntraVerificationTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        cls.public_key = cls.private_key.public_key()

    def claims(self):
        now = int(time.time())
        return {
            "iss": SETTINGS.issuer, "aud": AUDIENCE, "tid": TENANT, "azp": CLIENT,
            "oid": USER, "scp": EVIDENCE_SCOPE, "iat": now, "nbf": now - 1,
            "exp": now + 600,
        }

    async def verify(self, claims, *, key=None):
        token = jwt.encode(claims, key or self.private_key, algorithm="RS256")
        verifier = EntraTokenVerifier(SETTINGS)
        with patch.object(verifier.keys, "get_signing_key_from_jwt",
                          return_value=SimpleNamespace(key=self.public_key)):
            return await verifier.verify_token(token)

    async def test_valid_signed_delegated_token_passes(self):
        result = await self.verify(self.claims())
        self.assertIsNotNone(result)
        self.assertEqual(result.client_id, CLIENT)
        self.assertEqual(result.subject, USER)
        self.assertEqual(result.resource, AUDIENCE)
        self.assertEqual(result.scopes, [EVIDENCE_SCOPE])

    async def test_wrong_signature_tenant_audience_issuer_caller_and_scope_fail(self):
        replacements = {
            "aud": USER, "iss": "https://attacker.example", "tid": USER, "azp": USER,
            "oid": CLIENT, "scp": "Other.Read", "exp": int(time.time()) - 60,
            "nbf": int(time.time()) + 600,
        }
        for field, value in replacements.items():
            with self.subTest(field=field):
                claims = self.claims()
                claims[field] = value
                self.assertIsNone(await self.verify(claims))
        wrong_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.assertIsNone(await self.verify(self.claims(), key=wrong_key))

    async def test_missing_delegated_claim_and_nonstring_caller_fail(self):
        for field in ("iss", "aud", "exp", "iat", "nbf", "tid", "oid", "azp", "scp"):
            with self.subTest(missing=field):
                claims = self.claims()
                del claims[field]
                self.assertIsNone(await self.verify(claims))
        for field in ("tid", "oid", "azp", "scp"):
            with self.subTest(nonstring=field):
                claims = self.claims()
                claims[field] = []
                self.assertIsNone(await self.verify(claims))

    async def test_other_algorithms_and_audience_lists_are_rejected(self):
        claims = self.claims()
        claims["aud"] = [AUDIENCE, USER]
        self.assertIsNone(await self.verify(claims))
        token = jwt.encode(self.claims(), "a-fixture-only-key-that-is-not-a-secret", algorithm="HS256")
        verifier = EntraTokenVerifier(SETTINGS)
        with patch.object(verifier.keys, "get_signing_key_from_jwt",
                          return_value=SimpleNamespace(key=self.public_key)):
            self.assertIsNone(await verifier.verify_token(token))

    async def test_cancellation_is_not_converted_to_evidence_or_abstention(self):
        server = create_server({})
        with patch("mcp_server.retrieval.answer", AsyncMock(side_effect=asyncio.CancelledError)):
            with self.assertRaises(asyncio.CancelledError):
                await server.call_tool(
                    "retrieve_verified_workshop_evidence", {"question": "Question"},
                )


if __name__ == "__main__":
    unittest.main()
