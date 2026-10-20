---
title: Live rerun record - 2026-10-19
description: Live PDF retrieval and email delivery tests, executed Terraform plan, reproduced SDK failure, isolated dependency restoration, and remaining cloud gates.
ms.date: 2026-10-20
---

## Scope and current result

[All labs](index.md) | [Français](../fr/live-rerun-2026-10-19.md) | [Validation ledger](validation.md)

| Lab | Actual execution status | Remaining acceptance boundary |
|-----|-------------------------|-------------------------------|
| 0 | Azure identity, roles, quota and tools verified; owner approved paid tests | Full standard-harness readiness |
| 1 | Retrieval, refusal, directory, delivery and clarification checked; fresh validation 400 visible; new PDF answer passed five source checks | Historical full-answer audit, citation navigation and downstream connector error-body fidelity |
| 2 | Isolated 30-page licensing index connected through formal AccessKey; exact quote/edition/page/citation target and final source-aware abstention passed | External PDF viewer navigation unverified; nine connected Search questions total retain original failure |
| 3 | Native Standard topic executed once; privacy settings checked; exactly one genuine event matched five properties in KQL; logging disconnected and owned monitoring deleted | Published-channel behavior and absence of all platform identifiers not certified |
| 4 | Dedicated model invocation passed earlier; restored Standard prompt BYOM dialog inspected | Required API key conflicts with enforced Cognitive keyless policy; no connected BYOM pass |
| 5 | Private ingestion/projection checks passed; actual isolated Copilot hotel answer matched source location Qatar and unsupported request abstained | No navigable original hotel URLs; city fixture reconciled to source-stated location without changing corpus |
| 5.1 | Paid 15-instance deployment completed after model/security corrections | Not an unchanged-source apply or production network certification |
| 6 | Earlier MCP/Foundry calls and exact quotations passed; later real project and one formal Foundry connection attempt exercised | Formal Entra sign-in pop-up blocked; no Activity/Copilot conversation; earlier native citation/URL failures remain |

This is the execution follow-up requested after the original documentation review.
The checks below actually ran. They are not a claim that the whole workshop passed.
The [sanitized machine-readable results](../assets/runtime-2026-10-19/results.json)
retain the exact observed versions, counts, and failure without tenant identifiers,
private paths, credentials, or Terraform state.

## Supported backend and CLI continuation

The [October 20 backend report](backend-live-2026-10-20.md) records actual
authenticated environment/Dataverse reads and a successful official PAC clone
of the saved agent, tools and uploaded PDF. A short persistent path resolved
the observed clone failure. The existing user agent was not modified or
published and the original PAC profile was restored after each operation.
Direct Line endpoint discovery failed with a nested tenant-membership error;
maker evaluation discovery returned HTTP 403. No new conversation or email
was counted, and no additional paid resource was created.
Follow-up inspection identified the evaluation API's exact inner error:
`InsufficientDelegatedPermissions`, missing
`CopilotStudio.MakerOperations.Read`. A separate current-harness browser-open
attempt timed out without producing a conversation. Permission/consent changes
were not made, and the stopped scope request was not counted as a valid token.

The later [browser recovery and source audit](backend-live-2026-10-20.md)
executed three new Preview checks and independently verified the new answer's
edition, complete quotation and page 3 section against the retained PDF.
This later execution is separate from the earlier timed-out browser attempt;
it does not repair PAC application permissions or certify the whole workshop.
Following explicit credit approval, a three-case General quality evaluation
was saved and submitted once. It was observed Waiting for capacity without
grades. A later bounded browser recheck failed; current state is unknown.
The same report preserves the actual queue screenshot and recovery failures.
That uncertainty was later resolved by recovering the original completed run:
**1 pass, 2 failures, 7 Copilot Credits, 00:02:44**. No duplicate run was submitted.

## Foundry and MCP continuation

The [October 20 Foundry execution report](foundry-live-2026-10-20.md) adds actual
model, embedding, managed-identity connection and agent-tool execution. The
current Search MCP preview uses `query_variants`, not the older `queries`
argument. Its direct call returned the exact original title and content.
A Foundry-agent single-source call returned a verified original quotation.
The cross-source retry executed its reviewed full query, but all three claimed
quotations failed exact comparison. Formatting/length deviations are recorded
separately, not hidden by a passing transport status.

Activity configuration and independent readback passed with version 3 pinned
and Entra-only authorization. No Activity/Copilot conversation ran. The
[sanitized Foundry results](../assets/runtime-2026-10-19/foundry-results.json)
preserve both successes and failures. All three inventoried Azure resources and
their owned children were removed through guarded group deletion; independent
group absence passed. No paid test environment is intentionally retained.

## Private PDF ingestion continuation

The next isolated paid test completed the ingestion boundary left open by the
first paid run. It used a fresh **Basic** Search service in West US 2, private
Storage and the three original authorized hotel PDFs. The
[sanitized private-pipeline results](../assets/runtime-2026-10-19/private-pipeline-results.json)
record **25 passing checks**. This is actual service execution, not a reproduction
of a portal wizard screenshot or a complete connected-agent pass.

### Private transfer without weakening policy

The test kept Storage public networking, anonymous access and shared keys disabled.
A private Ubuntu runner had no public IP. Its user-assigned identity uploaded
through a Blob private endpoint, with private DNS resolution checked at runtime.
Each original PDF was downloaded again and its SHA-256 compared with the local
original: **812,743**, **812,380** and **825,009 bytes**, respectively.

The first large embedded VM Run Command returned provisioning success but no upload
marker. It was rejected as evidence; no specific payload limit or root cause was
proven. The working substitute was a temporary **Standard Azure Bastion** native
SSH/SCP tunnel. The VM host key was pinned from an authenticated Azure control-plane
read. SSH was allowed only from the Bastion subnet; the runner never received a
public IP. Three original files were transferred, then small VM commands performed
the keyless upload and hash verification. The local tunnel was stopped afterward.

A refreshed Terraform plan also tried to replace the existing NAT public IP because
Azure had injected service-managed IP tags. The working copy preserved that field
with narrowly scoped `ignore_changes = [ip_tags]`, not a broad drift exemption.
The reviewed Bastion plan then contained only three creates and one private NSG
update, with no existing IP replacement. The initial private environment had
30 Terraform instances; Bastion added three.

### Actual Blob indexer, child projections and integrated vectors

1. Assign the Search system identity Storage Blob Data Reader on the new account,
   and Cognitive Services OpenAI User on the new model resource.
2. Create a Search shared private link for the Blob group. Compare the account's
   private connection inventory before and after creation; approve only the one
   new connection. Verify both provisioning success and approval.
3. Create a Blob data source with a `ResourceId` connection string, not an account
   key. Use Search data-plane API `2026-04-01` and shared-link ARM API `2025-05-01`.
4. Create a child index with a chunk key, filterable `parent_id`, source filename,
   source URL, passage text and a retrievable 1,536-dimensional vector.
5. Configure Text Split for **400 characters** with **50-character overlap**.
   Follow it with the actual `text-embedding-ada-002` skill, using managed identity
   and no API key.
6. Configure one-to-many `indexProjections` with
   `projectionMode: skipIndexingParentDocuments`, mapping passage, vector and source
   metadata. Let Search populate the parent association.
7. Run the indexer with `executionEnvironment: private`, zero tolerated failures,
   and inspect its terminal result rather than only its creation response.
8. Retrieve the projected documents, inspect every vector and source field, then
   execute a natural-language vector query combined with semantic lexical search.

The final indexer result was **success: 3 processed, 0 failed, no errors and no
warnings**. Search produced **9 child chunks across 3 parents**, three per PDF.
All nine vectors contained 1,536 finite values and were nonzero. Every child
retained its original filename and Blob source URL. Semantic hybrid retrieval
returned three hits with reranker scores, with **Tokyo** first for the rooftop query.
Private URLs were checked as metadata, not certified as user-accessible citations.

The first automation attempt stopped after upload/link success because the
directory CLI command does not accept `--subscription`. Removing that argument
only from Graph directory lookups allowed a Search-only resume. Existing upload
and approval evidence was retained; the completed upload was not repeated.

### Cleanup ordering correction

The guarded cleanup inventory contained **17 Azure resources**; the delete-only
plan covered **33 Terraform instances**, including role assignments and helper
associations. Automatically created VM disk and private-endpoint NIC ownership
were verified before deletion.

The first destroy removed the other resources but Search returned HTTP 409,
`LockedSPLResourceFound`: it could not verify management locks on the already
deleted Storage target. This does not prove an actual management lock existed.
The recovery verified that the sole remaining Azure resource was the owned Search
service, checked the shared link's exact Storage target, deleted that owned link,
and reviewed a new deletion-only plan for the remaining Terraform objects.
No unrelated locks or resources were changed.

For reproduction, remove owned shared private links **before deleting either
Search or their target Storage account**. If a link is created outside Terraform,
do not assume the original deployment's destroy graph knows this dependency.
The structured evidence records the independent final resource-group absence
check, separately from the failed first destroy. The retry succeeded and Azure
independently confirmed that the group was absent. The tunnel was stopped and
the session SSH keys and temporary payload files were removed. No test resources
were intentionally retained. No exact billed total is claimed.

### Current limits and supported references

Basic support is not universal across all ages and regions of Search services.
The current [private-indexer guidance](https://learn.microsoft.com/en-us/azure/search/search-indexer-howto-access-private)
supports embedding skillsets on Basic or higher in supported high-capacity regions
for services created after April 3, 2024. This run tested one new West US 2 service,
not every SKU/region combination. The
[native Bastion transfer procedure](https://learn.microsoft.com/en-us/azure/bastion/vm-upload-download-native)
requires Standard or higher and native tunneling; Basic Bastion is not a substitute.

The Copilot Studio shell still failed on reload. The public shell bootstrapper
endpoint independently returned a connection reset from `curl` as well as the
browser. This is not evidence of a failed sign-in. The Azure portal Indexers route
opened, but its content frame did not load; no successful portal screenshot is
claimed for this pipeline. The pass evidence is the actual API/indexer result.

The hotel pipeline does not validate licensing-document isolation, the Copilot
Search connector, agent-originated telemetry, a connected BYOM prompt, or the
Foundry/MCP/Activity/connected-agent flow. Those acceptance boundaries remain open.

## Approved paid continuation

At **19:04 Eastern on October 19**, the owner explicitly approved paying for
the lab tests. Earlier statements about missing paid authorization below describe
the preceding checkpoints, not the current approval state. The continuation used
one new, tagged resource group for this first increment; no unrelated applications were repurposed.
The [sanitized paid results](../assets/runtime-2026-10-19/paid-cloud-results.json)
separate deployment, retrieval, synthetic telemetry and cleanup evidence.

### Terraform compatibility failures and working correction

The original create-only plan contained 15 Terraform instances. Azure created the
Search, Storage, identity, network and OpenAI resources, but rejected the original
GPT-4o `2024-05-13` deployment with HTTP 400, `ServiceModelDeprecating`.
Being listed by the model catalog did not mean it accepted new deployments.
Changing only that model version to **2024-11-20** allowed the missing deployment
to complete. This is a corrected workshop deployment, not an unchanged-source pass.

Azure policy had also set OpenAI local authentication off and Storage public
access/shared keys off. A refreshed plan tried to restore the old provider defaults.
The working-copy overrides instead preserved those policy-enforced settings.
No policy exemption or security-control rollback was used. The original source
folder was not edited.

![Partial live Azure resource grid with resource names masked](../assets/runtime-2026-10-19/lab51-live-paid-resources.png)

The portal capture is a genuine, partial grid showing the OpenAI and Search rows,
with resource links masked. The browser clipped the capture; missing rows or text
were not reconstructed. It is not a complete eight-resource inventory or proof
that a data-plane request succeeded; those assertions come from actual API checks.

### Real semantic embeddings and managed-identity vectorization

The final paid run passed **14 checks**. It used the three original hotel PDF
texts, local character-window chunking and the actual `text-embedding-ada-002`
deployment. These short inputs produced three passages, not multiple pages of
projected chunks. Each returned vector had **1,536 finite values**. The final
document-embedding batch reported **554 input tokens**; that is not the total
run's usage, which also included the earlier attempt and query-time vectorization.

The Search system-assigned identity received OpenAI User rights only on the new
lab model resource. Query-time `kind: text` vectorization then succeeded without
an API key in the vectorizer. Semantic hybrid retrieval returned three hits with
reranker scores, with **Tokyo** first. All three checked passages and source
filenames matched the original inputs. A Rome parent filter passed; explicitly
nonfilterable passage text returned HTTP 400; an unsupported lexical term returned
zero hits. The new GPT-4o deployment also returned the exact smoke-test marker,
using **18 total tokens** for that one request.

An initial negative test unexpectedly returned HTTP 200 because the test schema
omitted `filterable: false` on its string field. The owned disposable index was
deleted and recreated with that explicit property, then all checks were rerun.
This correction is recorded rather than hiding the failed first attempt.

This run proves real embeddings and managed-identity query vectorization. It does
not prove Blob ingestion, an indexer, one-to-many index projections, automatic
chunking inside Search or a grounded Copilot response. The policy-private Storage
account was not opened publicly to bypass its network boundary.

### Actual synthetic Application Insights ingestion and KQL

A dedicated workspace and Application Insights component were created in the same
isolated group. The test used Entra ID and a scoped Monitoring Metrics Publisher
role. The old `/v2/track` endpoint returned HTTP 400, **Authorization not supported**;
the AAD-capable `/v2.1/track` endpoint accepted exactly **one synthetic event**.

The first bounded query window did not yet show the event. A later read-only query
found exactly one matching event by its generated operation ID and run ID.
No accepted event was resent. This is ingestion-delay evidence, not an instantaneous
availability claim. The query was:

```kusto
customEvents
| where timestamp > ago(24h)
| where name == "AgentFactoryPaidValidationSynthetic"
| project name, operation_Id,
    Scope=tostring(customDimensions.Scope),
    RunId=tostring(customDimensions.RunId)
```

The returned operation ID and run ID were compared exactly with the submitted
event. Its scope explicitly said **Synthetic infrastructure test; not Copilot**.
This proves actual Application Insights ingestion and KQL correlation, not that
Copilot Studio emitted telemetry or that its telemetry settings were configured.

### Cleanup and remaining integration boundary

The cleanup inventory identified seven explicitly created Azure resources plus
an automatically created Failure Anomalies rule. That rule's sole scope was
verified as the new lab Insights component before including it in cleanup.
The machine-readable results record the delete-only Terraform plan and independent
resource-group absence check. No exact dollar total is inferred from token counts;
Azure billing can arrive later.

The new browser tab briefly rendered Home, but the classic popup was still not
exposed to automation and later navigation again hit the shell connection reset.
Paid approval is no longer the blocker. At the end of that increment, the remaining
gates included private Blob/indexer networking, covered by the later continuation
above. Standard-agent access, connected prompts and the Foundry/MCP/Activity/Copilot
connected-agent path remain open. No existing proof email was resent.

## Lab 0 - Actual environment preflight

Azure CLI authenticated successfully against the selected workshop subscription.
The current identity has resource-creation and role-assignment rights; the observed
roles include Owner and Foundry User at subscription scope. This checks the current
identity, not every participant's access.

The later explicit-subscription recheck returned **nine Cognitive Services accounts,
four Foundry project resources, seven Application Insights components, and zero
Search services** before the isolated tests. This corrects the earlier report of
no Application Insights components. Those resources belong to unrelated workloads;
existence and access do not authorize repurposing them or exporting their telemetry.
Existing unrelated applications were not modified.
The live eastus2 model inventory exposed `text-embedding-3-large` version `1` as
GenerallyAvailable, while the older GPT-4o versions were marked Deprecating.
Model listings and quota are prerequisites, not proof of a successful model deployment.

Terraform was initially missing from PATH. A portable **Terraform 1.16.6** binary
was restored into the private session tool directory and its archive SHA-256 was
checked against HashiCorp's published checksums. No machine-wide installation or
global PATH change was made.

## Lab 1 - Saved tools and refreshed agent

The user supplied the saved-agent screen and a newly shared direct agent page.
It shows the email and directory tools plus the licensing PDF. The saved-state
image is configuration evidence, not a newly completed knowledge or email test.

![User-provided saved agent, tools and knowledge configuration](../assets/runtime-2026-10-19/saved-tools-user-evidence.png)

The visible configuration uses **GPT-5.5 Chat**, **Send an email (V2)**,
**Search for users (V2)**, the licensing PDF, and **Search all websites**.
An accurate answer in this configuration would not, by itself, prove PDF-only
grounding. The live test must inspect the selected retrieval/tool activity.

### Fresh execution results

The newly shared Preview refreshed successfully and remained interactive. The test
used the existing agent and connections; the saved tools were preserved. No new
sign-in or consent was required.
The Agents list identified the **GitHub Copilot** harness. This validates an
equivalent core workflow in the new experience, not recreation of the original
standard-agent Topics interface.

1. The uploaded PDF retrieval executed. The answer identified **October 2026**.
   This demonstrates retrieval activity, not an independent audit of every
   licensing statement or proof that website search is globally disabled.
2. A tenant-specific discount question was refused rather than answered with
   an invented discount.
3. **Search for users (V2)** returned one matching, verified lab account.
4. **Send an email (V2)** completed without error in **1.6 seconds**.
5. The matching message was verified in both **Inbox** and **Sent Items**.
   Outlook displayed **2:44 PM**. Its unique subject was
   **Lab1 live rerun 2026-10-19 1844Z - Licensing summary**.

The exact supported prompt was:

> What Power Apps licensing options are described in the uploaded Power-Platform-Licensing-Guide.pdf? Cite the uploaded guide and identify its edition. Do not search the web or use general knowledge for this test.

The exact unsupported prompt was:

> Using only the uploaded licensing guide, what exact unpublished discount percentage and negotiated final Power Apps Premium price has Microsoft approved specifically for our Contoso tenant for next month? If the guide cannot establish that, say so. Do not invent a tenant-specific quote or search the web.

These are new browser-observed results, separate from the user's earlier screenshots.
The [sanitized Lab 1 execution record](../assets/runtime-2026-10-19/lab1-live-results.json)
preserves the observations without publishing account or tenant identifiers.
The self-mail has already been delivered. Do not resend it to obtain another screenshot.

The core retrieval, directory, send, and downstream delivery path was exercised.
At this first checkpoint, ambiguous-recipient handling and connector failure
were **not executed**. The later safe follow-up below records a conversational
clarification pass and an independently unverified connector-error attempt.
This rerun does not establish that all workshop labs passed.

### Fresh screenshots and capture limits

The following are privacy-safe crops of the new execution, not the original
workshop or user-supplied images. Browser capture exhibited a 1.5-DPR clipping
problem: the right side of the original captures is missing. No missing text was
reconstructed. Account identifiers and unrelated messages were excluded.
These partial images illustrate the observed activity; they are not full transcripts.
In particular, the mailbox subjects are truncated in the images. The full subject
and delivery results above come from the live browser observations.

#### Retrieval and unsupported-question response

![Fresh live Searched knowledge activity, partial capture](../assets/runtime-2026-10-19/lab1-live-knowledge.png)

The actual run invoked **Searched knowledge**. Expanded retrieval output, observed
during execution, identified the uploaded PDF with reference `turn1doc1`; that
complete output is not visible in this partial crop.

![Fresh refusal of an unsupported tenant-specific quote, partial capture](../assets/runtime-2026-10-19/lab1-live-unsupported.png)

The response declined to establish a tenant-specific negotiated price from the guide.

#### Directory and send-tool execution

![Fresh directory one-match response and 2.7-second latency, privacy-safe crop](../assets/runtime-2026-10-19/lab1-live-directory.png)

The directory result returned one match. Mailbox fields were excluded from the image.

![Fresh expanded send-tool excerpt and 1.6-second latency, recipient excluded](../assets/runtime-2026-10-19/lab1-live-send.png)

The expanded send-tool excerpt shows the actual input body and **1.6s** latency.
The tool did not return a message ID or delivery receipt. Downstream delivery was
checked separately in Outlook rather than inferred from the agent's response.

#### Downstream Inbox and Sent Items

![Fresh Inbox message row at 2:44 PM, partial subject](../assets/runtime-2026-10-19/lab1-live-inbox.png)

![Fresh Sent Items message row at 2:44 PM, partial subject](../assets/runtime-2026-10-19/lab1-live-sent.png)

The two folder views were checked for the same unique subject and summary.
Only the relevant message rows are included; unrelated mailbox content is excluded.

## Lab 5.1 - Terraform commands actually executed

The original Terraform package was copied to a private local execution directory.
The workshop source was not changed or published.

1. `terraform init -backend=false -input=false` succeeded.
2. `terraform validate` succeeded.
3. JSON validation reported `valid: true`, zero errors and zero warnings.
4. A local override set `resource_provider_registrations = "none"` to prevent
   automatic subscription writes during the planning exercise.
5. `terraform plan -input=false -refresh=false -detailed-exitcode` succeeded with
   exit code **2**, meaning a valid plan with proposed changes, not a failure.
6. The saved plan contains **15 planned resource instances**. No apply was performed.

| Resource type                    | Count |
|----------------------------------|-------|
| Cognitive account                | 1     |
| Model deployments                | 2     |
| Resource group                   | 1     |
| Role assignments                 | 6     |
| Search service                   | 1     |
| Storage account                  | 1     |
| User-assigned identity           | 1     |
| Virtual network                  | 1     |
| Local random identifier resource | 1     |

Resolved provider versions were AzureRM **4.45.1**, AzAPI **1.15.0**, AzureAD **2.48.0**,
Random **3.6.1**, and HTTP **3.6.2**. A provider lock was generated in the private
execution copy. The raw plan and state are not publication artifacts.

This validates initialization, provider/schema compatibility, and plan generation.
It does not validate resource deployment, model availability in the configured
deployment region, role propagation, indexing, networking, or later integrations.
The unmodified package still proposes a paid Standard Search service and the older
model configuration described in the [deployment guide](lab-05-1.md).

## Lab 5 - Actual input-readability checks

All three supplied hotel PDFs were opened with the installed PDF parser and their
text was extracted locally. Each is unencrypted and contains one page.
The Doha, Rome, and Tokyo city checks passed; extracted text lengths were **774**,
**767**, and **743** characters respectively. See the
[sanitized input results](../assets/runtime-2026-10-19/hotel-input-results.json).

This proves the supplied inputs are readable and nonempty, not that Azure ingested
them or that the advanced Search queries returned the expected results.

## Lab 6 - Actual dependency compatibility test

Only the notebook's import statements were executed. Cloud calls, reset code,
agent creation, and cleanup cells were excluded.

### Failure reproduced in the current environment

With `azure-search-documents==12.0.0` and `azure-ai-projects==2.3.0`, **14 of 15**
imports succeeded. The cell 14 import failed:

```text
cannot import name 'KnowledgeRetrievalMinimalReasoningEffort'
from 'azure.search.documents.indexes.models'
```

This is a reproduced SDK incompatibility, not a speculative source-review concern.
No silent fallback or replacement retrieval answer was used.

### Source-pinned restoration and retest

A separate virtual environment was created without changing the shared interpreter.
The runtime packages were restored from the versions pinned in the workshop:

```text
azure-ai-projects==2.0.0b3
azure-search-documents==11.7.0b2
azure-identity==1.25.1
azure-core==1.38.0
openai==2.16.0
python-dotenv==1.2.1
requests==2.32.5
```

All **15 of 15 imports passed** after restoration. This provides a working local
dependency baseline for the supplied code. It does not prove that the preview
contracts still work against the current Azure services; that remains a cloud test.

Further inspection verified that the current SDK exposes
`KnowledgeRetrievalMinimalReasoningEffort` in
`azure.search.documents.knowledgebases.models`, not `indexes.models`.
`KnowledgeBase` and `KnowledgeSourceReference` still exist under `indexes.models`;
`KnowledgeRetrievalOutputMode` does not exist in either inspected namespace.
Changing only one import is therefore not a complete notebook migration.
The GA REST retrieval test below avoids pretending that restoring imports proves
all historical preview contracts work.

The three inline data sets were also evaluated locally without executing notebook
cloud cells. Each contains eight records, for **24 total**. Every record has a
nonempty string `id`, `title`, and `content`, and IDs are unique within each set.
The protected content itself is not republished.

## Remaining execution gates

### Safe Lab 1 follow-up and independent source check

The ambiguity-only prompt asked what information was needed when several colleagues
were named Alex, expressly prohibiting connector calls. The response requested an
email address, full name, contextual identity or UPN before any action. This passed
the **conversational clarification guard**, not full send-time ambiguity enforcement.
No new email was sent.

A read-only self-search with `top=-1` was attempted. The agent reported HTTP 400,
`Top parameter should be a positive number.`, without retry. Initially the raw
execution card could not be inspected. After the user signed in again, **History
exposed the existing `SearchforusersV2` connector input, red failed activity and
Failed conversation status**. The observed input was the string `top: "-1"`,
with the verified self account and string `isSearchTermRequired: "true"`.
The failed activity took **4.62 seconds**. This independently confirms the controlled
connector call and failure indicator, not the specific HTTP status or error body:
the card did not expose an Output section. HTTP 400 and the quoted error text
remain model-reported. Expired-authentication handling was not tested.
No test, directory lookup or email was repeated to recover this evidence.

![Existing failed connector activity recovered from live History, identifiers excluded](../assets/runtime-2026-10-19/lab1-live-failed-activity.png)

An independent local copy of `Power-Platform-Licensing-Guide.pdf` was found in Downloads.
Its actual cover says **October 2026**. PDF pages 6 and 7 support the summary's
Premium per-user, per-app pay-as-you-go and limited included-rights statements.
Page 30 records the January 2026 per-app end-of-sale change. Six exact source checks
passed. The local file has 30 pages and SHA-256 recorded in the
[source-check results](../assets/runtime-2026-10-19/licensing-source-check.json).
The signed-in inspection subsequently opened the actual uploaded source, observed
its **File / Ready** state, and clicked **Download**. The user confirmed saving it
in Downloads. The freshly saved file was **867,776 bytes**, modified at **17:38:43
local time**, and its SHA-256 matched the previously audited copy:
`e1b4789118ff8f1bb633683d6fbeb750b80c25b16760d036eff247e477a524d6`.
All six source checks were rerun and passed. This establishes a matching downloaded
copy using **user-confirmed download provenance plus filesystem hashing**; no
browser download event, Content-Disposition filename or server-side hash was captured.
It is not a full citation audit or verification of today's applicable commercial terms.

![Actual local licensing PDF cover, not portal UI](../assets/runtime-2026-10-19/licensing-local-cover.png)

### Actual Azure Free-tier execution

Rather than create paid resources, the rerun used an isolated **Search Free SKU**,
**semanticSearch=free**, and **knowledgeRetrieval=free**. Current
[Search tier documentation](https://learn.microsoft.com/en-us/azure/search/search-sku-tier)
and [agentic billing documentation](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-enable-disable)
confirm the limited free tier and that requests exceeding the free retrieval
allowance fail instead of automatically entering the paid plan.
No Storage account, external model call, paid Search tier, or unrelated resource
was used. API keys remained in process memory and were not written to public evidence.

The first attempt in **eastus2** failed with `InsufficientResourcesAvailable`.
The alternate **westus2** Free service worked. A first semantic query returned HTTP
400 because `queryLanguage` is not accepted by the **2026-04-01** Search API.
Removing that parameter and rerunning the real requests resolved the failure.
The failed attempt is retained in the [sanitized cloud results](../assets/runtime-2026-10-19/free-cloud-results.json),
not overwritten with a success-only story.

#### Hotel retrieval: actual data and measured assertions

The three supplied hotel PDFs were extracted locally and uploaded as **three full
text documents**, not blob-indexed chunks. Each per-document upload status passed.

* The exact document count was **3**; lexical Doha, Rome and Tokyo queries each
  returned only the matching hotel.
* A Rome filter returned only Rome; the three city facets each had count **1**.
* `rooftop garden` with `searchMode=any` returned Tokyo, but `searchMode=all` returned
  zero. The actual supplied corpus has a rooftop term but no garden term.
* `bicycle storage` with all-terms matching returned zero: no supplied PDF contains
  the bicycle term. The source example is not automatically a positive test.
* Vector-only and hybrid requests ranked Tokyo first using explicit
  **three-dimensional city one-hot features**. These are transparent test features,
  **not semantic embeddings** or evidence of semantic relevance quality.
* A real semantic query returned Tokyo first with a non-null reranker score.
  The `title-boost` scoring profile also executed. No relevance improvement is claimed.
* Filtering on nonfilterable `content` returned **HTTP 400**.
  A request without credentials returned **HTTP 403**, not document data.

These tests validate actual Search indexing and retrieval API behavior. They do
not validate Storage ingestion, chunk projections, integrated embeddings, managed
identity, citation URLs, or the Copilot Studio Search connection required by the
original Labs 2 and 5.

#### Lab 6: actual three-source knowledge retrieval

The run-owned hotel index was removed to respect the Free tier's three-index limit.
The original notebook's three datasets were then uploaded into three fresh indexes:
**8 + 8 + 8 = 24 records**, with every individual upload status and final count checked.
Three real search-index knowledge sources and a knowledge base referencing all
three were created successfully.

The implementation used the current **2026-04-01 GA minimal/extractive REST contract**:
no LLM configuration, query planning, generated embeddings, or answer synthesis.
The current [minimal-retrieval guidance](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort)
and [GA knowledge-base contract](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
explain this supported alternative to the older preview notebook.

1. A specific fraud-pattern query returned **2 passages and 2 references**, from
   the fraud-pattern source.
2. The cross-source query `fraud investigation compliance` returned **17 passages
   and 17 references spanning all three sources**.
3. An unsupported nonsense query returned **0 passages and 0 references**.
4. All three knowledge sources appeared in activity for each request.
5. All **19 returned passage titles and contents matched their original indexed
   records exactly**, joined through each reference's `docKey`. `sourceData` was
   null; validation did not assume it contained the document.

The final run passed **34 HTTP/schema/count checks**, plus the three exact
retrieval-output/content checks above. The raw data and full responses remain
private; only counts, assertions and test metadata are published.
This proves Search knowledge retrieval, **not** a Foundry agent, MCP connection,
Activity endpoint, or Copilot Studio connected-agent flow.

#### Cleanup and remaining limits

All **four** isolated resource groups created across capacity-failure, initial
hotel, corrected hotel and multi-source attempts were deleted. Absence was verified
after each deletion. Only groups bearing the current run's exact ownership tag
and containing no unexpected resources were eligible for cleanup.
No existing service, agent, connection, or mailbox was deleted.

No billable resources have been created or applied. Requests for a deployment budget
received no actual user answer; an automated unavailable-user response is not treated
as approval. The pricing tool returned no rate for the attempted Search SKU queries,
so no price or hard spending guarantee is assumed.

The original paid deployment, Storage/vectorizer pipeline, correlated agent telemetry,
connected BYOM prompt and Foundry/Copilot connected-agent tests still need an approved
dedicated resource and spending boundary. Existing production resources are not
substitutes without workload-owner approval. The Free Search and source-verification
work above is real progress, but **the whole workshop is not certified passed**.

## What remains unchanged

### Final access recheck

An earlier bounded attempt opened the exact existing-agent Preview URL. It redirected
to Microsoft sign-in (`login.microsoftonline.com`) and the browser reported
`ERR_ABORTED (-3)` without returning a usable page ID. This is now an **interactive
authentication gate**, not evidence that the saved agent or its tools failed.
The user subsequently completed sign-in and shared the agent again. The **21:35-21:44
UTC follow-up succeeded**, recovering History and the uploaded-file dialog.
That authentication blocker is resolved for this observation window.
No authentication, consent or account selection was bypassed.

### Current authoring surface inspected after sign-in

The [sanitized follow-up record](../assets/runtime-2026-10-19/signed-in-followup.json)
records the read-only inspection. The selected model remained **GPT-5.5 Chat**;
no new harness identifier or product build version was exposed.

* Mode menu: **Build, Preview, Evaluate, Monitor**
* Settings: **Agent details, AI & behavior, Safety & access, Greeting & prompts**
* Add tool: **Featured, MCP, Connectors, Workflows**
* Connected agents: only published agents can connect; the picker displayed
  **Classic agent connections are not supported**

Conventional Topics, Application Insights configuration, a custom model endpoint
in the model menu, and a Foundry endpoint in the connected-agent picker were
**not exposed in the inspected controls**. This is a current-surface observation,
not a claim that those capabilities are globally unavailable. It explains why
the original standard-agent monitoring, prompt BYOM and connected-Foundry
instructions cannot be claimed reproduced just by inspecting this saved agent.
The Save control remained ARIA-disabled, and inspection dialogs were cancelled.
No configuration, connection, model, agent or publication was changed.

### Native monitoring checked against existing execution History

During **21:49-21:54 UTC**, **Monitor** opened successfully for this saved Draft
agent. The selected range was **Last 7 days, 10/13/26-10/19/26**.
The browser timezone was America/Toronto; the dashboard did not explicitly identify
its aggregation timezone. [Sanitized results](../assets/runtime-2026-10-19/monitor-results.json)
preserve the actual displayed values and limitations.

![Actual Monitor empty state and partial overview, not Application Insights](../assets/runtime-2026-10-19/lab3-live-monitor.png)

The overview displayed **0 sessions, 0 sec average duration, 0% success and 0 credits**
with **No data yet**. Its banner said information would appear after evaluation
and publication. These are empty/unavailable aggregates, not evidence of zero
historical consumption, instant execution or a true 0% success rate.
No Publish or Evaluate action was taken to change that state.

![Actual empty Sessions view, date range and transcript permission restriction](../assets/runtime-2026-10-19/lab3-live-sessions.png)

**Sessions > See all (0)** displayed no rows, `--` averages and a message that
the current identity lacked access to session transcripts. Download was disabled.
No permission escalation or transcript export was attempted.

The existing **Preview > History** conversation independently exposed the prior
directory call (**2.73s**), matching-subject email call (**1.63s**) and failed
directory call (**4.62s**). Its header separately showed **90.33 estimated credits**.
That estimate is not USD or an Azure bill, and the zero-credit Monitor aggregate
does not override it. Correlation was possible by existing conversation, tool
input and the unique email subject, **not** by Monitor rows, because none existed.

Finally, **Home > sidebar ... > Open classic experience > Skip feedback** was
found in the real UI. The destination popup did not become available; subsequent
shell requests returned `ERR_CONNECTION_RESET`. The route exists, but this run did
not prove that the same saved agent can use the standard-agent Topics, Application
Insights and Prompt/BYOM controls. No agent conversion or creation was attempted.
The native monitoring inspection is useful current-version evidence, **not an
Application Insights, custom-event or KQL pass**.

A read-only deployment inventory found **23 successful model deployments across
eight of the nine Cognitive Services accounts**. This establishes deployment
metadata, not permission to send workshop data to unrelated workloads, free
inference, endpoint compatibility, or successful BYOM execution. No inference
request was made and no key was retrieved from those existing accounts.

The original Word documents, notebook, and Terraform sources are unchanged.
Existing production or unrelated lab resources were not modified. The original
Lab 1 send/receipt screenshots remain historical user evidence, distinct from any
new assistant-executed test.
