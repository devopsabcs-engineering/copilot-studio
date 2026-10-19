---
title: Live rerun record - 2026-10-19
description: Live PDF retrieval and email delivery tests, executed Terraform plan, reproduced SDK failure, isolated dependency restoration, and remaining cloud gates.
ms.date: 2026-10-19
---

## Scope and current result

[All labs](index.md) | [Français](../fr/live-rerun-2026-10-19.md) | [Validation ledger](validation.md)

| Lab | Actual execution status | Remaining acceptance boundary |
|-----|-------------------------|-------------------------------|
| 0 | Azure identity, role, model inventory and portable Terraform verified | Dedicated paid-resource authorization |
| 1 | PDF retrieval, refusal, directory, self-mail delivery and clarification observed | Uploaded/local PDF identity, full citation audit and independently verified connector failure |
| 2 | Actual document indexing and Search API retrieval through a Free alternative | Blob ingestion, integrated embeddings and Copilot Search connection |
| 3 | Resource inventory corrected; unrelated telemetry left private | Agent telemetry configuration, synthetic event and correlated KQL evidence |
| 4 | Current BYOM procedure reviewed | Approved model invocation and connected prompt |
| 5 | 17 actual hotel Search assertions passed | Semantic embeddings, chunk pipeline and grounded Copilot answer |
| 5.1 | Original Terraform init, validate and 15-instance plan passed | Paid original apply not authorized; temporary Free alternative deployed and cleaned |
| 6 | 24 records, 3 indexes/sources, actual minimal retrieval and 19 exact source matches | Foundry model/agent, MCP, Activity and Copilot connected-agent flow |

This is the execution follow-up requested after the original documentation review.
The checks below actually ran. They are not a claim that the whole workshop passed.
The [sanitized machine-readable results](../assets/runtime-2026-10-19/results.json)
retain the exact observed versions, counts, and failure without tenant identifiers,
private paths, credentials, or Terraform state.

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
`Top parameter should be a positive number.`, without retry. The raw execution card
could not be inspected before Preview became blank again. This remains **model-reported,
not independently certified connector failure**. Expired-authentication handling
was not tested.

An independent local copy of `Power-Platform-Licensing-Guide.pdf` was found in Downloads.
Its actual cover says **October 2026**. PDF pages 6 and 7 support the summary's
Premium per-user, per-app pay-as-you-go and limited included-rights statements.
Page 30 records the January 2026 per-app end-of-sale change. Six exact source checks
passed. The local file has 30 pages and SHA-256 recorded in the
[source-check results](../assets/runtime-2026-10-19/licensing-source-check.json).
Its filename matches the uploaded file, but uploaded/local **byte identity was not
verified**. This is an independent check of the local guide, not proof of every
uploaded-file citation or of today's applicable commercial terms.

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

A further bounded attempt opened the exact existing-agent Preview URL. It redirected
to Microsoft sign-in (`login.microsoftonline.com`) and the browser reported
`ERR_ABORTED (-3)` without returning a usable page ID. This is now an **interactive
authentication gate**, not evidence that the saved agent or its tools failed.
An authorized user must complete sign-in/account selection and share the loaded
Preview again before the remaining agent-side acceptance checks can resume.
No authentication, consent or account selection was bypassed.

A read-only deployment inventory found **23 successful model deployments across
eight of the nine Cognitive Services accounts**. This establishes deployment
metadata, not permission to send workshop data to unrelated workloads, free
inference, endpoint compatibility, or successful BYOM execution. No inference
request was made and no key was retrieved from those existing accounts.

The original Word documents, notebook, and Terraform sources are unchanged.
Existing production or unrelated lab resources were not modified. The original
Lab 1 send/receipt screenshots remain historical user evidence, distinct from any
new assistant-executed test.
