---
title: Live rerun record - 2026-10-19
description: Executed Terraform initialization, validation and plan, reproduced SDK failure, isolated dependency restoration, and current live-lab gates.
ms.date: 2026-10-19
---

## Scope and current result

[All labs](index.md) | [Français](../fr/live-rerun-2026-10-19.md) | [Validation ledger](validation.md)

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

The selected-subscription inventory still returned no Azure AI Search service or
Application Insights component. Existing unrelated applications were not modified.
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

The test agent was directed to refresh the newly shared agent page and use the
saved tools, rather than the stale blank Home page. A new live result is recorded
only after the actual test completes.

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

The three inline data sets were also evaluated locally without executing notebook
cloud cells. Each contains eight records, for **24 total**. Every record has a
nonempty string `id`, `title`, and `content`, and IDs are unique within each set.
The protected content itself is not republished.

## Remaining execution gates

No billable resources have been created or applied. Requests for a deployment budget
received no actual user answer; an automated unavailable-user response is not treated
as approval. The pricing tool returned no rate for the attempted Search SKU queries,
so no price or hard spending guarantee is assumed.

The next cloud steps require a dedicated deployment boundary, an approved spend
threshold and cleanup decision, current model/region confirmation, then actual
indexing, retrieval, telemetry, prompt, and connected-agent tests.
Lab 1 can proceed independently using the already saved agent and approved connections.

## What remains unchanged

The original Word documents, notebook, and Terraform sources are unchanged.
Existing production or unrelated lab resources were not modified. The original
Lab 1 send/receipt screenshots remain historical user evidence, distinct from any
new assistant-executed test.
