import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from evidence import EvidenceError, Record
from retrieval import answer


class RetrievalTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.record = Record("fp-test", "fraud-patterns-ks", "fraud-patterns", "Fixture", "Exact.")
        self.records = {"fp-test": self.record}
        self.response = {
            "status": "completed", "error": None, "output": [{
                "type": "mcp_call", "name": "knowledge_base_retrieve", "server_label": "fraud-kb",
                "status": "completed", "error": None,
                "output": json.dumps({"documents": [{
                    "url": "https://owned.search.windows.net/indexes/fraud-patterns/docs/fp-test",
                    "content": json.dumps({"id": "fp-test", "content": "Exact."}),
                }]}),
            }],
        }
        retrieval = SimpleNamespace(id="retrieval-id", model_dump=lambda **_: self.response)
        selection = SimpleNamespace(
            id="selection-id", status="completed", error=None,
            output_text='{"record_ids":["fp-test"]}',
        )
        self.client = MagicMock()
        self.client.responses.create = AsyncMock(side_effect=[retrieval, selection])
        client_context = MagicMock()
        client_context.__aenter__ = AsyncMock(return_value=self.client)
        project = MagicMock()
        project.get_openai_client.return_value = client_context
        project_context = MagicMock()
        project_context.__aenter__ = AsyncMock(return_value=project)
        self.project_factory = patch("retrieval.AIProjectClient", return_value=project_context)
        self.credential_factory = patch("retrieval.DefaultAzureCredential")
        self.environment = patch.dict(os.environ, {
            "FOUNDRY_PROJECT_ENDPOINT": "https://owned.services.ai.azure.com/api/projects/test",
            "WORKSHOP_SEARCH_ENDPOINT": "https://owned.search.windows.net",
            "WORKSHOP_RETRIEVAL_AGENT": "isolated-stage", "WORKSHOP_RETRIEVAL_VERSION": "1",
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": "owned-model",
        })
        self.project_factory.start()
        self.credential_factory.start()
        self.environment.start()
        self.addCleanup(self.project_factory.stop)
        self.addCleanup(self.credential_factory.stop)
        self.addCleanup(self.environment.stop)

    async def test_only_verified_rendering_is_returned_after_two_requests(self):
        result = await answer("Actual question", self.records)
        self.assertIn('- "Exact." \u3010fraud-patterns-ks\u3011', result.text)
        self.assertEqual(result.record_ids, ("fp-test",))
        calls = self.client.responses.create.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertNotIn("instructions", calls[0].kwargs)
        self.assertEqual(calls[0].kwargs["extra_body"]["agent_reference"]["version"], "1")
        self.assertEqual(calls[0].kwargs["input"], "Actual question")
        self.assertTrue(calls[1].kwargs["text"]["format"]["strict"])
        self.assertFalse(calls[1].kwargs["store"])

    async def test_invalid_retrieval_stops_before_selection(self):
        self.response["status"] = "incomplete"
        with self.assertRaises(EvidenceError):
            await answer("Question", self.records)
        self.assertEqual(self.client.responses.create.call_count, 1)

    async def test_valid_no_documents_abstains_without_selection_request(self):
        self.response["output"][0]["output"] = '{"documents":[]}'
        result = await answer("Question", self.records)
        self.assertEqual(result.text, "Cannot determine from configured sources.")
        self.assertIsNone(result.selection_response_id)
        self.assertEqual(self.client.responses.create.call_count, 1)

    async def test_completed_blank_tool_output_abstains_without_selection(self):
        self.response["output"][0]["output"] = "\n"
        result = await answer("An unrelated astronomy question", self.records)
        self.assertEqual(result.text, "Cannot determine from configured sources.")
        self.assertEqual(result.record_ids, ())
        self.assertEqual(result.retrieval_response_id, "retrieval-id")
        self.assertIsNone(result.selection_response_id)
        self.assertEqual(self.client.responses.create.call_count, 1)

    async def test_invalid_questions_never_reach_azure(self):
        for question in ("", "   ", "x" * 12001, None):
            with self.subTest(question_type=type(question).__name__):
                with self.assertRaises(ValueError):
                    await answer(question, self.records)
        self.client.responses.create.assert_not_called()

    async def test_selector_cannot_return_an_unretrieved_record(self):
        self.client.responses.create.side_effect = [
            SimpleNamespace(id="retrieval-id", model_dump=lambda **_: self.response),
            SimpleNamespace(id="selection-id", status="completed", error=None,
                            output_text='{"record_ids":["invented"]}'),
        ]
        with self.assertRaises(EvidenceError):
            await answer("Question", self.records)

    async def test_failed_selector_never_returns_draft_text(self):
        self.client.responses.create.side_effect = [
            SimpleNamespace(id="retrieval-id", model_dump=lambda **_: self.response),
            SimpleNamespace(id="selection-id", status="incomplete", error=None,
                            output_text="Unsupported draft"),
        ]
        with self.assertRaises(EvidenceError):
            await answer("Question", self.records)
