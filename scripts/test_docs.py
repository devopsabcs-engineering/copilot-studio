"""Offline regression tests for documentation export and link validation."""
from datetime import datetime
from pathlib import Path
import json
import tempfile
import unittest

from build_wiki import export, page_name, render_wiki_metadata, rewrite_links
from check_revocation_readiness import assess_readiness
from validate_docs import local_link_errors, validate


class WikiTests(unittest.TestCase):
    def test_lab6_crosswalk_preserves_exact_scope_provenance_and_privacy(self):
        root = Path(__file__).resolve().parents[1]
        path = root / "docs/assets/runtime-2026-10-26/lab6-acceptance-crosswalk.json"
        raw = path.read_text("utf-8")
        receipt = json.loads(raw)
        self.assertNotRegex(raw, r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
        for private_marker in (".copilot-tracking", "C:\\", "OneDrive",
                               "conversation_id", "tenant_id", "client_secret",
                               "access_token", "captureQuestion", "upstream.txt"):
            self.assertNotIn(private_marker, raw)
        self.assertTrue(raw.endswith("\n"))
        self.assertEqual(receipt["reconciledDate"], "2026-10-26")
        self.assertTrue(receipt["documentaryCrosswalkDelivered"])
        self.assertFalse(receipt["T017RuntimeComplete"])
        self.assertFalse(receipt["workshopComplete"])
        self.assertEqual((receipt["newQuestions"], receipt["liveLabAttempts"]), (0, 0))
        boundary = receipt["sourceBoundary"]
        self.assertEqual(boundary["additionalProtectedMainRequirements"], "UNKNOWN")
        for key in ("protectedMainOpenedBypassedOrReconstructed",
                    "guideVariantsAreUniversalOriginalGates",
                    "nativeAnnotationsPublisherUrlsAndVerbatimQuotesAreUniversalOriginalGates"):
            self.assertFalse(boundary[key])
        self.assertTrue(boundary["historicalQuotationFailuresAndPassesPreserved"])
        expected = ["PASS"] * 3 + ["NOT_RUN"] * 2 + ["PARTIAL"] * 3 + ["NOT_RUN"] * 3 + ["PARTIAL"]
        rows = receipt["rows"]
        self.assertEqual([row["id"] for row in rows],
                         [f"F6-{number:02}" for number in range(1, 13)])
        self.assertEqual(len({row["id"] for row in rows}), 12)
        self.assertEqual([row.get("initialOfflineStatus", row["status"]) for row in rows], expected)
        self.assertEqual([row["status"] for row in rows],
                         ["PASS"] * 5 + ["PARTIAL", "PASS", "PASS", "FAIL", "NOT_RUN", "NOT_RUN", "PARTIAL"])
        initial = receipt["initialOfflineCheckpoint"]
        self.assertEqual((initial["newQuestions"], initial["liveLabAttempts"]), (0, 0))
        self.assertTrue(initial["topLevelZeroCountsDescribeOnlyThisInitialOfflineCheckpoint"])
        self.assertEqual(initial["statusCounts"], {"PASS": 3, "PARTIAL": 4, "NOT_RUN": 5})
        for row in rows[3:5]:
            self.assertTrue(row["initialOfflineAssessment"])
        added = {"F6-01", "F6-03", "F6-08", "F6-09", "F6-10", "F6-11"}
        for row in rows:
            self.assertEqual(row["sourceProvenance"],
                             "guide_added_validation" if row["id"] in added
                             else "workshop_source_backed")
            self.assertTrue(row["sourceAssessment"])
            self.assertTrue(row["evidenceBoundary"])
            self.assertIsInstance(row["exactEvidence"], list)
            self.assertIsInstance(row["relatedEvidence"], list)
        self.assertIn("not a runtime pass", receipt["statusDefinitions"]["PASS"])
        for row in rows[9:11]:
            self.assertEqual(row["exactEvidence"], [])
            self.assertTrue(row["relatedEvidence"])
        for index in (5, 6, 8):
            self.assertTrue(rows[index]["exactEvidence"])
        self.assertIn("setup explicitly includes", rows[4]["sourceAssessment"])
        self.assertIn("Lab 5 Search denial is not Lab 6 Foundry denial", rows[9]["evidenceBoundary"])
        self.assertIn("missing-protocol", rows[10]["evidenceBoundary"])
        self.assertIn("version 5 remains retained", rows[11]["evidenceBoundary"])

        def check_references(value):
            if isinstance(value, dict):
                for item in value.values():
                    check_references(item)
            elif isinstance(value, list):
                for item in value:
                    check_references(item)
            elif isinstance(value, str) and value.startswith("docs/"):
                filename, _, pointer = value.partition("#")
                target = root / filename
                self.assertTrue(target.is_file(), value)
                if target.suffix == ".json" and pointer:
                    current = json.loads(target.read_text("utf-8"))
                    for part in pointer.lstrip("/").split("/"):
                        part = part.replace("~1", "/").replace("~0", "~")
                        current = current[int(part)] if isinstance(current, list) else current[part]
        check_references(receipt)
        cohorts = receipt["cohorts"]
        original = cohorts["originalSpecialist"]
        self.assertEqual((original["nativeOriginalQuestionsPassed"],
                          original["nativeOriginalQuestionsTotal"]), (4, 4))
        self.assertFalse(original["underlyingNativeMcpMembershipIndependentlyJoined"])
        self.assertNotEqual(original["route"], cohorts["currentPostControlCandidate"]["route"])
        previous = json.loads((root / "docs/assets/runtime-2026-10-25/mcp-native-eleven-case-matrix.json").read_text("utf-8"))
        current = json.loads((root / "docs/assets/runtime-2026-10-25/mcp-native-control-repair-regression.json").read_text("utf-8"))
        self.assertTrue(previous["fullElevenCaseNativeMatrixPassed"])
        self.assertEqual(cohorts["previousCandidate"]["acceptedCases"], 11)
        self.assertEqual(cohorts["previousCandidate"]["explicitRetries"],
                         previous["explicitlyCountedQuestionRetries"])
        self.assertFalse(current["fullElevenCaseNativeMatrixPassed"])
        candidate = cohorts["currentPostControlCandidate"]
        self.assertEqual(candidate["acceptedCases"], current["acceptedDistinctOriginalCases"])
        self.assertEqual(candidate["acceptedCases"], 10)
        case9 = current["cases"][8]
        self.assertEqual(candidate["failedCase9Attempts"], case9["nativeOriginalQuestionSubmissions"])
        self.assertEqual(candidate["failedCase9Attempts"], 2)
        self.assertFalse(case9["rootCauseEstablished"])
        self.assertFalse(candidate["thirdReplaySubmitted"])
        self.assertFalse(case9["thirdAttemptSubmitted"])
        self.assertFalse(cohorts["hostedDiagnosticExtension"]["nativeCertified"])
        self.assertEqual(cohorts["hostedDiagnosticExtension"]["latestRetainedVersion"], "5")

    def test_lab6_crosswalk_is_linked_in_all_six_current_bilingual_docs(self):
        root = Path(__file__).resolve().parents[1]
        filename = "lab6-acceptance-crosswalk.json"
        expected = ["PASS"] * 5 + ["PARTIAL", "PASS", "PASS", "FAIL", "NOT_RUN", "NOT_RUN", "PARTIAL"]
        for language in ("en", "fr"):
            for name in ("lab-06", "validation", "completion-roadmap"):
                with self.subTest(language=language, page=name):
                    text = (root / "docs" / language / f"{name}.md").read_text("utf-8")
                    self.assertIn(f"](../assets/runtime-2026-10-26/{filename})", text)
                    self.assertIn("](../assets/runtime-2026-10-26/lab6-intake-local-native.json)", text)
                    for marker in ("2026-10-26", "T017", "10/11", "11/11", "UNKNOWN"):
                        self.assertIn(marker, text)
                    first_current_section = text.split("\n### ", 2)[1]
                    self.assertIn(filename, first_current_section)
                    self.assertIn("10/11", first_current_section)
                    self.assertIn("11/11", first_current_section)
                    self.assertIn("lab6-intake-local-native.json", first_current_section)
                    self.assertIn("prospective", first_current_section)
                    self.assertIn("SearchAndSummarizeContent", first_current_section)
                    self.assertIn("DynamicPlanFinished", first_current_section)
                    self.assertIn("activityProcessed=true", first_current_section)
                    self.assertIn("Error", first_current_section)
                    self.assertIn("displayed citation excerpt lacks" if language == "en"
                                  else "extrait de citation affiché ne contient pas",
                                  first_current_section)
                    self.assertNotRegex(first_current_section,
                                        r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
                    if name == "lab-06":
                        rows = [line for line in text.splitlines() if line.startswith("| F6-")]
                        self.assertEqual(len(rows), 12)
                        for row, status in zip(rows, expected):
                            self.assertTrue(row.split("|")[-2].strip().startswith(status), row)
                    elif name == "completion-roadmap":
                        self.assertIn("- [ ] T017 [Plan:4.1]", text)
                        self.assertNotIn("- [x] T017", text)
                    else:
                        self.assertIn("## Original review baseline" if language == "en"
                                      else "## État de la revue initiale", text)

    def test_lab6_multisource_native_check_proves_exact_membership_without_architecture_substitution(self):
        root = Path(__file__).resolve().parents[1]
        directory = root / "docs/assets/runtime-2026-10-26"
        for filename in ("lab6-multisource-native.json", "lab6-intake-routing-repair.json"):
            raw = (directory / filename).read_text("utf-8")
            self.assertTrue(raw.endswith("\n"))
            self.assertNotRegex(raw, r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
            for marker in (".copilot-tracking", "C:\\", "https://", "conversation_id",
                           "tenant_id", "client_secret", "access_token", ".zip"):
                self.assertNotIn(marker, raw)
            receipt = json.loads(raw)
            self.assertEqual(receipt["questionsSubmittedDuringPublication"], 0)
            self.assertFalse(receipt["acceptance"]["T017RuntimeComplete"])
            self.assertFalse(receipt["acceptance"]["workshopComplete"])
            self.assertFalse(receipt["acceptance"]["historicalArchitectureEquivalenceClaimed"])
        receipt = json.loads((directory / "lab6-multisource-native.json").read_text("utf-8"))
        self.assertEqual((receipt["case"], receipt["status"]), ("F6-07", "PASS"))
        self.assertEqual((receipt["nativeQuestionSubmissions"], receipt["freshConversations"]), (1, 1))
        self.assertEqual((receipt["replays"], receipt["extraPreflightQuestions"]), (0, 0))
        routing = receipt["routing"]
        self.assertEqual((routing["completedNativeMcpInvocations"], routing["returnedRecords"]), (1, 2))
        self.assertEqual(routing["verifiedApplicableSourceGroups"],
                         ["Investigation procedures", "Regulatory compliance"])
        self.assertEqual((routing["verifiedApplicableSourceGroupCount"],
                          routing["unprovenSourceGroupCount"]), (2, 0))
        self.assertTrue(routing["questionStepOutputAndRetrievalSelectionReceiptsCorrelated"])
        self.assertTrue(routing["completeReturnedRecordFieldsMatchPinnedLicensedCorpus"])
        self.assertEqual(routing["underlyingServiceHttpFanoutCount"], "NOT_ESTABLISHED")
        self.assertTrue(all(receipt["assertions"].values()))
        completion = receipt["completion"]
        for key in ("completeFinalParentMessage", "correlatedNativeDynamicPlanFinished",
                    "withinBoundedDeadline"):
            self.assertTrue(completion[key])
        self.assertFalse(completion["cancelled"])
        self.assertEqual(receipt["latencySeconds"]["serverReceiptToReply"], 35.0384)
        self.assertEqual(receipt["latencySeconds"]["sendToReply"], 41.144941)
        preservation = receipt["preservation"]
        self.assertEqual(preservation["priorArtifactsWithHashesAndModificationTimesUnchanged"], 42)
        for key in ("servedRootSettingsAndVersionUnchangedDuringCapture",
                    "instructionDigestUnchanged", "sourceIdentitiesVersionsAndStatusesUnchanged",
                    "retainedSnapshotAndPublisherSourcesUnchanged"):
            self.assertTrue(preservation[key])
        self.assertFalse(preservation["fullComponentPostflightReexport"])
        self.assertFalse(preservation["originalDocxRepaired"])
        self.assertFalse(receipt["acceptance"]["diagnosticExtensionCertified"])

    def test_lab6_intake_repair_preserves_failure_and_four_case_runtime_regression(self):
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "docs/assets/runtime-2026-10-26/lab6-intake-routing-repair.json")
                             .read_text("utf-8"))
        before = receipt["beforeFix"]
        self.assertEqual((before["nativeQuestionSubmissions"], before["extraQuestions"],
                          before["replays"]), (1, 0, 0))
        self.assertEqual(before["F6-06"]["status"], "FAIL")
        for key in ("nativeMcpInvocationReceipts", "retrievalOutputReceipts", "verifiedCorpusRecords"):
            self.assertEqual(before["F6-06"][key], 0)
        self.assertEqual((before["F6-09"]["status"], before["F6-09"]["nativeQuestionSubmissions"]),
                         ("NOT_RUN", 0))
        cause = receipt["cause"]
        self.assertTrue(cause["unanchoredIntakeCondition"])
        self.assertEqual((cause["matchedSubstring"], cause["containingWord"]), ("hi", "Which"))
        self.assertEqual(cause["zeroBasedHalfOpenSpan"], [1, 3])
        repair = receipt["repair"]
        self.assertEqual((repair["changedTopicCount"], repair["changedConditionLines"]), (1, 1))
        for key in ("wholeMessageAnchorsAdded", "reviewingACaseAlternativePreservesExactF604",
                    "otherTriggerAndActionFieldsPreserved", "existingConnectedCloneUsed",
                    "officialPortalEditorUsed", "currentConditionComparedBeforeEdit",
                    "savedConditionIndependentlyReadAfterReload",
                    "nativeTestPreflightAndPostflightConditionMatch"):
            self.assertTrue(repair[key])
        self.assertEqual((repair["staticRegressionTestsPassed"], repair["staticRoutingStringsChecked"],
                          repair["otherCloneFilesByteIdentical"]), (4, 16, 37))
        self.assertEqual((repair["portalTopicCheckerErrors"], repair["portalTopicCheckerWarnings"]), (0, 0))
        self.assertEqual(repair["topicComponentVersionProof"], "NOT_ESTABLISHED")
        for key in ("staticChecksArePowerFxRuntimeProof", "fullCloudComponentVersionAndByteAudit",
                    "officialLspValidationPassed", "manageBundleModified", "agentPublished"):
            self.assertFalse(repair[key])
        self.assertIn("@azure/msal-node-extensions", repair["officialLspBlocker"])
        post = receipt["postFix"]
        self.assertEqual((post["nativeQuestionSubmissions"], post["freshConversations"],
                          post["submissionsPerCase"]), (4, 4, 1))
        self.assertEqual((post["replaysWithinCohort"], post["extraQuestions"]), (0, 0))
        cases = post["cases"]
        self.assertEqual([case["id"] for case in cases], ["F6-06", "F6-09", "F6-04", "F6-05"])
        self.assertEqual([case["status"] for case in cases], ["PARTIAL", "FAIL", "PASS", "PASS"])
        self.assertTrue(all(case["nativeQuestionSubmissions"] == 1 for case in cases))
        self.assertTrue(all(case["completeFinalReply"] for case in cases))
        english, french, intake, glossary = cases
        self.assertEqual(english["behavioralRetrieval"], "PASS")
        self.assertEqual((english["completedNativeMcpInvocations"], english["verifiedCorpusRecords"]), (1, 2))
        self.assertEqual(english["originalConnectedFoundryChildInvocation"], "NOT_ESTABLISHED")
        self.assertEqual((french["completedNativeMcpInvocations"], french["verifiedCorpusRecords"]), (1, 1))
        self.assertEqual(french["supportedCoreMeaningAndJoinedLineage"], "PASS")
        self.assertEqual((french["finalAnswerLanguage"], french["requiredAnswerLanguage"]), ("English", "French"))
        self.assertEqual((intake["completedNativeMcpInvocations"], intake["completedLocalSearchSteps"],
                          intake["foundryEvidenceSteps"]), (0, 0, 0))
        self.assertTrue(intake["clarificationRequested"])
        self.assertTrue(intake["matchedTerminalProcessedCancellation"])
        self.assertFalse(intake["noncancelledDynamicPlanFinished"])
        self.assertEqual((glossary["completedNativeMcpInvocations"], glossary["completedLocalSearchSteps"]), (0, 1))
        for key in ("documentLevelSupport", "nativeSourceMatchesReadyMitMarkdown",
                    "supportInAnotherActuallyRetrievedChunk", "noncancelledDynamicPlanFinished"):
            self.assertTrue(glossary[key])
        self.assertFalse(glossary["displayedCitationChunkContainsExpansion"])
        self.assertFalse(glossary["exactCitationChunkSupportProven"])
        self.assertEqual(post["priorArtifactsWithHashesAndModificationTimesUnchanged"], 110)
        self.assertTrue(post["rootSettingsInstructionsModelAndSourceFingerprintsUnchangedDuringCapture"])
        for key in ("configurationEditsDuringCapture", "publishesDuringCapture", "extraResourcesCreated"):
            self.assertEqual(post[key], 0)
        history = receipt["historicalBoundaries"]
        self.assertTrue(history["originalFailureAndConditionalFrenchStopPreserved"])
        self.assertTrue(history["priorExactF607PassPreservedWithoutRerun"])
        self.assertTrue(history["retainedArchivePredatesConditionRepair"])
        self.assertEqual(history["originalElevenCaseCase9FailedAttempts"], 2)
        self.assertFalse(history["originalElevenCaseCase9Executed"])
        self.assertFalse(history["originalElevenCaseCase9ThirdReplaySubmitted"])
        self.assertTrue(receipt["acceptance"]["intakeInterceptionBehaviorCorrected"])
        self.assertFalse(receipt["acceptance"]["postFixFrenchLanguagePassed"])

    def test_lab6_language_attempt_does_not_erase_completed_failure_or_infer_delivery(self):
        root = Path(__file__).resolve().parents[1]
        directory = root / "docs/assets/runtime-2026-10-26"
        filename = "lab6-language-configured-attempt.json"
        raw = (directory / filename).read_text("utf-8")
        self.assertTrue(raw.endswith("\n"))
        self.assertNotRegex(raw, r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
        for marker in (".copilot-tracking", "C:\\", "https://", "conversation_id",
                       "tenant_id", "client_secret", "access_token", ".zip"):
            self.assertNotIn(marker, raw)
        receipt = json.loads(raw)
        self.assertEqual(receipt["status"], "BLOCKED_DELIVERY")
        config = receipt["configuration"]
        self.assertEqual((config["primaryLanguage"], config["secondaryLanguages"]), ("en-US", ["fr-FR"]))
        self.assertEqual(config["secondaryLanguagesAdded"], 1)
        self.assertTrue(config["persistedSettingsAndServedMetadataIndependentlyVerified"])
        for key in ("primaryLanguageChanged", "translatedStaticTopicStringsUploaded",
                    "dynamicLanguageSwitchingConfigured", "instructionsSourcesToolsAndModelEdited",
                    "agentPublished"):
            self.assertFalse(config[key])
        english, french = receipt["cases"]
        self.assertEqual([case["id"] for case in receipt["cases"]], ["F6-06", "F6-09"])
        self.assertEqual([case["status"] for case in receipt["cases"]], ["NOT_RUN", "NOT_RUN"])
        self.assertEqual(english["deliveryStatus"], "FAIL")
        self.assertEqual(english["nativeError"], "Cannot send empty message")
        self.assertEqual(english["captureWindowSeconds"], 240)
        for key in ("acceptedUserMessageReceiptObserved", "answerRetrievalOrCompletionProofObserved"):
            self.assertFalse(english[key])
        for key in ("serverReceiptToReplySeconds", "sendToReplySeconds"):
            self.assertIsNone(english[key])
        self.assertEqual(french["sendClicks"], 0)
        self.assertEqual((receipt["maximumAuthorizedIntents"], receipt["durableQuestionIntents"],
                          receipt["nativeSendClicks"]), (2, 1, 1))
        self.assertEqual(receipt["observedAcceptedNativeQuestionActivities"], 0)
        self.assertEqual(receipt["serverAcceptance"], "NOT_ESTABLISHED")
        self.assertEqual(receipt["underlyingServiceHttpFanoutCount"], "UNKNOWN")
        for key in ("replays", "extraQuestions", "observedNativeMcpOrRetrievalReceipts",
                    "questionsSubmittedDuringPublication"):
            self.assertEqual(receipt[key], 0)
        session = receipt["sessionLanguage"]
        self.assertTrue(session["englishMenuActivatedBeforeAttemptAndDuringRestoration"])
        self.assertTrue(session["overviewRestored"])
        for key in ("checkedRadioStateExposed", "selectedSessionLanguageVerified",
                    "frenchSelected", "englishRestorationVerified"):
            self.assertFalse(session[key])
        preservation = receipt["preservation"]
        self.assertEqual(preservation["priorPrivateAndPublisherFilesUnchangedByHashAndModificationTime"], 133)
        self.assertEqual(preservation["topicComponentVersionProof"], "NOT_ESTABLISHED")
        self.assertTrue(preservation["rootSettingsVersionInstructionsSourcesModelAndIntakeFingerprintsUnchangedDuringCapture"])
        self.assertTrue(preservation["retainedArchivePredatesIntakeAndLanguageChanges"])
        for key in ("configurationEditsDuringCapture", "publishesDuringCapture", "newAzureResources"):
            self.assertEqual(preservation[key], 0)
        acceptance = receipt["acceptance"]
        self.assertEqual(acceptance["lastCompletedF609Result"], "FAIL")
        self.assertTrue(acceptance["historicalFailuresPreserved"])
        self.assertEqual(acceptance["originalConnectedFoundryChildInvocation"], "NOT_ESTABLISHED")
        for key in ("newFrenchSessionPassClaimed", "automaticLanguageDetectionProven",
                    "completeStaticTopicLocalizationProven", "historicalArchitectureEquivalenceClaimed",
                    "T017RuntimeComplete", "workshopComplete"):
            self.assertFalse(acceptance[key])
        crosswalk = json.loads((directory / "lab6-acceptance-crosswalk.json").read_text("utf-8"))
        update = crosswalk["languageConfiguredAttempt"]
        self.assertEqual(update["reference"], "docs/assets/runtime-2026-10-26/" + filename)
        self.assertEqual(update["lastCompletedF609StatusStill"], crosswalk["rows"][8]["status"])
        self.assertEqual(update["lastCompletedF609StatusStill"], "FAIL")
        self.assertFalse(update["sessionLanguageAndRestorationVerified"])
        self.assertEqual(update["serverAcceptance"], "NOT_ESTABLISHED")
        counts = {status: sum(row["status"] == status for row in crosswalk["rows"])
                  for status in ("PASS", "PARTIAL", "FAIL", "NOT_RUN")}
        self.assertEqual(counts, crosswalk["intakeRoutingRepairUpdate"]["statusCountsAtCompletedCohort"])
        self.assertEqual(counts, {"PASS": 7, "PARTIAL": 2, "FAIL": 1, "NOT_RUN": 2})
        self.assertEqual(crosswalk["multisourceNativeUpdate"]["F607Status"], "PASS")
        self.assertEqual(crosswalk["intakeRoutingRepairUpdate"]["F606OverallStatus"], "PARTIAL")
        self.assertIn("original connected-Foundry-child", crosswalk["rows"][5]["evidenceBoundary"])
        for language in ("en", "fr"):
            for name in ("lab-06", "validation", "completion-roadmap"):
                text = (root / "docs" / language / f"{name}.md").read_text("utf-8")
                section = text.split("\n### ", 2)[1]
                for asset in (filename, "lab6-multisource-native.json", "lab6-intake-routing-repair.json"):
                    self.assertIn(f"](../assets/runtime-2026-10-26/{asset})", section)
                for marker in ("F6-07", "F6-09", "FAIL", "Which", "^...$", "reviewing a case",
                               "fr-FR", "en-US", "Cannot send empty message", "NOT_ESTABLISHED"):
                    self.assertIn(marker, section)
                if name == "completion-roadmap":
                    self.assertIn("- [ ] T017 [Plan:4.1]", text)
                    self.assertEqual(text.count("- [x] T"), 4)

    def test_lab6_two_exact_native_checks_preserve_completion_and_citation_limits(self):
        root = Path(__file__).resolve().parents[1]
        directory = root / "docs/assets/runtime-2026-10-26"
        raw = (directory / "lab6-intake-local-native.json").read_text("utf-8")
        receipt = json.loads(raw)
        self.assertNotRegex(raw, r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
        for marker in (".copilot-tracking", "C:\\", "https://", "conversation_id",
                       "tenant_id", "client_secret", "access_token", ".zip"):
            self.assertNotIn(marker, raw)
        self.assertTrue(raw.endswith("\n"))
        self.assertEqual(receipt["nativeQuestionSubmissions"], 2)
        self.assertEqual(receipt["freshConversations"], 2)
        self.assertTrue(receipt["oneQuestionPerFreshConversation"])
        for key in ("extraPreflightQuestions", "replays", "questionsSubmittedDuringPublication"):
            self.assertEqual(receipt[key], 0)
        intake, local = receipt["cases"]
        self.assertEqual([case["id"] for case in receipt["cases"]], ["F6-04", "F6-05"])
        for case in receipt["cases"]:
            self.assertEqual(case["status"], "PASS")
            self.assertEqual(case["nativeQuestionSubmissions"], 1)
            self.assertTrue(case["freshConversation"])
            self.assertTrue(case["completeFinalReply"])
            self.assertEqual(case["foundryOrMcpEvidenceInvocations"], 0)
        self.assertEqual(intake["localRetrievalInvocations"], 0)
        self.assertTrue(intake["clarificationRequested"])
        self.assertEqual(intake["serverReceiptToFinalSeconds"], 0.118115)
        self.assertTrue(intake["completion"]["allIntakeActionsComplete"])
        self.assertTrue(intake["completion"]["activityProcessed"])
        self.assertEqual(intake["completion"]["completedActions"],
                         ["SendActivity", "CancelAllDialogs"])
        self.assertFalse(intake["completion"]["dynamicPlanFinishedRequired"])
        self.assertNotEqual(intake["completion"]["proofType"], local["completion"]["proofType"])
        self.assertEqual(local["localRetrievalInvocations"], 1)
        self.assertEqual(local["atoExpansion"], "Account Takeover")
        self.assertEqual(local["serverReceiptToFinalSeconds"], 70.618165)
        self.assertEqual(local["completion"]["completedLocalAction"], "SearchAndSummarizeContent")
        self.assertTrue(local["completion"]["dynamicPlanFinished"])
        self.assertFalse(local["completion"]["cancelled"])
        citation = local["citation"]
        for key in ("actualNativeLocalSourceCitation", "nativeSourceMatchesFrozenReadyMarkdown",
                    "documentLevelSupport", "supportInAnotherActuallyRetrievedChunkOfSameSource"):
            self.assertTrue(citation[key])
        for key in ("displayedCitationChunkContainsExpansion", "exactCitationChunkSupportProven",
                    "globalCitationCriterionPassed"):
            self.assertFalse(citation[key])
        self.assertIn("displayed citation excerpt lacks", citation["limit"])
        config = receipt["configuration"]
        self.assertTrue(config["frozenProspectiveMcpAdaptedConfiguration"])
        self.assertFalse(config["historicalSpecialistConfigurationEquivalence"])
        self.assertIn("Ready MIT publisher Markdown", config["sourceAdaptation"])
        self.assertEqual(config["originalDocxIngestionStatus"], "Error")
        self.assertFalse(config["originalDocxReconstructed"])
        self.assertTrue(config["manualSdkArchiveMetadataHashAndServedConfigurationVerifiedBeforeCapture"])
        integrity = receipt["configurationIntegrity"]
        for key in ("configurationEdits", "sourceOrTopicEdits", "publishes", "resourcesCreated"):
            self.assertEqual(integrity[key], 0)
        for key in ("postflightRootVersionAndSettingsUnchanged", "instructionDigestUnchanged",
                    "bothSourceVersionsUnchanged", "publisherSourceArtifactHashesUnchanged",
                    "providedAndPreservedArchivesUnchanged", "trackedWorktreeCleanAfterCapture"):
            self.assertTrue(integrity[key])
        self.assertFalse(integrity["fullComponentPostflightReexport"])
        self.assertIn("no second complete component archive export", integrity["limit"])
        acceptance = receipt["acceptance"]
        self.assertTrue(acceptance["exactTwoIndependentChecksComplete"])
        for key in ("otherF6StatusesChanged", "thirdReplaySubmitted",
                    "diagnosticExtensionIdentityFixed", "T017RuntimeComplete", "workshopComplete"):
            self.assertFalse(acceptance[key])
        self.assertEqual((acceptance["candidateCurrentAcceptedCases"],
                          acceptance["candidateTotalCases"], acceptance["case9FailedAttempts"]), (10, 11, 2))
        crosswalk = json.loads((directory / "lab6-acceptance-crosswalk.json").read_text("utf-8"))
        update = crosswalk["currentNativeUpdate"]
        self.assertEqual(update["reference"],
                         "docs/assets/runtime-2026-10-26/lab6-intake-local-native.json")
        self.assertEqual((update["nativeQuestionSubmissions"], update["freshConversations"]), (2, 2))
        self.assertEqual((update["replays"], update["publicationQuestions"]), (0, 0))
        self.assertFalse(update["historicalSpecialistConfigurationEquivalence"])
        self.assertEqual(update["statusCounts"], {"PASS": 5, "PARTIAL": 4, "NOT_RUN": 3})
        for index, row in enumerate(crosswalk["rows"][3:5]):
            self.assertEqual(row["exactEvidence"],
                             [update["reference"] + f"#/cases/{index}"])
            self.assertEqual(row["status"], receipt["cases"][index]["status"])
            self.assertEqual(row["initialOfflineStatus"], "NOT_RUN")

    def test_lab6_private_history_is_response_only_with_unknown_plan_and_call_counts(self):
        root = Path(__file__).resolve().parents[1]
        directory = root / "docs/assets/runtime-2026-10-26"
        filename = "lab6-private-history-native.json"
        raw_bytes = (directory / filename).read_bytes()
        self.assertNotIn(b"\r", raw_bytes)
        self.assertTrue(raw_bytes.endswith(b"\n"))
        raw = raw_bytes.decode("utf-8")
        self.assertNotRegex(raw, r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
        for marker in (".copilot-tracking", "C:\\", "https://", "conversation_id",
                       "tenant_id", "client_secret", "access_token", ".zip"):
            self.assertNotIn(marker, raw)
        receipt = json.loads(raw)
        self.assertEqual((receipt["case"], receipt["status"]), ("F6-08", "PASS"))
        self.assertIn("Response-only", receipt["resultScope"])
        self.assertTrue(receipt["response_assertions_pass"])
        self.assertFalse(receipt["overallPlanClosureProven"])
        self.assertEqual(receipt["nativeQuestionSubmissions"], 1)
        self.assertTrue(receipt["oneShot"])
        for key in ("replays", "extraPreflightQuestions", "questionsSubmittedDuringPublication"):
            self.assertEqual(receipt[key], 0)
        self.assertEqual(receipt["serverReceiptToFinalSeconds"], 16.670226)
        self.assertEqual(receipt["sendToReplyWallSeconds"], 19.506164)
        self.assertEqual(receipt["serverTerminalFallbackSeconds"], 16.671472)
        for key in ("explicitConfiguredEvidenceLimitation", "refusesInference",
                    "noInventedPrivateCustomerEvents", "noFictionalCorpusHistorySubstitution",
                    "notClarificationOnly"):
            self.assertTrue(receipt["assertions"][key])
        self.assertFalse(receipt["assertions"]["zeroToolCallsOrZeroIrrelevantRecordsRequired"])
        completion = receipt["completion"]
        self.assertTrue(completion["nativeFinalMessageStream"])
        self.assertTrue(completion["matchingTerminalFallbackEndDialog"])
        self.assertEqual(completion["completedNoAnswerSupportState"], "AnswerNotFoundInSearchResults")
        self.assertFalse(completion["dynamicPlanFinishedObserved"])
        self.assertTrue(completion["captureDeadlineReached"])
        self.assertEqual(completion["captureWindowSeconds"], 240)
        self.assertEqual(completion["overallGenerativeOrMcpPlanCompletion"], "NOT_ESTABLISHED")
        routing = receipt["routing"]
        self.assertEqual((routing["completedLocalSearchSteps"], routing["localResultsReturned"]), (1, 3))
        self.assertTrue(routing["fallbackSearchAndSummarizeContentObserved"])
        self.assertTrue(routing["mcpUiLabelPresent"])
        self.assertFalse(routing["mcpInvocationOrOutputCorrelated"])
        for key in ("actualMcpInvocationCount", "actualUnderlyingFoundryInvocationCount",
                    "distinctLowLevelRetrievalCallCount"):
            self.assertEqual(routing[key], "NOT_ESTABLISHED")
            self.assertNotEqual(routing[key], 0)
        config = receipt["configuration"]
        self.assertTrue(config["sameFrozenProspectiveMcpAdaptedConfigurationAsF604AndF605"])
        self.assertFalse(config["historicalSpecialistConfigurationEquivalence"])
        self.assertFalse(config["originalDocxReconstructed"])
        preservation = receipt["preservation"]
        for key in ("rootConfigurationHashesAndVersionsUnchanged", "instructionDigestUnchanged",
                    "sourceHashesAndVersionsUnchanged", "priorReceiptsAndArchivesUnchanged",
                    "trackedWorktreeCleanAfterCapture"):
            self.assertTrue(preservation[key])
        for key in ("configurationEditsDuringCapture", "publishesDuringCapture", "newResourcesDuringCapture"):
            self.assertEqual(preservation[key], 0)
        self.assertFalse(preservation["fullComponentPostflightReexport"])
        limits = receipt["receiptLimitations"]
        self.assertTrue(limits["preSendTransientNetworkInterruption"])
        self.assertTrue(limits["boundedRecoveryBeforeQuestionSend"])
        self.assertFalse(limits["additionalSessionClickOrQuestionReplay"])
        acceptance = receipt["acceptance"]
        self.assertTrue(acceptance["distinctFromOriginalElevenCaseMatrixCase9"])
        self.assertEqual((acceptance["candidateCurrentAcceptedCases"],
                          acceptance["candidateTotalCases"], acceptance["case9FailedAttempts"]), (10, 11, 2))
        for key in ("case9RootCauseEstablished", "thirdReplaySubmitted", "T017RuntimeComplete",
                    "workshopComplete", "historicalArchitectureEquivalenceClaimed"):
            self.assertFalse(acceptance[key])
        crosswalk = json.loads((directory / "lab6-acceptance-crosswalk.json").read_text("utf-8"))
        row = crosswalk["rows"][7]
        self.assertEqual((row["id"], row["status"], row["initialOfflineStatus"]), ("F6-08", "PASS", "PARTIAL"))
        self.assertIn("Neither proves the exact native", row["initialOfflineAssessment"])
        self.assertEqual(row["exactEvidence"], ["docs/assets/runtime-2026-10-26/" + filename])
        for marker in ("Response-only", "DynamicPlanFinished", "240", "three records", "NOT_ESTABLISHED"):
            self.assertIn(marker, row["evidenceBoundary"])
        latest = crosswalk["latestPrivateHistoryUpdate"]
        self.assertEqual(latest["reference"], row["exactEvidence"][0])
        self.assertEqual(latest["nativeQuestionSubmissions"], 1)
        self.assertEqual((latest["replays"], latest["publicationQuestions"]), (0, 0))
        self.assertTrue(latest["response_assertions_pass"])
        self.assertTrue(latest["priorTwoQuestionNativeUpdateUnchanged"])
        self.assertEqual(latest["statusCounts"], {"PASS": 6, "PARTIAL": 3, "NOT_RUN": 3})
        self.assertEqual(latest["actualMcpAndUnderlyingFoundryCallCounts"], "NOT_ESTABLISHED")
        for key in ("overallPlanClosureProven", "T017RuntimeComplete", "workshopComplete"):
            self.assertFalse(latest[key])
        self.assertNotRegex(json.dumps(crosswalk), r'(?i)"[^"]*(?:percentage|percentComplete)[^"]*"\s*:')
        for language in ("en", "fr"):
            for name in ("lab-06", "validation", "completion-roadmap"):
                text = (root / "docs" / language / f"{name}.md").read_text("utf-8")
                section = text.split("\n### ", 2)[1]
                self.assertIn(f"](../assets/runtime-2026-10-26/{filename})", section)
                for marker in ("F6-08", "DynamicPlanFinished", "240", "NOT_ESTABLISHED"):
                    self.assertIn(marker, section)
                self.assertIn("response-only" if language == "en" else "réponse uniquement", section)
                self.assertIn("plan closure remains unproven" if language == "en"
                              else "clôture du plan reste non prouvée", section)
                if name == "completion-roadmap":
                    self.assertIn("- [ ] T017 [Plan:4.1]", text)

    def test_roadmap_covers_every_lab_and_explicit_lab6_reconciliation(self):
        root = Path(__file__).resolve().parents[1]
        for language, heading in (
            ("en", "## Lab coverage and where to resume"),
            ("fr", "## Couverture des labs et point de reprise"),
        ):
            with self.subTest(language=language):
                text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
                coverage = text.split(heading + "\n", 1)[1].split("\n## ", 1)[0]
                guides = {path.name for path in (root / "docs" / language).glob("lab-*.md")}
                rows = [line for line in coverage.splitlines()
                        if line.startswith("| [")]
                self.assertEqual(len(rows), len(guides))
                for guide in guides:
                    self.assertEqual(sum(f"]({guide})" in row for row in rows), 1)
                self.assertIn("T005,T006,T007,T017", coverage)
                self.assertIn("T003/T004", coverage)
                self.assertIn("T007/T008", coverage)
                self.assertIn("- [ ] T017 [Plan:4.1]", text)
                requirement = next(line for line in text.splitlines()
                                   if line.startswith("| REQ-004"))
                self.assertIn("T007,T008,T017", requirement)
                self.assertIn("F6-01", text)
                self.assertIn("F6-12", text)
                self.assertEqual(text.count("- [x] T"), 4)

    def test_native_search_picker_connection_is_not_paired_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        filename = "native-search-index-picker.json"
        path = root / "docs" / "assets" / "runtime-2026-10-26" / filename
        raw = path.read_bytes()
        receipt = json.loads(raw)
        self.assertNotRegex(raw.decode("utf-8"),
                            r"(?i)\b[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}\b")
        self.assertTrue(raw.endswith(b"\n"))
        self.assertEqual(len(receipt["cohorts"]), 2)
        for cohort in receipt["cohorts"]:
            native = cohort["native"]
            self.assertEqual(native["createSubmissions"], 1)
            self.assertTrue(native["manualCredentialEntry"])
            self.assertTrue(native["savedNotificationObserved"])
            self.assertEqual(native["independentInventoryStatus"], "Connected")
            self.assertEqual(native["pickerError"], "Something went wrong.")
            self.assertEqual(native["consoleHttpStatus"], 400)
            self.assertFalse(native["httpResponseBodyAvailable"])
            self.assertFalse(native["addToAgentEnabled"])
            self.assertEqual((native["refreshes"], native["retries"]), (0, 0))
            cleanup = cohort["cleanup"]
            self.assertTrue(cleanup["independentlyVerified"])
            self.assertEqual(cleanup["ownedResourcesRemaining"], 0)
            self.assertTrue(cleanup["credentialExplicitlyRevokedAndIdentityDeleted"])
            self.assertTrue(cleanup["protectedSecretFileRemoved"])
        first, second = receipt["cohorts"]
        self.assertTrue(first["permissions"]["metadataListingPermissionGapDocumented"])
        self.assertIsNone(first["permissions"]["metadataRole"])
        self.assertEqual(len(first["cleanup"]["failuresPreserved"]), 2)
        self.assertEqual(len(first["cleanup"]["recovery"]), 2)
        permissions = second["permissions"]
        self.assertEqual(permissions["metadataActions"],
                         ["Microsoft.Search/searchServices/indexes/read"])
        self.assertEqual(permissions["metadataAssignmentScope"], "Existing Search service")
        self.assertEqual(permissions["metadataDataActions"], [])
        self.assertEqual(permissions["metadataWriteActions"], [])
        self.assertFalse(permissions["metadataOperationsReadGranted"])
        self.assertEqual(permissions["dedicatedPrincipalExactAssignmentCount"], 2)
        self.assertTrue(permissions["exactAssignmentsIndependentlyVerified"])
        self.assertEqual(second["directControls"]["correctServicePrincipalMetadataListing"], "PASS")
        self.assertEqual(second["directControls"]["ownSyntheticCanaryQuery"], "PASS")
        self.assertEqual(second["cleanup"]["failuresPreserved"], [])
        self.assertEqual(second["cleanup"]["separateVerifyCleanedExitCode"], 0)
        acceptance = receipt["acceptance"]
        for key in ("nativeSourceAdditions", "nativePositiveQuestions",
                    "nativeNegativeQuestions", "modelQuestions"):
            self.assertEqual(acceptance[key], 0)
        for key in ("positive", "negative", "postRevocationDirect403"):
            self.assertEqual(acceptance[key], "NOT_RUN")
        self.assertEqual(acceptance["noLeakAcceptance"], "NOT_PROVEN")
        self.assertEqual(acceptance["effectiveNativeRuntimePrincipal"], "NOT_PROVEN")
        self.assertEqual(acceptance["specificHttp400Cause"], "UNKNOWN")
        for key in ("indexBound", "schemaAndFieldMappingValidated", "sourceReady",
                    "metadataAdditionProvenFix", "connectedOrDirectControlsAreNativeAcceptance",
                    "partialPairedTestPass", "S5_10Passed", "T014Complete",
                    "T016Complete", "workshopComplete"):
            self.assertFalse(acceptance[key])
        preservation = receipt["preservation"]
        self.assertEqual([preservation[key] for key in
                          ("originalAgents", "originalConnections", "originalSearchSchemas",
                           "historicalFilesUnchanged")], [5, 7, 3, 181])
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md"):
                text = (root / "docs" / language / name).read_text("utf-8")
                self.assertIn(filename, text)
                self.assertIn(receipt["issueUrl"], text)

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

    def test_completion_checkpoint_preserves_cost_and_release_boundaries(self):
        from decimal import Decimal

        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-23"
        result = json.loads((assets / "completion-progress.json").read_text("utf-8"))
        self.assertFalse(result["overall_workshop_certified"])
        self.assertEqual(result["roadmap_tasks_closed"], [])
        inventory = result["ownership_inventory"]
        self.assertTrue(inventory["resource_group_id_and_run_tag_match_retained_ownership"])
        self.assertTrue(inventory["account_project_search_ids_match_retained_ownership"])
        self.assertTrue(inventory["account_project_search_managed_identity_ids_match_retained_ownership"])
        self.assertFalse(inventory["T001_complete"])
        costs = inventory["cost_control"]
        search = sum(Decimal(row["cost"]) for row in costs["search_daily_returned_costs"])
        self.assertEqual(search, Decimal(costs["reported_search_subtotal"]))
        self.assertEqual(search + Decimal(costs["reported_account_subtotal"]),
                         Decimal(costs["reported_pretax_subtotal"]))
        self.assertTrue(costs["pagination_complete"])
        self.assertTrue(costs["billing_data_may_lag_and_current_day_is_partial"])
        self.assertFalse(costs["complete_lifetime_or_final_invoice_claimed"])
        self.assertTrue(costs["resources_remain_live_and_billable"])
        self.assertIsNone(costs["named_retention_owner"])
        self.assertIsNone(costs["approved_review_deadline"])
        release = result["release"]
        self.assertEqual(release["recorded_source_hashes_checked"], 8)
        self.assertEqual(release["recorded_source_hashes_matched"], 8)
        self.assertTrue(all(value == "pending" for value in release["required_role_approvals"].values()))
        self.assertFalse(release["general_permission_promoted_to_role_signoff"])
        self.assertFalse(release["T002_complete"])
        hosted = result["foundry_metadata"]["hosted_extension"]
        self.assertFalse(hosted["repair_redeployed"])
        self.assertFalse(hosted["new_hosted_activity_test"])
        self.assertEqual(hosted["endpoint_authorization_schemes"], ["Entra", "BotServiceRbac"])
        control = result["foundry_metadata"]["original_retrieval_control"]
        self.assertEqual(control["latest_version"], "4")
        self.assertTrue(control["version_definition_matches_retained_creation_receipt"])
        self.assertFalse(control["native_answer_or_whole_turn_retested"])
        self.assertFalse(result["native_browser"]["page_open_failure_or_no_side_effect_proven"])
        self.assertTrue(all(not value for value in result["preservation"].values()))
        for language in ("en", "fr"):
            for filename in ("completion-roadmap.md", "backend-live-2026-10-20.md"):
                text = (root / "docs" / language / filename).read_text("utf-8")
                self.assertIn("completion-progress.json", text)
                self.assertIn("native-state-readback.json", text)
                self.assertIn("independent-lab-review.json", text)

    def test_current_native_readback_is_not_native_runtime_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "docs" / "assets" / "runtime-2026-10-23"
                              / "native-state-readback.json").read_text("utf-8"))
        self.assertEqual(receipt["surface"]["http_status_codes"], [200, 200, 200])
        diagnostic = receipt["current_diagnostic"]
        self.assertEqual((diagnostic["statecode"], diagnostic["statuscode"]), (1, 2))
        self.assertTrue(diagnostic["definition_matches_retained_baseline"])
        attachment = receipt["current_original_retrieval_attachment"]
        self.assertEqual(attachment["state_label"], "Active")
        self.assertTrue(attachment["target_agent_name_matches_historical_capture"])
        self.assertIsNone(attachment["definition_matches_retained_baseline"])
        self.assertFalse(attachment["byte_for_byte_attachment_unchanged_verified"])
        self.assertFalse(receipt["roadmap"]["tasks_marked_complete"])
        self.assertTrue(all(not value for value in receipt["safety"].values()))

    def test_independent_lab_review_does_not_close_historical_partial_criteria(self):
        root = Path(__file__).resolve().parents[1]
        receipt = json.loads((root / "docs" / "assets" / "runtime-2026-10-23"
                              / "independent-lab-review.json").read_text("utf-8"))
        self.assertEqual(receipt["scope"]["roadmap_task_ids"], ["T009", "T010", "T014"])
        self.assertEqual(receipt["scope"]["roadmap_tasks_closed"], [])
        self.assertEqual(receipt["scope"]["new_native_agent_acceptance_passes"], 0)
        self.assertFalse(receipt["scope"]["workshop_complete"])
        self.assertFalse(receipt["execution_boundary"]["sdk_or_direct_results_promoted_to_native"])
        self.assertTrue(receipt["execution_boundary"]["prior_failures_preserved"])
        self.assertFalse(receipt["current_observations"]["browser"]["usable_shared_page_available"])
        refreshed = json.loads((root / "docs" / "assets" / "runtime-2026-10-23"
                                / "lab-prerequisite-refresh.json").read_text("utf-8"))
        self.assertFalse(refreshed["overall_lab_0_ready"])
        self.assertFalse(refreshed["lab_4_byom_passed"])
        self.assertEqual(refreshed["roadmap_tasks_closed"], [])
        self.assertTrue(all(state == "Registered"
                            for state in refreshed["resource_providers"].values()))
        for quota in refreshed["regional_model_quota"]["records"]:
            self.assertEqual(quota["unit"], "Count")
            self.assertEqual(quota["limit"] - quota["currentValue"], quota["unallocated"])
        byom = refreshed["lab_4_public_contract_rechecked"]
        self.assertEqual(byom["connector_documented_authentication_types"], ["Default"])
        self.assertFalse(byom["policy_exception_or_lab_exclusion_approved"])
        self.assertFalse(byom["T011_T012_completed"])
        for language in ("en", "fr"):
            for filename in ("lab-00.md", "lab-04.md"):
                self.assertIn("lab-prerequisite-refresh.json",
                              (root / "docs" / language / filename).read_text("utf-8"))
        for path in root.glob("docs/assets/runtime-2026-10-23/*.json"):
            text = path.read_text("utf-8")
            self.assertNotRegex(text, r'(?i)authorization["\s:]+bearer\s+')
            self.assertNotRegex(text, r"eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.")
            self.assertNotIn("subscriptions/", text)
            self.assertNotIn(".crm.dynamics.com", text)
            self.assertNotIn("access_token", text)

    def test_authorized_release_preserves_failed_v2_and_hosted_only_v3_results(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-23"
        result = json.loads((assets / "authorized-release.json").read_text("utf-8"))
        self.assertFalse(result["overall_workshop_certified"])
        self.assertEqual(result["authorization"]["reference"], "user-turn-20261023T161249-0400")
        self.assertFalse(result["authorization"][
            "organization_role_membership_or_third_party_signatures_inferred"])
        self.assertEqual([item["version"] for item in result["deployments"]], ["2", "3"])
        self.assertTrue(all(item["azd_exit_code"] == 0 for item in result["deployments"]))
        self.assertTrue(all(not item["endpoint_authorization_changed"]
                            for item in result["deployments"]))
        earlier = json.loads((assets / "hosted-negative-checks.json").read_text("utf-8"))
        self.assertEqual(earlier["result"], "FAIL")
        self.assertEqual((earlier["passed"], earlier["failed"]), (1, 1))
        self.assertFalse(earlier["acceptance_closed"])
        final = json.loads((assets / "hosted-version3-regression.json").read_text("utf-8"))
        self.assertEqual(final["active_version"], "3")
        self.assertEqual(final["result"], "PASS")
        self.assertEqual(final["activity_requests_attempted"], 3)
        self.assertEqual(final["automatic_retries"], 0)
        self.assertEqual([case["result"] for case in final["cases"]], ["PASS"] * 3)
        positive, abstention, invalid = final["cases"]
        self.assertTrue(positive["whole_record_checks_passed"])
        self.assertTrue(positive["individual_marker_checks_passed"])
        self.assertTrue(abstention["explicit_abstention"])
        self.assertFalse(abstention["selection_invoked"])
        self.assertTrue(invalid["explicit_application_error"])
        self.assertEqual(invalid["actual_total_model_requests"], 0)
        self.assertFalse(final["native_pass"])
        self.assertFalse(final["full_matrix_pass"])
        self.assertFalse(final["legal_completion"])
        self.assertTrue(final["historical_evidence_hashes_unchanged"])
        self.assertEqual(result["roadmap"]["completed_tasks"], ["T003", "T004"])
        self.assertEqual(result["request_accounting"]["total_activity_posts"], 6)
        self.assertEqual(result["request_accounting"]["native_evaluation_runs"], 0)
        for language in ("en", "fr"):
            for filename in ("completion-roadmap.md", "backend-live-2026-10-20.md", "validation.md"):
                text = (root / "docs" / language / filename).read_text("utf-8")
                self.assertIn("authorized-release.json", text)
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [x] T003", roadmap)
            self.assertIn("- [x] T004", roadmap)
            self.assertIn("- [x] T013", roadmap)
            self.assertIn("- [x] T008", roadmap)
            self.assertEqual(roadmap.count("- [x] T"), 4)

    def test_native_sdk_portability_checks_do_not_claim_runtime_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-23"
        clone = json.loads((assets / "native-sdk-candidate.json").read_text("utf-8"))
        self.assertTrue(clone["official_cli_clone_completed"])
        self.assertTrue(clone["real_agent_workspace_created"])
        self.assertTrue(clone["integrated_authentication_preserved_in_clone"])
        self.assertFalse(clone["candidate_created"])
        self.assertFalse(clone["whole_parent_response_captured"])
        self.assertEqual(clone["question_submissions"], 0)
        self.assertEqual(clone["remote_content_writes"], 0)
        self.assertTrue(clone["active_cli_profile_restored"])
        packaging = json.loads((assets / "native-sdk-packaging.json").read_text("utf-8"))
        self.assertTrue(packaging["official_pack_executed"])
        self.assertEqual(packaging["pack_exit_code"], 1)
        self.assertFalse(packaging["zip_created"])
        self.assertTrue(packaging["clone_contains_two_real_knowledge_payloads"])
        self.assertEqual(packaging["knowledge_payload_sizes_bytes"], [163840, 8525])
        self.assertTrue(packaging["clone_unchanged"])
        self.assertEqual(packaging["cloud_operations"], 0)
        author = json.loads((assets / "native-sdk-author.json").read_text("utf-8"))
        self.assertEqual(author["pack_exit_code"], 1)
        self.assertEqual(author["zip_count"], 0)
        self.assertEqual(author["source_files_count"], 34)
        self.assertTrue(author["source_hashes_unchanged"])
        self.assertTrue(author["knowledge_bytes_and_extensions_preserved"])
        self.assertFalse(author["components_dropped"])
        self.assertFalse(author["yaml_edits"])
        self.assertFalse(author["runtime_or_acceptance_verified"])
        template = json.loads((assets / "native-sdk-template-candidate.json").read_text("utf-8"))
        self.assertEqual(template["source_component_count"], 26)
        self.assertEqual(template["exported_component_count"], 21)
        self.assertFalse(template["parent_routing_instructions_preserved_by_template"])
        self.assertFalse(template["inactive_action_preserved_by_template"])
        self.assertEqual(template["file_column_name"], "filedata")
        self.assertTrue(template["both_live_payload_hashes_match_clone"])
        self.assertTrue(template["existing_approved_connection_binding_resolved"])
        self.assertFalse(template["candidate_binding_verified"])
        self.assertTrue(template["original_parent_and_all_component_full_rows_unchanged"])
        self.assertTrue(template["pac_profile_restored"])
        self.assertEqual(template["service_content_writes"], 0)
        self.assertEqual(template["question_submissions"], 0)
        self.assertFalse(template["permissions_changed"])
        self.assertFalse(template["whole_parent_response_captured"])
        self.assertFalse(template["roadmap_complete"])
        staging_assets = root / "docs" / "assets" / "runtime-2026-10-24"
        failed = json.loads((staging_assets / "native-sdk-staging.json").read_text("utf-8"))
        self.assertEqual(failed["status"], "failed")
        self.assertFalse(failed["candidate_retained"])
        self.assertTrue(failed["no_candidate_exists_after_failure"])
        staging = json.loads(
            (staging_assets / "native-sdk-staging-corrected-name.json").read_text("utf-8")
        )
        self.assertEqual(staging["candidate_instances_created"], 1)
        self.assertTrue(staging["display_name_correction_reused_same_schema"])
        self.assertEqual(staging["candidate_component_count"], 21)
        self.assertEqual(staging["source_component_count"], 26)
        self.assertTrue(staging["routing_instruction_and_missing_component_reconstruction_pending"])
        self.assertEqual(staging["file_uploads_attempted"], 2)
        self.assertEqual(staging["file_hashes_verified"], 2)
        self.assertTrue(staging["connection_binding_verified"])
        self.assertEqual(staging["authenticationmode"], 2)
        self.assertEqual(staging["accesscontrolpolicy"], 2)
        self.assertEqual(staging["authenticationtrigger"], 1)
        self.assertTrue(staging["unpublished_independently_verified"])
        self.assertTrue(staging["original_rows_files_and_reference_unchanged"])
        self.assertTrue(staging["pac_profile_restored"])
        self.assertFalse(staging["sdk_ready"])
        self.assertEqual(staging["questions"], 0)
        self.assertEqual(staging["publish_attempts"], 0)
        self.assertEqual(staging["permission_changes"], 0)
        self.assertFalse(staging["roadmap_complete"])
        reconstruction = json.loads(
            (staging_assets / "native-sdk-reconstruction.json").read_text("utf-8")
        )
        self.assertEqual(reconstruction["source_component_coverage"], 26)
        self.assertEqual(reconstruction["existing_candidate_components_mapped"], 21)
        self.assertEqual(reconstruction["missing_component_definitions_reconstructed"], 5)
        self.assertTrue(reconstruction["instructions_exact_after_internal_reference_normalization"])
        self.assertTrue(reconstruction["schema_validation_passed"])
        self.assertEqual(reconstruction["schema_validated_definition_count"], 24)
        self.assertEqual(reconstruction["schema_warning_count"], 1)
        self.assertTrue(reconstruction["projected_operation_result_matches_all_26_desired_rows"])
        self.assertTrue(reconstruction["source_clone_hashes_unchanged"])
        self.assertTrue(reconstruction["both_knowledge_payload_hashes_verified_locally"])
        self.assertTrue(reconstruction["inactive_diagnostic_state_encoded"])
        self.assertTrue(reconstruction["entra_controls_preserved_locally"])
        self.assertEqual(reconstruction["component_ids_reserved_not_created"], 5)
        self.assertEqual(reconstruction["cloud_writes_executed"], 0)
        self.assertFalse(reconstruction["publish_attempted"])
        self.assertFalse(reconstruction["remote_reconstruction_verified"])
        self.assertFalse(reconstruction["runtime_acceptance_verified"])
        self.assertTrue(
            reconstruction["requires_manage_preflight_atomic_execution_and_independent_postflight"]
        )

    def test_native_root_concurrency_guard_blocks_writes_and_sdk_capture(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-24"
        apply = json.loads((assets / "native-sdk-managed-apply.json").read_text("utf-8"))
        self.assertEqual(apply["status"], "blocked_preflight_stale_candidate_root_etag")
        self.assertFalse(apply["atomic_changeset_submitted"])
        self.assertEqual(apply["content_writes"], 0)
        self.assertEqual(apply["candidate_component_count"], 21)
        self.assertEqual(apply["reserved_components_still_absent"], 5)
        self.assertTrue(apply["candidate_unpublished"])
        self.assertTrue(apply["auth_controls_verified"])
        self.assertTrue(apply["candidate_components_match_author_preconditions"])
        self.assertTrue(apply["only_background_sync_root_fields_differ"])
        self.assertTrue(apply["source_parent_and_all_component_full_rows_unchanged"])
        self.assertTrue(apply["source_and_candidate_file_hashes_verified"])
        self.assertTrue(apply["source_binding_unchanged"])
        self.assertEqual(apply["permission_changes"], 0)
        self.assertEqual(apply["publish_attempts"], 0)
        capture = json.loads((assets / "native-sdk-capture.json").read_text("utf-8"))
        self.assertEqual(capture["question_submissions"], 0)
        self.assertEqual(capture["activities_captured"], 0)
        self.assertEqual(capture["completion_events_observed"], [])
        self.assertFalse(capture["final_answer_captured"])
        self.assertEqual(capture["application_or_grant_writes"], 0)
        self.assertEqual(capture["temporary_scope_tokens_created"], 0)
        self.assertEqual(capture["existing_tokens_or_refresh_tokens_removed"], 0)
        self.assertFalse(capture["roadmap_complete"])
        reconciled = json.loads(
            (assets / "native-sdk-managed-apply-reconciled.json").read_text("utf-8")
        )
        self.assertEqual(reconciled["status"], "applied_verified_unpublished")
        self.assertTrue(reconciled["root_reconciliation_allowlisted_and_stable"])
        self.assertTrue(reconciled["atomic_changeset_submitted"])
        self.assertEqual(reconciled["subresponse_codes"], [204] * 14)
        self.assertEqual(reconciled["candidate_component_count"], 26)
        self.assertTrue(reconciled["fidelity_passed"])
        self.assertTrue(reconciled["source_full_rows_unchanged"])
        self.assertEqual(reconciled["file_hashes_verified"], 4)
        self.assertTrue(reconciled["binding_verified"])
        self.assertTrue(reconciled["auth_controls_preserved"])
        self.assertFalse(reconciled["published"])
        self.assertEqual(reconciled["questions"], 0)
        self.assertFalse(reconciled["permissions_changed"])
        pending_capture = json.loads(
            (assets / "native-sdk-capture-reconciled.json").read_text("utf-8")
        )
        self.assertEqual(pending_capture["question_submissions"], 0)
        self.assertFalse(pending_capture["final_answer_captured"])
        self.assertFalse(pending_capture["completion_event_observed"])
        self.assertFalse(pending_capture["permission_changes"])

    def test_candidate_publication_requires_api_proof_and_does_not_imply_sdk_capture(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-24"
        published = json.loads((assets / "native-sdk-publish-confirmed.json").read_text("utf-8"))
        self.assertEqual(published["official_pac_exit_code"], 1)
        self.assertTrue(published["cli_status_parser_failed"])
        self.assertEqual(published["api_publish_result"], "Succeeded")
        self.assertTrue(published["published_timestamp_verified"])
        self.assertTrue(published["candidate_only"])
        self.assertEqual(published["candidate_component_count"], 26)
        self.assertTrue(published["auth_access_trigger_preserved"])
        self.assertTrue(published["source_full_rows_and_file_hashes_unchanged"])
        self.assertTrue(published["bindings_unchanged"])
        self.assertEqual(published["question_submissions"], 0)
        self.assertTrue(published["temporary_grant_and_manifest_exactly_restored"])
        self.assertTrue(published["existing_access_and_refresh_entries_retained"])
        self.assertTrue(published["pac_profile_restored"])
        self.assertFalse(published["roadmap_complete"])
        capture = json.loads((assets / "native-sdk-capture-owned-client.json").read_text("utf-8"))
        self.assertEqual(capture["status"], "blocked")
        self.assertFalse(capture["owned_client_caller_verified"])
        self.assertEqual(capture["question_submissions"], 0)
        self.assertEqual(capture["question_retries"], 0)
        self.assertEqual(capture["start_activity_count"], 0)
        self.assertEqual(capture["turn_activity_counts"], [])
        self.assertTrue(capture["grant_exactly_restored"])
        self.assertTrue(capture["app_permissions_exactly_restored"])
        self.assertTrue(capture["original_access_entries_retained"])
        self.assertTrue(capture["refresh_entries_retained"])
        self.assertEqual(capture["restoration_error_count"], 0)
        self.assertFalse(capture["dynamic_plan_finished_observed"])
        self.assertTrue(capture["whole_parent_completion_not_inferred_from_silence"])
        self.assertFalse(capture["roadmap_complete"])

    def test_sdk_consent_diagnostic_uses_verified_profile_and_closes_expired_callback(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-24"
        diagnostic = json.loads((assets / "native-sdk-auth-diagnostic.json").read_text("utf-8"))
        self.assertEqual(diagnostic["silent_with_error_attempts"], 1)
        self.assertEqual(diagnostic["silent_result"]["error_codes"], [65001])
        self.assertEqual(diagnostic["silent_result"]["suberror"], "consent_required")
        self.assertFalse(diagnostic["silent_result"]["claims_challenge_present"])
        self.assertEqual(diagnostic["browser_attempts"][0]["prompt"], "none")
        self.assertEqual(diagnostic["browser_attempts"][0]["result"]["error"], "consent_required")
        self.assertEqual(diagnostic["browser_attempts"][1]["result"], "no_callback_before_bound")
        self.assertTrue(diagnostic["verified_admin_edge_profile_used"])
        self.assertFalse(diagnostic["cookies_or_session_databases_read"])
        self.assertFalse(diagnostic["tokens_or_auth_codes_logged"])
        capture = json.loads((assets / "native-sdk-capture-recovered.json").read_text("utf-8"))
        self.assertEqual(capture["actual_auth_error"], "AADSTS65001")
        self.assertEqual(capture["sdk_service_requests_sent"], 0)
        self.assertEqual(capture["question_submissions"], 0)
        self.assertFalse(capture["normal_interactive_callback_observed"])
        self.assertTrue(capture["loopback_listener_closed"])
        self.assertTrue(capture["right_admin_profile_verified_from_metadata"])
        self.assertTrue(capture["grant_and_manifest_final_get_match_baseline"])
        self.assertTrue(capture["original_access_entries_retained"])
        self.assertTrue(capture["refresh_entries_retained"])
        self.assertTrue(capture["candidate_publication_confirmed"])
        self.assertTrue(capture["candidate_auth_access_trigger_preserved"])
        self.assertTrue(capture["source26_full_rows_unchanged"])
        self.assertTrue(capture["source_and_candidate_file_hashes_verified"])
        self.assertTrue(capture["binding_preserved"])
        self.assertTrue(capture["pac_profile_1_active"])
        self.assertEqual(capture["restoration_error_count"], 0)
        self.assertFalse(capture["dynamic_plan_finished_observed"])
        self.assertFalse(capture["roadmap_complete"])

    def test_invoke_auth_success_does_not_promote_typing_to_completed_capture(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-auth-consent-recovery-final.json").read_text("utf-8"))
        self.assertTrue(result["resource_client_account_scope_mapping_verified"])
        self.assertGreaterEqual(result["grant_retention_seconds"], 300)
        self.assertEqual(result["force_refresh_probes"], 1)
        self.assertTrue(result["verified_invoke_token_acquired"])
        self.assertEqual(result["same_public_api_constructed_extra_scopes"],
                         ["offline_access", "openid", "profile"])
        self.assertTrue(result["scope_construction_is_not_original_http_capture"])
        self.assertTrue(result["oidc_scope_causation_not_assumed"])
        self.assertFalse(result["plain_oauth_fallback_needed"])
        self.assertEqual(result["sdk_start_activity_count"], 1)
        self.assertEqual(result["question_submissions"], 0)
        self.assertFalse(result["whole_parent_completion_observed"])
        self.assertTrue(result["all_current_user_grants_exactly_restored"])
        self.assertTrue(result["manifest_exactly_restored"])
        self.assertTrue(result["maker_and_valid_refresh_entries_retained"])
        self.assertTrue(result["candidate26_and_original_source_preserved"])
        self.assertTrue(result["pac_profile_1_verified"])
        self.assertEqual(result["unresolved_permission_restoration_errors"], 0)
        self.assertTrue(result["expired_tab_cleanup_unverifiable"])
        self.assertFalse(result["roadmap_complete"])

    def test_header_aware_parent_capture_exposes_runtime_connector_blocker(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-24"
        start = json.loads((assets / "native-sdk-start-diagnostic.json").read_text("utf-8"))
        capture = json.loads((assets / "native-sdk-capture-start-recovered.json").read_text("utf-8"))
        self.assertTrue(start["server_conversation_header_observed"])
        self.assertFalse(start["start_emit_event"])
        self.assertFalse(start["greeting_acceptance"])
        self.assertEqual(start["start_stream_status"], "closed_normally")
        self.assertTrue(start["start_iterator_closed"])
        self.assertTrue(start["non_activity_sse_visibility_limited_by_sdk"])
        self.assertEqual(capture["http_statuses"], [200, 200, 200])
        self.assertTrue(capture["server_conversation_header_verified"])
        self.assertEqual(capture["question_submissions"], 2)
        self.assertEqual(capture["question_retries"], 0)
        self.assertEqual(capture["turn_stream_statuses"], ["closed_normally"] * 2)
        self.assertTrue(capture["hello_readiness_text_captured"])
        self.assertTrue(capture["sar_response_adaptive_card_captured"])
        self.assertTrue(capture["runtime_user_connector_connection_required"])
        self.assertFalse(capture["connect_or_continue_invoked"])
        self.assertFalse(capture["sar_domain_answer_captured"])
        self.assertEqual(capture["actual_sar_event_names"], [
            "DynamicPlanReceived", "DynamicPlanStepTriggered", "DynamicPlanStepBindUpdate",
        ])
        self.assertFalse(capture["dynamic_plan_finished_observed"])
        self.assertEqual(capture["source_quote_comparisons_performed"], 0)
        self.assertFalse(capture["sdk_transport_error_observed"])
        self.assertTrue(capture["initial_text_only_assertion_preserved_and_reclassified"])
        self.assertTrue(capture["permission_manifest_and_all_current_user_grants_exactly_restored"])
        self.assertEqual(capture["temporary_invoke_access_tokens_removed"], 1)
        self.assertTrue(capture["maker_access_and_valid_refresh_entries_retained"])
        self.assertTrue(capture["source_candidate_files_bindings_auth_preserved"])
        self.assertTrue(capture["pac_profile_1_verified"])
        self.assertTrue(capture["two_case_capture_is_not_full_acceptance"])
        self.assertFalse(capture["roadmap_complete"])

    def test_connector_auth_stops_before_unverified_website_account_action(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-connector-authorization.json").read_text("utf-8"))
        self.assertEqual(result["status"], "blocked_before_connect")
        self.assertEqual(result["boundary_code"], "ADMIN_WEBSITE_SESSION_NOT_VERIFIED_VIA_UIA")
        for key in (
            "connect_navigation_count", "connect_submissions", "continue_submissions",
            "fresh_question_submissions", "question_retries", "temporary_permission_changes",
            "publication_attempts", "cloud_write_requests", "verification_error_count",
            "rollback_error_count",
        ):
            with self.subTest(key=key):
                self.assertEqual(result[key], 0)
        for key in (
            "owned_app_and_all_current_user_grants_exact_baseline",
            "source_root_and_all26_full_rows_exactly_unchanged",
            "candidate26_definitions_states_refs_and_published_auth_preserved",
            "all_four_file_hashes_and_approved_bindings_verified",
            "owned_dpapi_cache_bytes_unchanged_this_phase",
            "maker_access_and_valid_refresh_entries_not_modified",
            "pac_profile_1_verified", "manual_admin_session_verification_required",
        ):
            with self.subTest(key=key):
                self.assertTrue(result[key])
        self.assertFalse(result["whole_parent_completion_observed"])
        self.assertFalse(result["domain_answer_observed"])
        self.assertFalse(result["roadmap_complete"])

    def test_scoped_visual_connector_check_preserves_identity_boundary(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-connector-visual-verification.json").read_text("utf-8"))
        self.assertEqual(result["boundary_code"],
                         "ADMIN_IDENTITY_NOT_VISIBLE_IN_SCOPED_PRINTWINDOW_CAPTURE")
        self.assertTrue(result["window_scoped_image_inspected"])
        self.assertFalse(result["visual_identity_verified"])
        self.assertTrue(result["original_window_minimized_state_independently_verified"])
        for key in ("connect_submissions", "continue_submissions", "fresh_question_submissions",
                    "temporary_permission_changes", "cloud_write_requests", "rollback_error_count"):
            with self.subTest(key=key):
                self.assertEqual(result[key], 0)
        self.assertTrue(result["source_root_and_all26_full_rows_exactly_unchanged"])
        self.assertTrue(result["owned_dpapi_cache_bytes_unchanged_this_phase"])
        self.assertTrue(result["manual_admin_session_verification_required"])
        self.assertFalse(result["roadmap_complete"])

    def test_azure_refresh_scopes_cost_and_matches_deployed_model_quota(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "azure-preflight-refresh.json").read_text("utf-8"))
        self.assertTrue(result["azure_extension_admin_tenant_verified"])
        self.assertTrue(result["azure_cli_admin_tenant_verified"])
        self.assertTrue(result["extension_and_cli_contexts_verified_separately"])
        self.assertFalse(result["browser_website_identity_verified"])
        self.assertEqual(result["retained_arm_resource_count"], 4)
        self.assertEqual(sum(result["resource_types"].values()), 4)
        self.assertEqual(len(result["registered_providers"]), 4)
        self.assertTrue(result["insights_case_sensitive_list_filter_omission_resolved_by_explicit_get"])
        self.assertEqual(result["foundry_region"], "swedencentral")
        self.assertTrue(result["foundry_disable_local_auth"])
        self.assertTrue(result["search"]["disable_local_auth"])
        self.assertEqual(result["search"]["status"], "running")
        self.assertEqual(result["search"]["replicas"], 1)
        self.assertEqual(result["search"]["partitions"], 1)
        self.assertEqual(len(result["deployments"]), 2)
        for deployment in result["deployments"]:
            with self.subTest(model=deployment["model"]):
                self.assertEqual(deployment["provisioning_state"], "Succeeded")
                self.assertEqual(deployment["capacity"], deployment["quota_current"])
                self.assertEqual(deployment["quota_headroom"],
                                 deployment["quota_limit"] - deployment["quota_current"])
                self.assertGreater(deployment["quota_headroom"], 0)
        self.assertEqual(result["deployments"][0]["quota_meter"], "OpenAI.Standard.gpt4.1-mini")
        self.assertEqual(result["deployments"][0]["quota_current"], 26)
        self.assertEqual(result["deployments"][0]["quota_limit"], 5000)
        cost = result["cost"]
        self.assertEqual(cost["currency"], "USD")
        self.assertEqual(cost["reported_pretax_cost"], 7.650361288)
        self.assertEqual(cost["reported_search_cost"], 7.373)
        self.assertFalse(cost["unrelated_subscription_costs_included"])
        self.assertFalse(cost["next_link_present"])
        self.assertTrue(cost["reporting_may_lag"])
        self.assertFalse(cost["is_final_invoice"])
        self.assertFalse(cost["is_copilot_credit_total"])
        for key in ("model_inference_calls", "new_agent_questions", "cloud_configuration_writes",
                    "role_or_policy_changes", "provider_registration_writes",
                    "billing_configuration_changes", "resource_deletions"):
            with self.subTest(key=key):
                self.assertEqual(result[key], 0)
        self.assertFalse(result["numeric_budget_approved"])
        self.assertFalse(result["tenant_credit_allocation_verified"])
        licenses = result["maker_license_read"]
        self.assertTrue(licenses["graph_me_admin_object_id_and_upn_verified"])
        self.assertEqual(licenses["license_detail_record_count"], 4)
        self.assertEqual(licenses["filtered_maker_related_plan_count"], 7)
        self.assertEqual(licenses["filtered_plan_provisioning_statuses"], ["Success"])
        self.assertEqual(licenses["additional_grants_requested"], 0)
        self.assertFalse(licenses["full_standard_harness_entitlement_proven"])
        self.assertFalse(licenses["tenant_credit_allocation_proven"])
        self.assertFalse(licenses["environment_pay_as_you_go_binding_proven"])
        self.assertFalse(result["full_lab0_acceptance"])
        self.assertFalse(result["roadmap_complete"])

    def test_foreground_guard_does_not_capture_an_unrelated_window(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-connector-foreground-verification.json").read_text("utf-8"))
        self.assertEqual(result["boundary_code"], "OTHER_WINDOW_FOREGROUND_SHARED_DESKTOP_GUARD")
        self.assertTrue(result["another_window_was_foreground"])
        for key in ("foreground_guard_passed", "screen_capture_taken", "target_window_changed",
                    "unrelated_window_inspected_or_captured", "foreground_takeover_attempted",
                    "visual_identity_verified", "whole_parent_completion_observed",
                    "domain_answer_observed", "roadmap_complete"):
            with self.subTest(key=key):
                self.assertFalse(result[key])
        for key in ("connect_submissions", "continue_submissions", "fresh_question_submissions",
                    "cloud_write_requests", "temporary_permission_changes", "rollback_error_count"):
            with self.subTest(key=key):
                self.assertEqual(result[key], 0)
        self.assertTrue(result["source_root_and_all26_full_rows_exactly_unchanged"])
        self.assertTrue(result["owned_dpapi_cache_bytes_unchanged_this_phase"])

    def test_focus_success_is_not_website_identity_or_connector_success(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-connector-focus-request.json").read_text("utf-8"))
        self.assertEqual(result["boundary_code"],
                         "FOCUS_SUCCEEDED_ACCOUNT_INVOKE_UNSUPPORTED_CAPTURE_BOUNDS_REJECTED")
        for key in ("foreground_request_occurred", "foreground_request_succeeded",
                    "actual_foreground_was_verified_target", "target_was_visible_nonminimized",
                    "original_target_minimized_state_verified_restored",
                    "source_root_and_all26_full_rows_exactly_unchanged",
                    "owned_dpapi_cache_bytes_unchanged_this_phase",
                    "manual_admin_session_verification_required"):
            with self.subTest(key=key):
                self.assertTrue(result[key])
        for key in ("account_menu_invoke_pattern_supported", "account_region_bounds_guard_passed",
                    "screenshot_taken", "whole_parent_completion_observed",
                    "domain_answer_observed", "roadmap_complete"):
            with self.subTest(key=key):
                self.assertFalse(result[key])
        for key in ("connect_submissions", "continue_submissions", "fresh_question_submissions",
                    "cloud_write_requests", "temporary_permission_changes",
                    "verification_error_count", "rollback_error_count"):
            with self.subTest(key=key):
                self.assertEqual(result[key], 0)

    def test_storage_rbac_does_not_override_enforced_network_boundary(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "lab5-blob-ingestion.json").read_text("utf-8"))
        self.assertEqual(result["status"], "execution_failed")
        self.assertEqual(result["storage_public_network_access_readback"], "Disabled")
        self.assertTrue(result["storage_public_network_modify_policy_activity_observed"])
        self.assertEqual(result["upload_http_status"], 403)
        self.assertEqual(result["bounded_upload_attempts"], 25)
        self.assertTrue(result["rbac_alone_does_not_override_disabled_public_networking"])
        self.assertEqual(result["completed_tests"], [])
        self.assertFalse(result["indexer_executed"])
        self.assertEqual(result["policy_exemptions_created"], 0)
        self.assertEqual(result["model_inference_calls"], 0)
        self.assertTrue(result["temporary_storage_account_absence_verified"])
        self.assertTrue(result["all_original_search_objects_roles_and_arm_inventory_verified_unchanged"])
        self.assertEqual(result["cleanup_error_count"], 0)

    def test_private_upload_is_not_indexer_acceptance_and_cleanup_failure_is_preserved(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "lab5-private-fictional-ingestion.json").read_text("utf-8"))
        self.assertEqual(result["completed_tests"], ["S5-01"])
        self.assertEqual(result["fixture_files"], ["forest.txt", "harbor.txt"])
        self.assertEqual(result["private_blob_roundtrip_count"], 2)
        self.assertTrue(result["private_keyless_storage_verified"])
        self.assertTrue(result["uploader_has_no_public_ip"])
        self.assertFalse(result["public_network_or_key_auth_policy_weakened"])
        self.assertFalse(result["indexer_executed"])
        self.assertEqual(result["initial_cleanup_error_count"], 2)
        self.assertTrue(result["initial_cleanup_errors_preserved"])
        self.assertEqual(result["cleanup_error_count"], 0)
        self.assertTrue(result["all_owned_temporary_resources_absence_verified"])
        self.assertFalse(result["connected_answer_proven"])
        self.assertFalse(result["citation_navigation_proven"])
        self.assertFalse(result["roadmap_complete"])

    def test_private_indexer_success_does_not_hide_vector_readback_failure(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "lab5-private-fictional-ingestion-retry.json").read_text("utf-8"))
        self.assertEqual(result["status"], "execution_failed")
        self.assertEqual(result["completed_tests"], ["S5-01"])
        self.assertTrue(result["private_keyless_storage_verified"])
        self.assertTrue(result["owned_shared_private_link_approved_and_ready"])
        self.assertEqual(result["indexer_execution_environment"], "private")
        self.assertEqual(result["indexer_status"], "success")
        self.assertEqual(result["indexer_items_processed"], 2)
        self.assertEqual(result["indexer_items_failed"], 0)
        self.assertEqual(result["indexer_warning_count"], 0)
        self.assertEqual(result["document_readback_http_status"], 400)
        self.assertFalse(result["readable_chunk_and_vector_verification_completed"])
        self.assertTrue(result["successful_indexer_is_not_full_s5_02_without_readable_chunks"])
        self.assertTrue(result["all_owned_temporary_resources_absence_verified"])
        self.assertTrue(result["original_search_objects_roles_shared_links_and_arm_inventory_preserved"])
        self.assertEqual(result["cleanup_error_count"], 0)
        self.assertFalse(result["public_network_or_key_auth_policy_weakened"])
        self.assertFalse(result["roadmap_complete"])

    def test_private_ingestion_requires_exact_chunks_vectors_and_final_cleanup(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "lab5-private-fictional-ingestion-vector-readback.json").read_text("utf-8"))
        self.assertEqual(result["status"], "scoped_private_ingestion_passed")
        self.assertEqual(result["completed_tests"], ["S5-01", "S5-02"])
        self.assertEqual(result["fixture_files"], ["forest.txt", "harbor.txt"])
        self.assertTrue(result["original_fictional_text_only"])
        self.assertFalse(result["protected_documents_used"])
        self.assertTrue(result["private_keyless_storage_verified"])
        self.assertTrue(result["uploader_has_no_public_ip"])
        self.assertEqual(result["private_blob_roundtrip_count"], 2)
        self.assertTrue(result["owned_shared_private_link_approved_and_ready"])
        self.assertEqual(result["indexer_execution_environment"], "private")
        self.assertEqual(result["indexer_status"], "success")
        self.assertEqual(result["indexer_items_processed"], 2)
        self.assertEqual(result["indexer_items_failed"], 0)
        self.assertEqual(result["indexer_warning_count"], 0)
        self.assertEqual(result["indexed_child_chunks"], 2)
        self.assertTrue(result["exact_passages_and_real_1536_dimension_vectors_verified"])
        self.assertTrue(result["prior_expired_token_failure_preserved_privately"])
        self.assertEqual(result["prior_authentication_cleanup_errors"], 16)
        self.assertTrue(result["supported_cli_authentication_recovery_used"])
        self.assertTrue(result["resumed_without_redeploy_or_reupload"])
        self.assertTrue(result["all_owned_temporary_resources_absence_verified"])
        self.assertTrue(result["original_search_objects_roles_shared_links_and_arm_inventory_preserved"])
        self.assertEqual(result["cleanup_error_count"], 0)
        self.assertFalse(result["public_network_or_key_auth_policy_weakened"])
        self.assertFalse(result["full_lab_acceptance"])
        self.assertFalse(result["roadmap_complete"])
        for language in ("en", "fr"):
            guide = (root / "docs" / language / "lab-05.md").read_text("utf-8")
            for test_id in result["completed_tests"]:
                row = next(line for line in guide.splitlines() if line.startswith(f"| {test_id} "))
                self.assertIn("Pass:" if language == "en" else "Réussi :", row)

    def test_entra_openai_action_is_not_native_prompt_byom_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "byom-authentication-contracts.json").read_text("utf-8"))
        self.assertEqual(result["foundry_inference"]["documented_authentication_types"], ["Default"])
        self.assertEqual(result["foundry_inference"]["required_connection_fields"], ["Target Uri", "API Key"])
        self.assertFalse(result["foundry_inference"]["documented_entra_alternative"])
        connector = result["azure_openai"]
        self.assertEqual(connector["documented_entra_auth_id"], "oauth")
        self.assertFalse(connector["entra_connection_shareable"])
        self.assertEqual(connector["managed_identity_applicability"], "LOGICAPPS only")
        self.assertFalse(connector["native_prompt_byom_compatibility_proven"])
        self.assertTrue(result["native_prompt"]["chat_completions_endpoint_required"])
        self.assertFalse(result["native_prompt"]["native_dialog_reinspected"])
        for key in ("connection_created", "connector_action_executed", "agent_or_prompt_modified",
                    "policy_or_role_changed", "substitute_or_exclusion_approved",
                    "native_byom_acceptance_passed", "roadmap_complete"):
            with self.subTest(key=key):
                self.assertFalse(result[key])
        for language in ("en", "fr"):
            guide = (root / "docs" / language / "lab-04.md").read_text("utf-8")
            self.assertIn("byom-authentication-contracts.json", guide)
            self.assertIn("https://learn.microsoft.com/en-us/connectors/azureopenai/", guide)

    def test_verified_browser_identity_does_not_promote_failed_connector_create(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-browser-page-recovery.json").read_text("utf-8"))
        self.assertTrue(result["website_admin_upn_verified"])
        self.assertTrue(result["website_target_environment_route_verified"])
        self.assertFalse(result["edge_profile_label_verified"])
        self.assertFalse(result["manual_admin_session_verification_required"])
        self.assertEqual(result["supported_browser_attempts"], 1)
        self.assertEqual(result["connect_navigation_count"], 1)
        self.assertEqual(result["connector_create_submissions"], 1)
        self.assertEqual(result["cloud_write_requests"], 1)
        self.assertEqual(result["observed_connector_error"], "Unable to sign in. Please try again.")
        self.assertFalse(result["observed_connection_success"])
        self.assertEqual(result["continue_submissions"], 0)
        self.assertEqual(result["fresh_sar_submissions"], 0)
        self.assertEqual(result["runtime_events_this_attempt"], [])
        self.assertFalse(result["consent_accepted"])
        for key in ("owned_app_and_all_current_user_grants_exact_baseline",
                    "source_root_and_all26_full_rows_exactly_unchanged",
                    "candidate26_definitions_states_refs_and_published_auth_preserved",
                    "all_four_file_hashes_and_approved_bindings_verified",
                    "owned_dpapi_cache_bytes_unchanged_this_phase", "pac_profile_1_verified"):
            with self.subTest(key=key):
                self.assertTrue(result[key])
        self.assertEqual(result["verification_error_count"], 0)
        self.assertEqual(result["rollback_error_count"], 0)
        self.assertFalse(result["whole_parent_completion_observed"])
        self.assertFalse(result["domain_answer_observed"])
        self.assertFalse(result["roadmap_complete"])

    def test_signin_audit_absence_does_not_prove_runtime_authorization(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-connector-signin-audit.json").read_text("utf-8"))
        self.assertEqual(result["graph_api_version"], "v1.0")
        self.assertTrue(result["existing_authorization_only"])
        self.assertEqual([q["returned_events"] for q in result["queries"]], [0, 4, 0])
        self.assertEqual(result["queries"][1]["reported_error_codes"], [0] * 4)
        self.assertTrue(all(not q["more_results"] for q in result["queries"]))
        self.assertEqual(result["queries"][2]["additional_filter"], "isInteractive eq false")
        self.assertTrue(result["no_returned_event_is_not_proof_of_no_authentication_attempt"])
        self.assertTrue(result["logging_latency_and_query_scope_limit_inference"])
        self.assertTrue(result["popup_blocking_not_proven"])
        self.assertEqual(result["root_cause"], "unclassified")
        for key in ("new_connector_submissions", "continue_submissions", "new_questions",
                    "permission_or_policy_changes"):
            self.assertEqual(result[key], 0)
        self.assertFalse(result["beta_api_used"])
        self.assertFalse(result["runtime_connector_authorization_proven"])
        self.assertFalse(result["roadmap_complete"])
        for language in ("en", "fr"):
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("native-connector-signin-audit.json", roadmap)

    def test_trusted_browser_click_does_not_promote_failed_signin(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-trusted-click-recovery.json").read_text("utf-8"))
        self.assertTrue(result["page_reloaded_before_submission"])
        self.assertEqual(result["public_oidc_metadata_status"], 200)
        self.assertEqual(result["public_oidc_request_credentials"], "omit")
        self.assertTrue(result["trusted_click"]["isTrusted"])
        self.assertTrue(result["trusted_click"]["userActivationActive"])
        self.assertEqual(result["connect_submissions"], 1)
        self.assertIsNone(result["cloud_write_requests"])
        self.assertTrue(result["automatic_deletion_ui_observed"])
        self.assertFalse(result["automatic_deletion_http_status_or_absence_verified"])
        listing = result["subsequent_current_user_connection_listing"]
        self.assertTrue(listing["target_environment_route_verified"])
        self.assertEqual(listing["foundry_connection_rows"], 1)
        self.assertTrue(listing["only_foundry_row_connected"])
        self.assertFalse(listing["additional_foundry_row_observed"])
        self.assertTrue(listing["exact_attempt_connection_id_not_available"])
        self.assertTrue(result["temporary_click_diagnostic_removed"])
        self.assertFalse(result["runtime_connection_success_observed"])
        self.assertEqual(result["observed_connector_error"], "Unable to sign in. Please try again.")
        self.assertEqual(result["root_cause"], "unclassified")
        self.assertTrue(result["network_errors_not_established_as_signin_cause"])
        for key in ("continue_submissions", "fresh_question_submissions",
                    "temporary_permission_changes", "publication_attempts",
                    "verification_error_count", "rollback_error_count"):
            self.assertEqual(result[key], 0)
        for key in ("owned_app_and_all_current_user_grants_exact_baseline",
                    "source_root_and_all26_full_rows_exactly_unchanged",
                    "candidate26_definitions_states_refs_and_published_auth_preserved",
                    "all_four_file_hashes_and_approved_bindings_verified",
                    "owned_dpapi_cache_bytes_unchanged_this_phase", "pac_profile_1_verified"):
            self.assertTrue(result[key])
        self.assertFalse(result["roadmap_complete"])

    def test_native_studio_association_recovers_delivery_not_source_fidelity(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-studio-existing-connection.json").read_text("utf-8"))
        self.assertEqual(result["channel"], "pva-studio")
        self.assertTrue(result["website_required_administrator_verified"])
        self.assertEqual(result["user_connection_status_before"], "Not Connected")
        self.assertTrue(result["existing_connection_picker_offered"])
        self.assertTrue(result["existing_approved_connection_selected"])
        self.assertEqual(result["existing_connection_association_submissions"], 1)
        self.assertEqual(result["new_connection_creates"], 0)
        self.assertEqual(result["new_oauth_flows"], 0)
        self.assertEqual(result["permission_or_policy_changes"], 0)
        self.assertEqual(result["question_submissions_after_association"], 1)
        self.assertEqual(result["rendered_domain_answer_messages"], 3)
        self.assertFalse(result["connection_card_present_at_capture"])
        comparisons = result["source_comparisons"]
        self.assertEqual([c["quoted_passages"] for c in comparisons], [9, 6, 0])
        self.assertEqual([c["exact_source_matches"] for c in comparisons], [7, 5, 0])
        self.assertEqual([c["mismatch_count"] for c in comparisons], [2, 1, 0])
        self.assertTrue(comparisons[2]["zero_quoted_passages_is_not_a_source_fidelity_pass"])
        self.assertFalse(result["source_fidelity_acceptance"])
        self.assertFalse(result["retrieval_membership_independently_proven"])
        self.assertFalse(result["protocol_plan_finished_event_captured"])
        self.assertFalse(result["published_channel_authorization_retested"])
        self.assertFalse(result["source_text_or_raw_answers_published"])
        self.assertFalse(result["roadmap_complete"])

    def test_verified_invocations_delivery_preserves_auth_and_native_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "verified-invocations-delivery.json").read_text("utf-8"))
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["active_hosted_version"], "5")
        self.assertEqual(result["new_immutable_versions_created"], 2)
        self.assertEqual(result["local_service_tests_passed"], 54)
        self.assertEqual(result["actual_protocols"], ["activity", "invocations"])
        self.assertEqual(result["actual_authorization_schemes"], ["Entra", "BotServiceRbac"])
        self.assertEqual(result["service_request_limits"],
                         {"question_characters": 12000, "raw_body_bytes": 150000})
        controls = {case["case"]: case for case in result["hosted_controls"]}
        self.assertEqual(len(controls), 7)
        self.assertTrue(all(case["result"] == "PASS" for case in controls.values()))
        self.assertEqual(controls["unauthenticated"]["http_status"], 401)
        self.assertEqual(controls["openapi"]["http_status"], 200)
        for case, status in (("blank", 400), ("integer-parser-limit", 400), ("body-limit", 413)):
            self.assertEqual(controls[case]["http_status"], status)
            self.assertEqual(controls[case]["observed_downstream_responses_posts"], 0)
            self.assertTrue(controls[case]["model_invocation_excluded_by_session_logs"])
            self.assertTrue(controls[case]["reference_correlated"])
        self.assertTrue(controls["no-relevant-evidence"]["explicit_abstention"])
        self.assertFalse(controls["no-relevant-evidence"]["selection_invoked"])
        self.assertTrue(controls["activity_compatibility"]["exact_renderer_match"])
        self.assertEqual(result["activity_initial_missing_api_version_http_status"], 400)
        self.assertEqual(result["activity_corrected_required_query_parameter_http_status"], 200)
        self.assertEqual(result["doctor"], {"passed": 11, "failed": 0, "skipped": 2})
        for key in ("local_loopback_smoke_passed", "temporary_local_servers_stopped",
                    "hosted_original_case6_unchanged", "hosted_positive_exact_renderer_match",
                    "original_four_arm_resources_and_roles_preserved",
                    "original_hosted_identity_preserved",
                    "original_retriever_version4_definition_preserved",
                    "deployment_cli_timeout_preserved",
                    "deployment_timeout_followed_by_readonly_active_version_verification"):
            self.assertTrue(result[key])
        for key in ("native_pass", "full_native_matrix_pass", "published_sdk_authorization_resolved",
                    "anonymous_hosted_access_enabled", "redeploy_after_timeout", "roadmap_complete",
                    "retrieval_membership_payload_independently_fetched",
                    "source_text_raw_answers_tokens_or_private_identifiers_published"):
            self.assertFalse(result[key])
        self.assertEqual(result["new_native_questions"], 0)
        self.assertEqual(result["azure_policy_or_storage_networking_changes"], 0)
        self.assertEqual(result["additional_generated_evaluation_suite"], "deferred_user_unavailable")
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "backend-live-2026-10-20.md", "validation.md"):
                self.assertIn("verified-invocations-delivery.json",
                              (root / "docs" / language / name).read_text("utf-8"))

    def test_native_preservation_after_invocations_is_not_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-preservation-after-invocations.json").read_text("utf-8"))
        self.assertEqual(result["active_hosted_version"], "5")
        for key in ("owned_app_and_all_current_user_grants_exact_baseline",
                    "source_root_and_all26_full_rows_exactly_unchanged",
                    "candidate26_definitions_states_refs_and_published_auth_preserved",
                    "all_four_file_hashes_and_approved_bindings_verified",
                    "owned_dpapi_cache_bytes_unchanged_this_phase", "pac_profile_1_verified"):
            self.assertTrue(result[key])
        for key in ("verification_error_count", "rollback_error_count", "cloud_write_requests",
                    "fresh_question_submissions", "publication_attempts", "temporary_permission_changes"):
            self.assertEqual(result[key], 0)
        self.assertFalse(result["native_pass"])
        self.assertFalse(result["whole_parent_completion_observed"])
        self.assertFalse(result["roadmap_complete"])

    def test_native_followup_preserves_failed_grounding_and_clone_boundary(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        protocol = json.loads((assets / "native-protocol-followup.json").read_text("utf-8"))
        self.assertTrue(protocol["browserVisibilityRecovered"])
        self.assertTrue(protocol["exactExpectedWebsiteAdministratorVerified"])
        self.assertEqual(protocol["freshCatalogVisibleOperationCount"], 10)
        self.assertFalse(protocol["hostedInvocationsOrResponsesObservedInTenantCatalog"])
        self.assertFalse(protocol["backendOperationAbsenceProven"])
        self.assertFalse(protocol["candidateClone"]["completed"])
        self.assertFalse(protocol["candidateClone"]["agentFilesCreated"])
        self.assertEqual(protocol["configurationOrAuthorizationChanges"], 0)
        self.assertFalse(protocol["roadmapComplete"])
        navigation = json.loads((assets / "native-lab1-navigation.json").read_text("utf-8"))
        self.assertEqual(navigation["questionCount"], 1)
        self.assertTrue(navigation["unchangedOriginalInput"])
        self.assertEqual(navigation["criteria"]["displayedCitationPassageSupportsCTRThreshold"], "fail")
        self.assertEqual(navigation["criteria"]["originalLicensingPDFNavigation"], "not-assessed")
        self.assertFalse(navigation["preservation"]["originalParentInteraction"])
        self.assertFalse(navigation["preservation"]["agentConfigurationWrites"])
        self.assertTrue(all(value is False for value in navigation["completion"].values()))

    def test_supported_management_recovery_does_not_use_wrong_tenant(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "management-recovery.json").read_text("utf-8"))
        self.assertEqual(result["result"], "blocked")
        self.assertEqual(result["bundleFailure"]["missingDependency"], "@azure/msal-node-extensions")
        self.assertTrue(result["installedManagementInstructionsLocated"])
        self.assertTrue(result["unmodifiedManagementBundleInvoked"])
        self.assertTrue(result["pacCloneCapabilityConfirmed"])
        for key in ("scriptsPatchedOrMonkeyPatched", "pacActiveIdentityMatchesRequiredTenantAdministrator",
                    "pacAuthenticationChanged", "cloneUnderWrongIdentityAttempted",
                    "candidateCloneCompleted", "agentYamlCreated", "roadmapComplete"):
            self.assertFalse(result[key])
        self.assertEqual(result["configurationOrPermissionChanges"], 0)
        self.assertTrue(result["officialDependencyInstallAttempted"])
        self.assertTrue(result["offlineCacheInstallAttempted"])
        self.assertEqual(result["dependencyInstallResult"], "EALLOWREMOTE")
        self.assertEqual(result["packageSourceOrPolicyOverrides"], 0)
        self.assertFalse(result["nativeDependencyRecoveryCompleted"])

    def test_supported_auth_recovery_preserves_identity_and_stops_helpers(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "supported-auth-recovery.json").read_text("utf-8"))
        self.assertEqual(result["result"], "blocked")
        self.assertTrue(result["supported_plugin_update_completed"])
        self.assertTrue(result["plugin_already_latest"])
        self.assertEqual(result["documented_device_code_attempts"], 2)
        self.assertTrue(result["auth_helpers_stopped"])
        self.assertTrue(result["shared_browser_returned_to_agents_inventory"])
        self.assertTrue(result["original_pac_profiles_preserved_and_profile1_active"])
        self.assertFalse(result["new_verified_admin_profile_created"])
        self.assertFalse(result["candidate_clone_completed"])
        self.assertFalse(result["password_supplied"])
        self.assertFalse(result["mfa_or_consent_bypassed"])
        self.assertEqual(result["package_policy_overrides"], 0)
        self.assertEqual(result["agent_configuration_or_permission_changes"], 0)
        self.assertFalse(result["roadmap_complete"])

    def test_candidate_recovery_preserves_failure_and_exact_current_readback(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        recovery = json.loads((assets / "candidate-authoring-recovery.json").read_text("utf-8"))
        self.assertTrue(recovery["authentication"]["humanDeviceCodeSignInCompleted"])
        self.assertTrue(recovery["authentication"][
            "pacOrgWhoIndependentlyVerifiedRequestedAdministratorTenantAndEnvironment"])
        self.assertFalse(recovery["authentication"]["mfaConsentOrPackagePolicyBypassed"])
        self.assertFalse(recovery["authentication"]["pluginNativeDependencyRecovered"])
        management = recovery["supportedManagement"]
        self.assertTrue(management["officialPacCloneSucceeded"])
        self.assertTrue(management[
            "finalThreeAuthoringFilesExactlyMatchIndependentPersistedReadback"])
        self.assertEqual(management["correctedLookupPushChanges"], 3)
        self.assertEqual(management["broadSarInstructionPushChanges"], 1)
        self.assertFalse(management["published"])
        self.assertFalse(recovery["historicalFailure"]["intermediateCopyCauseEstablished"])
        first = json.loads((assets / "strict-lookups-native.json").read_text("utf-8"))
        self.assertEqual(first["result"], "fail")
        self.assertEqual(first["execution"]["actualQuestions"], 1)
        self.assertFalse(first["localEvidenceDiscrepancy"]["causeEstablished"])
        corrected = json.loads((assets / "corrected-lookups-native.json").read_text("utf-8"))
        self.assertEqual(corrected["result"], "pass")
        self.assertEqual(corrected["execution"]["questionOrder"], [2, 3, 1])
        self.assertEqual(corrected["execution"]["actualQuestions"], 3)
        self.assertEqual(corrected["execution"]["questionRetries"], 0)
        self.assertTrue(all(case["literalSendActivityRenderedTextMatched"]
                            for case in corrected["cases"]))
        self.assertFalse(corrected["completion"]["nativeFullElevenMatrix"])
        self.assertTrue(all(value is False for value in recovery["boundaries"].values()))

    def test_candidate_live_preservation_allows_only_two_topics_and_instructions(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "lookup-preservation.json").read_text("utf-8"))
        self.assertEqual(result["result"], "pass")
        self.assertTrue(all(result["checks"].values()))
        self.assertEqual(result["originalComponentCount"], 26)
        self.assertEqual(result["candidateComponentCount"], 28)
        self.assertEqual(result["ownedTopicAdditions"], 2)
        self.assertEqual(result["modifiedPreexistingComponents"], 1)
        self.assertEqual(result["cloudWritesDuringVerification"], 0)
        self.assertEqual(result["actionStates"], {
            "Workshopverifiedevidencediagnostic": "Off",
            "workshopretrievalspecialist": "On",
            "workshopvalidationspecialist": "On",
        })
        current = json.loads((assets / "broad-sar-corrected-native.json").read_text("utf-8"))
        self.assertEqual(result["authoringSha256"]["agent.mcs.yml"],
                         current["candidateVerification"]["agentSha256"])
        self.assertFalse(result["publicationPerformed"])
        self.assertFalse(result["wholeRoadmapComplete"])

    def test_broad_sar_correct_synthesis_does_not_erase_intermediate_failure(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "broad-sar-corrected-native.json").read_text("utf-8"))
        self.assertEqual(result["nativeUserSubmissions"], 1)
        self.assertEqual(result["automaticRetries"], 0)
        self.assertEqual(result["visibleAnswerMessages"], 2)
        self.assertEqual(result["route"]["verdict"], "PASS")
        self.assertTrue(result["route"]["complementaryLocalSearch"])
        self.assertFalse(result["route"]["narrowDeadlineTopicObserved"])
        self.assertEqual(result["wholeOutputCoverage"]["verdict"], "PASS")
        self.assertEqual(result["sourceVerification"]["totalQuotedExcerpts"], 16)
        self.assertEqual(result["sourceVerification"]["exactAndIndividuallyAttributed"], 15)
        self.assertEqual(result["verdicts"]["overall"], "FAIL")
        self.assertFalse(result["roadmapCompletionClaimed"])
        recovery = json.loads((assets / "candidate-authoring-recovery.json").read_text("utf-8"))
        emission = recovery["emissionInvestigation"]
        self.assertEqual(emission["operation"], "SendActivityV2")
        self.assertFalse(emission["supportedPerActionMessageSuppressionOrCaptureSwitchFound"])
        self.assertFalse(emission["unsupportedPropertiesAdded"])
        self.assertFalse(emission["rawSpecialistPayloadOrEmitterIdentityEstablished"])
        self.assertFalse(recovery["broadSar"]["originalProtectedRetrieverModified"])

    def test_final_current_lookup_regressions_are_exact_and_bounded(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "final-lookup-regressions.json").read_text("utf-8"))
        self.assertEqual(result["result"], "pass")
        self.assertEqual(result["execution"]["order"], [2, 3, 1])
        self.assertEqual(result["execution"]["actualUserInputs"], 3)
        self.assertEqual(result["execution"]["freshSessions"], 3)
        self.assertEqual(result["execution"]["modelPreflightQuestions"], 0)
        self.assertEqual(result["execution"]["questionRetries"], 0)
        self.assertTrue(result["comparison"]["wholeParentMessagesNotSelectedSubmessageProxy"])
        self.assertFalse(result["comparison"]["lexicalParaphraseAccepted"])
        preservation = json.loads((assets / "lookup-preservation.json").read_text("utf-8"))
        self.assertEqual(result["comparison"]["agentSha256"],
                         preservation["authoringSha256"]["agent.mcs.yml"])
        for case in result["cases"]:
            self.assertEqual(case["result"], "pass")
            self.assertEqual(case["submissions"], 1)
            self.assertTrue(case["wholeParentFinalResponseCompared"])
            self.assertTrue(case["literalRenderedTextMatched"])
            self.assertEqual(case["answerMessagesAfterUserInput"], 1)
            self.assertFalse(case["extraParaphraseMessageObserved"])
        self.assertFalse(result["limitations"]["broadSarRetested"])
        self.assertFalse(result["limitations"]["fullMatrixPassClaimed"])
        self.assertFalse(result["limitations"]["runtimeDynamicPlanFinishedClaimed"])
        self.assertFalse(result["limitations"]["wholeRoadmapComplete"])

    def test_mcp_preflight_is_not_a_connection_or_new_human_approval(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "mcp-onboarding-preflight.json").read_text("utf-8"))
        self.assertTrue(result["createModelContextProtocolOptionVisible"])
        self.assertTrue(result["streamableEndpointFieldVisible"])
        self.assertTrue(result["oauth2OptionVisible"])
        self.assertIn("Manual", result["oauthTypesVisible"])
        self.assertTrue(result["wizardCancelledWithLeaveConfirmation"])
        for key in ("credentialsEntered", "createSubmitted", "connectorOrConnectionCreated",
                    "newHumanDesignChoiceReceived", "unavailableFormCountedAsApproval",
                    "realOAuthOrNativeMcpDeliveryVerified", "roadmapComplete"):
            self.assertFalse(result[key])
        self.assertEqual(result["cloudResourcesProvisioned"], 0)
        self.assertEqual(result["nativeQuestionsSubmitted"], 0)

    def test_real_local_mcp_proof_retains_native_and_oauth_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "mcp-evidence-local.json").read_text("utf-8"))
        self.assertEqual(result["result"], "pass")
        self.assertTrue(result["officialMcpClientUsed"])
        self.assertTrue(result["protocolInitializeAndToolDiscoveryPassed"])
        self.assertTrue(result["unchangedOriginalQuestion"])
        self.assertEqual(result["originalCaseNumber"], 6)
        self.assertEqual(result["paidToolCalls"], 1)
        self.assertEqual(result["automaticRetries"], 0)
        self.assertEqual(result["recordIds"], ["rc-002", "ip-006"])
        self.assertEqual(result["recordCount"], len(result["recordIds"]))
        self.assertTrue(result["textExactlyMatchesDeterministicRenderer"])
        self.assertTrue(result["allStructuredRecordsExactlyMatchPinnedCorpus"])
        self.assertTrue(result["protectedRetrieverDefinitionUnchangedBeforeAndAfter"])
        self.assertTrue(result["loopbackOnly"])
        self.assertEqual(result["followupParserHardenedTransportAndAuthenticationTests"], 17)
        self.assertEqual(result["requestByteLimit"], 150000)
        self.assertTrue(result["exactRequestByteLimitAcceptedInProtocolTest"])
        self.assertTrue(result["requestByteLimitPlusOneRejectedInProtocolTest"])
        self.assertTrue(result["loopbackHelperStopped"])
        for key in ("remoteMcpDeployment", "realEntraMcpOAuthFlowVerified",
                    "nativeMcpCandidateBindingCreated", "nativeBroadSarFidelityRepaired",
                    "wholeRoadmapComplete"):
            self.assertFalse(result[key])

    def test_hosted_mcp_preflight_keeps_positive_oauth_and_native_gates_open(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-hosted-preflight.json").read_text("utf-8"))
        self.assertEqual(result["result"], "hosted-preflight-pass-delegated-sign-in-blocked")
        hosting = result["hosting"]
        self.assertEqual(hosting["runtime"], "PYTHON|3.13")
        self.assertEqual(hosting["noBearerHttpStatus"], 401)
        self.assertEqual(hosting["invalidBearerHttpStatus"], 401)
        self.assertEqual(hosting["protectedResourceDiscoveryHttpStatus"], 200)
        self.assertTrue(hosting["httpsOnly"])
        self.assertTrue(hosting["scmAndFtpBasicPublishingDisabled"])
        self.assertTrue(hosting["completeEntraSettingsReadBack"])
        self.assertTrue(hosting["managedIdentityCredentialExplicitlyConfigured"])
        self.assertEqual(hosting["newManagedIdentityRoles"], 1)
        self.assertFalse(hosting["outboundManagedIdentityRetrievalVerified"])
        self.assertEqual(result["newOwnedResources"]["singleTenantAppRegistrations"], 2)
        self.assertEqual(result["newOwnedResources"]["storageAccounts"], 0)
        self.assertEqual(result["newOwnedResources"]["foundryOrModelDeployments"], 0)
        self.assertTrue(result["package"]["allowlistIndependentlyVerified"])
        self.assertFalse(result["package"]["environmentCredentialCacheOrTestFilesIncluded"])
        self.assertEqual(result["paidMcpToolCalls"], 0)
        self.assertEqual(result["newNativeQuestionsSubmitted"], 0)
        self.assertFalse(result["nativeBroadSarWholeOutputFidelityRepaired"])
        self.assertFalse(result["fullElevenCaseNativeMatrixPassed"])
        self.assertFalse(result["wholeRoadmapComplete"])

    def test_hosted_mcp_human_boundary_has_no_fabricated_consent_or_orphan_helper(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-hosted-preflight.json").read_text("utf-8"))
        self.assertFalse(result["unavailableQuestionCountedAsApproval"])
        connector = result["connector"]
        self.assertTrue(connector["createdThroughOfficialPac"])
        self.assertTrue(connector["actualNativeMcpCatalogEntryVisible"])
        self.assertLessEqual(len(connector["displayName"]), 30)
        self.assertTrue(connector["generatedUniqueCallbackIndependentlyReadBack"])
        self.assertTrue(connector["callbackRegisteredOnOwnedClientAndReadBack"])
        self.assertTrue(connector["transientSecretInputAndRawDownloadedPropertiesRemoved"])
        self.assertFalse(connector["rawCredentialPrintedOrCommitted"])
        self.assertEqual(connector["dedicatedDelegatedApiScope"], "Evidence.Read")
        self.assertEqual(connector["graphPermissionsRequested"], [])
        self.assertEqual(connector["userConsentGrantsObserved"], 0)
        self.assertFalse(connector["tenantWideConsentGranted"])
        self.assertFalse(connector["usableDelegatedConnectionVerified"])
        self.assertFalse(connector["candidateBindingCreated"])
        auth = result["authenticationBoundary"]
        self.assertTrue(auth["nativeConsentPopupBlockedByIntegratedBrowser"])
        self.assertTrue(auth["standardNewTabAuthorizationCodeWithPkceAttempted"])
        self.assertTrue(auth["intendedAdministratorPasswordPromptObserved"])
        self.assertFalse(auth["genuineEntraBearerSuccessVerified"])
        self.assertTrue(auth["boundedLoopbackHelperStopped"])
        self.assertTrue(auth["loopbackPortVerifiedClosed"])
        self.assertTrue(auth["temporaryLoopbackRedirectRemoved"])
        self.assertTrue(auth["actualConnectorCallbackPreserved"])
        self.assertFalse(auth["oauthCodeOrTokensPersisted"])
        self.assertEqual(auth["forcedDomActions"], 0)
        self.assertEqual(result["billing"]["publishedComputeRetailUsdPerHour"], 0.018)
        self.assertTrue(result["billing"]["retainedHostRemainsBillable"])
        self.assertFalse(result["billing"]["numericalBudgetProvided"])
        self.assertFalse(result["billing"]["retentionOwnerAndReviewDateProvided"])

    def test_hosted_mcp_fresh_native_preservation_matches_prior_draft(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        before = json.loads((assets / "lookup-preservation.json").read_text("utf-8"))
        after = json.loads((assets / "mcp-hosted-native-preservation.json").read_text("utf-8"))
        hosted = json.loads((assets / "mcp-hosted-preflight.json").read_text("utf-8"))
        self.assertEqual(after["result"], "pass")
        self.assertEqual(after["checks"], before["checks"])
        self.assertEqual(after["authoringSha256"], before["authoringSha256"])
        self.assertEqual(after["actionStates"], before["actionStates"])
        self.assertEqual(after["originalComponentCount"], 26)
        self.assertEqual(after["candidateComponentCount"], 28)
        self.assertEqual(after["cloudWritesDuringVerification"], 0)
        self.assertFalse(after["publicationPerformed"])
        preserved = hosted["preservation"]
        self.assertTrue(preserved["protectedRetrieverFullDefinitionExactlyUnchanged"])
        self.assertEqual(preserved["currentHostedVersion"], "5")
        self.assertTrue(preserved["currentHostedDefinitionExactlyUnchanged"])
        self.assertTrue(preserved["currentHostedPrincipalAndClientIdsUnchanged"])
        self.assertFalse(preserved["wholeIdentityObjectEqualityClaimed"])
        self.assertEqual(preserved["azurePolicyOrStorageNetworkingChanges"], 0)
        self.assertFalse(preserved["publicationPerformed"])

    def test_actual_app_container_identity_proof_checks_complete_records_and_retains_failures(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-managed-identity-runtime.json").read_text("utf-8"))
        self.assertEqual(result["result"], "pass")
        for key in ("actualManagedIdentityMicrosoftSignatureVerified",
                    "actualManagedIdentityPrincipalAndTenantVerified",
                    "defaultCredentialContainsOnlyManagedIdentity"):
            self.assertTrue(result["identity"][key])
        self.assertFalse(result["identity"]["tokensOrIdentityHeadersPersisted"])
        self.assertTrue(result["source"]["allFiveDeployedSourceHashesVerified"])
        self.assertTrue(result["source"]["runtimeConfigurationMatchesProtectedBaseline"])
        self.assertTrue(result["source"]["packageUnchangedFromHostedPreflight"])
        retrieval = result["retrieval"]
        self.assertEqual(retrieval["originalCaseNumber"], 6)
        self.assertTrue(retrieval["unchangedOriginalQuestion"])
        self.assertEqual(retrieval["actualSharedRetrievalAttempts"], 4)
        self.assertEqual(retrieval["earlierHttp403Failures"], 2)
        self.assertEqual(retrieval["successfulOriginalCaseProofs"], 2)
        self.assertEqual(retrieval["automaticModelRetries"], 0)
        self.assertEqual(retrieval["recordIds"], ["rc-002", "ip-006"])
        self.assertEqual(retrieval["recordCount"], len(retrieval["recordIds"]))
        for key in ("completeRecordsIndependentlyMatchPinnedCorpus",
                    "completeTextIndependentlyMatchesDeterministicRenderer",
                    "bothProofsHaveDistinctRetrievalAndSelectionResponseIds",
                    "confirmationAfterCleanupReceiptAtLeast600Seconds"):
            self.assertTrue(retrieval[key])
        self.assertGreaterEqual(retrieval["observedSecondsAfterRoleCleanupReceipt"], 600)
        self.assertTrue(result["preservation"]
                        ["protectedRetrieverFullDefinitionUnchangedBeforeAndAfterBothProofs"])

    def test_actual_runtime_role_is_project_scoped_and_acknowledges_authoring_permission(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "mcp-managed-identity-runtime.json").read_text("utf-8"))
        authorization = result["authorization"]
        self.assertEqual(authorization["currentOwnedIdentityAssignments"], 1)
        self.assertEqual(authorization["scope"], "Existing Foundry project only")
        self.assertEqual(authorization["controlPlaneActions"], [])
        self.assertEqual(authorization["dataActions"], [
            "Microsoft.CognitiveServices/accounts/AIServices/agents/read",
            "Microsoft.CognitiveServices/accounts/AIServices/agents/write",
        ])
        self.assertTrue(authorization["agentWritePermissionAlsoAllowsAuthoring"])
        self.assertEqual(authorization["directAgentAuthoringRequests"], 0)
        self.assertEqual(authorization["removedOwnedTrialAssignments"], 3)
        for key in ("accountScopedModelRoleRemoved", "trialResponsesAndConsumerAssignmentsRemoved",
                    "allRemovedAssignmentsIndependentlyVerifiedOwned"):
            self.assertTrue(authorization[key])
        self.assertFalse(authorization["foundryUserOwnerStorageOrSearchRoleGranted"])
        self.assertFalse(authorization["existingPrincipalRolesChanged"])
        self.assertFalse(authorization["authorizationOnlyProbesCountedAsRetrievalSuccess"])
        historical = json.loads((assets / "mcp-hosted-preflight.json").read_text("utf-8"))
        self.assertTrue(result["historicalPreflightReceiptUnmodified"])
        self.assertEqual(historical["hosting"]["newManagedIdentityRoles"], 1)
        self.assertFalse(historical["hosting"]["outboundManagedIdentityRetrievalVerified"])

    def test_actual_runtime_proof_keeps_delegated_native_and_governance_gates_open(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "mcp-managed-identity-runtime.json").read_text("utf-8"))
        controls = result["inboundControls"]
        self.assertEqual(controls["missingBearerHttpStatus"], 401)
        self.assertEqual(controls["invalidBearerHttpStatus"], 401)
        self.assertEqual(controls["protectedResourceDiscoveryHttpStatus"], 200)
        self.assertFalse(controls["genuineDelegatedMcpBearerSuccessVerified"])
        self.assertEqual(result["mcpToolCalls"], 0)
        self.assertEqual(result["newNativeQuestionsSubmitted"], 0)
        for key in ("nativeMcpCandidateBindingCreated", "nativeBroadSarWholeOutputFidelityRepaired",
                    "fullElevenCaseNativeMatrixPassed", "wholeRoadmapComplete"):
            self.assertFalse(result[key])
        self.assertEqual(result["completedRoadmapTasks"], [])
        before = json.loads((assets / "mcp-hosted-native-preservation.json").read_text("utf-8"))
        after = json.loads((assets / result["preservation"]["freshNativeReceipt"]).read_text("utf-8"))
        self.assertEqual(after["checks"], before["checks"])
        self.assertEqual(after["authoringSha256"], before["authoringSha256"])
        self.assertEqual(after["actionStates"], before["actionStates"])
        self.assertEqual(after["cloudWritesDuringVerification"], 0)
        self.assertFalse(after["publicationPerformed"])
        self.assertTrue(result["preservation"]["currentHostedDefinitionAndPrincipalClientIdsUnchanged"])
        self.assertTrue(result["billing"]["retainedHostRemainsBillable"])
        self.assertFalse(result["billing"]["actualModelChargesOrTotalCopilotCreditsEstablished"])
        self.assertFalse(result["billing"]["numericalBudgetProvided"])
        self.assertFalse(result["billing"]["retentionOwnerAndReviewDateProvided"])

    def test_native_mcp_consent_is_explicit_human_tenant_wide_and_historical_receipts_remain(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        result = json.loads((assets / "mcp-native-sar.json").read_text("utf-8"))
        oauth = result["oauth"]
        self.assertTrue(oauth["humanExplicitlyApprovedTenantWideConsent"])
        self.assertEqual(oauth["consentType"], "AllPrincipals")
        self.assertEqual(oauth["scope"], "Evidence.Read")
        self.assertIsNone(oauth["principalId"])
        self.assertEqual(oauth["assistantGraphGrantWriteRequests"], 0)
        self.assertEqual(oauth["nativeConnectionCreateSubmissions"], 1)
        self.assertEqual(oauth["officialPacConnectionStatus"], "Connected")
        for key in ("existingProfilesOrCookiesCopied", "credentialsEnteredByAutomation",
                    "rawBearerTokensOrAuthorizationCodesPrintedOrExported",
                    "npmPolicyOrBrowserSecurityPolicyOverridden"):
            self.assertFalse(oauth[key])
        self.assertTrue(result["historicalReceiptsPreserved"])
        historical = json.loads((assets / "mcp-managed-identity-runtime.json").read_text("utf-8"))
        self.assertFalse(historical["nativeMcpCandidateBindingCreated"])
        self.assertEqual(historical["newNativeQuestionsSubmitted"], 0)

    def test_native_mcp_sar_pass_checks_whole_turn_exact_records_and_real_binding(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-native-sar.json").read_text("utf-8"))
        binding = result["nativeBinding"]
        self.assertEqual(binding["candidateComponentCountBefore"], 28)
        self.assertEqual(binding["candidateComponentCountAfter"], 29)
        self.assertEqual(binding["generatedOperationMetadataKind"], "ModelContextProtocolMetadata")
        self.assertEqual(binding["nativeDiscoveredTool"], "retrieve_verified_workshop_evidence")
        self.assertTrue(binding["bindingMatchesExactVerifiedConnectionAndConnector"])
        self.assertTrue(result["authoring"]["nativeInstructionsExactlyMatchAuthoredText"])
        self.assertTrue(result["authoring"]["oldEmittingRetrievalToolDisabled"])
        self.assertFalse(result["authoring"]["managementBundlePatchedOrMonkeyPatched"])
        sar = result["nativeSar"]
        self.assertEqual(sar["result"], "pass")
        self.assertEqual(sar["originalCaseNumber"], 6)
        self.assertEqual(sar["nativeQuestionSubmissions"], 1)
        self.assertEqual(sar["nativeMcpToolExecutionsObserved"], 1)
        self.assertEqual(sar["userFacingDomainAnswerCount"], 1)
        self.assertEqual(sar["allSourceQuotations"], 2)
        self.assertEqual(sar["allSourceQuotations"], sar["exactCompletePinnedRecordQuotations"])
        self.assertEqual(sar["recordIds"], ["rc-002", "ip-006"])
        for key in ("completeVisibleSnapshotNotTruncated", "canonicalSourceMarkersExact",
                    "localKnowledgeSearchObserved", "nativeLocalReferenceVisible",
                    "broadSarCoverageChecksPassed", "legalApplicabilityLimitPreserved",
                    "noRawToolMetadataInUserFacingAnswer", "nativeConnectionConsentCardRetained"):
            self.assertTrue(sar[key])
        self.assertFalse(sar["rawDynamicPlanFinishedCaptured"])
        self.assertTrue(sar["nativeVisibleCompletionObserved"])
        self.assertFalse(result["boundaries"]["fullElevenCaseNativeMatrixPassed"])
        self.assertFalse(result["boundaries"]["wholeRoadmapComplete"])
        self.assertFalse(result["preservation"]["publicationPerformed"])
        self.assertEqual(result["preservation"]["missingBearerHttpStatus"], 401)
        self.assertEqual(result["preservation"]["malformedBearerHttpStatus"], 401)

    def test_initial_native_matrix_retains_actual_attribution_failure_and_completion_types(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-native-matrix-initial.json").read_text("utf-8"))
        self.assertEqual(result["nativeQuestionSubmissions"], 5)
        self.assertEqual(result["questionRetries"], 0)
        self.assertEqual(result["officialNativeDialogExportsRetained"], 5)
        self.assertEqual([case["result"] for case in result["cases"]],
                         ["pass", "pass", "pass", "pass", "fail"])
        for case in result["cases"][:3]:
            self.assertTrue(case["activityProcessedCompletionTraceObserved"])
            self.assertEqual(case["dynamicPlanFinished"], "not-applicable-deterministic-OnActivity")
            self.assertEqual(case["nativeMcpEvidenceToolInvocations"], 0)
        local = result["cases"][3]
        self.assertTrue(local["dynamicPlanFinishedObserved"])
        self.assertFalse(local["planCancelled"])
        self.assertEqual(local["nativeMcpEvidenceToolInvocations"], 0)
        self.assertTrue(local["mcpCapabilityDiscoveryNotCountedAsEvidenceRetrieval"])
        failed = result["cases"][4]
        self.assertEqual(failed["factualBulletCount"], 7)
        self.assertEqual(failed["individuallyAttributedFactualBulletCount"], 0)
        self.assertTrue(failed["returnedRecordsExactlyMatchPinnedCorpus"])
        protocol = result["actualNativeProtocolDiscovery"]
        self.assertEqual(protocol["protocolVersion"], "2024-11-05")
        self.assertEqual(protocol["nativeToolDefinitionKind"], "DynamicServerToolDefinition")
        self.assertEqual(protocol["toolIdentifier"], "retrieve_verified_workshop_evidence")
        self.assertEqual(protocol["requiredInputName"], "question")
        self.assertEqual(protocol["requiredInputType"], "String")
        self.assertFalse(result["repairBoundary"]["fullElevenCaseNativeMatrixPassed"])
        self.assertFalse(result["repairBoundary"]["wholeRoadmapComplete"])

    def test_native_renderer_boundary_and_local_punctuation_failures_are_not_hidden(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        boundary = json.loads((assets / "mcp-native-source-boundary-failure.json").read_text("utf-8"))
        self.assertEqual(boundary["nativeQuestionSubmissions"], 2)
        self.assertEqual(boundary["case5"]["result"], "pass")
        self.assertEqual(boundary["case5"]["factualParagraphCount"], 3)
        self.assertEqual(boundary["case5"]["individuallyAttributedFactualParagraphCount"], 3)
        sar = boundary["case6"]
        self.assertEqual(sar["result"], "fail")
        self.assertTrue(sar["returnedBoundaryNoticePresentInRendererText"])
        self.assertFalse(sar["returnedBoundaryNoticePresentInAnyPinnedRecordContent"])
        self.assertFalse(sar["exactRecordQuotationAcceptanceRelaxed"])
        punctuation = json.loads((assets / "mcp-native-local-quote-failure.json").read_text("utf-8"))
        self.assertEqual(punctuation["nativeQuestionSubmissions"], 1)
        self.assertEqual(punctuation["questionRetries"], 0)
        self.assertEqual(punctuation["nativeMcpEvidenceToolInvocations"], 2)
        self.assertEqual(punctuation["actualReturnedRecordIdsPerInvocation"],
                         [["rc-002"], ["rc-002", "ip-006"]])
        self.assertTrue(punctuation["eachInvocationRecordsAndRendererExactlyMatchPinnedCorpus"])
        self.assertTrue(punctuation["sourceBoundaryNoticeNoLongerQuotedOrMisattributed"])
        self.assertEqual(punctuation["exactCompletePinnedRecordQuotations"], 2)
        failure = punctuation["failure"]
        self.assertEqual(failure["generatedQuotation"], failure["actualLocalCell"] + ".")
        self.assertFalse(failure["exactContiguousSourceQuotation"])
        self.assertFalse(punctuation["verifierCorrection"]["sourceQuotationAndAttributionCriteriaRelaxed"])
        self.assertFalse(punctuation["preservation"]["publicationPerformed"])
        self.assertFalse(punctuation["nextBoundary"]["fullElevenCaseNativeMatrixPassed"])
        self.assertFalse(punctuation["nextBoundary"]["wholeRoadmapComplete"])

    def test_native_matrix_failure_chronology_is_linked_in_both_languages_and_service_readme(self):
        root = Path(__file__).resolve().parents[1]
        pages = [root / "docs" / language / name for language in ("en", "fr")
                 for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md")]
        pages.append(root / "examples" / "verified-retrieval" / "workshop-verified-retrieval" / "README.md")
        for page in pages:
            text = page.read_text("utf-8")
            for receipt in ("mcp-native-matrix-initial.json", "mcp-native-source-boundary-failure.json",
                            "mcp-native-local-quote-failure.json", "mcp-native-eleven-case-matrix.json"):
                self.assertIn(receipt, text, str(page))

    def test_complete_native_matrix_counts_real_attempts_routes_sources_and_immutable_configuration(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-native-eleven-case-matrix.json").read_text("utf-8"))
        self.assertTrue(result["fullElevenCaseNativeMatrixPassed"])
        self.assertFalse(result["allCasesPassedOnFirstAttempt"])
        self.assertEqual(result["nativeOriginalQuestionSubmissions"], 12)
        self.assertEqual(result["explicitlyCountedQuestionRetries"], 1)
        self.assertEqual(result["automaticQuestionRetries"], 0)
        self.assertEqual(result["nativeMcpEvidenceToolInvocations"], 7)
        self.assertEqual(result["officialMatrixExportsRetained"], 12)
        self.assertEqual(result["officialExportsIncludingIndependentControl"], 13)
        self.assertTrue(result["all13NativeAgentContentExportsByteIdentical"])
        self.assertEqual(result["totalKnownNativeQuestionsAcrossHistoricalCohortsAndControl"], 22)
        cases = result["cases"]
        self.assertEqual([case["number"] for case in cases], list(range(1, 12)))
        self.assertEqual(sum(case["nativeUserSubmissionsIncludingKnownFailedAttempts"] for case in cases), 12)
        for case in cases:
            self.assertEqual(case["result"], "pass")
            self.assertEqual(case["userFacingDomainAnswerCount"], 1)
            self.assertTrue(case["completeNativeReplyRetainedPrivately"])
            self.assertTrue(case["unchangedOriginalQuestionVerified"])
            self.assertTrue(case["expectedRouteVerified"])
            self.assertTrue(case["directSemanticRelevanceCoverageAndApplicabilityReviewPassed"])
            self.assertTrue(case["allFactualBulletsAndParagraphsIndividuallyAttributed"])
            self.assertEqual(case["nativeAgentContentSha256"], result["nativeAgentContentSha256"])
            self.assertEqual(len(case["nativeReplySha256"]), 64)
            self.assertEqual(len(case["nativeDialogSha256"]), 64)
            self.assertEqual(case["completionEvidence"],
                             "activity-processed-deterministic-topic" if case["number"] <= 3
                             else "non-cancelled-DynamicPlanFinished")
            self.assertEqual(case["actualLocalKnowledgeSearchObserved"],
                             case["number"] in (4, 6, 8, 9, 10, 11))
            if case["number"] >= 5:
                self.assertTrue(case["mcpQuestionArgumentExactlyOriginal"])
                self.assertTrue(case["completeReturnedRecordsAndRendererPinned"])
                self.assertTrue(case["actuallyReturnedRecordIds"])
        self.assertEqual(cases[6]["successfulAttempt"], 2)
        self.assertEqual(sum(case["sourceQuotationCount"] for case in cases), 12)
        self.assertEqual(result["quotationBoundary"]["sourceQuotationsInFinalMcpDomainAnswers"], 0)
        self.assertTrue(result["quotationBoundary"]["finalMcpDomainAnswersUseSourceAuditedUnquotedParaphrases"])
        recovery = result["case7Recovery"]
        self.assertEqual(recovery["firstAttemptDomainReplies"], 0)
        self.assertEqual(recovery["firstAttemptPlanSteps"], 0)
        self.assertFalse(recovery["platformErrorOrRootCauseEstablished"])
        self.assertTrue(recovery["failedOfficialExportRetained"])
        self.assertTrue(recovery["oneSeparatelyGuardedRetryPassed"])
        self.assertFalse(recovery["failedAttemptErasedOrMergedIntoSuccessfulReply"])

    def test_complete_native_matrix_does_not_hide_duplicate_control_or_close_unrelated_gates(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-native-eleven-case-matrix.json").read_text("utf-8"))
        control = result["independentValidationControl"]
        self.assertFalse(control["partOfOriginalElevenCaseMatrix"])
        self.assertEqual(control["nativeQuestionSubmissions"], 1)
        self.assertEqual(control["actualIdenticalValidationReplies"], 2)
        self.assertTrue(control["actualTopicThenDirectValidationActionBothCompleted"])
        self.assertTrue(control["duplicateRetainedNotSilentlyDeduplicated"])
        self.assertFalse(control["singleReplyControlPassed"])
        self.assertTrue(control["relatedControlRepairRemainsOpen"])
        self.assertTrue(result["preservation"]["protectedOriginalRootAnd26CompleteRowsExactlyUnchanged"])
        self.assertEqual(result["preservation"]["candidateComponentCount"], 29)
        self.assertFalse(result["preservation"]["publicationPerformed"])
        self.assertFalse(result["preservation"]["freshCloudFoundryDefinitionReadbackIncluded"])
        self.assertTrue(result["roadmap"]["T008ElevenCaseEvidenceComplete"])
        self.assertTrue(result["roadmap"]["T007WorkingControlDuplicateStillOpen"])
        self.assertFalse(result["roadmap"]["wholeRoadmapComplete"])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [x] T008 [Plan:4.1]", text)
            self.assertIn("- [ ] T007 [Plan:4.1]", text)

    def test_control_repair_regression_counts_failed_actual_calls_without_claiming_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-native-control-repair-regression.json").read_text("utf-8"))
        self.assertFalse(result["fullElevenCaseNativeMatrixPassed"])
        self.assertEqual(result["acceptedDistinctOriginalCases"], 10)
        self.assertEqual(result["unacceptedOriginalCases"], [9])
        attempts = result["attempts"]
        self.assertEqual(len(attempts), 15)
        self.assertEqual(sum(item["caseNumber"] != 0 for item in attempts), 13)
        self.assertEqual(sum(item["caseNumber"] == 0 for item in attempts), 2)
        self.assertEqual(sum(item["officialExportRetained"] for item in attempts), 14)
        self.assertEqual(sum(item["actualSuccessfulMcpEvidenceInvocations"] for item in attempts), 7)
        self.assertEqual(result["totalKnownNativeQuestionsAcrossHistoricalCohortsAndControl"], 37)
        self.assertEqual(result["automaticQuestionRetries"], 0)
        self.assertEqual(result["knownFailedCaptureOrAnswerAttemptsRetained"], 4)
        cases = result["cases"]
        self.assertEqual([case["number"] for case in cases], list(range(1, 12)))
        self.assertEqual(sum(case["result"] == "pass" for case in cases), 10)
        failed = cases[8]
        self.assertEqual(failed["actualSuccessfulMcpEvidenceInvocations"], 1)
        self.assertFalse(failed["parentAnswerAcceptance"])
        self.assertFalse(failed["rootCauseEstablished"])
        self.assertFalse(failed["thirdAttemptSubmitted"])
        self.assertEqual(len(failed["attemptFailures"]), 2)
        self.assertTrue(failed["completedEvidenceAndPlanNotCountedAsParentAnswer"])
        self.assertEqual(cases[6]["sourceQuotationCount"], 2)
        self.assertTrue(cases[6]["actualIntendedLocalSearchObserved"])

    def test_control_repair_has_one_real_invocation_not_two_cancellation_trace_records(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "mcp-native-control-repair-regression.json").read_text("utf-8"))
        control = result["controlRepair"]
        for key in ("actualValidationBeginDialogInvocations", "actualConnectedValidationTaskBindings",
                    "exactConstantValidationReplies", "nativeSaveClicks"):
            self.assertEqual(control[key], 1)
        self.assertEqual(control["cancellationTraceRecords"], 2)
        self.assertFalse(control["cancellationTraceRecordsCountedAsAgentInvocations"])
        self.assertFalse(control["hardcodedSuccessReplyAdded"])
        self.assertTrue(control["firstBoundedNoAnswerAttemptAndOfficialExportRetained"])
        self.assertTrue(result["allAvailableNativeAgentContentExportsByteIdentical"])
        self.assertEqual(result["nativeAgentContentSha256"],
                         "ba967713ddd94f78a80e917593559b5fae313f24bf5ad45480bf2d5dad8a8132")
        self.assertTrue(all(result["boundaries"][key] for key in (
            "case2FirstVisibleReplyNotAcceptedWithoutOfficialExport",
            "case2StrandedUnreadExportCommandQuarantinedNeverReplayed",
            "queuePermissionRetryLimitedToFilesystemIoNotBrowserActions",
            "previousElevenCasePassNotCombinedWithCurrentConfiguration",
            "historicalDuplicateControlAndAllEarlierFailuresPreserved",
        )))
        self.assertEqual(result["preservation"]["candidateComponentCount"], 29)
        self.assertTrue(result["preservation"]["protectedOriginalRootAnd26CompleteRowsExactlyUnchanged"])
        self.assertTrue(result["preservation"]["allOtherCompleteCandidateRowsExactlyUnchanged"])
        self.assertFalse(result["preservation"]["publicationPerformed"])
        self.assertTrue(result["execution"]["ownedBrowserClosedNormally"])
        self.assertFalse(result["execution"]["otherBrowsersTouched"])
        self.assertEqual(result["execution"]["newAzureDeploymentsResourcesRolesGrantsOrPolicyChanges"], 0)
        self.assertFalse(result["roadmap"]["T007Complete"])
        self.assertTrue(result["roadmap"]["T008PriorAcceptedRunRetained"])
        self.assertFalse(result["roadmap"]["currentConfigurationElevenCaseAcceptanceComplete"])
        self.assertFalse(result["roadmap"]["wholeRoadmapComplete"])

    def test_control_repair_partial_regression_is_linked_in_both_languages_and_example(self):
        root = Path(__file__).resolve().parents[1]
        documents = [root / "docs" / language / name
                     for language in ("en", "fr")
                     for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md")]
        documents.append(root / "examples" / "verified-retrieval" / "workshop-verified-retrieval" / "README.md")
        for path in documents:
            text = path.read_text("utf-8")
            self.assertIn("mcp-native-control-repair-regression.json", text)
            self.assertIn("10/11", text)

    def test_owned_boundary_refresh_includes_mcp_without_fabricating_governance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "owned-boundary-refresh.json").read_text("utf-8"))
        self.assertTrue(result["identityTenantAndSubscriptionVerified"])
        self.assertEqual(result["exactOwnedArmResourceCount"], 6)
        resources = result["resourceStates"]
        self.assertEqual(len(resources), 6)
        self.assertEqual(len({row["type"] for row in resources}), 6)
        plan = next(row for row in resources if row["type"] == "Microsoft.Web/serverfarms")
        self.assertEqual(plan["skuName"], "B1")
        self.assertEqual(plan["capacity"], 1)
        self.assertEqual(next(row for row in resources
                              if row["type"] == "Microsoft.Web/sites")["state"], "Running")
        self.assertEqual(result["cloudConfigurationWritesInferenceOrNativeQuestions"], 0)
        for key in ("retentionOwnerAssigned", "retentionReviewDateAssigned", "numericalBudgetApproved",
                    "attributableProductOwnerSecurityAndTechLeadSignoffsRecorded",
                    "T001Complete", "T002Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])
        self.assertTrue(result["humanUnavailableFormPlaceholderNotInterpretedAsApproval"])

    def test_owned_billing_refresh_retains_throttle_and_excludes_unposted_costs_and_credits(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "owned-boundary-refresh.json").read_text("utf-8"))
        self.assertIn("Exact six retained ARM resource IDs", result["costScope"])
        self.assertEqual(result["readOnlyBillingQueryPosts"], 2)
        self.assertTrue(result["initialHttp429Retained"])
        self.assertEqual(result["recoveryHttpStatus"], 200)
        self.assertFalse(result["automaticThirdBillingQuery"])
        self.assertEqual(result["currency"], "USD")
        self.assertAlmostEqual(result["reportedPretaxCost"], 11.26126391, places=8)
        self.assertEqual(result["reportedCostRows"], 10)
        self.assertEqual(result["distinctResourceIdsWithReportedCostRows"], 2)
        self.assertEqual(result["latestReportedUsageDate"], 20261025)
        self.assertFalse(result["finalInvoiceOrCompleteCurrentSpend"])
        self.assertFalse(result["copilotCreditsIncluded"])
        self.assertTrue(result["absentResourceCostRowsDoNotEstablishFreeResources"])
        self.assertTrue(result["lastReportedUsageDateNotProofAllChargesPosted"])
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md"):
                self.assertIn("owned-boundary-refresh.json",
                              (root / "docs" / language / name).read_text("utf-8"))

    def test_endpoint_model_already_present_does_not_reclassify_native_failures(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "agent-endpoints-readonly.json").read_text("utf-8"))
        observation = result["observations"]
        for name in ("baselineGetStatus", "featureHeaderGetStatus"):
            self.assertEqual(observation[name], 200)
        for name in ("approvedTenantAndActorVerified", "completeResponseBodiesByteIdentical",
                     "agentEndpointPresent", "uniqueInstanceIdentityPresent", "blueprintPresent",
                     "newEndpointModelAlreadyPresent"):
            self.assertTrue(observation[name])
        self.assertEqual(observation["latestVersion"], "5")
        self.assertEqual(observation["protocols"], ["activity", "invocations"])
        self.assertEqual(observation["authorizationSchemes"], ["Entra", "BotServiceRbac"])
        self.assertEqual(observation["protocolConfigurationLocation"], "agent_endpoint.protocol_configuration")
        self.assertEqual(observation["versionSelectorLocation"], "agent_endpoint.version_selector")
        self.assertEqual(observation["versionSelection"], "@latest")
        self.assertEqual(observation["trafficPercentage"], 100)
        self.assertEqual(observation["publishApprovalStatus"], "not_published")
        self.assertTrue(result["documentation"]["entraRemainsSupportedAzureRbacAlias"])
        boundary = result["boundary"]
        self.assertEqual(boundary["remoteGetRequests"], 2)
        for name, value in boundary.items():
            if name != "remoteGetRequests":
                self.assertEqual(value, 0 if type(value) is int else False)
        self.assertTrue(all(value is False for value in result["acceptance"].values()))
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md"):
                self.assertIn("agent-endpoints-readonly.json",
                              (root / "docs" / language / name).read_text("utf-8"))
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            for task in ("T005", "T006", "T016"):
                self.assertIn(f"- [ ] {task}", roadmap)

    def test_native_blueprint_identity_correlation_is_not_a_native_fix(self):
        root = Path(__file__).resolve().parents[1]
        receipt_name = "native-blueprint-identity-correlation.json"
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / receipt_name).read_text("utf-8"))
        observed = result["observed"]
        self.assertEqual(observed["historicalNativeStatus"], 400)
        self.assertEqual(observed["historicalNativeCode"], "ConnectorRequestFailure")
        for name in ("exactErrorPatternMatched", "activityBlueprintIdIsGuid",
                     "activityBlueprintIdEqualsApprovedAdministratorObjectId",
                     "activityBlueprintIdEqualsRetainedDelegatedCallerObjectId",
                     "summaryBlueprintIdMatchesSavedTargetBlueprintClientId",
                     "summaryBlueprintIdMatchesCurrentTargetBlueprintClientId",
                     "savedAndCurrentTargetBlueprintClientIdIdentical",
                     "savedAndCurrentTargetInstanceClientIdIdentical"):
            self.assertTrue(observed[name])
        for name in ("activityBlueprintIdMatchesTargetBlueprintClientId",
                     "activityBlueprintIdMatchesTargetBlueprintPrincipalId"):
            self.assertFalse(observed[name])
        self.assertTrue(result["interpretation"]["callerIdentifierMismatchCorrelated"])
        for name, value in result["interpretation"].items():
            if name != "callerIdentifierMismatchCorrelated":
                self.assertFalse(value)
        for name, value in result["boundary"].items():
            if name == "historicalFailureAndRestorationPreserved":
                self.assertTrue(value)
            else:
                self.assertEqual(value, 0 if type(value) is int else False)
        self.assertTrue(all(value is False for value in result["acceptance"].values()))
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md"):
                self.assertIn(receipt_name, (root / "docs" / language / name).read_text("utf-8"))

    def test_interrupted_paired_sp_cleanup_is_not_native_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab5-paired-sp-interrupted-cleanup.json").read_text("utf-8"))
        questions = result["nativeQuestions"]
        for key in ("authorizedDurableIntentCount", "deniedDurableIntentCount",
                    "queuedOrConsumedSubmissionOperations"):
            self.assertEqual(questions[key], 0)
        self.assertTrue(questions["priorCohortsExcluded"])
        cleanup = result["ownedCleanup"]
        for key in ("applicationGetStatus", "servicePrincipalGetStatus",
                    "nativeDraftDataverseGetStatus", "searchServiceGetStatus",
                    "resourceGroupGetStatus"):
            self.assertEqual(cleanup[key], 404)
        self.assertEqual(cleanup["credentialRemovalStatus"], 204)
        self.assertEqual(cleanup["exactRoleAssignmentsGet404"], 4)
        for key in ("disposableConnectionCreateIntentCount",
                    "extraConnectionsInBeforeAfterOfficialInventories", "remainingOwnedObjectsObserved"):
            self.assertEqual(cleanup[key], 0)
        for key in ("emptyApplicationCredentialsVerifiedBeforeDeletion",
                    "localEncryptedCredentialHandoffAbsent", "credentialNotDecryptedDuringRecovery",
                    "nativeDraftAbsentFromOfficialPacInventory", "indexAbsentThroughVerifiedParentDeletion"):
            self.assertTrue(cleanup[key])
        original = result["originalPreservation"]
        self.assertEqual(original["agentCount"], 5)
        self.assertEqual(original["connectionCount"], 7)
        self.assertEqual(original["originalSearchSchemaCount"], 3)
        self.assertEqual(original["historicalFilesHashed"], 181)
        self.assertEqual(original["changedOrMissingHistoricalFiles"], 0)
        for key in ("agentRowsMatchAfterWhitespaceTokenization", "completeConnectionInventoryExact",
                    "originalSearchSchemaHashesExact", "embeddingResourceAndCompleteRoleInventoryExact",
                    "hostedRetrievalAgentAndVersion5Exact", "earlierHoldAndCleanupReceiptsUnchanged"):
            self.assertTrue(original[key])
        portal = result["nativePortalVerification"]
        self.assertTrue(portal["attempted"])
        self.assertTrue(portal["redirectedToMicrosoftSignIn"])
        for key in ("actualInventoryCaptured", "loginAttempted", "portalAbsenceClaimed"):
            self.assertFalse(portal[key])
        self.assertTrue(portal["ownedBrowserClosedNormally"])
        boundary = result["recoveryBoundary"]
        self.assertTrue(boundary["previousLifecycleProcessesAbsentBeforeMutation"])
        self.assertEqual(boundary["newQuestionsOrRemoteResources"], 0)
        for key in ("sharedProcessesOrBrowsersTerminated", "authenticationPolicyOrCacheChanges",
                    "privilegeElevation", "actualSpendingFinalized", "zeroSpendingClaimed"):
            self.assertFalse(boundary[key])
        self.assertTrue(all(value is False for value in result["acceptance"].values()))
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md"):
                self.assertIn("lab5-paired-sp-interrupted-cleanup.json",
                              (root / "docs" / language / name).read_text("utf-8"))
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            for task in ("T014", "T016"):
                self.assertIn(f"- [ ] {task}", roadmap)

    def test_dataverse_history_auth_recovery_does_not_grant_transcript_access(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab1-dataverse-history.json").read_text("utf-8"))
        auth = result["authentication"]
        self.assertEqual(auth["initialGraphStatus"], 401)
        self.assertEqual(auth["initialGraphChallenge"], "TokenCreatedWithOutdatedPolicies")
        self.assertEqual(auth["normalBrowserCliLoginTimedOutAfterSeconds"], 300)
        self.assertEqual(auth["laterIndependentGraphReadStatus"], 200)
        self.assertTrue(auth["approvedTenantAndActorVerified"])
        self.assertTrue(auth["approvedSubscriptionVerifiedEnabled"])
        self.assertTrue(auth["globalAdministratorMembershipVerified"])
        self.assertFalse(auth["deviceLoginStarted"])
        self.assertFalse(auth["recoveryCauseOrExactLatencyEstablished"])
        data = result["dataverse"]
        self.assertEqual(data["transcriptMetadataStatus"], 200)
        self.assertEqual(data["originalAgentFilteredTranscriptMetadataQueryStatus"], 403)
        self.assertEqual(data["missingPrivilege"], "prvReadconversationtranscript")
        self.assertEqual(data["powerPlatformAdminEnvironmentReadStatus"], 200)
        self.assertEqual(data["directRoleNames"], ["Basic User", "Environment Maker"])
        self.assertTrue(data["originalDirectRoleRowsPreserved"])
        self.assertFalse(data["transcriptContentRead"])
        self.assertTrue(data["definedPrivilegeCapabilities"]["prvReadRole"])
        for name in ("prvReadconversationtranscript", "prvCreateRole", "prvAssignRole", "prvAppendRole"):
            self.assertFalse(data["definedPrivilegeCapabilities"][name])
        self.assertFalse(data["earlierCapabilityAudit"]["completenessAssertionPassed"])
        self.assertEqual(data["earlierCapabilityAudit"]["requestedDefinitionNotFound"], "prvAppendToSystemUser")
        self.assertTrue(data["newDefinedCapabilityAuditComplete"])
        self.assertTrue(data["tenantAdminReadDoesNotEstablishDataverseTranscriptOrRoleAssignmentAccess"])

    def test_dataverse_original_history_stays_open_on_all_bilingual_surfaces(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab1-dataverse-history.json").read_text("utf-8"))
        history = result["originalHistory"]
        self.assertTrue(history["exactOriginalAgentRunAndQuestionVerified"])
        self.assertEqual(history["displayedRunDate"], "2026-10-19")
        self.assertEqual(history["displayedState"], "In progress")
        self.assertTrue(history["visibleConversationOnlyGreetingAndOriginalQuestion"])
        self.assertFalse(history["completeAnswerExposed"])
        self.assertFalse(history["newerAnswerSubstituted"])
        self.assertFalse(history["historicalAnswerReconstructed"])
        self.assertIsNone(history["atomicClaimCounts"])
        execution = result["executionBoundary"]
        for name in ("newQuestions", "roleOrPolicyWrites"):
            self.assertEqual(execution[name], 0)
        for name in ("systemAdministratorSelfElevationAttempted", "transcriptPolicyOrRetentionChanged",
                     "deniedTranscriptQueryReplayed", "authenticationPolicyOrMfaBypassAttempted",
                     "sharedCredentialCachesCleared", "originalAgentConfigurationChanged",
                     "emailSent", "modelReasoningOpened"):
            self.assertFalse(execution[name])
        self.assertTrue(execution["ownedNormalCliLoginProcessTreeStopped"])
        self.assertTrue(all(value is False for value in result["acceptance"].values()))
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md", "lab-01.md"):
                self.assertIn("lab1-dataverse-history.json",
                              (root / "docs" / language / name).read_text("utf-8"))
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [ ] T009", roadmap)
            self.assertIn("- [ ] T016", roadmap)

    def test_original_licensing_history_followup_does_not_substitute_a_newer_answer(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab1-history-citation-followup.json").read_text("utf-8"))
        original = result["originalHistory"]
        self.assertTrue(original["exactOriginalAgentAndQuestionVerified"])
        self.assertEqual(original["displayedRunDate"], "2026-10-19")
        self.assertEqual(original["displayedState"], "In progress")
        self.assertEqual(original["normalRefreshes"], 1)
        self.assertTrue(original["refreshOnlyAddedRefreshControlLabel"])
        self.assertFalse(original["completeAnswerObserved"])
        self.assertFalse(original["historicalAnswerReconstructed"])
        self.assertTrue(result["separateCompletedHistory"]["differentQuestionNotSubstitutedForOriginal"])
        self.assertEqual(result["separateCompletedHistory"]["displayedRunDate"], "2026-10-24")
        for value in result["acceptance"].values():
            self.assertFalse(value)

    def test_inline_licensing_citation_failure_preserves_exact_counts_and_source(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab1-history-citation-followup.json").read_text("utf-8"))
        citation = result["separateCompletedHistory"]
        self.assertEqual(citation["inlineCitationAnchors"], 9)
        self.assertEqual(citation["normalInlineCitationClicks"], 1)
        for key in ("allCitationHrefsEmpty", "visibleTextOnlyAddedReviewCounter",
                    "sameHistoryAndSingleTabRetained"):
            self.assertTrue(citation[key])
        for key in ("newSourceDialogOrPdfViewerObserved", "approvedPdfDownloadObserved",
                    "targetEditionPassageAndPageNavigationVerified"):
            self.assertFalse(citation[key])
        self.assertEqual(result["approvedRetainedPdf"]["bytes"], 867776)
        self.assertEqual(result["approvedRetainedPdf"]["sha256"],
                         "e1b4789118ff8f1bb633683d6fbeb750b80c25b16760d036eff247e477a524d6")
        self.assertTrue(result["approvedRetainedPdf"]["unchanged"])
        self.assertEqual(result["execution"]["newNativeQuestions"], 0)
        self.assertEqual(result["execution"]["configurationWrites"], 0)
        self.assertTrue(result["execution"]["ownedBrowserClosedNormally"])
        self.assertFalse(result["execution"]["otherBrowsersTouched"])

    def test_published_wiki_checkpoint_preserves_public_visibility_and_partial_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "wiki-publication.json").read_text("utf-8"))
        self.assertEqual(result["status"], "PUBLISHED_IN_PROGRESS_SNAPSHOT")
        self.assertEqual(result["canonicalSourceRevision"],
                         "bf0f72c5745271db31e5999aba2dedcb5964288e")
        self.assertEqual(result["verifiedWikiRevision"],
                         "762188c57fb087ee7a7c552ad6a85e0aa7ebcc9c")
        self.assertEqual(result["wikiBranch"], "master")
        self.assertEqual(result["repositoryVisibilityObserved"], "PUBLIC")
        self.assertEqual(result["priorTrackedFilesReviewed"], 133)
        self.assertEqual(result["divergentHumanEditsFound"], 0)
        self.assertEqual(result["generatedMarkdownPages"], 38)
        self.assertGreater(result["generatedFilesComparedWithValidatedSnapshot"], 133)
        for key in ("validatedSnapshotMatchesPublishedFiles", "normalPushUsed",
                    "repositoryAndWikiRemoteRevisionsIndependentlyVerified",
                    "initialEnglishBrowserOpenFailed", "englishNormalNavigationRecoveryVerified",
                    "onlyReviewedSanitizedCanonicalContentPublished", "T016PublicationPortionVerified"):
            self.assertTrue(result[key])
        for key in ("repositoryVisibilityChanged", "humanChangesOverwritten", "forcePushUsed",
                    "originalSourcePdfPublished", "privateRuntimeEvidencePublished",
                    "agentOrAzureDeploymentPerformed", "T016WholeTaskComplete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])
        for language in ("en", "fr"):
            page = result["renderedBrowserChecks"][language]
            self.assertTrue(page["incompleteRegressionVisible"])
            self.assertEqual(page["evidenceLinkVisible"], 1)
            self.assertTrue(page["finalReleaseUnchecked"])

    def test_history_and_publication_followups_are_linked_without_closing_release(self):
        root = Path(__file__).resolve().parents[1]
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md"):
                text = (root / "docs" / language / name).read_text("utf-8")
                self.assertIn("lab1-history-citation-followup.json", text)
                self.assertIn("wiki-publication.json", text)
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [ ] T009", roadmap)
            self.assertIn("- [ ] T016", roadmap)
        self.assertIn("wiki-publication.json", (root / "docs" / "publishing.md").read_text("utf-8"))

    def test_native_lab5_entra_recovery_preserves_failure_and_policy(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab5-native-entra-connected.json").read_text("utf-8"))
        self.assertEqual(result["status"], "FICTIONAL_NATIVE_CONNECTED_SCOPE_PASSED")
        connection = result["connectionRecovery"]
        self.assertEqual(connection["authentication"], "Microsoft Entra ID Integrated")
        self.assertEqual(connection["documentedAiNamespaceAttempt"], "FAILED_NATIVE_CONNECTION_TEST")
        self.assertEqual(connection["firstAttemptSavedConnectionCount"], 0)
        self.assertEqual(connection["separatelyGuardedHttpsEndpointAttempt"], "CONNECTED")
        self.assertTrue(connection["realOAuthPopupObserved"])
        for key in ("keysEntered", "disableLocalAuthWeakened", "browserPolicyOverridden"):
            self.assertFalse(connection[key])
        configuration = result["configuration"]
        self.assertFalse(configuration["webSearchEnabled"])
        self.assertFalse(configuration["generalModelKnowledgeEnabled"])
        self.assertFalse(configuration["published"])
        self.assertEqual(configuration["nativeKnowledgeStatus"], "Ready")
        self.assertTrue(configuration["independentOfficialPacCloneVerification"])
        self.assertEqual(configuration["officialValidatorError"],
                         "Cannot find module '@azure/msal-node-extensions'")
        self.assertFalse(configuration["bundledScriptsModified"])
        self.assertFalse(configuration["yamlSchemaValidationSucceeded"])

    def test_native_lab5_frozen_cohorts_are_not_combined(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab5-native-entra-connected.json").read_text("utf-8"))
        tests = result["nativeTests"]
        self.assertEqual(tests["totalActualQuestionSubmissions"], 8)
        self.assertEqual(tests["independentConversations"], 8)
        self.assertEqual(tests["automaticQuestionReplays"], 0)
        self.assertEqual(tests["initialCohort"]["accepted"], 3)
        self.assertTrue(tests["initialCohort"]["frenchQuestionAnsweredInEnglish"])
        self.assertTrue(tests["initialCohort"]["failureRetained"])
        recovery = tests["multilingualCohort"]
        self.assertEqual((recovery["accepted"], recovery["cases"]), (4, 4))
        self.assertEqual(recovery["configurationWritesDuringFourCases"], 0)
        self.assertEqual(recovery["independentBeforeAfterAuthoredYamlFilesExactlyEqual"], 17)
        self.assertEqual(recovery["secondaryLanguage"], "fr-FR")
        self.assertTrue(recovery["nativeFrenchTestLanguageSelected"])
        self.assertEqual(recovery["actualRecordedUserActivityLocale"], "en-US")
        self.assertFalse(recovery["automaticTypedLanguageDetectionVerified"])
        self.assertEqual(recovery["bicycle"]["time"], "07:00")
        self.assertEqual(recovery["reading"]["time"], "21:00")
        self.assertTrue(recovery["shuttle"]["explicitSourceSupportAbstention"])
        self.assertFalse(recovery["shuttle"]["inventedPrice"])
        self.assertTrue(recovery["shuttle"]["citationIsNotEvidenceOfAPrice"])
        self.assertEqual(recovery["french"]["answerLanguage"], "French")
        self.assertEqual(recovery["french"]["exactTimes"], ["07:00", "21:00"])
        self.assertEqual(recovery["french"]["individualActualCitations"],
                         ["Harbor Training Hotel", "Forest Training Lodge"])
        self.assertTrue(tests["nativeUniversalSearchTracesVerifyOnlyIntendedKnowledgeSource"])
        self.assertTrue(tests["finalCitationSnippetsExactlyMatchActualRetrievedResults"])
        self.assertEqual(tests["officialNativeDiagnosticArchives"], 8)
        self.assertEqual(tests["configurationPayloadPresentInArchives"], 7)
        self.assertTrue(tests["oneMultilingualBicycleConfigurationPayloadEmpty"])
        self.assertTrue(tests["emptyPayloadLimitationNotHiddenOrQuestionReplayed"])
        self.assertTrue(tests["separateCohortsNotCombinedIntoAcceptance"])

    def test_native_lab5_navigation_cleanup_and_remaining_gates(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab5-native-entra-connected.json").read_text("utf-8"))
        self.assertEqual(result["completedTestsInFictionalNativeScope"],
                         ["S5-04", "S5-07", "S5-08", "S5-09"])
        navigation = result["sourceNavigation"]
        self.assertEqual(navigation["actualNativeCitationClicks"], 1)
        self.assertTrue(navigation["newExternalBrowserTabObserved"])
        self.assertTrue(navigation["exactImmutablePublishedSourceFileMatched"])
        self.assertTrue(navigation["bothExactFixtureFactsVisible"])
        self.assertFalse(navigation["sectionFragmentRetainedByBrowser"])
        self.assertFalse(navigation["originalHotelPdfNavigationAcceptance"])
        cleanup = result["cleanup"]
        for key in ("ownedDraftDeletedAndOfficialPacListAbsenceVerified",
                    "allFivePreexistingAgentIdentifiersPreserved",
                    "ownedConnectionDeletedAndReloadedInventoryAbsenceVerified",
                    "threeOriginalCompleteSearchSchemaHashesExactlyPreserved",
                    "ownedBrowserClosedNormally"):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup["preexistingConnectionNameConnectorStatusRowsPreserved"], 7)
        self.assertEqual(cleanup["ownedIndexDeleteStatus"], 204)
        self.assertEqual(cleanup["ownedIndexIndependentGetStatus"], 404)
        self.assertEqual(cleanup["remainingTemporaryLogicalObjects"], 0)
        self.assertEqual(cleanup["newArmResourcesCreatedOrDeleted"], 0)
        self.assertEqual(cleanup["rolePolicyOrOriginalAuthenticationChanges"], 0)
        self.assertFalse(cleanup["otherBrowsersTouched"])
        self.assertFalse(cleanup["privateRawExportsPublished"])
        for key in ("deniedIdentityTestExecuted", "originalHotelCorpusAcceptance",
                    "fullLabAcceptance", "T014Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])

    def test_native_lab5_progress_is_bilingual_and_keeps_final_release_open(self):
        root = Path(__file__).resolve().parents[1]
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md",
                         "backend-live-2026-10-20.md", "lab-05.md"):
                text = (root / "docs" / language / name).read_text("utf-8")
                self.assertIn("lab5-native-entra-connected.json", text)
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [ ] T014", roadmap)
            self.assertIn("- [ ] T016", roadmap)
            lab = (root / "docs" / language / "lab-05.md").read_text("utf-8")
            for criterion in ("S5-04", "S5-07", "S5-08", "S5-09"):
                row = next(line for line in lab.splitlines() if line.startswith(f"| {criterion} "))
                self.assertNotIn("Not run", row)
                self.assertNotIn("Non exécuté", row)
            denied = next(line for line in lab.splitlines() if line.startswith("| S5-10 "))
            self.assertIn("Failed:" if language == "en" else "Échec :", denied)

    def test_isolated_native_permission_removal_failure_is_not_a_pass(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab5-isolated-permission-removal.json").read_text("utf-8"))
        self.assertEqual(result["status"], "NATIVE_PERMISSION_REMOVAL_NO_LEAK_CHECK_FAILED")
        scope = result["scope"]
        self.assertEqual(scope["fictionalTrainingDocumentsOnly"], 2)
        self.assertTrue(scope["sameApprovedAdministratorOnSeparateNewSearchService"])
        self.assertFalse(scope["independentlyUnprivilegedUserTest"])
        self.assertFalse(scope["originalAdministratorWorkingPermissionsRemoved"])
        self.assertTrue(scope["searchLocalAuthenticationDisabled"])
        self.assertTrue(scope["webAndGeneralKnowledgeDisabled"])
        self.assertTrue(scope["exactlyOneNativeKnowledgeSource"])
        self.assertEqual(scope["inheritedSearchDataAssignmentsAtFinalRead"], 0)
        self.assertTrue(result["authorizedBaseline"]["accepted"])
        removal = result["permissionRemoval"]
        self.assertTrue(removal["onlyOwnedIndexScopedReaderRemoved"])
        self.assertEqual(removal["independentAssignmentGetStatus"], 404)
        for key in ("directQueryWithBeforeRemovalTokenStatus",
                    "directQueryWithTokenRequestedAfterRemovalStatus",
                    "postNativeDirectQueryStatus"):
            self.assertEqual(removal[key], 403)
        self.assertTrue(removal["bothTokenRequestsReturnedSameCachedJwt"])
        self.assertFalse(removal["newlyIssuedTokenClaimed"])
        denied = result["nativeDeniedAttempt"]
        self.assertEqual(denied["nativeQuestions"], 1)
        self.assertEqual(denied["automaticQuestionReplays"], 0)
        self.assertTrue(denied["distinctConversationFromAuthorizedBaseline"])
        self.assertTrue(denied["sameQuestionAndFrozenConfiguration"])
        self.assertTrue(denied["actualNativeSearchSourceAndSnippetsVerified"])
        self.assertEqual(denied["returnedAndVerifiedSourceRecords"], 2)
        self.assertEqual(denied["nativeSearchErrorCount"], 0)
        self.assertEqual(denied["answerOpeningTime"], "07:00")
        self.assertEqual(denied["actualIndividualCitation"], "Harbor Training Hotel")
        for key in ("noLeakCheckAccepted", "nativeEffectivePrincipalEstablished",
                    "rootCauseEstablished", "cachePropagationOrPrivilegeExplanationClaimed"):
            self.assertFalse(denied[key])
        for key in ("S5_10Accepted", "independentDeniedIdentityAcceptance",
                    "originalHotelCorpusAcceptance", "T014Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])

    def test_identity_audit_does_not_promote_signin_or_timing_to_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab5-isolated-permission-removal.json").read_text("utf-8"))
        audit = result["readOnlyIdentityAudit"]
        self.assertEqual(audit["interactiveAndNoninteractiveReadStatuses"], [200, 200])
        self.assertEqual(audit["successfulSearchConnectorSignIns"], 1)
        self.assertTrue(audit["approvedAdministratorOnly"])
        self.assertTrue(audit["signInPrecedesRevocationIntent"])
        self.assertLess(audit["secondsFromDeleteIntentToNativeSearchEvent"],
                        audit["documentedGeneralRbacPropagationSeconds"])
        for field in ("deletionCompletionIntervalEstablished", "timingGapProvesRootCause",
                      "signInProvesEffectiveNativeRequestPrincipal", "historicalFailureReclassified",
                      "readinessGuardCertifiesNativeAcceptance"):
            self.assertFalse(audit[field])
        self.assertEqual(audit["newSearchOrNativeQuestions"], 0)
        self.assertEqual(audit["resourceOrPermissionWrites"], 0)
        self.assertFalse(result["S5_10Accepted"])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("check_revocation_readiness.py", text)
            self.assertIn("600", text)

    def test_delayed_denial_guard_stops_before_native_question(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab5-delayed-denial-preflight.json").read_text("utf-8"))
        self.assertEqual(result["status"], "PREFLIGHT_BLOCKED_NO_NATIVE_QUESTION")
        self.assertTrue(result["scope"]["directAuthorizedBaselinePassed"])
        self.assertFalse(result["scope"]["pairedAuthorizedNativeThenRevokedTest"])
        revocation = result["revocation"]
        self.assertEqual(revocation["assignmentGetStatus"], 404)
        self.assertGreaterEqual(revocation["actualSecondsSinceConfirmedRevocation"], 600)
        self.assertEqual(revocation["directQueryAfterWaitStatus"], 403)
        self.assertTrue(revocation["newConnectionCreatedOnlyAfterWait"])
        preflight = result["nativePreflight"]
        self.assertEqual(preflight["sourceStatus"], "Ready")
        self.assertEqual(preflight["readinessGuardStatus"], "BLOCK")
        self.assertFalse(preflight["successfulFreshSearchConnectorSignInEstablished"])
        self.assertFalse(preflight["metadataAccountNameSubstitutedForPrincipalProof"])
        self.assertFalse(preflight["missingAuthenticationTimestampInvented"])
        self.assertEqual(preflight["nativeQuestionSubmissions"], 0)
        self.assertEqual(result["capture"]["officialExportUserMessages"], 0)
        self.assertEqual(result["capture"]["officialExportSourceExecutionEvents"], 0)
        for key in ("S5_10Accepted", "effectiveNativeRequestPrincipalEstablished",
                    "historicalFailureReclassified", "rootCauseEstablished",
                    "T014Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])

    def test_later_authentication_audit_does_not_retroactively_pass_guard(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab5-delayed-denial-preflight.json").read_text("utf-8"))
        audit = result["laterReadOnlyAuthenticationAudit"]
        self.assertEqual(audit["successfulMatchingSearchConnectorSignIns"], 1)
        self.assertTrue(audit["approvedAdministratorAndExpectedConnectorResourceMatched"])
        for key in ("resourceOrPermissionWrites", "nativeQuestionsSubmitted"):
            self.assertEqual(audit[key], 0)
        for key in ("exactAuditAvailabilityLatencyMeasured", "cleanedCohortRecreated",
                    "originalBlockedPreflightReclassified", "nativeDeniedQueryAcceptanceEstablished",
                    "effectivePerRequestPrincipalEstablished", "historicalNoLeakFailureCauseEstablished",
                    "futureCohortMayReuseThisAuthenticationEvidence"):
            self.assertFalse(audit[key])
        self.assertEqual(result["nativePreflight"]["readinessGuardStatus"], "BLOCK")
        self.assertFalse(result["S5_10Accepted"])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("00:36:59 UTC", text)
            self.assertIn("00:57:46 UTC", text)

    def test_delayed_denial_cleanup_and_bilingual_limits(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab5-delayed-denial-preflight.json").read_text("utf-8"))
        cleanup = result["cleanup"]
        self.assertTrue(cleanup["ownedDraftConnectionRolesSearchIndexAndGroupAbsent"])
        self.assertEqual(cleanup["parentIndependentGroupAndSearchGetStatuses"], [404, 404])
        self.assertEqual(cleanup["parentIndependentOwnedRoleGetStatuses"], [404] * 4)
        for key in ("allFiveOriginalAgentRowsAndSevenConnectionRowsExact",
                    "originalEmbeddingAccountAndCompleteRoleInventoryExact",
                    "allThreeOriginalSchemasExact"):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup["remainingOwnedCohortObjects"], 0)
        self.assertEqual(cleanup["pendingBrowserCommands"], 0)
        self.assertFalse(cleanup["globalAzureInventoryClaimedEmpty"])
        self.assertFalse(cleanup["actualSpendingFinalized"])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("lab5-delayed-denial-preflight.json", text)
            self.assertIn("- [ ] T014", text)
            self.assertIn("- [ ] T016", text)

    def test_native_denied_first_use_recorded_guard_really_passes(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab5-native-denied-first-use.json").read_text("utf-8"))
        guard = result["guard"]
        assessed = datetime.fromisoformat(guard["assessedAtUtc"])
        readiness = assess_readiness(guard["receipt"], assessed)
        self.assertEqual(readiness["status"], "READY_FOR_SEPARATE_NATIVE_TEST_NOT_ACCEPTANCE")
        self.assertFalse(readiness["nativeAcceptancePassed"])
        self.assertEqual(guard["status"], readiness["status"])
        direct = datetime.fromisoformat(guard["receipt"]["directQueryVerifiedAtUtc"])
        fresh = datetime.fromisoformat(guard["receipt"]["freshConversationVerifiedAtUtc"])
        self.assertAlmostEqual((assessed - direct).total_seconds(),
                               guard["directEvidenceAgeSecondsAtGuard"], places=6)
        self.assertAlmostEqual((assessed - fresh).total_seconds(),
                               guard["freshConversationAgeSecondsAtGuard"], places=6)
        self.assertGreaterEqual(
            result["authenticationAndTiming"]["actualSecondsWaitedBeforeConnectionCreation"], 600)
        self.assertFalse(result["authenticationAndTiming"]["oldCohortAuthenticationEvidenceReused"])
        self.assertFalse(result["scope"]["authorizedNativeBaselineInThisCohort"])
        native = result["nativeExecution"]
        self.assertEqual(native["questionSubmissions"], 1)
        self.assertEqual(native["automaticQuestionReplays"], 0)
        self.assertEqual(native["nativeErrorCode"], "ConnectorRequestFailure")
        self.assertEqual(native["nativeReasonCode"], "AzureAISearchClientError")
        self.assertIsNone(native["nativeHttpStatus"])
        self.assertFalse(native["nativeHttp403Claimed"])
        for key in ("returnedRecords", "verifiedRecords", "citations"):
            self.assertEqual(native[key], 0)
        self.assertEqual(native["fullParentResponse"],
                         "I'm sorry, I'm not sure how to help with that. Can you try rephrasing?")
        self.assertFalse(native["sourceFactReturnedInThisSingleResponse"])
        self.assertFalse(native["friendlyPermissionSpecificParentErrorEstablished"])
        for key in ("historicalBlockOrNoLeakFailureReclassified", "effectivePerRequestNativePrincipalEstablished",
                    "rootCauseOfHistoricalFailureEstablished", "acceptanceCombinedAcrossCohorts",
                    "independentDeniedIdentityAcceptance", "S5_10Accepted", "T014Complete",
                    "wholeRoadmapComplete"):
            self.assertFalse(result[key])

    def test_native_denied_first_use_cleanup_and_all_bilingual_surfaces(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "lab5-native-denied-first-use.json").read_text("utf-8"))
        cleanup = result["cleanup"]
        self.assertTrue(cleanup["ownedDraftConnectionRolesSearchIndexAndGroupAbsent"])
        self.assertEqual(cleanup["parentIndependentGroupAndSearchGetStatuses"], [404, 404])
        self.assertEqual(cleanup["parentIndependentOwnedRoleGetStatuses"], [404] * 4)
        for key in ("allFiveOriginalAgentRowsAndSevenConnectionRowsExact",
                    "originalEmbeddingAccountAndCompleteRolesExact",
                    "allThreeOriginalSchemasExact", "ownedBrowserClosedNormally"):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup["pendingBrowserCommands"], 0)
        self.assertEqual(cleanup["remainingOwnedCohortObjects"], 0)
        self.assertFalse(cleanup["globalAzureInventoryClaimedEmpty"])
        self.assertFalse(cleanup["actualSpendingFinalized"])
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md", "backend-live-2026-10-20.md", "lab-05.md"):
                text = (root / "docs" / language / name).read_text("utf-8")
                self.assertIn("lab5-native-denied-first-use.json", text)
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [ ] T014", roadmap)
            self.assertIn("- [ ] T016", roadmap)

    def test_isolated_denial_capture_and_cleanup_preserve_failure_and_originals(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab5-isolated-permission-removal.json").read_text("utf-8"))
        capture = result["captureAndConfiguration"]
        self.assertTrue(capture["originalPostSubmissionReadTimeoutPreserved"])
        self.assertTrue(capture["officialSnapshotRecoveredFromExistingConversation"])
        self.assertEqual(capture["newQuestionsDuringRecovery"], 0)
        self.assertEqual(capture["officialSnapshotsPreservedPrivately"], 2)
        self.assertEqual(capture["bothConfigurationPayloadBytes"], 47651)
        self.assertEqual(capture["independentAfterNativeCloneUnchangedAuthoredFiles"], 17)
        for key in ("bothConfigurationSha256", "authorizedZipSha256", "deniedZipSha256"):
            self.assertRegex(capture[key], r"^[0-9a-f]{64}$")
        self.assertNotEqual(capture["authorizedZipSha256"], capture["deniedZipSha256"])
        self.assertFalse(capture["modelReasoningInspected"])
        cleanup = result["cleanup"]
        for key in ("ownedDraftAndConnectionIndependentlyAbsent", "allFourOwnedRoleAssignmentsAbsent",
                    "ownedSearchServiceAndIndexIndependentlyAbsent",
                    "ownedGroupIndependentlyEmptyBeforeDeletionAndNowAbsent",
                    "cliConnectionDeleteRejectedByEnvironmentRouteFilterMismatch",
                    "failedCliResponsePreserved", "allFivePriorAgentIdentifiersPreserved",
                    "allSevenOtherConnectionNameConnectorStatusRowsPreserved",
                    "originalEmbeddingAccountAndEveryOriginalRoleExactlyPreserved",
                    "allThreeOriginalSearchSchemaHashesExactlyPreserved", "ownedBrowserClosedNormally"):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup["correctlyScopedFirstPartyConnectionGetStatus"], 200)
        self.assertEqual(cleanup["correctlyScopedFirstPartyConnectionDeleteStatus"], 200)
        self.assertEqual(cleanup["correctlyScopedFirstPartyConnectionAbsenceStatus"], 404)
        self.assertEqual(cleanup["remainingOwnedTestObjects"], 0)
        for key in ("successfulAgentDeleteReplayed", "otherBrowsersTouched",
                    "actualSpendingFinalized", "privateRawEvidencePublished"):
            self.assertFalse(cleanup[key])

    def test_isolated_denial_failure_is_bilingual_and_keeps_release_open(self):
        root = Path(__file__).resolve().parents[1]
        for language in ("en", "fr"):
            for name in ("completion-roadmap.md", "validation.md",
                         "backend-live-2026-10-20.md", "lab-05.md"):
                text = (root / "docs" / language / name).read_text("utf-8")
                self.assertIn("lab5-isolated-permission-removal.json", text)
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [ ] T014", roadmap)
            self.assertIn("- [ ] T016", roadmap)
            guide = (root / "docs" / language / "lab-05.md").read_text("utf-8")
            row = next(line for line in guide.splitlines() if line.startswith("| S5-10 "))
            self.assertIn("Failed:" if language == "en" else "Échec :", row)
            self.assertNotIn("Not run" if language == "en" else "Non exécuté", row)

    def test_application_activity_preflight_cannot_certify_native_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "native-activity-application-preflight.json").read_text("utf-8"))
        self.assertEqual(result["status"], "ACTIVITY_APPLICATION_DEPLOYMENT_REJECTED_BEFORE_NATIVE_TEST")
        self.assertEqual(result["scope"]["copiedUnchangedSourceAndDependencyFiles"], 6)
        self.assertTrue(result["hostedDeployment"]["supportedMultipartDeploymentSucceeded"])
        self.assertTrue(result["hostedDeployment"]["jsonRejectionAndZeroObjectCleanupPreserved"])
        self.assertFalse(result["hostedDeployment"]["platformEnvironmentInjectionRuntimeVerified"])
        application = result["application"]
        self.assertEqual(application["explicitTypeDefaultPolicyRejectedStatus"], 400)
        self.assertTrue(application["documentedMinimumBodyCreateSucceeded"])
        self.assertEqual(application["readbackAuthorizationScheme"], "Default")
        self.assertEqual(application["readbackIsolationKeySource"], "Entra")
        deployment = result["deployment"]
        self.assertEqual(deployment["createStatus"], 400)
        self.assertEqual(deployment["requestedProtocol"], "Agent")
        self.assertTrue(deployment["protocolValueListedByOfficialArmReferenceAndManagementSdk"])
        self.assertTrue(deployment["serviceRejectedProtocolEnumConversion"])
        self.assertTrue(deployment["failureAndOriginalRequestPreserved"])
        self.assertFalse(deployment["actualActivityDeploymentReady"])
        self.assertFalse(deployment["alternateUndocumentedProtocolNamesTried"])
        execution = result["execution"]
        for key in ("nativeQuestionsSubmitted", "directModelQuestionsSubmitted", "automaticQuestionReplays"):
            self.assertEqual(execution[key], 0)
        for key in ("nativeWholeParentOutputCaptured", "effectiveNativeCallerIdentityEstablished",
                    "nativeActivityAcceptancePassed"):
            self.assertFalse(execution[key])
        for key in ("T005Complete", "T006Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])

    def test_application_activity_cleanup_and_bilingual_boundary_are_explicit(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "native-activity-application-preflight.json").read_text("utf-8"))
        cleanup = result["cleanup"]
        for key in ("ownedAgentApplicationDeploymentAndBotIndependentlyAbsent",
                    "ownedRoleAssignmentsAbsent", "originalAgentVersion5DefinitionIdentityAndMetadataExact",
                    "originalArmResourceInventoryExact", "originalAccountRoleAssignmentInventoryExact"):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup["ownedDirectoryObjectGetStatuses"], [404, 404, 404, 404])
        self.assertEqual(cleanup["originalBlueprintDirectoryObjectControlGetStatus"], 200)
        self.assertFalse(cleanup["directoryDeletedItemsPurged"])
        self.assertFalse(cleanup["actualSpendingFinalized"])
        self.assertFalse(cleanup["privateRawEvidencePublished"])
        self.assertFalse(result["scope"]["anonymousAccessEnabled"])
        self.assertFalse(result["scope"]["broadPermissionsAdded"])
        self.assertFalse(result["connector"]["nativeActionSavedOrBound"])
        for language in ("en", "fr"):
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("native-activity-application-preflight.json", roadmap)
            self.assertIn("SendActivityApplication", roadmap)
            self.assertIn("authorizationScheme=Default", roadmap)
            self.assertIn("- [ ] T005", roadmap)
            self.assertIn("- [ ] T006", roadmap)

    def test_earlier_activity_api_failures_preserve_original_version_and_cleanup(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "native-activity-earlier-api.json").read_text("utf-8"))
        self.assertEqual(result["status"], "EARLIER_ADVERTISED_ACTIVITY_APIS_REJECT_DOCUMENTED_PROTOCOL")
        self.assertEqual(result["scope"]["immutableOriginalAgentVersionReferenced"], "5")
        self.assertEqual(result["scope"]["originalAgentOrEndpointWriteRequests"], 0)
        self.assertFalse(result["scope"]["newHostedAgentOrBotCreated"])
        self.assertEqual(result["scope"]["applicationAuthorizationReadback"], "Default")
        self.assertEqual(result["scope"]["applicationIsolationReadback"], "Entra")
        self.assertEqual([item["apiVersion"] for item in result["attempts"]],
                         ["2025-10-01-preview", "2026-01-15-preview"])
        for attempt in result["attempts"]:
            self.assertEqual(attempt["protocol"], "Agent")
            self.assertEqual(attempt["createSubmissions"], 1)
            self.assertEqual(attempt["createStatus"], 400)
            self.assertTrue(attempt["serviceRejectedAgentProtocolEnumConversion"])
            self.assertEqual(attempt["deploymentGetAfterRejection"], 404)
        for key in ("nativeQuestionsSubmitted", "directModelQuestionsSubmitted", "automaticQuestionReplays"):
            self.assertEqual(result["execution"][key], 0)
        for key in ("undocumentedProtocolNamesTried", "authenticationWeakened",
                    "nativeAcceptancePassed", "acceptanceMergedAcrossApiVersions"):
            self.assertFalse(result["execution"][key])
        for key in ("ownedApplicationAndDeploymentIndependentlyAbsent",
                    "originalAgentAndVersionFullReadbacksExactlyPreserved",
                    "originalArmInventoryAndAccountRolesExact", "originalApplicationInventoryExact"):
            self.assertTrue(result["cleanup"][key])
        self.assertEqual(result["cleanup"]["ownedApplicationDirectoryObjectGetStatuses"], [404, 404])
        self.assertEqual(result["cleanup"]["originalBlueprintDirectoryControlGetStatus"], 200)
        for key in ("T005Complete", "T006Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("native-activity-earlier-api.json", text)
            self.assertIn("- [ ] T005", text)
            self.assertIn("- [ ] T006", text)

    def test_remaining_activity_api_probes_do_not_claim_child_advertisement(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-26"
                             / "native-activity-remaining-api.json").read_text("utf-8"))
        self.assertEqual(result["status"], "REMAINING_ACTIVITY_API_PROBES_REJECT_DOCUMENTED_PROTOCOL")
        self.assertTrue(result["scope"]["nativeDenialCleanupIndependentlyVerifiedBeforeProbe"])
        metadata = result["providerMetadata"]
        self.assertEqual(metadata["advertisedResourceType"], "accounts/projects/applications")
        self.assertFalse(metadata["deploymentChildResourceTypeIndependentlyAdvertised"])
        self.assertTrue(metadata["parentAdvertisementDoesNotProveChildApiSupport"])
        self.assertTrue(metadata["initialLocalChildMetadataSelectionFailedBeforeAnyWrite"])
        self.assertTrue(metadata["emptyOutputDirectoryVerifiedBeforeGuardedResume"])
        self.assertEqual([attempt["apiVersion"] for attempt in result["attempts"]],
                         ["2026-03-15-preview", "2026-05-15-preview", "2026-07-15-preview"])
        for attempt in result["attempts"]:
            self.assertEqual(attempt["protocol"], "Agent")
            self.assertEqual(attempt["protocolVersion"], "2.0.0")
            self.assertEqual(attempt["createSubmissions"], 1)
            self.assertEqual(attempt["createStatus"], 400)
            self.assertTrue(attempt["serviceRejectedAgentProtocolEnumConversion"])
            self.assertTrue(attempt["serviceAlsoReportedDefinitionFieldRequired"])
            self.assertEqual(attempt["deploymentGetAfterRejection"], 404)
        self.assertEqual(result["execution"]["nativeQuestionsSubmitted"], 0)
        self.assertFalse(result["execution"]["authenticationWeakened"])
        self.assertFalse(result["execution"]["nativeAcceptancePassed"])
        self.assertTrue(result["cleanup"]["originalAgentAndVersionFullReadbacksExactlyPreserved"])
        self.assertTrue(result["cleanup"]["ownedApplicationAndDeploymentIndependentlyAbsent"])
        self.assertEqual(result["cleanup"]["ownedApplicationDirectoryObjectGetStatuses"], [404, 404])
        for key in ("T005Complete", "T006Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("native-activity-remaining-api.json", text)
            self.assertIn("- [ ] T005", text)
            self.assertIn("- [ ] T006", text)

    def test_private_channel_package_does_not_turn_defaults_into_legal_approval(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "native-channel-package-preflight.json").read_text("utf-8"))
        self.assertEqual(result["status"], "PRIVATE_CHANNEL_PACKAGE_BLOCKED_BY_UNAPPROVED_LEGAL_METADATA")
        self.assertEqual(result["scope"]["copiedUnchangedSourceAndDependencyFiles"], 6)
        self.assertEqual(result["scope"]["originalAgentOrEndpointWriteRequests"], 0)
        self.assertTrue(result["scope"]["originalFullAgentAndVersionMatchPrePortalBaselines"])
        self.assertEqual(result["scope"]["ownedPrincipalRoleAssignmentsObserved"], 0)
        deployment = result["deployment"]
        self.assertTrue(deployment["initialFailureIndependentlyVerifiedNoCloudObjectsOrRoleChanges"])
        self.assertEqual(deployment["correctedDeploySubmissions"], 1)
        self.assertTrue(deployment["supportedMultipartDeploymentSucceeded"])
        self.assertTrue(deployment["actualBotClientMatchesOwnedInstance"])
        self.assertFalse(deployment["platformEnvironmentInjectionRuntimeVerified"])
        package = result["generatedPackage"]
        self.assertTrue(package["botWebApplicationAndCustomEngineIdsMatchOwnedInstance"])
        self.assertTrue(package["defaultPrivacyAndTermsUrlsPointToProductDocumentation"])
        self.assertFalse(package["defaultsEstablishWorkshopLegalApproval"])
        self.assertFalse(package["packageUploadedOrInstalled"])
        preparation = result["servicePackagePreparation"]
        self.assertEqual(preparation["postSubmissions"], 1)
        self.assertEqual(preparation["requestedScope"], "Shared")
        self.assertTrue(preparation["privacyAndTermsFieldsOmitted"])
        self.assertEqual(preparation["status"], 400)
        self.assertEqual(preparation["errorCode"], "dependency_error")
        self.assertEqual(preparation["errorMessageWithoutRequestIdentifier"], "PrivacyUrl must be a valid HTTPS URL")
        for key in ("privacyAndTermsUrlValuesInvented", "termsValidationReached",
                    "validatedServiceZipReturned", "publishEndpointCalled", "catalogPublicationOrPackageUpload"):
            self.assertFalse(preparation[key])

    def test_private_channel_cleanup_preserves_original_and_open_acceptance(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "native-channel-package-preflight.json").read_text("utf-8"))
        for key in ("nativeQuestionsSubmitted", "directModelQuestionsSubmitted", "automaticQuestionReplays"):
            self.assertEqual(result["execution"][key], 0)
        for key in ("nativeWholeParentOutputCaptured", "effectiveNativeCallerIdentityEstablished",
                    "nativeAcceptancePassed", "publishedChannelAcceptancePassed"):
            self.assertFalse(result["execution"][key])
        cleanup = result["cleanup"]
        for key in ("ownedAgentApplicationDeploymentAndBotIndependentlyAbsent",
                    "ownedRoleAssignmentsAbsent", "originalFullAgentEndpointAndVersion5ExactlyPreserved",
                    "originalArmResourceInventoryExact", "originalAccountRoleAssignmentInventoryExact"):
            self.assertTrue(cleanup[key])
        self.assertEqual(cleanup["ownedDirectoryObjectGetStatuses"], [404, 404])
        self.assertEqual(cleanup["originalBlueprintDirectoryObjectControlGetStatus"], 200)
        for key in ("directoryDeletedItemsPurged", "actualSpendingFinalized", "privateRawEvidencePublished"):
            self.assertFalse(cleanup[key])
        for key in ("T005Complete", "T006Complete", "T016Complete", "wholeRoadmapComplete"):
            self.assertFalse(result[key])
        for language in ("en", "fr"):
            text = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("native-channel-package-preflight.json", text)
            self.assertIn("PrivacyUrl must be a valid HTTPS URL", text)
            for task in ("T005", "T006", "T016"):
                self.assertIn("- [ ] " + task, text)

    def test_historical_licensing_answer_is_not_reconstructed(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-25"
                             / "lab1-full-answer-audit.json").read_text("utf-8"))
        self.assertEqual(result["result"], "UNAVAILABLE")
        self.assertFalse(result["criterion_can_close"])
        self.assertFalse(result["answer_provenance"]["complete_answer_retained_and_matched"])
        self.assertTrue(result["source_verification"]["matches_prior_october_19_and_20_receipts"])
        self.assertFalse(result["atomic_claim_audit"]["complete"])
        self.assertIsNone(result["atomic_claim_audit"]["substantive_claim_count"])
        self.assertEqual(result["execution"]["new_questions"], 0)
        self.assertEqual(result["execution"]["network_calls"], 0)

    def test_actual_licensing_navigation_and_lab2_blockers_remain_distinct(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-25"
        licensing = json.loads((assets / "licensing-pdf-navigation.json").read_text("utf-8"))
        self.assertEqual(licensing["lab"], 1)
        self.assertFalse(licensing["acceptance_passed"])
        self.assertTrue(all(licensing["preconditions"].values()))
        self.assertEqual(licensing["execution"]["new_questions"], 1)
        self.assertEqual(licensing["execution"]["question_retries"], 0)
        self.assertTrue(licensing["execution"]["intended_uploaded_pdf_retrieval_observed"])
        self.assertEqual(licensing["execution"]["actual_pdf_source_button_clicks"], 1)
        self.assertFalse(licensing["execution"]["pdf_viewer_opened_observed"])
        self.assertFalse(licensing["source_checks"]["citation_navigation_target_edition_passage_and_page_verified"])
        self.assertTrue(licensing["source_checks"]["two_selected_new_answer_passages_match_retained_source"])
        self.assertFalse(licensing["boundaries"]["fraud_candidate_result_reused_as_lab1_acceptance"])
        self.assertFalse(licensing["boundaries"]["overall_lab1_certified"])
        search = json.loads((assets / "lab2-source-navigation.json").read_text("utf-8"))
        self.assertEqual(search["status"], "blocked")
        self.assertFalse(search["acceptance_passed"])
        self.assertFalse(search["observations"]["exact_permitted_lab2_agent_identified"])
        self.assertEqual(search["execution_boundary"]["new_agent_questions"], 0)
        self.assertEqual(search["execution_boundary"]["citation_clicks"], 0)
        self.assertFalse(search["execution_boundary"]["remote_changes"])
        self.assertFalse(search["criterion_outcomes"]["roadmap_task_closed"])

    def test_native_hosted_diagnostic_preserves_tenant_error_and_restoration(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-studio-verified-diagnostic.json").read_text("utf-8"))
        self.assertEqual(result["observed_http_status"], 403)
        self.assertEqual(result["boundary_code"], "BOTSERVICE_RBAC_CALLER_TENANT_ID_REQUIRED")
        self.assertEqual(result["observed_tool_status"], "Failed")
        self.assertEqual(result["observed_tool_tokens"], 0)
        self.assertEqual(result["fresh_question_submissions"], 1)
        self.assertEqual(result["diagnostic_state_change_submissions"], 2)
        self.assertFalse(result["diagnostic_final_ui_switch_checked"])
        self.assertFalse(result["endpoint_authentication_changed"])
        for key in ("owned_app_and_all_current_user_grants_exact_baseline",
                    "source_root_and_all26_full_rows_exactly_unchanged",
                    "candidate26_definitions_states_refs_and_published_auth_preserved",
                    "all_four_file_hashes_and_approved_bindings_verified",
                    "owned_dpapi_cache_bytes_unchanged_this_phase", "pac_profile_1_verified"):
            self.assertTrue(result[key])
        for key in ("verification_error_count", "rollback_error_count",
                    "new_connections_or_oauth_flows", "publication_attempts"):
            self.assertEqual(result[key], 0)
        self.assertFalse(result["domain_answer_observed"])
        self.assertFalse(result["whole_parent_completion_observed"])
        self.assertFalse(result["roadmap_complete"])

    def test_native_entra_only_diagnostic_restores_exact_controls_within_bound(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-studio-entra-only-diagnostic.json").read_text("utf-8"))
        self.assertEqual(result["observed_http_status"], 400)
        self.assertEqual(result["boundary_code"], "ACTIVITY_BLUEPRINT_ID_MISMATCH")
        self.assertEqual(result["observed_error_code"], "ConnectorRequestFailure")
        self.assertEqual(result["observed_tool_status"], "Failed")
        self.assertEqual(result["observed_tool_tokens"], 0)
        self.assertEqual(result["fresh_question_submissions"], 1)
        self.assertEqual(result["diagnostic_state_change_submissions"], 2)
        self.assertTrue(result["temporary_endpoint_authorization_change"])
        self.assertEqual(result["diagnostic_authorization_schemes"], ["Entra"])
        self.assertEqual(result["restored_authorization_schemes"], ["Entra", "BotServiceRbac"])
        self.assertEqual(result["active_hosted_version"], "3")
        elapsed = (datetime.fromisoformat(result["completed_utc"])
                   - datetime.fromisoformat(result["ready_utc"])).total_seconds()
        self.assertGreater(elapsed, 0)
        self.assertLess(elapsed, result["maximum_active_window_seconds"])
        self.assertEqual(result["maximum_active_window_seconds"], 300)
        for key in ("exact_endpoint_and_agent_card_restored",
                    "agent_version_definition_identity_preserved",
                    "original_manifest_byte_identical", "azure_rbac_not_changed",
                    "other_two_specialist_switches_remained_on",
                    "source_root_and_all26_full_rows_exactly_unchanged",
                    "candidate26_definitions_states_refs_and_published_auth_preserved",
                    "owned_app_and_all_current_user_grants_exact_baseline",
                    "all_four_file_hashes_and_approved_bindings_verified",
                    "owned_dpapi_cache_bytes_unchanged_this_phase", "pac_profile_1_verified"):
            self.assertTrue(result[key])
        for key in ("verification_error_count", "rollback_error_count",
                    "new_connections_or_oauth_flows", "publication_attempts",
                    "new_deployments_or_versions_created", "temporary_permission_changes"):
            self.assertEqual(result[key], 0)
        for key in ("diagnostic_final_ui_switch_checked", "anonymous_access_enabled",
                    "domain_answer_observed", "whole_parent_completion_observed",
                    "source_fidelity_acceptance", "retrieval_membership_independently_proven",
                    "original_corpus_changed", "source_text_or_raw_answers_published",
                    "roadmap_complete"):
            self.assertFalse(result[key])

    def test_native_connector_catalog_is_not_assumed_from_public_reference(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-connector-operation-contract.json").read_text("utf-8"))
        self.assertEqual(result["visible_catalog_action_count"], 10)
        self.assertEqual(len(result["visible_catalog_actions"]), 10)
        self.assertTrue(result["public_reference_lists_hosted_invocations_and_responses"])
        self.assertEqual(result["hosted_invocation_actions_not_observed_in_current_catalog"],
                         ["InvokeHostedAgentInvocations", "InvokeHostedAgentResponses"])
        self.assertTrue(result["catalog_observation_is_not_backend_operation_absence_proof"])
        self.assertEqual(result["current_attachment_operation_id"], "SendActivityV2")
        self.assertEqual(result["application_based_action_preview_operation_id"],
                         "SendActivityApplication")
        self.assertTrue(result["existing_approved_connection_offered_in_preview"])
        self.assertTrue(result["preview_cancelled_and_leave_confirmed"])
        self.assertTrue(result["empty_tool_list_verified_after_cancellation"])
        self.assertTrue(result["other_two_specialist_switches_remained_on"])
        self.assertEqual(result["add_and_configure_submissions"], 0)
        self.assertEqual(result["configuration_write_submissions"], 0)
        self.assertEqual(result["question_submissions_in_catalog_inspection"], 0)
        self.assertEqual(result["actual_restored_endpoint_protocols"], ["activity"])
        self.assertEqual(result["actual_restored_authorization_schemes"],
                         ["Entra", "BotServiceRbac"])
        for key in ("tool_added", "diagnostic_final_ui_switch_checked",
                    "identity_or_activity_payload_override_attempted",
                    "first_party_fix_for_exact_blueprint_error_verified",
                    "identity_migration_cause_proven",
                    "source_text_tokens_or_private_identifiers_published", "roadmap_complete"):
            self.assertFalse(result[key])

    def test_published_sdk_retest_does_not_inherit_studio_authorization(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                             / "native-sdk-post-studio-authorization.json").read_text("utf-8"))
        self.assertTrue(result["studio_existing_connection_association_precondition"])
        self.assertTrue(result["separate_published_channel_retested"])
        self.assertEqual(result["question_submissions"], 1)
        self.assertEqual(result["question_retries"], 0)
        self.assertTrue(result["unchanged_original_case6"])
        self.assertEqual(result["http_statuses"], [200, 200])
        self.assertTrue(result["start_stream_closed_normally"])
        self.assertTrue(result["turn_stream_closed_normally"])
        self.assertTrue(result["owned_iterators_closed"])
        self.assertEqual(result["turn_activity_count"], 5)
        self.assertEqual(result["actual_event_names"],
                         ["DynamicPlanReceived", "DynamicPlanStepTriggered", "DynamicPlanStepBindUpdate"])
        self.assertTrue(result["foundry_connection_adaptive_card_captured"])
        self.assertTrue(result["runtime_user_connector_authorization_required"])
        self.assertTrue(result["studio_association_does_not_establish_published_authorization"])
        self.assertEqual(result["temporary_owned_manifest_scope_additions"], 1)
        self.assertEqual(result["temporary_current_user_grant_scope_additions"], 1)
        self.assertEqual(result["only_new_invoke_access_tokens_removed"], 1)
        for key in ("manifest_exactly_restored", "all_current_user_grants_exactly_restored",
                    "maker_access_and_valid_refresh_entries_retained",
                    "source_candidate_files_bindings_auth_preserved",
                    "pac_profile_1_verified", "original_case_fixture_unchanged"):
            self.assertTrue(result[key])
        for key in ("connect_or_continue_submissions", "new_connection_creates",
                    "source_quote_comparisons_performed", "publication_attempts",
                    "rollback_error_count"):
            self.assertEqual(result[key], 0)
        for key in ("domain_answer_observed", "dynamic_plan_finished_observed",
                    "end_of_conversation_observed", "tenant_wide_consent_added",
                    "greeting_acceptance", "full_acceptance_claimed",
                    "source_text_tokens_connection_urls_or_private_identifiers_published",
                    "roadmap_complete"):
            self.assertFalse(result[key])
        self.assertIsNone(result["primary_error_type"])
        self.assertIsNone(result["preservation_verification_error_type"])

    def test_synthetic_search_fixture_preserves_failures_scope_and_cleanup(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-23"
        initial = json.loads((assets / "lab5-synthetic-search.json").read_text("utf-8"))
        self.assertEqual(initial["status"], "execution_failed")
        self.assertEqual(initial["document_upload_results"], [201, 201])
        self.assertEqual(initial["observed_index_statistics_document_counts"], [0] * 6)
        self.assertEqual(initial["completed_tests"], [])
        self.assertEqual(initial["embedding_requests"], 1)
        self.assertTrue(initial["owned_fixture_index_deleted_and_absence_verified"])
        result = json.loads((assets / "lab5-synthetic-search-retry.json").read_text("utf-8"))
        self.assertEqual(result["status"], "scoped_retrieval_checks_passed")
        self.assertTrue(result["correct_admin_mngenv_identity_verified"])
        self.assertEqual(result["indexed_document_count"], 2)
        self.assertEqual(result["embedding_dimensions"], 1536)
        self.assertEqual(result["embedding_model"], "text-embedding-3-small")
        self.assertEqual(result["embedding_requests"], 0)
        self.assertTrue(result["exact_input_embeddings_reused_from_recorded_first_attempt"])
        self.assertTrue(result["readiness_verified_by_actual_document_search_count"])
        self.assertEqual(result["completed_tests"], ["S5-03", "S5-05", "S5-06"])
        queries = result["query_results"]
        self.assertEqual([query["method"] for query in queries], [
            "lexical", "natural_language_vector", "hybrid", "semantic_hybrid",
            "copied_parent_filter", "nonfilterable_field",
        ])
        for query in queries[:4]:
            self.assertEqual(query["http_status"], 200)
            self.assertEqual(query["returned_ids"][0], "harbor")
        self.assertEqual(queries[4]["returned_ids"], ["harbor"])
        self.assertEqual(queries[5]["http_status"], 400)
        self.assertTrue(result["nonfilterable_field_error_identifies_chunk"])
        self.assertTrue(all(query["latency_ms"] > 0 for query in queries))
        self.assertEqual(result["original_index_schemas_verified_unchanged"], 3)
        self.assertTrue(result["owned_fixture_index_deleted_and_absence_verified"])
        self.assertTrue(result["fixture_source_ids_are_urns_not_navigable_citation_urls"])
        self.assertFalse(result["blob_container_created"])
        self.assertFalse(result["indexer_executed"])
        self.assertFalse(result["roles_or_authentication_changed"])
        self.assertFalse(result["denied_identity_test_executed"])
        self.assertEqual(result["native_agent_questions_submitted"], 0)
        self.assertFalse(result["connected_agent_or_source_navigation_acceptance"])
        self.assertFalse(result["latency_percentiles_or_generalized_hit_rate_claimed"])
        self.assertFalse(result["full_lab_acceptance"])
        self.assertFalse(result["roadmap_complete"])
        for language in ("en", "fr"):
            guide = (root / "docs" / language / "lab-05.md").read_text("utf-8")
            self.assertIn("lab5-synthetic-search-retry.json", guide)
            for test_id in result["completed_tests"]:
                row = next(line for line in guide.splitlines() if line.startswith(f"| {test_id} "))
                self.assertIn("Pass:" if language == "en" else "Réussi :", row)
            ingestion = json.loads((root / "docs" / "assets" / "runtime-2026-10-24"
                                    / "lab5-private-fictional-ingestion.json").read_text("utf-8"))
            for test_id in ingestion["completed_tests"]:
                row = next(line for line in guide.splitlines() if line.startswith(f"| {test_id} "))
                self.assertIn("Pass:" if language == "en" else "Réussi :", row)
            denied_row = next(line for line in guide.splitlines() if line.startswith("| S5-10 "))
            self.assertIn("Failed:" if language == "en" else "Échec :", denied_row)
            self.assertIn("search-security-rbac#grant-access-to-a-single-index", guide)
            roadmap = (root / "docs" / language / "completion-roadmap.md").read_text("utf-8")
            self.assertIn("- [ ] T014", roadmap)

    def test_native_recovery_alternatives_preserve_permission_and_profile_boundaries(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-23"
                             / "native-recovery-alternatives.json").read_text("utf-8"))
        self.assertTrue(result["correct_admin_mngenv_dataverse_identity_verified_by_official_pac"])
        self.assertTrue(result["existing_global_administrator_membership_verified"])
        self.assertFalse(result["dataverse_system_administrator_role_present"])
        recovery = result["documented_owned_client_self_elevation"]
        self.assertEqual(recovery["http_status"], 403)
        self.assertEqual(recovery["required_delegated_permission"], "UserManagement.Users.Apply")
        self.assertFalse(recovery["required_scope_in_live_published_resource_metadata"])
        self.assertEqual(recovery["new_permissions_granted"], 0)
        self.assertTrue(recovery["original_role_set_verified_unchanged"])
        pac = result["official_pac"]
        self.assertEqual(pac["version"], "2.14.1")
        self.assertTrue(pac["same_admin_identity_and_environment_verified"])
        self.assertTrue(pac["all_attempts_original_role_set_unchanged"])
        self.assertTrue(pac["all_attempts_original_active_profile_restored"])
        self.assertTrue(result["official_local_mcp"]["capability_discovery_succeeded"])
        self.assertEqual(result["official_local_mcp"]["cloud_tools_invoked"], 0)
        self.assertTrue(result["official_local_mcp"]["server_stopped"])
        self.assertEqual(result["evaluation_runs_submitted"], 0)
        self.assertEqual(result["new_roles_assigned"], 0)
        self.assertFalse(result["application_required_permissions_changed"])
        self.assertFalse(result["native_acceptance"])
        self.assertFalse(result["roadmap_complete"])

    def test_terraform_reconciliation_closes_only_its_measured_scope(self):
        root = Path(__file__).resolve().parents[1]
        result = json.loads((root / "docs" / "assets" / "runtime-2026-10-23"
                             / "terraform-reconciliation.json").read_text("utf-8"))
        self.assertEqual(result["roadmap_task_completed"], "T013")
        self.assertEqual(result["terraform_version"], "1.16.6")
        self.assertTrue(result["official_archive_sha256_verified"])
        self.assertEqual(result["source_file_count"], 23)
        self.assertTrue(result["source_and_private_copy_rehashed_unchanged_after_validation"])
        self.assertTrue(result["protected_sources_plan_state_and_private_ids_not_published"])
        self.assertEqual(result["resolved_providers"]["registry.terraform.io/hashicorp/azurerm"],
                         "4.45.1")
        self.assertEqual(result["resolved_providers"]["registry.terraform.io/hashicorp/http"],
                         "3.6.3")
        self.assertEqual(result["init_exit_code"], 0)
        self.assertEqual(result["validate_exit_code"], 0)
        self.assertEqual(result["validation_error_count"], 0)
        self.assertEqual(result["validation_warning_count"], 0)
        self.assertEqual(result["plan_exit_code"], 2)
        self.assertEqual(result["planned_resource_instances"], 15)
        self.assertFalse(result["apply_executed"])
        self.assertFalse(result["destroy_executed"])
        self.assertTrue(result["provider_auto_registration_disabled"])
        self.assertTrue(result["plan_only_resource_group_independently_verified_absent"])
        findings = result["unchanged_source_security_and_identity_findings"]
        self.assertEqual(findings["search_sku"], "standard")
        self.assertFalse(findings["search_has_attached_identity"])
        self.assertEqual(findings["private_endpoint_instances"], 0)
        self.assertEqual(findings["foundry_project_instances"], 0)
        self.assertFalse(findings["data_plane_search_index_created_by_plan"])
        historical = result["historical_corrected_paid_execution"]
        self.assertFalse(historical["new_execution"])
        self.assertTrue(historical["corrected_apply_passed"])
        self.assertEqual(historical["original_model_rejected"]["http_status"], 400)
        self.assertEqual(historical["corrected_chat_model_version"], "2024-11-20")
        self.assertTrue(historical["cleanup_and_resource_group_absence_verified"])
        self.assertFalse(historical["full_private_network_certification"])
        self.assertFalse(result["full_lab_5_1_acceptance"])
        self.assertFalse(result["roadmap_complete"])
        for language in ("en", "fr"):
            guide = (root / "docs" / language / "lab-05-1.md").read_text("utf-8")
            self.assertIn("terraform-reconciliation.json", guide)

    def test_authenticated_native_canary_preserves_failure_and_verified_rollback(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-23"
        canary = json.loads((assets / "native-authenticated-canary.json").read_text("utf-8"))
        self.assertEqual(canary["submitted_count"], 1)
        self.assertEqual(canary["post_retry_count"], 0)
        self.assertEqual(canary["submission_http_status"], 202)
        self.assertEqual(canary["completion_status"], "Completed")
        self.assertTrue(canary["draft_requested"])
        self.assertTrue(canary["explicit_authenticated_binding_requested"])
        self.assertTrue(canary["caller_metadata_match"])
        self.assertTrue(canary["returned_authenticated_binding_matches_request"])
        self.assertTrue(canary["returned_owner_matches_verified_caller"])
        self.assertNotIn("owner_metadata_limitation_adjudicated_by_user", canary)
        self.assertFalse(canary["connection_owner_object_id_independently_verified"])
        self.assertEqual(canary["general_quality_pass_count"], 1)
        self.assertEqual(canary["general_quality_fail_count"], 1)
        self.assertEqual(len(canary["case_checks"]), 2)
        for case in canary["case_checks"]:
            self.assertFalse(case["final_response_captured"])
            self.assertFalse(case["substantive_acceptance"])
            self.assertEqual(case["whole_parent_exactness"]["status"], "not_verifiable")
        self.assertFalse(canary["expected_answers_modified"])
        self.assertFalse(canary["case_id_to_question_mapping_independently_verified"])
        for action, state in (("activate", "Active"), ("restore", "Inactive")):
            transition = json.loads(
                (assets / f"native-diagnostic-{action}-supported.json").read_text("utf-8"))
            self.assertEqual(transition["mutation_http_status"], 204)
            self.assertEqual(transition["saved_state"], state)
            for key in ("caller_admin_mngenv_verified", "live_state_metadata_verified",
                        "saved_state_independently_read_back", "optimistic_concurrency_used",
                        "exact_diagnostic_definition_preserved",
                        "original_attachment_full_row_unchanged", "parent_full_row_unchanged"):
                self.assertTrue(transition[key])
            for key in ("definition_yaml_edited", "endpoint_authentication_changed",
                        "roles_or_consent_changed", "published"):
                self.assertFalse(transition[key])
        restored = json.loads((assets / "native-canary-restoration.json").read_text("utf-8"))
        self.assertTrue(restored["diagnostic_restored_inactive"])
        self.assertTrue(restored["saved_restoration_independently_read_back"])
        self.assertFalse(restored["roadmap_complete"])
        self.assertEqual(restored["hosted_version"], "3")
        self.assertEqual(restored["native_facing_endpoint_version_rule"], "@latest")
        self.assertEqual(restored["endpoint_authorization"], ["Entra", "BotServiceRbac"])
        self.assertEqual(restored["transcript_read"]["http_status"], 403)
        self.assertEqual(restored["transcript_read"]["missing_privilege"],
                         "prvReadconversationtranscript")
        self.assertFalse(restored["transcript_read"]["role_or_consent_changes"])
        self.assertFalse(restored["browser_read"]["keyboard_input_sent"])

    def test_owned_client_recovery_does_not_claim_native_evaluation_readiness(self):
        root = Path(__file__).resolve().parents[1]
        assets = root / "docs" / "assets" / "runtime-2026-10-23"
        recovery = json.loads((assets / "native-api-access-recovery.json").read_text("utf-8"))
        self.assertTrue(recovery["native_api_access_recovered"])
        self.assertFalse(recovery["paid_native_tests_now_possible"])
        own_client = recovery["executed_routes"][-1]
        self.assertEqual(own_client["http_status"], 200)
        self.assertEqual(own_client["test_set_count"], 0)
        self.assertEqual(own_client["evaluation_runs"], 0)
        self.assertIn("2026-10-23T16:12:49.900-04:00", own_client["approval_reference"])
        self.assertNotIn("16:39", own_client["approval_reference"])
        release = json.loads((assets / "authorized-release.json").read_text("utf-8"))
        auth = release["native_authorization"]
        self.assertTrue(auth["consent_current_user_only"])
        for key in ("tenant_wide_consent_added", "directory_roles_added",
                    "client_secret_created", "azure_profile_changed",
                    "first_party_preauthorization_bypassed"):
            self.assertFalse(auth[key])
        prepared = json.loads((assets / "native-canary-preparation.json").read_text("utf-8"))
        self.assertEqual(prepared["case_count"], 2)
        self.assertTrue(prepared["csv_roundtrip_verified"])
        self.assertFalse(prepared["replaces_acceptance"])
        self.assertFalse(prepared["cloud_testset_created"])
        self.assertFalse(prepared["authenticated_profile_created_or_verified"])
        self.assertFalse(prepared["future_run"]["runOnPublishedBot"])
        self.assertFalse(prepared["future_run"]["anonymous_fallback"])
        self.assertEqual(prepared["safety"]["evaluation_runs"], 0)
        ui = json.loads((assets / "native-ui-setup.json").read_text("utf-8"))
        self.assertTrue(ui["admin_mngenv_verified"])
        self.assertTrue(ui["owned_bot_verified"])
        self.assertTrue(ui["testset_saved"])
        self.assertTrue(ui["testset_persistence_verified_by_full_navigation"])
        self.assertEqual(ui["imported_case_count"], 2)
        self.assertTrue(ui["mcs_connection_verified"])
        self.assertFalse(ui["authenticated_profile_persistence_verified"])
        self.assertEqual(ui["safety"]["evaluation_runs"], 0)
        readiness = json.loads((assets / "native-run-readiness.json").read_text("utf-8"))
        self.assertTrue(readiness["caller_proof"]["token_tenant_and_object_id_match_intended_admin"])
        self.assertTrue(readiness["caller_proof"]["dataverse_whoami_matches_same_entra_user"])
        self.assertFalse(readiness["caller_proof"]["system_administrator_role_proven"])
        self.assertEqual(readiness["testset"]["get_http_status"], 200)
        self.assertEqual(readiness["testset"]["totalTestCases"], 2)
        self.assertTrue(readiness["schema_support"][
            "ui_profile_persistence_is_not_a_documented_requirement_for_explicit_api_binding"])
        self.assertFalse(readiness["connection_evidence"]["owner_object_id_independently_verified"])
        self.assertEqual(readiness["evaluation_runs"], 0)

    def test_verified_retrieval_debug_configuration_uses_own_entrypoint_and_environment(self):
        root = Path(__file__).resolve().parents[1]
        tasks = json.loads((root / ".vscode" / "tasks.json").read_text("utf-8"))
        launch = json.loads((root / ".vscode" / "launch.json").read_text("utf-8"))
        server = next(task for task in tasks["tasks"]
                      if task["label"] == "Run verified retrieval debug server")
        self.assertEqual(server["type"], "process")
        self.assertTrue(server["command"].endswith(
            "echo-activity\\.venv\\Scripts\\python.exe"))
        self.assertEqual(server["args"],
                         ["-m", "debugpy", "--listen", "127.0.0.1:5679", "main.py"])
        self.assertTrue(server["options"]["cwd"].endswith("src\\echo-activity"))
        self.assertEqual(launch["configurations"][0]["connect"]["port"], 5679)
        self.assertNotIn("terminateAll", json.dumps(tasks))
        self.assertNotIn("agentdev", json.dumps(tasks))

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
