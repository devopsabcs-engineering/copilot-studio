import os
import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

from azure.core.exceptions import ClientAuthenticationError, ResourceNotFoundError

from configure_stage import main, stage_definition


class StageTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        environment = patch.dict(os.environ, {
            "FOUNDRY_PROJECT_ENDPOINT": "https://owned.services.ai.azure.com/api/projects/test",
            "WORKSHOP_SEARCH_ENDPOINT": "https://owned.search.windows.net",
            "WORKSHOP_RETRIEVAL_AGENT": "isolated-stage",
            "AZURE_AI_MODEL_DEPLOYMENT_NAME": "owned-model",
            "WORKSHOP_KNOWLEDGE_BASE": "owned-kb",
            "WORKSHOP_SEARCH_CONNECTION": "owned-connection",
        })
        environment.start()
        self.addCleanup(environment.stop)
        self.latest = {
            "id": "isolated-stage:1", "status": "active",
            "metadata": {"Purpose": "verified-source-retrieval"},
            "definition": stage_definition(),
        }
        self.project = MagicMock()
        self.project.agents.get = AsyncMock(return_value=SimpleNamespace(
            as_dict=lambda: {"versions": {"latest": self.latest}},
        ))
        self.project.agents.create_version = AsyncMock(return_value=SimpleNamespace(
            as_dict=lambda: {"id": "isolated-stage:1"},
        ))
        context = MagicMock()
        context.__aenter__ = AsyncMock(return_value=self.project)
        factory = patch("configure_stage.AIProjectClient", return_value=context)
        credential = patch("configure_stage.DefaultAzureCredential")
        printing = patch("builtins.print")
        for mock in (factory, credential, printing):
            mock.start()
            self.addCleanup(mock.stop)

    async def test_identical_owned_stage_is_verified_without_writes(self):
        await main()
        self.project.agents.get.assert_awaited_once_with("isolated-stage")
        self.project.agents.create_version.assert_not_called()

    async def test_different_definition_is_never_replaced(self):
        self.latest["definition"]["instructions"] = "Different instructions"
        with self.assertRaisesRegex(RuntimeError, "refusing"):
            await main()
        self.project.agents.create_version.assert_not_called()

    async def test_different_purpose_is_never_replaced(self):
        self.latest["metadata"]["Purpose"] = "another-workload"
        with self.assertRaisesRegex(RuntimeError, "refusing"):
            await main()
        self.project.agents.create_version.assert_not_called()

    async def test_inactive_stage_is_rejected(self):
        self.latest["status"] = "failed"
        with self.assertRaisesRegex(RuntimeError, "refusing"):
            await main()
        self.project.agents.create_version.assert_not_called()

    async def test_only_not_found_creates_a_new_named_stage(self):
        self.project.agents.get.side_effect = ResourceNotFoundError("Missing")
        await main()
        call = self.project.agents.create_version.call_args.kwargs
        self.assertEqual(call["agent_name"], "isolated-stage")
        self.assertEqual(call["definition"], stage_definition())
        self.assertEqual(call["metadata"]["Purpose"], "verified-source-retrieval")
        self.assertTrue(call["metadata"]["RunId"])

    async def test_authentication_failure_does_not_attempt_creation(self):
        self.project.agents.get.side_effect = ClientAuthenticationError("Denied")
        with self.assertRaises(ClientAuthenticationError):
            await main()
        self.project.agents.create_version.assert_not_called()
