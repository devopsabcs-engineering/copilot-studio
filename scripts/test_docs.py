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

    def test_new_pdf_answer_audit_preserves_citation_boundary(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "pdf-answer-audit.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["passed"], 5)
        self.assertEqual(result["failed"], 0)
        self.assertEqual(result["passed"], sum(result["checks"].values()))
        self.assertEqual(result["source_bytes"], 867776)
        self.assertEqual(result["quotation_found_on_physical_pages"], [3])
        self.assertTrue(result["checks"]["edition_matches_page_3"])
        self.assertFalse(result["citation_click_target_or_page_anchor_verified"])
        self.assertFalse(result["historical_full_answer_audited"])
        self.assertFalse(result["current_remote_file_bytes_retrieved_during_this_audit"])
        self.assertFalse(result["overall_workshop_certified"])

    def test_approved_evaluation_does_not_claim_unobserved_grades(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "evaluation-results.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["testSet"]["persisted"])
        self.assertEqual(result["testSet"]["grader"], "General quality")
        self.assertEqual(result["testSet"]["testCaseCount"], 3)
        self.assertEqual(len(result["cases"]), 3)
        self.assertTrue(result["run"]["submitted"])
        self.assertEqual(result["run"]["totalRuns"], 1)
        self.assertFalse(result["run"]["duplicateRunCreated"])
        self.assertFalse(result["run"]["completed"])
        self.assertIsNone(result["run"]["score"])
        self.assertIsNone(result["run"]["creditsUsed"])
        for case in result["cases"]:
            self.assertIsNone(case["actualResponse"])
            self.assertIsNone(case["score"])
        follow_up = result["boundedFollowUp"]
        self.assertEqual(follow_up["navigationRecoveryAttempts"], 2)
        self.assertEqual(follow_up["newRunsSubmitted"], 0)
        self.assertFalse(follow_up["completedRunClaimed"])
        self.assertFalse(result["citationNavigationFollowUp"]["pageAnchorVerified"])
        self.assertFalse(result["workshopComplete"])
        final_path = path.with_name("evaluation-final-recheck.json")
        final = json.loads(final_path.read_text(encoding="utf-8"))
        self.assertEqual(final["supportedNavigationAttempts"], 1)
        self.assertEqual(final["newRunsSubmitted"], 0)
        self.assertIsNone(final["newScores"])
        self.assertIsNone(final["newCreditTotals"])
        self.assertFalse(final["workshopComplete"])

    def test_foundry_quote_recovery_keeps_failed_citation_gate(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-quote-recovery.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["quotation_acceptance_passed"])
        self.assertFalse(result["citation_output_acceptance_passed"])
        self.assertFalse(result["passed"])
        attribution = result["independent_verification"]["source_attribution"]
        self.assertEqual(len(attribution), 2)
        for run in attribution:
            self.assertTrue(run["original_and_tool_source_attribution_passed"])
            self.assertEqual(len(run["source_checks"]), 3)
            for check in run["source_checks"]:
                self.assertTrue(check["exact_original"])
                self.assertTrue(check["exact_actual_tool_content"])
                self.assertTrue(check["owned_search_index_document_url_matches"])
                self.assertTrue(check["citation_whitespace_only"])
        verification = result["independent_verification"]
        self.assertEqual(verification["unsupported_actual_tool_documents"], 7)
        self.assertFalse(verification["unsupported_zero_documents_verified"])
        self.assertTrue(verification["unsupported_model_abstention_passed"])
        cleanup = verification["group_and_resource_absence"]
        self.assertEqual(len(cleanup), 4)
        for attempt in cleanup:
            self.assertTrue(attempt["group_absent"])
            self.assertTrue(attempt["only_manifest_owned_resources_deleted"])
            self.assertEqual(attempt["resource_get_status"], {"account": 404, "search": 404})
        self.assertTrue(result["all_new_owned_resources_absent"])
        self.assertFalse(result["production_or_user_agent_modified"])
        self.assertFalse(result["copilot_or_activity_executed"])

    def test_portal_setup_error_does_not_override_backend_reads(self):
        root = Path(__file__).resolve().parents[1]
        evidence = root / "docs" / "assets" / "runtime-2026-10-20"
        portal = json.loads((evidence / "evaluation-restored-tab.json").read_text(encoding="utf-8"))
        self.assertTrue(portal["initialInspection"]["newUserSharedTabInspectedBeforeNavigation"])
        self.assertEqual(portal["evaluation"]["newRunsSubmitted"], 0)
        self.assertIsNone(portal["evaluation"]["newCreditUsage"])
        backend = json.loads((evidence / "evaluation-backend-diagnosis.json").read_text(encoding="utf-8"))
        self.assertEqual(len(backend["checks"]), 3)
        self.assertTrue(all(check["httpStatus"] == 200 for check in backend["checks"]))
        self.assertTrue(backend["checks"][0]["matchesSuppliedPortalEnvironment"])
        self.assertEqual(backend["checks"][0]["provisioningState"], "Succeeded")
        self.assertTrue(backend["checks"][2]["matchesSuppliedPortalAgent"])
        self.assertEqual(backend["safety"]["httpMethods"], ["GET"])
        self.assertFalse(backend["safety"]["provisioningOrAgentChanges"])
        self.assertFalse(backend["safety"]["permissionConsentOrIdentityChanges"])

    def test_offline_contract_diagnosis_does_not_invent_native_citations(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-citation-contract.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["diagnosis_completed"])
        self.assertEqual(result["local_checks"]["passed"], 45)
        self.assertEqual(result["local_checks"]["failed"], 0)
        self.assertTrue(result["contract"]["native_annotations_documented"])
        self.assertFalse(result["contract"]["strict_json_native_marker_inner_title_binding_documented"])
        self.assertEqual(result["contract"]["annotations_in_captured_cross_source_responses"], 0)
        self.assertEqual(sum(case["blank_citation_fields"] for case in result["cases"]), 6)
        self.assertEqual(result["live_native_citation_acceptance"], "failed_unrecovered")

    def test_supported_format_retest_keeps_url_and_annotation_failures(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-supported-citation-retest.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertFalse(result["passed"])
        self.assertTrue(result["configuration"]["old_json_native_title_regex_not_applied"])
        replay = result["independent_actual_payload_replay"]
        self.assertEqual(replay["cross_source_final_answers"], 1)
        self.assertEqual(replay["unsupported_final_answers"], 1)
        self.assertEqual(replay["actual_native_annotation_count"], 0)
        self.assertEqual(replay["actual_tool_url_matches"], 0)
        self.assertEqual(len(replay["source_checks"]), 3)
        for source in replay["source_checks"]:
            self.assertTrue(source["original_title_and_id_passed"])
            self.assertTrue(source["quote_sentence_exact_before_markdown_hard_break"])
            self.assertFalse(source["strict_entire_blockquote_line_equal"])
            self.assertFalse(source["actual_tool_url_in_source_section"])
            self.assertFalse(source["native_annotation_association"])
        environments = result["new_environment_independent_absence"] + result["prior_environments_absent_after"]
        self.assertEqual(len(environments), 5)
        for environment in environments:
            self.assertTrue(environment["group_absent"])
            self.assertEqual(environment["resource_get_status"], {"account": 404, "search": 404})
        self.assertFalse(result["production_or_user_agent_modified"])
        self.assertFalse(result["copilot_or_activity_executed"])

    def test_completed_evaluation_preserves_real_failures_and_usage(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "evaluation-completed.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["existing_run_only"])
        self.assertFalse(result["new_run_submitted"])
        self.assertEqual(result["credits_used_displayed"], 7)
        self.assertEqual(result["duration"], "00:02:44")
        self.assertEqual(result["total_cases"], 3)
        self.assertEqual(result["passed"], 1)
        self.assertEqual(result["failed"], 2)
        self.assertEqual(sum(case["grade"] == "Pass" for case in result["cases"]), 1)
        self.assertEqual(sum(case["grade"] == "Fail" for case in result["cases"]), 2)

    def test_real_agent_telemetry_is_not_synthetic_ingestion(self):
        root = Path(__file__).resolve().parents[1]
        folder = root / "docs" / "assets" / "runtime-2026-10-20"
        execution = json.loads((folder / "agent-telemetry-execution.json").read_text(encoding="utf-8"))
        event = json.loads((folder / "agent-telemetry-event.json").read_text(encoding="utf-8"))
        self.assertEqual(execution["official_push_changes"], 1)
        self.assertEqual(execution["operator_prompt_submissions"], 1)
        self.assertEqual(execution["event_node"], "LogCustomTelemetryEvent")
        settings = execution["privacy_settings_verified_by_persisted_ui_readback"]
        self.assertTrue(settings["enable_logging"])
        for key in ("conversation_details", "sensitive_properties", "node_execution_events"):
            self.assertFalse(settings[key])
        self.assertTrue(event["agent_event_found"])
        self.assertEqual(event["matching_rows"], 1)
        self.assertTrue(event["exact_property_shape_verified"])
        self.assertEqual(event["expected_correlation"], execution["synthetic_properties"]["RunCorrelationId"])
        self.assertFalse(execution["synthetic_emitter_used"])
        self.assertTrue(event["no_synthetic_emitter_executed"])
        self.assertFalse(execution["agent_published"])

    def test_trial_and_disconnect_do_not_imply_full_integration_or_cleanup(self):
        root = Path(__file__).resolve().parents[1]
        folder = root / "docs" / "assets" / "runtime-2026-10-20"
        trial = json.loads((folder / "trial-extension.json").read_text(encoding="utf-8"))
        self.assertTrue(trial["explicit_user_approval_received"])
        self.assertTrue(trial["generative_settings_restored"])
        for key in ("expiry_date_verified", "recurring_purchase",
                    "new_environment_or_database", "unrelated_consent_or_admin_grants",
                    "bing_or_web_search_activated", "original_agents_changed",
                    "knowledge_tools_agents_auth_contracts_verified_by_this_receipt"):
            self.assertFalse(trial[key])
        disconnected = json.loads((folder / "agent-telemetry-disconnection.json").read_text(encoding="utf-8"))
        self.assertTrue(disconnected["persisted_connection_absent"])
        self.assertFalse(disconnected["persisted_enable_logging"])
        self.assertTrue(all(value is False for value in disconnected["privacy_flags"].values()))
        self.assertEqual(disconnected["additional_user_prompts"], 0)
        self.assertFalse(disconnected["resource_cleanup_verified_by_this_receipt"])

    def test_agent_monitoring_cleanup_preserves_shared_resources(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "agent-telemetry-cleanup.json"
        cleanup = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(cleanup["remote_connection_absent_and_logging_off_verified"])
        self.assertTrue(cleanup["ancillary_alert_single_owned_component_scope_verified"])
        self.assertEqual(cleanup["exact_allowlist_inventory_count"], 3)
        for key in ("group_get_http_status", "component_get_http_status",
                    "workspace_get_http_status", "ancillary_alert_get_http_status"):
            self.assertEqual(cleanup[key], 404)
        self.assertTrue(cleanup["shared_action_groups_before_http200"])
        self.assertTrue(cleanup["shared_action_groups_after_http200"])
        self.assertFalse(cleanup["external_resources_mutated"])
        self.assertTrue(cleanup["secret_handoff_removed"])
        self.assertTrue(cleanup["complete"])

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
