"""Exercise verified evidence over the real HTTP host without model calls."""
import asyncio
import importlib.util
import json
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
from azure.core.exceptions import AzureError

from evidence import EvidenceError, Record, render_evidence
from retrieval import VerifiedAnswer


class InvocationTransportTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.corpus = {
            "fp-fixture": Record(
                "fp-fixture", "fraud-patterns-ks", "fraud-patterns", "Fixture", "Exact."
            ),
        }
        self.text = render_evidence({"record_ids": ["fp-fixture"]}, self.corpus)
        self.result = VerifiedAnswer(
            self.text, ("fp-fixture",), "fixture-retrieval", "fixture-selection",
        )

    async def request(self, answer_mock, method="POST", path="/invocations", **kwargs):
        spec = importlib.util.spec_from_file_location(
            "invocation_transport_fixture", Path(__file__).with_name("main.py"),
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("Cannot load the entry point for the transport test")
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
                return await client.request(method, path, **kwargs)

    def assert_error(self, response, status, code):
        self.assertEqual(response.status_code, status, response.text)
        error = response.json()["error"]
        self.assertEqual(set(error), {"code", "message", "reference"})
        self.assertEqual(error["code"], code)
        self.assertTrue(error["message"])
        self.assertRegex(error["reference"], r"^[0-9a-f-]{36}$")
        self.assertNotIn("text", response.json())
        self.assertNotIn(self.text, response.text)

    async def test_delivers_exact_rendered_text_and_provenance(self):
        answer_mock = AsyncMock(return_value=self.result)
        response = await self.request(answer_mock, json={"question": "Fixture question"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), {
            "text": self.text, "record_ids": ["fp-fixture"],
            "retrieval_response_id": "fixture-retrieval",
            "selection_response_id": "fixture-selection",
        })
        answer_mock.assert_awaited_once_with("Fixture question", self.corpus)

    async def test_abstention_has_no_selected_records(self):
        answer_mock = AsyncMock(return_value=VerifiedAnswer(
            "Cannot determine from configured sources.", (), "fixture-retrieval", None,
        ))
        response = await self.request(answer_mock, json={"question": "Unrelated question"})
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(response.json(), {
            "text": "Cannot determine from configured sources.", "record_ids": [],
            "retrieval_response_id": "fixture-retrieval", "selection_response_id": None,
        })

    async def test_rejects_invalid_questions_before_retrieval(self):
        for payload in (None, [], {}, {"question": None}, {"question": False},
                        {"question": " \n"}, {"question": "x" * 12001},
                        {"question": "Fixture", "record_ids": ["fp-fixture"]}):
            with self.subTest(payload_type=type(payload).__name__):
                answer_mock = AsyncMock()
                response = await self.request(
                    answer_mock, content=json.dumps(payload),
                    headers={"Content-Type": "application/json"},
                )
                self.assert_error(response, 400, "invalid_request")
                answer_mock.assert_not_awaited()

    async def test_accepts_exact_question_length_limit_without_rewriting(self):
        question = " " + "x" * 11998 + " "
        answer_mock = AsyncMock(return_value=self.result)
        response = await self.request(answer_mock, json={"question": question})
        self.assertEqual(response.status_code, 200, response.text)
        answer_mock.assert_awaited_once_with(question, self.corpus)

    async def test_rejects_malformed_json_and_invalid_utf8(self):
        for body in (b"{", b"\xff"):
            with self.subTest(body=body):
                answer_mock = AsyncMock()
                response = await self.request(
                    answer_mock, content=body, headers={"Content-Type": "application/json"},
                )
                self.assert_error(response, 400, "invalid_request")
                answer_mock.assert_not_awaited()

    async def test_accepts_maximum_unicode_question_with_escaped_json(self):
        question = "\U0001f600" * 12000
        answer_mock = AsyncMock(return_value=self.result)
        response = await self.request(
            answer_mock, content=json.dumps({"question": question}),
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        self.assertEqual(response.status_code, 200, response.text)
        answer_mock.assert_awaited_once_with(question, self.corpus)

    async def test_rejects_json_parser_resource_limits_before_retrieval(self):
        for body in (
            '{"question":' + '[' * 2000 + '0' + ']' * 2000 + '}',
            '{"question":' + '9' * 5000 + '}',
        ):
            with self.subTest(size=len(body)):
                answer_mock = AsyncMock()
                response = await self.request(
                    answer_mock, content=body,
                    headers={"Content-Type": "application/json"},
                )
                self.assert_error(response, 400, "invalid_request")
                answer_mock.assert_not_awaited()

    async def test_rejects_oversized_body_before_retrieval(self):
        answer_mock = AsyncMock()
        response = await self.request(
            answer_mock, content=b" " * 150001, headers={"Content-Type": "application/json"},
        )
        self.assert_error(response, 413, "request_too_large")
        answer_mock.assert_not_awaited()

    async def test_rejects_unsupported_content_type(self):
        answer_mock = AsyncMock()
        response = await self.request(answer_mock, content="Fixture question")
        self.assert_error(response, 415, "unsupported_media_type")
        answer_mock.assert_not_awaited()

    async def test_verification_failure_does_not_return_partial_evidence(self):
        response = await self.request(
            AsyncMock(side_effect=EvidenceError("Fixture rejection")),
            json={"question": "Fixture question"},
        )
        self.assert_error(response, 502, "source_verification_failed")

    async def test_model_json_failure_is_not_misclassified_as_user_input(self):
        response = await self.request(
            AsyncMock(side_effect=json.JSONDecodeError("Fixture rejection", "", 0)),
            json={"question": "Fixture question"},
        )
        self.assert_error(response, 502, "source_verification_failed")

    async def test_timeout_is_an_explicit_gateway_timeout(self):
        response = await self.request(
            AsyncMock(side_effect=TimeoutError()), json={"question": "Fixture question"},
        )
        self.assert_error(response, 504, "retrieval_timed_out")

    async def test_upstream_error_does_not_become_successful_abstention(self):
        response = await self.request(
            AsyncMock(side_effect=AzureError("Fixture upstream failure")),
            json={"question": "Fixture question"},
        )
        self.assert_error(response, 502, "retrieval_failed")

    async def test_cancellation_is_not_converted_into_a_success_or_error_answer(self):
        with self.assertRaises(asyncio.CancelledError):
            await self.request(
                AsyncMock(side_effect=asyncio.CancelledError()),
                json={"question": "Fixture question"},
            )

    async def test_openapi_describes_the_actual_transport_contract(self):
        answer_mock = AsyncMock()
        response = await self.request(
            answer_mock, "GET", "/invocations/docs/openapi.json",
        )
        self.assertEqual(response.status_code, 200, response.text)
        schema = response.json()
        self.assertEqual(schema["openapi"], "3.1.0")
        self.assertEqual(schema["security"], [{"foundryBearer": []}])
        operation = schema["paths"]["/invocations"]["post"]
        body = operation["requestBody"]["content"]["application/json"]["schema"]
        self.assertEqual(body["required"], ["question"])
        self.assertFalse(body["additionalProperties"])
        self.assertEqual(body["properties"]["question"]["maxLength"], 12000)
        result = operation["responses"]["200"]["content"]["application/json"]["schema"]
        self.assertEqual(set(result["required"]), {
            "text", "record_ids", "retrieval_response_id", "selection_response_id",
        })
        answer_mock.assert_not_awaited()

    async def test_get_cannot_submit_an_invocation(self):
        answer_mock = AsyncMock()
        response = await self.request(answer_mock, "GET")
        self.assertEqual(response.status_code, 405)
        answer_mock.assert_not_awaited()
