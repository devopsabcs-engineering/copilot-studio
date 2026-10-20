"""Offline regression tests for documentation export and link validation."""
from pathlib import Path
import json
import tempfile
import unittest

from build_wiki import export, page_name, render_wiki_metadata, rewrite_links
from validate_docs import local_link_errors, validate


class WikiTests(unittest.TestCase):
    def test_page_names(self):
        root = Path(__file__).resolve().parents[1]
        self.assertEqual(page_name(root / "README.md"), "Home")
        self.assertEqual(page_name(root / "docs/fr/lab-05-1.md"), "FR-lab-05-1")

    def test_relative_links_and_images(self):
        root = Path(__file__).resolve().parents[1]
        source = root / "docs/en/lab-01.md"
        text = "[FR](../fr/lab-01.md) ![Image](../assets/lab-01/image2.png) [Web](https://example.org/a)"
        result = rewrite_links(text, source)
        self.assertIn("[FR](FR-lab-01)", result)
        self.assertIn("![Image](assets/lab-01/image2.png)", result)
        self.assertIn("[Web](https://example.org/a)", result)

    def test_fragment_is_preserved(self):
        root = Path(__file__).resolve().parents[1]
        result = rewrite_links("[Guide](index.md#start-here)", root / "docs/en/lab-01.md")
        self.assertEqual(result, "[Guide](EN-index#start-here)")

    def test_wiki_metadata_is_rendered_as_a_title(self):
        source = "---\ntitle: Guide français\ndescription: Example\n---\n\n## Goal\n"
        self.assertEqual(render_wiki_metadata(source), "# Guide français\n\n## Goal\n")
        with self.assertRaises(ValueError):
            render_wiki_metadata("No metadata")

    def test_export_does_not_overwrite_sources(self):
        root = Path(__file__).resolve().parents[1]
        with self.assertRaises(ValueError):
            export(root / "docs/en")
        with self.assertRaises(ValueError):
            export(root)

    def test_broken_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "page.md"
            path.write_text("[Missing](missing.md)\n", encoding="utf-8")
            self.assertEqual(len(local_link_errors(path)), 1)

    def test_export_and_repository_integrity(self):
        with tempfile.TemporaryDirectory() as directory:
            export(Path(directory))
            errors, counts = validate(wiki=Path(directory))
            self.assertEqual(errors, [])
            self.assertGreaterEqual(counts["bilingual_pairs"], 13)
            self.assertGreaterEqual(counts["screenshots"], 29)

    def test_backend_evidence_preserves_acceptance_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-19" / "backend-results.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(result["overall_workshop_certified"])
        self.assertEqual(result["power_platform"]["scoped_component_count"], 4)
        cli = result["official_cli"]
        self.assertEqual(cli["windows_authenticode_status"], "Valid")
        self.assertTrue(cli["clone_persistent_short_path_passed"])
        self.assertTrue(cli["original_active_profile_restored"])
        for key in ("global_cli_installation", "tls_validation_disabled",
                    "proxy_settings_changed", "package_policy_overridden"):
            self.assertFalse(cli[key])
        audit = result["lab1_source_identity_audit"]
        self.assertEqual(audit["checks"], audit["passed"] + audit["blocked"] + audit["failed"])
        self.assertTrue(audit["cloned_pdf_matches_fresh_original_hash"])
        self.assertFalse(audit["complete_answer_claim_accuracy_verified"])
        self.assertFalse(audit["citation_target_fidelity_verified"])
        runtime = result["runtime_boundaries"]
        self.assertEqual(runtime["directline_discovery_outer_http_status"], 400)
        self.assertEqual(runtime["maker_evaluation_discovery_http_status"], 403)
        self.assertEqual(runtime["maker_evaluation_inner_error"],
                         "InsufficientDelegatedPermissions")
        self.assertEqual(runtime["maker_evaluation_missing_delegated_permission"],
                         "CopilotStudio.MakerOperations.Read")
        for key in ("directline_endpoint_obtained", "directline_root_cause_established",
                    "evaluation_run_started", "new_agent_conversation_executed",
                    "standard_harness_connection_verified"):
            self.assertFalse(runtime[key])
        preservation = result["preservation"]
        self.assertFalse(preservation["existing_agent_modified"])
        self.assertFalse(preservation["existing_agent_published_by_this_test"])
        self.assertEqual(preservation["emails_resent"], 0)
        self.assertEqual(preservation["new_paid_azure_resources"], 0)

    def test_runtime_retries_do_not_invent_conversation_or_consent(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-19" / "backend-results.json"
        result = json.loads(path.read_text(encoding="utf-8"))["additional_runtime_attempts"]
        self.assertTrue(result["explicit_read_scope_token_request_started"])
        self.assertTrue(result["explicit_read_scope_token_request_stopped"])
        self.assertFalse(result["explicit_read_scope_token_obtained"])
        self.assertFalse(result["package_policy_override_attempted"])
        self.assertEqual(result["consent_or_permission_changes"], 0)
        self.assertEqual(result["browser_open_attempts"], 1)
        self.assertEqual(result["browser_open_result"], "tool_timeout")
        self.assertFalse(result["browser_open_page_id_returned"])
        self.assertFalse(result["browser_open_eventual_effect_known"])
        for key in ("new_benign_prompts_submitted", "new_complete_answers_captured",
                    "new_citation_checks", "new_screenshots"):
            self.assertEqual(result[key], 0)

    def test_browser_recovery_preserves_acceptance_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "browser-results.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["gate"]["narrow_live_checks_passed"], 3)
        self.assertEqual(result["gate"]["full_workshop_status"], "blocked")
        checks = {check["id"]: check for check in result["checks"]}
        answer = checks["fresh-uploaded-pdf-conversation"]
        self.assertIn("cite:1", answer["complete_final_answer_markdown"])
        self.assertEqual(answer["citation_mapping"]["retrieval_reference"], "turn1doc1")
        directory = checks["fresh-directory-invalid-top"]
        self.assertEqual(directory["actual_tool_input"]["top"], -1)
        self.assertIn("400", directory["actual_tool_error_panel"])
        self.assertFalse(directory["observed_retry"])
        self.assertFalse(checks["evaluate-browser-route"]["create_evaluation_clicked"])
        safety = result["safety"]
        self.assertEqual(safety["new_runtime_prompts"], 3)
        for key in ("email_sent", "agent_configuration_modified", "agent_created",
                    "agent_published", "permissions_or_consent_modified",
                    "authentication_modified", "azure_resources_created",
                    "paid_test_resources_recreated", "evaluation_created_or_run"):
            self.assertFalse(safety[key])
        self.assertEqual(result["screenshots"]["saved_files"], [])

    def test_foundry_evidence_preserves_acceptance_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-19" / "foundry-results.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(result["overall_workshop_certified"])
        retrieval = result["indexing_and_ga_retrieval"]
        self.assertEqual(retrieval["original_records"], 24)
        self.assertEqual(sum(query["passages"] for query in retrieval["queries"]),
                         retrieval["exact_original_passage_matches"])
        self.assertTrue(result["mcp"]["current_preview"]["passed"])
        self.assertFalse(result["mcp"]["historical_preview"]["tool_call_passed"])
        self.assertTrue(result["foundry_agent"]["single_source"]["passed"])
        self.assertFalse(result["foundry_agent"]["single_source"]["requested_output_constraints_followed"])
        cross = result["foundry_agent"]["cross_source_recovery"]
        self.assertFalse(cross["passed"])
        self.assertEqual(len(cross["final_quotation_checks"]), 3)
        self.assertTrue(all(not check["exact_original_quotation"] for check in cross["final_quotation_checks"]))
        self.assertTrue(result["activity"]["configuration_passed"])
        self.assertFalse(result["activity"]["activity_conversation_executed"])
        self.assertFalse(result["activity"]["copilot_connection_executed"])
        self.assertTrue(result["cleanup"]["deleted"])
        self.assertTrue(result["cleanup"]["independent_group_absence"])


if __name__ == "__main__":
    unittest.main()
