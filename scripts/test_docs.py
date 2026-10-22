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

    def test_advanced_contract_inspection_does_not_claim_runtime_success(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "advanced-integration-contracts.json"
        contracts = json.loads(path.read_text(encoding="utf-8"))
        search = contracts["search_knowledge"]
        self.assertIn("Microsoft Entra ID Integrated", search["authentication_choices"])
        self.assertFalse(search["connection_runtime_verified_by_this_receipt"])
        byom = contracts["prompt_byom"]
        self.assertIn("API Key", byom["required_fields"])
        self.assertEqual(byom["authentication_selector_count"], 0)
        self.assertTrue(byom["conflicts_with_enforced_keyless_cognitive_policy"])
        self.assertTrue(byom["provisioning_for_key_only_path_held"])
        foundry = contracts["foundry_connected_agent"]
        self.assertTrue(foundry["activity_protocol_required_by_official_docs"])
        self.assertFalse(foundry["connection_runtime_verified_by_this_receipt"])
        self.assertEqual(contracts["connections_created_during_inspection"], 0)
        self.assertEqual(contracts["new_consents_granted"], 0)

    def test_search_popup_blocker_is_not_a_connected_runtime_pass(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-connected-attempt.json"
        attempt = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(attempt["status"], "blocked")
        self.assertEqual(attempt["cloud_readiness"]["vectorizer_smoke_queries"], 2)
        connection = attempt["connection_attempt"]
        self.assertIn("pop-up window has been blocked", connection["exact_error"])
        for key in ("actual_signin_or_consent_screen_opened", "new_consent_accepted",
                    "connection_created", "index_selection_reached",
                    "field_mapping_reached", "knowledge_source_saved"):
            self.assertFalse(connection[key])
        self.assertEqual(attempt["copilot_user_prompts_submitted"], 0)
        for key in ("licensing_positive", "licensing_unsupported_negative",
                    "hotel_positive", "hotel_unsupported_negative"):
            self.assertEqual(attempt[key], "not_run")
        self.assertFalse(attempt["copilot_retrieval_provenance_verified"])
        self.assertFalse(attempt["licensing_citation_navigation_verified"])
        self.assertFalse(attempt["browser_popup_security_modified"])
        self.assertFalse(attempt["user_available_for_popup_recovery_form"])
        readback = attempt["cleanup_ready_readback"]
        self.assertTrue(readback["saved_knowledge_empty_after_navigation"])
        self.assertTrue(readback["unsaved_wizard_discarded"])
        self.assertFalse(readback["endpoint_or_reference_retained_in_portal_visible_components"])
        self.assertFalse(attempt["cleanup_verified_by_this_receipt"])

    def test_keyless_search_cleanup_removes_only_owned_resources_and_roles(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-cleanup.json"
        cleanup = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(cleanup["remote_saved_connection_source_tool_absence_confirmed"])
        self.assertEqual(cleanup["exact_run_tagged_group_inventory_count"], 2)
        self.assertEqual(cleanup["deleted_owned_role_assignments_count"], 4)
        self.assertEqual(cleanup["role_assignment_get_http_statuses"], [404] * 4)
        for key in ("group_get_http_status", "account_get_http_status",
                    "search_get_http_status", "deployment_get_http_status"):
            self.assertEqual(cleanup[key], 404)
        self.assertFalse(cleanup["unrelated_principals_or_external_policy_destinations_modified"])
        self.assertFalse(cleanup["new_provisioning_or_data_queries"])
        self.assertTrue(cleanup["private_connection_handoff_removed"])
        self.assertTrue(cleanup["complete"])

    def test_formal_key_connection_preserves_real_runtime_failure(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-accesskey-execution.json"
        execution = json.loads(path.read_text(encoding="utf-8"))
        connection = execution["connection"]
        self.assertEqual(connection["actual_readback"], "Connected")
        self.assertFalse(connection["oauth_popup_required"])
        self.assertFalse(connection["new_consent_shown_or_accepted"])
        self.assertFalse(connection["manual_yaml_or_api_connection_writes"])
        self.assertTrue(execution["azure_authentication"]["cognitive_keyless_preserved"])
        runtime = execution["runtime"]
        self.assertEqual(runtime["submitted_user_prompts"], 4)
        self.assertEqual(runtime["licensing_negative"]["verdict"], "failed_abstention")
        self.assertTrue(runtime["licensing_positive"]["citation_target_matches_verified_publisher_pdf_and_page"])
        self.assertFalse(runtime["licensing_positive"]["browser_click_navigation_and_viewer_verified"])
        hotel = runtime["hotel_positive"]
        self.assertEqual(hotel["actual_answer_location"], hotel["actual_source_location"])
        self.assertTrue(hotel["source_grounding_passed"])
        self.assertTrue(hotel["fixture_source_mismatch"])
        self.assertFalse(hotel["city_criterion_satisfied"])
        self.assertFalse(execution["resources_deleted_by_this_receipt"])
        self.assertFalse(execution["full_workshop_certified"])

    def test_native_rework_keeps_generic_fallback_and_navigation_limits(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-portal-rework.json"
        rework = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(rework["authoring"]["all_three_instruction_paragraphs_persisted"])
        self.assertFalse(rework["authoring"]["pac_push"])
        self.assertFalse(rework["historical_cli_limitation"]["source_files_stripped_to_bypass_pack"])
        retests = rework["retests"]
        self.assertEqual(retests["submitted_user_prompts"], 3)
        self.assertEqual(retests["total_connected_questions_including_baseline"], 7)
        self.assertEqual(retests["original_negative"]["unsupported_claim_safety"], "passed")
        self.assertEqual(retests["original_negative"]["source_specific_absence_explanation"], "not_met")
        self.assertEqual(retests["distinct_negative"]["source_specific_absence_explanation"], "passed")
        self.assertTrue(retests["positive_regression"]["complete_audited_quote_matches"])
        self.assertFalse(retests["positive_regression"]["browser_viewer_navigation_verified"])
        self.assertFalse(rework["hotel_fixture"]["original_corpus_changed"])
        self.assertFalse(rework["baseline_failure_erased"])
        self.assertFalse(rework["resources_deleted_by_this_receipt"])
        self.assertFalse(rework["full_workshop_certified"])

    def test_source_aware_branch_preserves_positive_answer_and_failure_history(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-source-noanswer.json"
        final = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(final["authoring"]["persisted_branch_verified"])
        self.assertFalse(final["authoring"]["global_fallback_or_error_handling_edited"])
        self.assertTrue(final["authoring"]["nonempty_answer_path_and_citations_preserved"])
        retests = final["retests"]
        self.assertEqual(retests["submitted_user_prompts"], 2)
        self.assertEqual(retests["total_connected_search_questions_including_history"], 9)
        self.assertEqual(retests["original_negative"]["source_specific_absence_explanation"], "passed")
        self.assertEqual(retests["original_negative"]["citation_count"], 0)
        self.assertTrue(retests["positive_regression"]["single_final_answer"])
        self.assertEqual(retests["positive_regression"]["noanswer_message_occurrences"], 0)
        self.assertTrue(final["historical_failures_preserved"])
        self.assertFalse(final["full_workshop_certified"])

    def test_foundry_auth_failure_does_not_claim_activity_or_saved_connection(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-formal-auth.json"
        auth = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(auth["actual_arm_returned_project_endpoint_used"])
        self.assertTrue(auth["project_preparation"]["cognitive_keyless_and_network_security_preserved"])
        self.assertEqual(auth["formal_create_clicks"], 1)
        self.assertIn("pop-up window has been blocked", auth["exact_error"])
        self.assertFalse(auth["authentication_succeeded"])
        self.assertFalse(auth["new_consent_or_admin_permissions_accepted"])
        self.assertEqual(auth["saved_state"]["foundry_connection_rows"], 0)
        self.assertFalse(auth["saved_state"]["copilot_foundry_reference_created"])
        self.assertEqual(auth["model_or_agent_queries"], 0)
        self.assertFalse(auth["browser_security_modified"])
        self.assertFalse(auth["oauth_urls_or_tokens_extracted"])

    def test_final_remote_removal_preserves_revised_draft_and_other_connections(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-accesskey-removal.json"
        removal = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(removal["knowledge_absence_verified_after_navigation"])
        self.assertTrue(removal["agent_connection_permissions_empty"])
        self.assertTrue(removal["source_aware_blank_branch_preserved"])
        self.assertTrue(removal["nonempty_answer_path_preserved"])
        self.assertEqual(removal["formal_connection"]["owned_search_connection_matches"], 0)
        self.assertEqual(removal["formal_connection"]["foundry_connection_rows"], 0)
        self.assertTrue(removal["other_connections_unchanged"])
        self.assertFalse(removal["broad_external_access_cleared"])
        self.assertTrue(removal["cleanup_ready"])
        self.assertFalse(removal["cloud_deletion_verified_by_this_receipt"])

    def test_current_accesskey_cleanup_is_distinct_and_preserves_governance(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "search-accesskey-cleanup.json"
        cleanup = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(cleanup["complete"])
        self.assertEqual(cleanup["owned_child_projects"], 1)
        self.assertEqual(cleanup["owned_scoped_roles"], 1)
        self.assertEqual(set(cleanup["independent_get_http_statuses"]), {
            "project", "role", "group", "search", "account", "embedding"
        })
        self.assertTrue(all(status == 404 for status in cleanup["independent_get_http_statuses"].values()))
        self.assertTrue(cleanup["external_governance_destination_http200_before_and_after"])
        self.assertFalse(cleanup["unrelated_principals_groups_resources_modified"])
        self.assertTrue(cleanup["private_secret_handoff_removed"])
        self.assertTrue(cleanup["ephemeral_project_endpoint_handoff_removed"])

    def test_native_pdf_viewer_does_not_invent_original_clickthrough(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "native-pdf-viewer.json"
        viewer = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(viewer["browser_address_matches_verified_publisher_pdf_page3"])
        self.assertEqual(viewer["native_document_label"], "PDF document containing 30 pages")
        self.assertEqual(viewer["native_page_number"], 3)
        self.assertTrue(viewer["using_this_guide_heading_found"])
        self.assertTrue(viewer["complete_audited_sentence_found"])
        self.assertFalse(viewer["original_chat_citation_clickthrough_proven"])
        self.assertFalse(viewer["pdf_bytes_hash_recomputed_from_native_viewer"])
        self.assertFalse(viewer["screenshot_evidence_published"])
        self.assertFalse(viewer["browser_security_or_policy_changed"])

    def test_external_native_input_blocker_is_not_an_authentication_failure(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-external-native-auth.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "blocked_before_authentication_submission")
        self.assertTrue(result["external_power_apps_document_verified"])
        self.assertTrue(result["existing_sso_session_reached_connections"])
        self.assertEqual(result["authentication_type"], "Microsoft Entra ID User Login")
        self.assertFalse(result["project_endpoint_native_value_verified"])
        self.assertEqual(result["endpoint_field_length_at_readback"], 0)
        self.assertFalse(result["create_enabled_at_readback"])
        for key in ("create_invocations", "authentication_submissions", "new_models",
                    "new_agents", "new_roles", "new_inference_calls"):
            self.assertEqual(result[key], 0)
        for key in ("connection_created_by_automation", "authentication_rejection_observed",
                    "external_browser_popup_behavior_tested", "root_cause_established",
                    "browser_security_changed", "tokens_cookies_or_oauth_urls_extracted",
                    "unrelated_browser_tabs_inspected_or_altered", "overall_workshop_certified"):
            self.assertFalse(result[key])
        model = result["model_connector_inspection"]
        self.assertFalse(model["authentication_choices_verified"])
        self.assertFalse(model["native_prompt_byom_entra_support_established"])
        self.assertEqual(model["create_invocations"], 0)

    def test_external_foundry_cleanup_preserves_soft_delete_and_ui_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-external-auth-cleanup.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["complete"])
        self.assertEqual(result["actual_formal_authentication_submissions"], 0)
        self.assertTrue(result["final_saved_connection_list_absence_verified"])
        self.assertTrue(result["earlier_unverified_saved_list_disposition_superseded"])
        self.assertEqual(result["independent_get_http_statuses"],
                         {"project": 404, "account": 404, "group": 404})
        self.assertEqual(result["residual_live_owned_resources"], [])
        self.assertTrue(result["private_endpoint_handoff_removed"])
        self.assertEqual(result["external_governance_destination_http_status_before"], 200)
        self.assertEqual(result["external_governance_destination_http_status_after"], 200)
        self.assertFalse(result["external_governance_resources_modified"])
        self.assertFalse(result["unrelated_principals_groups_resources_modified"])
        self.assertEqual(result["soft_deleted_account_recovery_record_http_status"], 200)
        self.assertTrue(result["soft_deleted_account_recovery_record_retained"])
        self.assertFalse(result["soft_delete_purge_attempted"])
        self.assertFalse(result["power_apps_tab_closed"])

    def test_unreached_legacy_probe_does_not_claim_unsupported_input(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-native-input-prerequisite.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["status"], "blocked_before_legacy_input_probe")
        self.assertFalse(result["exact_window_foreground_guard_passed"])
        self.assertTrue(result["stopped_on_foreground_guard_failure"])
        self.assertFalse(result["endpoint_control_reached"])
        self.assertEqual(result["legacy_pattern_support"], "unverified")
        for key in ("legacy_setvalue_invocations", "create_invocations",
                    "authentication_submissions", "resources_provisioned"):
            self.assertEqual(result[key], 0)
        for key in ("public_probe_entered", "prior_endpoint_input_methods_retried",
                    "clipboard_access", "consent_granted", "browser_security_changed",
                    "unrelated_tabs_inspected_or_altered", "overall_workshop_certified"):
            self.assertFalse(result[key])
        self.assertTrue(result["fresh_unfiltered_native_connection_absence_verified"])

    def test_shared_browser_input_is_not_external_authentication_recovery(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-shared-browser-input.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(result["normal_keyboard_activation_opened_form"])
        self.assertTrue(result["probe_persisted_after_blur"])
        self.assertTrue(result["create_enabled_after_probe"])
        self.assertTrue(result["form_canceled_and_dialog_closed"])
        self.assertTrue(result["returned_to_saved_connections_page"])
        for key in ("create_invocations", "authentication_submissions", "resources_provisioned"):
            self.assertEqual(result[key], 0)
        for key in ("external_edge_input_recovery_proven",
                    "integrated_browser_popup_restriction_resolved", "consent_granted",
                    "browser_security_changed", "tokens_or_cookies_extracted",
                    "overall_workshop_certified"):
            self.assertFalse(result[key])

    def test_manual_connection_and_direct_smoke_do_not_imply_activity_success(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-manual-connection-runtime.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["manual_connection"]["status"], "Connected")
        self.assertFalse(result["manual_connection"]["consent_details_inferred"])
        runtime = result["owned_runtime"]
        self.assertEqual(runtime["lifecycle"], "live_held_for_connected_diagnosis")
        self.assertEqual(runtime["deployment_sku"], "Standard")
        self.assertEqual(runtime["deployment_capacity"], 1)
        self.assertTrue(runtime["keyless_preserved"])
        self.assertFalse(runtime["expiry_tag_is_automatic_cleanup"])
        self.assertEqual(runtime["new_role_grants"], 0)
        self.assertEqual(result["native_attachment"]["operation"], "SendActivityV2")
        self.assertTrue(result["native_attachment"]["saved_and_reopened"])
        self.assertFalse(result["initial_generic_prompt"]["passed"])
        self.assertFalse(result["corrective_topic"]["hardcoded_success_response"])
        native = result["corrective_native_test"]
        self.assertEqual(native["prompt_count"], 1)
        self.assertTrue(native["begin_dialog_trace_verified"])
        self.assertTrue(native["target_binding_trace_verified"])
        for key in ("downstream_dispatch_verified", "downstream_execution_verified",
                    "response_received", "platform_timeout_or_authentication_error_observed",
                    "runtime_passed"):
            self.assertFalse(native[key])
        direct = result["direct_responses_diagnostic"]
        self.assertTrue(direct["completed"])
        self.assertEqual(direct["attempts"], 1)
        self.assertEqual(direct["retries"], 0)
        self.assertEqual(direct["total_tokens"], direct["input_tokens"] + direct["output_tokens"])
        self.assertFalse(direct["activity_transport_verified"])
        self.assertFalse(direct["connector_identity_verified"])
        self.assertEqual(result["diagnosis"]["root_cause"], "unknown")
        self.assertFalse(result["diagnosis"]["speculative_fix_applied"])
        self.assertFalse(result["original_agents_modified"])
        self.assertFalse(result["overall_workshop_certified"])

    def test_connected_activity_success_does_not_erase_failures_or_certify_retrieval(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-connected-activity-success.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        native = result["instrumented_test"]
        self.assertEqual(native["prompt_count"], 1)
        self.assertTrue(native["begin_dialog_and_target_binding_verified"])
        self.assertTrue(native["reply_confirmed_visible"])
        self.assertTrue(native["connected_synthetic_smoke_passed"])
        self.assertFalse(native["parent_topic_hardcoded_success_response"])
        self.assertEqual(native["reply"],
                         "I am the workshop validation specialist. Foundry connection verified.")
        self.assertLess(native["reply_latency_seconds"], 90)
        self.assertFalse(result["server_correlation"]["earlier_candidate_definitively_joined_to_native_activity"])
        diagnostics = result["temporary_observability"]
        self.assertFalse(diagnostics["ingestion_verified"])
        self.assertFalse(diagnostics["logging_caused_runtime_recovery_proven"])
        self.assertEqual(diagnostics["workspace_get_after_cleanup"], 404)
        self.assertEqual(diagnostics["project_diagnostic_get_after_cleanup"], 404)
        self.assertTrue(diagnostics["account_policy_diagnostics_unchanged"])
        preflight = result["current_provenance_preflight"]
        self.assertEqual(preflight["checks_passed"], 117)
        self.assertEqual(preflight["new_retrieval_resources"], 0)
        self.assertFalse(preflight["distinct_supported_native_citation_repair_confirmed"])
        self.assertIsNone(preflight["original_inline_publisher_urls"])
        self.assertFalse(preflight["retrieval_acceptance_passed"])
        preservation = result["preservation"]
        self.assertTrue(preservation["earlier_native_no_reply_failure_retained"])
        self.assertTrue(preservation["account_project_model_agent_connection_retained"])
        self.assertFalse(preservation["overall_workshop_certified"])

    def test_original_lab_retrieval_keeps_rate_fix_separate_from_grounding(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs" / "assets" / "runtime-2026-10-20" / "foundry-original-lab-retrieval-validation.json"
        result = json.loads(path.read_text(encoding="utf-8"))
        original = result["primary_source_reconciliation"]
        self.assertTrue(original["accessible_notebook_requires_grounded_source_attribution"])
        self.assertFalse(original["native_annotation_arrays_explicitly_required"])
        self.assertFalse(original["publisher_urls_explicitly_required_for_synthetic_records"])
        self.assertFalse(original["main_protected_document_bypassed"])
        self.assertTrue(original["byom_custom_foundry_prompt_is_original_requirement"])
        self.assertEqual(result["owned_retrieval"]["exact_source_joins_verified"], 24)
        native = result["native_category_tests_before_capacity_fix"]
        self.assertEqual(native["submission_attempts"], 4)
        self.assertEqual(native["confirmed_native_user_messages"], 3)
        self.assertEqual(native["grounded_answer_passes"], 0)
        self.assertFalse(native["rate_limit_error_definitively_correlated_to_native_tests"])
        self.assertEqual(result["direct_rate_diagnostic"]["final_generation_error"],
                         "rate_limit_exceeded")
        capacity = result["capacity_fix"]
        self.assertEqual(capacity["new_capacity"], 26)
        self.assertGreaterEqual(capacity["new_tpm_verified"],
                                capacity["estimated_required_tokens_per_minute"])
        self.assertFalse(capacity["estimate_is_measured_usage"])
        self.assertFalse(capacity["provisioned_throughput_used"])
        for regression in result["direct_regressions"]:
            self.assertEqual(regression["attempts"], 1)
            self.assertEqual(regression["retries"], 0)
            self.assertTrue(regression["completed"])
            self.assertEqual(regression["total_tokens"],
                             regression["input_tokens"] + regression["output_tokens"])
            self.assertEqual(regression["exact_source_joins"], 24)
            self.assertFalse(regression["full_grounding_passed"])
        extractive = result["direct_regressions"][-1]
        self.assertEqual(extractive["displayed_extracts"],
                         extractive["unchanged_complete_source_sentences"])
        self.assertFalse(extractive["all_selected_material_relevant"])
        self.assertFalse(extractive["fabricated_record_ids_or_urls_present"])
        self.assertTrue(result["preservation"]["working_synthetic_smoke_agent_unchanged"])
        self.assertTrue(result["preservation"]["search_project_account_models_agents_connections_still_live"])
        self.assertFalse(result["preservation"]["overall_workshop_certified"])

    def test_model_comparison_preserves_failure_and_cleanup_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        filename = "foundry-model-comparison.json"
        path = root / "docs" / "assets" / "runtime-2026-10-20" / filename
        result = json.loads(path.read_text(encoding="utf-8"))
        initial = result["initial_request_validation"]
        self.assertEqual(initial["http_status"], 400)
        self.assertFalse(initial["completion_returned"])
        comparison = result["isolated_comparison"]
        self.assertEqual(comparison["changed_definition_fields"], ["model"])
        self.assertTrue(comparison["instructions_tools_temperature_and_prompt_unchanged"])
        self.assertEqual(comparison["inference_attempts"], 1)
        self.assertEqual(comparison["retries"], 0)
        self.assertTrue(comparison["completed"])
        self.assertEqual(comparison["total_tokens"],
                         comparison["input_tokens"] + comparison["output_tokens"])
        self.assertEqual(comparison["exact_original_source_joins"], 24)
        self.assertEqual(sum(comparison["source_counts"].values()), 24)
        self.assertTrue(comparison["displayed_record_source_locators_exist_and_match_actual_source"])
        self.assertFalse(comparison["semantic_grounding_passed"])
        self.assertEqual(len(comparison["failure_families"]), 3)
        self.assertFalse(comparison["connected_acceptance_passed"])
        self.assertFalse(comparison["failed_configuration_promoted_to_native_agent"])
        cleanup = result["cleanup"]
        self.assertEqual(cleanup["temporary_agent_get_after_delete"], 404)
        self.assertEqual(cleanup["temporary_deployment_get_after_delete"], 404)
        self.assertTrue(cleanup["both_temporary_resource_deletions_verified"])
        preservation = result["preservation"]
        self.assertTrue(preservation["existing_retrieval_and_smoke_agents_unchanged"])
        self.assertTrue(preservation["existing_search_project_models_and_agents_still_live"])
        self.assertEqual(preservation["security_policy_role_and_consent_changes"], 0)
        self.assertFalse(preservation["private_answers_and_source_excerpts_published"])
        self.assertFalse(preservation["overall_workshop_certified"])
        for language in ("en", "fr"):
            report = root / "docs" / language / "backend-live-2026-10-20.md"
            self.assertIn(filename, report.read_text(encoding="utf-8"))

    def test_source_provenance_recovery_does_not_certify_missing_native_cases(self):
        root = Path(__file__).resolve().parents[1]
        filename = "foundry-source-provenance-recovery.json"
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-20" / filename)
                            .read_text(encoding="utf-8"))
        repair = result["source_provenance_repair"]
        self.assertEqual(repair["original_records"], 24)
        self.assertTrue(repair["original_id_title_content_preserved"])
        self.assertTrue(repair["agent_model_instructions_tools_unchanged"])
        self.assertTrue(repair["provider_also_returns_original_title"])
        self.assertIn("title", repair["actual_mcp_record_fields"])
        self.assertEqual(repair["new_model_inferences_during_metadata_update"], 0)
        self.assertEqual(repair["embedding_calls_during_metadata_update"], 0)
        self.assertEqual(repair["new_resources_roles_policies"], 0)
        self.assertTrue(repair["completed_first_regression_response_recovered_without_new_inference"])
        questions = result["original_notebook_questions"]
        self.assertTrue(questions["questions_unchanged"])
        self.assertTrue(questions["extractive_adaptation"])
        self.assertEqual(questions["baseline"]["content_and_canonical_source_attribution_passes"], 2)
        after = questions["after_metadata_repair"]
        self.assertEqual(after["content_and_canonical_source_attribution_passes"], 4)
        self.assertEqual(after["actual_original_record_joins"], [19, 14, 18, 24])
        for run in (questions["baseline"], after):
            self.assertEqual(run["attempts"], 4)
            self.assertEqual(run["retries"], 0)
            self.assertEqual(sum(run["response_tokens_by_case"]), run["response_tokens_total"])
        self.assertFalse(after["native_conversations"])
        native = result["focused_native_procedure"]
        self.assertTrue(native["real_domain_reply_received"])
        self.assertTrue(native["source_attribution_relevance_and_material_conditions_passed"])
        self.assertGreater(native["reply_latency_seconds"], 350)
        self.assertFalse(native["sdk_proxy_used_to_fill_native_evidence_gap"])
        self.assertFalse(native["native_tool_trace_independently_joined"])
        batch = result["native_original_category_batch"]
        self.assertFalse(batch["current_user_message_delivery_confirmed"])
        self.assertFalse(batch["reaching_case_two_treated_as_case_one_pass"])
        self.assertFalse(batch["full_native_matrix_certified"])
        self.assertEqual(batch["resubmissions_during_recovery"], 0)
        quick_reference = result["native_quick_reference_ingestion"]
        self.assertTrue(quick_reference["upload_accepted"])
        self.assertEqual(quick_reference["observed_status_sequence"], ["In progress", "Error"])
        self.assertEqual(quick_reference["upload_attempts"], 1)
        self.assertEqual(quick_reference["reuploads"], 0)
        self.assertFalse(quick_reference["ready_or_searchable_verified"])
        self.assertFalse(quick_reference["protection_removed_or_contents_reconstructed"])
        self.assertFalse(quick_reference["encryption_established_as_root_cause"])
        self.assertFalse(result["remaining_boundaries"]["original_native_prompt_byom_completed"])
        self.assertFalse(result["preservation"]["overall_workshop_certified"])
        self.assertFalse(result["preservation"][
            "private_answers_source_passages_or_authenticated_lookup_urls_published"])
        for language in ("en", "fr"):
            report = root / "docs" / language / "backend-live-2026-10-20.md"
            self.assertIn(filename, report.read_text(encoding="utf-8"))

    def test_native_category_recovery_preserves_retry_and_source_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        filename = "foundry-native-category-recovery.json"
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-20" / filename)
                            .read_text(encoding="utf-8"))
        before = result["native_version_3_recovery"]
        self.assertEqual(before["actual_native_replies"], 4)
        self.assertEqual(before["displayed_content_and_individual_attribution_passes"], 3)
        self.assertEqual(before["first_fraud_answer_uncited_excerpts"], 2)
        after = result["targeted_version_4_correction"]
        self.assertEqual(after["changed_fields"], ["definition.instructions"])
        self.assertEqual(after["native_expertise_submissions"], 5)
        self.assertEqual(after["bounded_combined_transport_reattempts"], 1)
        self.assertEqual(after["displayed_content_and_individual_attribution_passes"], 4)
        self.assertEqual(sum(case["authentic_correctly_attributed_excerpts"]
                             for case in after["cases"]), 13)
        self.assertTrue(all(0 < case["latency_seconds"] < 30 for case in after["cases"]))
        self.assertFalse(after["unacknowledged_submission_proves_backend_absence"])
        self.assertFalse(after["native_mcp_trace_independently_joined"])
        self.assertTrue(after["original_corpus_match_not_called_native_retrieval_membership"])
        guide = result["licensed_publisher_reference"]
        self.assertEqual(guide["exact_original_record_id_title_content_matches"], 24)
        self.assertEqual(guide["exact_original_full_test_question_matches"], 4)
        self.assertEqual(guide["native_status"], "Ready")
        self.assertEqual(guide["native_upload_attempts"], 1)
        self.assertTrue(guide["publisher_provenance_and_complete_mit_notice_appended"])
        self.assertFalse(guide["equivalence_to_unreadable_docx_claimed"])
        self.assertFalse(guide["protected_docx_converted_decrypted_or_reconstructed"])
        canary = result["natural_routing_canary"]
        self.assertTrue(canary["actual_uploaded_source_id_in_native_search_trace"])
        self.assertTrue(canary["native_reply_citation_identifies_uploaded_filename"])
        self.assertTrue(canary["greeting_also_searched_local_knowledge"])
        self.assertFalse(canary["pure_no_knowledge_greeting_demonstrated_by_this_canary"])
        self.assertFalse(canary["foundry_invocation_observed"])
        self.assertFalse(canary["expanded_eleven_scenarios_replaced_by_canary"])
        self.assertFalse(result["preservation"]["overall_workshop_certified"])
        self.assertFalse(result["preservation"][
            "private_passages_answers_and_authenticated_lookup_urls_published"])
        for language in ("en", "fr"):
            self.assertIn(filename, (root / "docs" / language / "backend-live-2026-10-20.md")
                          .read_text(encoding="utf-8"))

    def test_expanded_matrix_failure_is_not_erased_by_focused_rework(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-20"
        matrix_name = "foundry-native-natural-matrix.json"
        matrix = json.loads((assets / matrix_name).read_text(encoding="utf-8"))
        source = matrix["sourceVerification"]
        self.assertEqual(source["originalScenarioQuestionsChecked"], 11)
        self.assertEqual(source["originalScenarioQuestionsMatched"], 11)
        execution = matrix["execution"]
        self.assertEqual(execution["targetSubmissions"], 3)
        self.assertEqual(execution["replays"], 0)
        self.assertEqual(execution["unsubmittedScenarios"], 8)
        self.assertFalse(execution["backendAbsenceConclusion"])
        self.assertEqual([case["result"] for case in matrix["cases"][:2]],
                         ["fail", "partial"])
        self.assertFalse(matrix["claims"]["fullMatrixExecuted"])
        self.assertFalse(matrix["claims"]["workshopCertified"])
        self.assertTrue(all(not value for value in matrix["publicationSafety"].values()))
        rework_name = "foundry-native-intake-rework.json"
        rework = json.loads((assets / rework_name).read_text(encoding="utf-8"))
        self.assertEqual(rework["changes"]["parent_instructions_current_characters"], 2622)
        focused = rework["focused_native_regression"]
        self.assertEqual(focused["submissions"], 3)
        self.assertEqual(focused["server_acknowledged_final_replies"], 3)
        self.assertEqual(focused["replays"], 0)
        self.assertFalse(focused["cases"][0]["specific_registered_intake_topic_execution_established"])
        self.assertFalse(focused["cases"][0]["local_search_event_observed"])
        self.assertTrue(all(case["actual_uploaded_source_id_in_native_search_trace"]
                            for case in focused["cases"][1:]))
        self.assertFalse(focused["expanded_eleven_scenarios_replaced_by_focused_regression"])
        self.assertFalse(rework["preservation"]["overall_workshop_certified"])
        self.assertFalse(rework["external_browser"]["external_test_result_obtained"])
        retest_name = "foundry-native-natural-matrix-rework.json"
        retest = json.loads((assets / retest_name).read_text(encoding="utf-8"))
        self.assertEqual(retest["counts"]["preflightSubmissions"], 1)
        self.assertEqual(retest["counts"]["targetSubmissions"], 0)
        self.assertEqual(retest["counts"]["targetReplays"], 0)
        self.assertEqual(retest["counts"]["notRunTargets"], 11)
        self.assertFalse(retest["stop"]["backendAbsenceConclusion"])
        self.assertFalse(retest["claims"]["acceptanceGatePassed"])
        self.assertFalse(retest["claims"]["targetedReworkValidatedByThisRound"])
        self.assertTrue(all(case["result"] == "not_run" for case in retest["cases"]))
        self.assertTrue(all(case["localSearchAttemptObserved"] is None
                            for case in retest["cases"]))
        self.assertTrue(all(not value for value in retest["publicationSafety"].values()))
        for language in ("en", "fr"):
            text = (root / "docs" / language / "backend-live-2026-10-20.md").read_text("utf-8")
            self.assertIn(matrix_name, text)
            self.assertIn(rework_name, text)
            self.assertIn(retest_name, text)

    def test_native_persistence_recovery_does_not_rewrite_earlier_evidence(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-20"
        old = json.loads((assets / "foundry-native-intake-rework.json").read_text("utf-8"))
        self.assertFalse(old["changes"]["nonfactual_guarded_intake_topic_yaml_persistence_initially_established"])
        self.assertTrue(old["changes"]["earlier_yaml_persistence_claim_retracted_after_native_readback"])
        self.assertFalse(old["changes"]["topic_yaml_readback_performed_during_initial_rework"])
        filename = "foundry-native-persistence-recovery.json"
        receipt = json.loads((assets / filename).read_text("utf-8"))
        repair = receipt["persistence_repair"]
        self.assertTrue(repair["initial_topic_readback_was_empty_on_recognized_intent"])
        self.assertTrue(repair["normal_line_by_line_keyboard_editing_used"])
        self.assertFalse(repair["dom_or_monaco_model_mutation_used"])
        self.assertEqual(repair["parse_errors"], 0)
        self.assertTrue(repair["topic_enabled"])
        self.assertEqual(repair["offline_guard_and_readback_tests_passed"], 5)
        self.assertTrue(receipt["native_recovery_preflight"]["native_topic_and_action_trace_observed"])
        self.assertTrue(receipt["original_intake_scenario"]["registered_intake_execution_proven"])
        workflow = receipt["verified_delivery_workflow"]
        self.assertTrue(workflow["immediate_post_persistence_hello_also_failed"])
        self.assertFalse(workflow["sole_causal_attribution_to_delay_or_send_button"])
        self.assertFalse(workflow["external_browser_test_result_obtained"])
        routing = receipt["routing_clarification"]
        self.assertEqual(routing["saved_parent_instruction_characters"], 3005)
        self.assertFalse(routing["financial_answers_hardcoded"])
        boundary = receipt["capture_boundary"]
        self.assertTrue(boundary["child_stream_final_is_not_parent_completion"])
        self.assertTrue(boundary["dynamic_plan_finished_required_for_generative_turns"])
        self.assertTrue(boundary["absence_of_source_id_in_narrow_trace_not_called_retrieval_absence"])
        self.assertFalse(receipt["preservation"]["overall_workshop_certified"])
        self.assertFalse(receipt["preservation"]["native_mcp_membership_or_version_join_claimed"])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "backend-live-2026-10-20.md").read_text("utf-8")
            self.assertIn(filename, text)
            self.assertIn("DynamicPlanFinished", text)

    def test_complete_native_turns_do_not_certify_failed_quotation_or_example_gates(self):
        root = Path(__file__).resolve().parents[1]
        filename = "foundry-native-matrix-completion-recovery.json"
        path = root / "docs" / "assets" / "runtime-2026-10-20" / filename
        receipt = json.loads(path.read_text("utf-8"))
        self.assertEqual(receipt["current_parent_instruction_characters"], 3005)
        self.assertEqual(receipt["complete_native_turns"], 11)
        self.assertEqual(receipt["original_exact_question_matches"], 11)
        self.assertEqual([row["scenario"] for row in receipt["cases"]], list(range(1, 12)))
        for row in receipt["cases"]:
            number = row["scenario"]
            self.assertTrue(row["completed_native_turn"])
            self.assertTrue(row["original_question_exact_match"])
            self.assertIn(row["reply_activity_id"], row["displayed_response_activity_ids"])
            self.assertFalse(row["native_mcp_membership_or_version_join_claimed"])
            self.assertTrue(row["quoted_block_audit_covers_all_displayed_messages"])
            self.assertEqual(row["knowledge_search_event_observed"],
                             number in (2, 3, 4, 8, 9, 10, 11))
            self.assertEqual(row["foundry_step_triggered"], number >= 5)
            self.assertEqual(row["foundry_step_finished"], number >= 5)
            if number == 1:
                self.assertTrue(row["direct_intake_topic_action_proven"])
            else:
                self.assertTrue(row["whole_generative_plan_finished"])
            if number >= 8:
                self.assertTrue(row["displayed_response_local_filename_citation"])
                self.assertEqual(row["original_example_content_review"], "partial_or_unconfirmed")
        self.assertEqual(receipt["quoted_block_count"], 67)
        self.assertEqual(receipt["nonliteral_quoted_block_count"], 4)
        self.assertEqual(receipt["blocks_without_correct_individual_marker"], 20)
        self.assertFalse(receipt["all_audited_blocks_authentic"])
        self.assertFalse(receipt["all_audited_blocks_individually_attributed"])
        counts = receipt["execution_accounting"]
        self.assertEqual(counts["total_targets_since_r3_including_control_flow_inferred_r4"], 32)
        self.assertEqual(counts["reexecuted_targets_after_r3"], 21)
        self.assertTrue(counts["r4_deferred_batch_handle_expired"])
        self.assertEqual(counts["r4_individual_case_metadata_recovered"], [7])
        self.assertTrue(counts["r4_seven_earlier_answer_bodies_not_recovered"])
        self.assertEqual(counts["within_round_target_retries"], 0)
        rollback = receipt["discarded_incident_rework"]
        self.assertTrue(rollback["unsupported_exact_aggregate_total_invented"])
        self.assertTrue(rollback["change_not_promoted"])
        self.assertTrue(rollback["prior_3005_character_configuration_restored"])
        self.assertTrue(rollback["post_rollback_canary_did_not_invent_a_deposit_count_or_total"])
        claims = receipt["acceptance_boundary"]
        self.assertTrue(claims["all_eleven_expected_handler_routes_observed"])
        self.assertFalse(claims["full_matrix_acceptance_passed"])
        self.assertFalse(claims["all_original_expected_response_items_certified"])
        self.assertFalse(claims["original_native_prompt_byom_completed"])
        self.assertFalse(claims["overall_workshop_certified"])
        self.assertTrue(all(not value for value in receipt["publication_safety"].values()))
        for language in ("en", "fr"):
            text = (root / "docs" / language / "backend-live-2026-10-20.md").read_text("utf-8")
            self.assertIn(filename, text)

    def test_verified_extension_does_not_promote_backend_proof_to_native_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        filename = "foundry-verified-extension.json"
        receipt = json.loads((root / "docs/assets/runtime-2026-10-20" / filename).read_text("utf-8"))
        self.assertFalse(receipt["overall_workshop_certified"])
        self.assertEqual(receipt["implementation"]["unit_tests_passed"], 30)
        self.assertFalse(receipt["implementation"]["native_verified_evidence_delivery_passed"])
        cases = receipt["backend_cases"]
        self.assertEqual([case["original_case"] for case in cases], [6, 8, 9, 11])
        self.assertEqual(sum(case["literal_individually_attributed_quotes"] for case in cases), 12)
        self.assertTrue(all(not case["native_delivery_claimed"] for case in cases))
        native = receipt["native_diagnostic"]
        self.assertEqual(native["http_status"], 403)
        self.assertFalse(native["acceptance_passed"])
        self.assertFalse(native["verified_pipeline_execution_claimed"])
        self.assertFalse(receipt["existing_route_control"]["whole_plan_completion_observed"])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "backend-live-2026-10-20.md").read_text("utf-8")
            self.assertIn(filename, text)

    def test_verified_extension_preserves_unapproved_authentication_and_readback_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "docs/assets/runtime-2026-10-20/foundry-verified-extension.json")
                             .read_text("utf-8"))
        preservation = receipt["preservation"]
        for key in ("endpoint_authorization_approval_obtained", "endpoint_authorization_changed",
                    "additional_manual_role_or_consent_changes_during_auth_diagnosis",
                    "original_parent_instructions_changed",
                    "existing_retrieval_version_changed",
                    "diagnostic_disabled_persistence_independently_verified"):
            self.assertFalse(preservation[key])
        self.assertTrue(preservation["diagnostic_disabled_observed_in_ui"])
        self.assertTrue(preservation["new_azure_bot_resource_created"])
        self.assertTrue(preservation["new_resources_remain_live_and_billable"])

    def test_verified_extension_sdk_recovery_preserves_hosted_and_native_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "docs/assets/runtime-2026-10-20/foundry-verified-extension.json")
                             .read_text("utf-8"))
        recovery = receipt["followup_recovery"]
        state = recovery["diagnostic_saved_state"]
        self.assertTrue(state["independently_verified"])
        self.assertTrue(state["parent_bot_binding_verified"])
        self.assertEqual((state["statecode"], state["statuscode"], state["state_label"]),
                         (1, 2, "Inactive"))
        direct = recovery["authenticated_direct_activity"]
        self.assertEqual(direct["http_status"], 500)
        self.assertTrue(direct["hosted_session_observed"])
        self.assertTrue(direct["caller_metadata_matches_acquired_entra_token"])
        self.assertFalse(direct["copilot_studio_native"])
        self.assertFalse(direct["pipeline_execution_claimed"])
        repair = recovery["local_sdk_repair"]
        self.assertEqual(repair["unit_tests_passed"], 33)
        self.assertEqual(repair["tested_activity_version"], "1.0.0b4")
        self.assertEqual(repair["pinned_microsoft_agents_version"], "1.9.0")
        self.assertEqual(repair["real_entry_point_and_adapter_asgi_tests_passed"], 2)
        for key in ("real_hosted_identity_regression_passed", "transport_evidence_unchanged",
                    "transport_validation_failure_explicit", "complete_activity_requires_service_url"):
            self.assertTrue(repair[key])
        for key in ("vendor_source_modified", "redeployed", "hosted_repair_retested",
                    "downstream_hosted_permissions_certified", "native_403_resolved"):
            self.assertFalse(repair[key])
        self.assertFalse(recovery["endpoint_authorization_changed"])
        self.assertFalse(recovery["additional_manual_role_or_consent_changes"])

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
