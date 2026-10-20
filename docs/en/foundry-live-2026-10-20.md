---
title: "Lab 6 live Foundry and MCP results - 2026-10-20"
description: "Actual keyless embeddings, Search provenance, authenticated MCP and Foundry-agent tests, including failed quotation checks, current API substitutions and verified cleanup."
ms.date: 2026-10-20
ms.topic: how-to
---

## Result and evidence boundary

[Lab 6 guide](lab-06.md) | [Français](../fr/foundry-live-2026-10-20.md) | [All-lab execution ledger](live-rerun-2026-10-19.md) | [Sanitized results](../assets/runtime-2026-10-19/foundry-results.json)

The isolated paid continuation actually exercised Foundry and Search services.
It did not certify the whole lab. The owner had approved paid lab testing;
no new production-release approval or human sign-off is implied.

| Check | Actual result | Boundary |
|-------|---------------|----------|
| Foundry prompt agent | API `v1`, exact smoke marker, 41 total tokens | Model/agent invocation, not a Copilot conversation |
| Embeddings and indexes | 24 real Ada002 embeddings; three indexes of eight records; 1,536 dimensions | Original authorized training records, not enterprise data |
| Stored-data verification | All 24 vectors and original source fields rechecked without re-embedding | Vectors explicitly made retrievable |
| Managed-identity hybrid query | Semantic reranker scores present | Does not certify every ranking |
| GA provenance | 2 specific, 20 cross-source and 0 unsupported passages; 22 exact original matches | Different run from the earlier Free result of 19 |
| Current-preview direct MCP | Exact original title and complete original content returned | Tool discovery alone was not counted as success |
| Foundry single-source call | One reviewed approval, one successful MCP call, one exact original quotation | Formatting and requested length were not followed |
| Initial cross-source request | Agent narrowed the request to one source | Unexpected query was not approved |
| Revised cross-source request | Version 3 executed the reviewed full question; all three requested titles present in tool output | Final exact-quotation check failed |
| Activity endpoint | Activity and Responses enabled, version 3 pinned, Entra-only authorization read back | No Activity conversation or Copilot connected-agent test |
| Cleanup | Three inventoried Azure resources and owned children deleted; group absence independently verified | No exact billed amount claimed |

The cross-source tool output contained two complete original content fields and
all three requested titles. That is not evidence that every complete source
record was returned. All three final purported quotations differed from both the
original content and the tool output. This establishes a failed exact-quotation
criterion, not proof that every paraphrased factual statement was false.

A later [approved quotation-recovery test](#8-approved-quotation-recovery-and-remaining-citation-failure)
recovered exact quotations twice. It did not pass native citation output or
the unsupported query's zero-document criterion. The original run below is
preserved separately from that continuation.

## 1. Keep the test isolated and keyless

Use a fresh approved resource group with an ownership tag and a private ownership
manifest. The tested configuration used an AIServices S0 account and project in
Sweden Central, Basic Search in West US 2, GPT-4o and `text-embedding-ada-002`.
Both model deployments used configured capacity 10. GPT-4o's lifecycle was checked
for this run; do not treat its success as a recommendation for a new production system.

Preserve disabled local authentication. Give the project identity Search Index
Data Reader on the new Search service, and the Search identity Cognitive Services
OpenAI User on the new model account. Authoring and document-loading permissions
belong to the authorized test operator, scoped to the dedicated service.
Do not reuse unrelated projects or grant subscription-wide data permissions.

The Search ARM creation request rejected simultaneous `disableLocalAuth: true`
and non-null `authOptions`. Removing `authOptions` preserved keyless operation.
Its provisioning states were lowercase; normalize enum casing when polling,
while still rejecting failed/canceled states and enforcing a deadline.

## 2. Verify actual embeddings and provenance before MCP

1. Keep the original three eight-record lists private and unchanged.
2. Generate actual 1,536-dimensional embeddings. Inspect every upload result,
   then poll document counts within a deadline because visibility is eventual.
3. Preserve exact `id`, `title` and `content` fields, a semantic configuration
   and a managed-identity vectorizer aligned with the deployed embedding model.
4. Set the vector field's `retrievable` property explicitly to `true` if the
   acceptance test must inspect stored values. Omitting it in this run left the
   field nonretrievable, and selecting it returned HTTP 400.
5. For the three owned indexes, enabling retrieval through a schema update worked
   without deleting documents or regenerating embeddings. The update returned
   HTTP 204; query the definition/data afterward instead of requiring a JSON body.
6. Use GA Search API `2026-04-01` for the minimal/extractive baseline described in
   the [Lab 6 guide](lab-06.md). Match passage `ref_id` to reference `id` with
   explicit string normalization, rejecting duplicate normalized identifiers.
   The observed response used integer passage IDs and string reference IDs.
7. Join each reference's `activitySource` to the activity's knowledge-source
   name, then `docKey` to the original record. Require exact title/content equality.
   Do not use a model-written label or nullable `sourceData` as provenance proof.

The paid run returned 22 exactly matched passages. Counts are observations,
not future ranking guarantees. The unsupported control returned zero passages.

## 3. Use the live MCP schema, not an older preview's argument names

The tested MCP endpoint pattern was:

```text
https://<owned-search>.search.windows.net/knowledgebases/<owned-kb>/mcp?api-version=2026-08-01-preview
```

Use a Search bearer token with audience `https://search.azure.com/` and accept
JSON or server-sent events. Send `tools/list`, verify the expected read-only tool
and inspect its `inputSchema` before calling it. The live August preview declared
exactly one required property, `query_variants`: an array containing one complete
natural-language question, maximum 400 characters.

The request shape below is illustrative, not the protected question used in the run:

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "knowledge_base_retrieve",
    "arguments": {
      "query_variants": ["Which sources describe the approved investigation process?"]
    }
  }
}
```

The May preview declared `queries` instead. It returned a missing-planning-model
error even after its own configuration readback showed a model. The cause of
that discrepancy was not established. Submitting `queries` to the August preview
also failed, explicitly requiring `query_variants`. Calling the August preview
with its actual declared argument succeeded.

The knowledge base had a keyless GPT-4o planning-model configuration, low reasoning
effort and extractive output, read back through preview APIs. Those properties
are not part of the GA minimal-retrieval configuration. Native MCP content did not
provide the separate retrieve API's activity/reference arrays; no inner-planner
token count or independent planning trace is claimed.

## 4. Create and independently verify the project connection

The installed `azd` needed a local initialized environment even with an explicit
project endpoint. When the project had no connections, it also required the full
`AZURE_AI_PROJECT_ID` persisted in that local environment.

Use an empty private working directory, not a shared application checkout.
Replace every placeholder with values from your new owned manifest. These
commands initialize local context and create a connection; they do not run
`azd up` or provision another environment:

```powershell
$env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
azd init --minimal --environment lab6-validation --subscription '<subscription-id>' --location swedencentral --no-prompt
azd env set AZURE_AI_PROJECT_ID '<full-owned-project-ARM-ID>' --environment lab6-validation
azd ai connection create lab6-search-mcp --kind remote-tool --target '<owned-MCP-URL>' --auth-type project-managed-identity --audience 'https://search.azure.com/' --project-endpoint '<owned-project-endpoint>' --no-prompt
azd ai connection show lab6-search-mcp --project-endpoint '<owned-project-endpoint>' --no-prompt --output json
```

Set the user-agent variable only in the current process; do not save it with
`azd env set`. Keep the project binding private. Read back the connection's ARM
properties and require the exact owned target, `RemoteTool` category,
`ProjectManagedIdentity` authentication and Search audience. The authenticated
agent call, not only the interactive Search call, then tests that connection.

## 5. Create a current agent version and review every approval

The source-pinned Projects SDK `2.0.0b3` rejected agent creation with API version
`v1` locally, although the service supported it. The working substitute used
documented REST `POST /agents/<name>/versions?api-version=v1`. The pinned client
still supplied the OpenAI Responses client; no shared interpreter was upgraded.
Foundry MCP management tooling had a separate credential-chain failure, so its
failure was not treated as proof that Azure CLI authentication had failed.

Limit the MCP tool to the owned endpoint and one read-only tool. The server
normalized the allowed-tool list to the following form on readback:

```json
{
  "type": "mcp",
  "server_label": "training-kb",
  "server_url": "<owned-MCP-URL>",
  "project_connection_id": "lab6-search-mcp",
  "allowed_tools": {"tool_names": ["knowledge_base_retrieve"]},
  "require_approval": "always"
}
```

Invoke through the Responses client with an explicit `agent_reference` containing
`name`, `version` and `type: agent_reference`. Use fresh state for independent
questions, bounded output and at most one tool call per test.

1. Inspect each `mcp_approval_request` server label, tool name and parsed arguments.
2. Approve only the intended complete question. Do not approve a narrowed query
   merely because it names a familiar source.
3. Submit `mcp_approval_response` with the correct request ID and
   `previous_response_id`; inspect the actual `mcp_call` output and error.
4. Compare final quotations against both tool output and original source text.
5. Retain private accepted responses for local analysis instead of resending
   successful calls merely to capture evidence.

Version 2's single-source quotation was an exact 574-character original substring.
Its Markdown-fenced JSON and length violated the requested format/160-character
limit; those deviations remain recorded. Version 2's cross-source request was not
approved because it selected only one source. A bounded version 3 instruction
correction produced the complete reviewed query and a successful MCP call.
Its final excerpts were 171, 166 and 170 characters and were not exact quotations.
The cross-source final-answer acceptance result therefore remains failed.

## 6. Separate Activity configuration from a real conversation

The supported configuration route was
`PATCH /agents/<name>?api-version=v1` with content type
`application/merge-patch+json`. It enabled `activity`, preserved `responses`,
set Entra-only authorization and pinned version 3 with a 100-percent
`FixedRatio` selection rule. An independent GET verified all four properties.

No Activity request, Teams publication or Copilot connected-agent conversation
was executed. Do not invent a callback service URL to simulate one. Channel
authorization must be reviewed separately; an Entra-only configuration readback
does not establish every Copilot/Teams integration prerequisite.

## 7. Preserve truthful evidence and remove the paid environment

The Foundry browser reached its landing/sign-in route but reported an IndexedDB
missing-object-store error. This is not evidence that the user's credentials were
invalid. No new authenticated product-execution screenshot was obtained.
The [existing screenshot gallery](evidence.md) remains useful, with its provenance
labels; historical figures are not relabeled as this run's evidence.

Cleanup checked the exact group ID, ownership tag and resource allowlist before
deletion. Azure listed three owned resources, with models, connections, agent
versions, indexes and other children removed with their owning resources.
An independent group-existence query returned false.

Private raw answers, source records, identities, endpoints and tokens were not
published. The public JSON was generated from the actual results, checked against
saved responses and rejected private identifier/credential markers.

To complete the lab, restore the supported standard Copilot authoring route,
repair and rerun the final-answer grounding criterion, then execute the original
bilingual routing, negative-access, Activity and connected-agent acceptance cases.
Create any replacement paid environment only within the approved scope and
remove it after testing. Documentation publication is not full lab certification.

## 8. Approved quotation recovery and remaining citation failure

After renewed Azure resource approval, four disposable environments were tested
sequentially, not concurrently. Each used a fresh tagged ownership-manifest
group, keyless Foundry account/project, Basic Search and GPT-4o/Ada002
capacity 10. Only roles scoped to these new resources were added; no broad
subscription grant, application permission or consent was changed.

The original saved failure was rechecked: all three purported quotations
were paraphrases, not an escaping-only comparison error. Subsequent attempts
exposed three separate compatibility issues:

1. Low-effort native MCP still reported a missing planning model despite
   configuration readback. That path remains unresolved.
2. Minimal retrieval worked, but installed Projects SDK 2.3.0 lacked the
   `AgentReference` helper. Explicit agent-reference request dictionaries
   resolved this SDK compatibility issue.
3. The actual minimal MCP tool schema required short queries. Its three title
   queries were initially rejected by the earlier full-question approval guard.
   The new test instructions and guard were aligned to one reviewed tool call
   containing all three exact requested title queries.

Explicit extraction instructions, rather than summarization, then produced
two actual model responses with **3/3 exact quotations each**. All six
quotations matched original records and actual tool content, with independently
verified source IDs, titles and owned Search index-document URLs. The excerpts
contained 80, 109 and 144 characters. Both answers were valid unfenced JSON.
Each cross-source tool response contained 24 documents, all matching the corpus.
No deterministic replacement answer was substituted.

Complete output acceptance still **failed twice**: every `citation` string
contained whitespace only and the output-text annotation arrays were empty.
Independently proven provenance and correct titles are not native citations.
The unsupported control returned the actual answer `{"sources":[]}`, so model
abstention passed; however, its tool returned **seven off-topic documents**.
Successful MCP completion does not establish zero-document retrieval.

The [sanitized recovery evidence](../assets/runtime-2026-10-20/foundry-quote-recovery.json)
keeps quotation fidelity, citation output, abstention and retrieval precision
as separate checks. Actual source text and complete model responses remain
private. No user agent, Activity or connected Copilot configuration was changed
or exercised in this continuation.

All four owned groups were deleted. Independent verification at
**12:55:32 UTC** confirmed four absent groups and **eight ARM 404 responses**
for the four account/Search pairs. Only manifest-owned resources were deleted.
ARM absence does not certify provider soft-delete or inference-retention policy.
Observed usage was **16,184 agent-response tokens**, **13,288 embedding tokens**
and 96 embeddings across four batches of the same 24 unique records.
Direct MCP reasoning-token metadata is recorded separately; no billed amount
or complete hidden-planning total was observed.

Quotation fidelity is now recovered within this narrow test. Native citations,
zero-document retrieval, the low-effort planner path and connected-agent
acceptance remain open. No paid test environment is intentionally retained.

## Current references

- [Search knowledge-base creation and API distinctions](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Retrieve API and MCP contract](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-retrieve)
- [Foundry MCP tools and approvals](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Foundry version selection, protocols and authorization](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-agent)
- [Copilot Studio Foundry connected-agent requirements](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent)
