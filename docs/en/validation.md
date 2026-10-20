---
title: Workshop validation ledger
description: Evidence, completed checks, runtime limitations, and the acceptance criteria still required for each workshop lab.
ms.date: 2026-10-20
---

## Overall verdict

[All labs](index.md) | [Français](../fr/validation.md) | [Evidence gallery](evidence.md)

Latest execution evidence: [actual rerun record](live-rerun-2026-10-19.md).
The owner approved paid testing. A corrected 15-instance Terraform deployment,
14 keyless model/retrieval checks, and one actual synthetic Application Insights
event with exact KQL correlation passed; the owned resources were deleted and
absence verified. A further private PDF pipeline passed 25 checks, including an
actual Blob indexer, nine child projections and integrated 1,536-dimensional
embeddings. The latest record separates its cleanup from the earlier run.
Lab 6's SDK failure and isolated restoration were also tested. Its later
[paid Foundry run](foundry-live-2026-10-20.md) generated 24 real embeddings and
verified 22 retrieved passages. Direct authenticated MCP and single-source
Foundry-agent grounding passed. Cross-source final exact quotations failed;
Activity configuration passed without an Activity/Copilot conversation.
That isolated environment was also deleted and its absence independently verified.
The later [approved quotation recovery](foundry-live-2026-10-20.md#8-approved-quotation-recovery-and-remaining-citation-failure)
passed all three exact quotations twice, but native citation fields were blank.
The unsupported model abstained despite seven off-topic retrieved documents.
Four new sequential test environments were deleted; independent checks confirmed
four absent groups and eight account/Search ARM 404 responses.
The [backend continuation](backend-live-2026-10-20.md) authenticated to Dataverse
and cloned the actual saved agent through official PAC. Direct Line discovery
and PAC evaluation authorization remain blocked; a clone is not a conversation.
The later [browser recovery](backend-live-2026-10-20.md#browser-recovery-and-three-new-runtime-checks)
did execute three fresh Preview checks: uploaded-PDF retrieval/answer capture,
unsupported-price refusal and visible invalid-input validation 400.
Evaluate UI access recovered, but no evaluation was created or run.
An independent retained-PDF audit then passed all five checks for the new
answer's source identity, edition, complete quotation and page 3 section.
Historical full-answer auditing, citation navigation and connected-lab acceptance
remain open.
With explicit credit approval, one three-case General quality evaluation was
then saved and submitted. It was observed queued, not graded; the 11:36 UTC
browser recovery failed, so its current state is unknown.
The [approved-run evidence](backend-live-2026-10-20.md#approved-evaluation-submitted-grading-not-observed)
does not claim a score, credit total or repaired PAC permission.
The next shared tab displayed a Dataverse setup error, but fresh authenticated
reads returned HTTP 200 for the same provisioned environment, identity and saved
bot. That portal message does not prove deletion or justify a replacement database.
An offline Foundry citation-contract diagnosis also passed 45 checks, identifying
unsupported JSON/title-binding assumptions without inventing missing native annotations.
One supported-format live retest then preserved source sentences but invented
all three document URLs and still produced zero native annotations.
It stopped without repair prompting. The fifth owned environment was deleted;
all five groups and ten account/Search ARM 404s were independently verified.
The tables below retain the original review baseline unless superseded by those records.

The working session later recovered the original completed evaluation:
**1 pass, 2 failures, 7 Copilot Credits, 00:02:44**. No duplicate was submitted.
The [completed-run report](backend-live-2026-10-20.md#completed-evaluation-recovered-from-the-working-session)
preserves the refusal/relevance mismatch and PDF completeness/citation failure.
A Standard authoring/test destination is now reachable, but merely reaching
its integration controls does not pass the connected-lab gates.
The later [Lab 3 connected test](lab-03.md#later-connected-agent-test-passed)
did pass the remaining agent-originated telemetry boundary: one real native
topic execution, privacy-settings readback and one independently matched
Application Insights event with five synthetic properties. No synthetic emitter
or published channel was used. Platform conversation/channel identifier keys
still exist; their values are excluded from published evidence.

After explicit user approval, the
[trial extension](../assets/runtime-2026-10-20/trial-extension.json)
removed the expired-trial dialog and restored generative settings. No recurring
purchase, new environment, unrelated consent or web-search activation occurred.
The expiry date was not displayed or verified; advanced connector authentication
contracts still require inspection.

Documentation review and publication are separate from live lab validation.
The workshop is **not certified as fully rerun**. Lab 1 has user-provided evidence
of its email outcome plus a fresh core-path rerun. Other labs now have real cloud
subsystem evidence, but their complete connected-agent integrations remain unverified.

The browser initially reached an authentication barrier. The user then signed in
and initialized the GitHub wiki. That removed the publication barrier; it did not
automatically create Search, telemetry, models, indexes, knowledge bases, or connectors.

## Status definitions

| Status                 | Meaning                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------- |
| Observed user run      | The provided evidence shows a specific outcome; not a new assistant rerun             |
| Read-only check passed | A tool directly observed a narrow prerequisite or repository condition                |
| Procedure reviewed     | The source workflow was compared with official guidance; execution is still needed    |
| Static check           | A local file or code property was inspected without executing its cloud operations    |
| Blocked                | A prerequisite, permission, environment, or supported integration prevents completion |
| Not run                | No execution result is available                                                      |

An unavailable or untested step remains blocked/not run. A screenshot from a Word
document, a generated diagram, or a plausible agent answer cannot upgrade that status.

## Original review baseline

The following table preserves the initial review state. Use the linked
[current per-lab execution table](live-rerun-2026-10-19.md) for later real results.

| Lab                | Current result                                                                      | Required evidence before a full pass                                                                            |
| ------------------ | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [0](lab-00.md)     | Partial read-only preflight; complete environment readiness not established         | Environment, entitlement/capacity, policy, data permissions, quota, Terraform, and budget verified              |
| [1](lab-01.md)     | Observed user run: send tool and received message; not every negative test executed | New controlled run with grounded answer, recipient resolution, send result, receipt, and negative tests         |
| [2](lab-02.md)     | Procedure reviewed; no demonstrated complete retrieval run                          | Successful indexer, nonempty relevant Search results, connected Copilot answer with expected sources            |
| [3](lab-03.md)     | Procedure reviewed; no demonstrated telemetry ingestion                             | Deliberate event correlated to a recent lab interaction and visible in the intended log query                   |
| [4](lab-04.md)     | Procedure reviewed; no demonstrated connected-model run                             | Direct model test, parsed retrieval, prompt invocation, grounded answer, explicit empty/error behavior          |
| [5.1](lab-05-1.md) | Static deployment review; no apply performed                                        | Compatible providers, reviewed plan, approved apply, expected resources and private configuration               |
| [5](lab-05.md)     | Source/static review; advanced query results not observed                           | Supplied corpus indexed, required queries executed, expected fields/ranking/filter behavior recorded            |
| [6](lab-06.md)     | Source/static review; end-to-end connected-agent run not observed                   | Complete data/configuration, supported SDK/API, direct retrieval, Foundry agent and Copilot connection verified |

## Checks performed in this session

| Check                                    | Observed result                                                                                    | Scope limitation                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Source inventory                         | Labs 0–6 and supplement 5.1 found, plus supporting files                                           | Does not prove the runtime package is complete                                                |
| Word source access                       | Readable ZIP-based documents extracted locally; compound-format files read through installed Word  | Protected source documents are not republished                                                |
| Lab numbering                            | Monitoring/BYOM internal titles contradict their filenames                                         | Guides consistently follow filenames                                                          |
| Azure CLI                                | Installed version 2.91.0; selected account query succeeded                                         | No claim about every subscription or tenant                                                   |
| Provider registration                    | Search, Cognitive Services, Insights observed Registered                                           | Registration does not prove role rights, capacity, network access, or deployment success      |
| Selected-subscription resource inventory | Original absence claim corrected by explicit recheck: 9 Cognitive accounts, 4 projects, 7 unrelated Insights components, 0 Search before disposable tests | Free Search tests and verified cleanup are in the latest runtime record |
| Terraform executable                     | Not found on PATH                                                                                  | No terraform init, validate, plan, or apply claimed                                           |
| Copilot browser                          | Sign-in succeeded and Home was visible; agent navigation then returned a persistent blank page     | Licensing advisor could not be opened; no new knowledge question was submitted                |
| GitHub publication access                | Private repository created; wiki enabled and initialized by the owner                              | Repository and wiki require separate commits and remote verification                          |
| Lab 1 attachments                        | Send-tool/result crop and matching received-email crop preserved                                   | No independent transport-header or licensing-content audit                                    |
| Current product guidance                 | Official Microsoft Learn references checked for the documented substitutions                       | Documentation checks are not runtime tests                                                    |
| Lab 6 notebook                           | 11 of 11 code cells syntax-valid; 24 inline records identified                                     | Syntax and data presence do not prove API, inference, retrieval, or integration compatibility |
| Advanced-lab examples                    | Four JSON examples checked; SVG diagrams parsed; acceptance IDs aligned between languages          | Examples and diagrams do not prove cloud behavior                                             |

The advanced-lab review also identified Terraform identity/network gaps, disabled
Foundry provisioning, embedding-dimension consistency requirements, API/SDK drift,
and destructive reset behavior that must be resolved or consciously gated before a
live run. Consult the detailed findings in Labs 5.1, 5, and 6 rather than applying the
original package unchanged.

### Advanced-package findings that need action

1. The supplied Terraform configuration disables the Foundry module, so the
   advertised Foundry project is not provisioned by that path.
2. The Search module does not apply the supplied allowed-IP/Entra options as expected,
   and the required service identity is not attached. Review effective resources and
   role assignments before treating the configuration as an identity/network baseline.
3. The deployment supplement uses 1,536-dimensional embeddings while Lab 6 expects
   3,072. These are different configuration expectations, not interchangeable indexes.
   Align the model output, index field, and query embedding for the selected lab.
4. Preview SDK, ARM, and MCP contracts require compatibility reconciliation. The
   connected-agent route requires the supported Activity/new-portal agent contract.
5. Notebook reset code deletes fixed-name objects; the final cleanup is commented
   out. Do not run reset cells against a shared project.

The notebook also references a quick-reference Markdown file that is absent.
The package supplies `data\quick_reference_guide.docx` instead. Renaming an extension
does not convert a document; obtain an authorized source in the expected format.

## Documentation and tooling gates

The offline gates are reproducible using:

```powershell
python -m py_compile scripts\build_wiki.py scripts\validate_docs.py scripts\test_docs.py
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts\build_wiki.py --output .wiki-build
python scripts\validate_docs.py --wiki .wiki-build
```

The offline checks passed for the publication snapshot: Python compilation, seven
unit tests, 28 canonical Markdown files, 13 English/French page pairs, 29 manifested
PNG figures, and 30 exported wiki Markdown files. There were no broken local links
or missing image/provenance entries. No pre-existing linter or package build was
configured in the initially empty repository.

The final publication is accepted only after these checks succeed and the remote
repository/wiki commits match the local published commits. These checks validate the
documentation deliverable, not cloud execution. See
[publication procedure](../publishing.md) for export details and maintenance.

## Remaining live validation work

1. Confirm the selected workshop environment, harness, credits, permissions, quota,
   data policies, approved budget, and cleanup owner.
2. Preserve the working Lab 1 agent before changing its knowledge or topics.
3. Provision only the dedicated, approved Search and telemetry resources required
   by the selected labs. Do not reuse unrelated production resources.
4. Execute the test matrices in each guide in dependency order.
5. Capture new, redacted evidence with input, result, timestamp, source edition,
   model/API version, and downstream outcome where applicable.
6. Fix the smallest failing boundary, retest it, then retest the integrated path.
7. Update both language ledgers and distinguish partial tests from a complete lab pass.

The initial documentation-only phase created no billable resources. Later owner-approved
paid tests and their cleanup are explicitly recorded in the execution ledger.
No billing-policy change or modification of unrelated applications was made.
Stop at blocked rather than inventing an integrated pass from subsystem results.
