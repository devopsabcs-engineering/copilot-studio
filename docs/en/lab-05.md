---
title: "Lab 5: Advanced retrieval with Azure AI Search"
description: "Build a chunked search index, compare retrieval methods, and connect a standard Copilot Studio agent with measurable acceptance criteria."
ms.date: 2026-10-19
ms.topic: tutorial
---

## Purpose and evidence status

[Lab index](index.md) | [Français](../fr/lab-05.md) | [Infrastructure prerequisite](lab-05-1.md) | [Next: Foundry IQ](lab-06.md)

Build a retrieval-augmented generation (RAG) pipeline: ingest documents, split them into passages, generate vectors, retrieve relevant passages, and ground an answer in those passages. Allow 90–120 minutes after infrastructure is available. Retrieval and answer generation are different stages; a plausible answer does not prove retrieval worked.

> [!IMPORTANT]
> Actual Free-tier Search execution now supplements the original review.
> Three supplied PDFs were indexed and queried with lexical, filter, facet,
> semantic, vector-contract, hybrid and negative checks. All 17 hotel checks passed
> after removing unsupported `queryLanguage` from the current API request.
> The vectors were explicit city features, not semantic embeddings; Storage,
> integrated vectorization and the Copilot connection remain unexecuted.
> All isolated resources were deleted. See the [actual results](live-rerun-2026-10-19.md).

These are original teaching instructions, not a republication of protected workshop text or code. The original three PDF demonstration files exist locally but are not distributed here. No protected screenshots are included.

## Architecture and prerequisites

![Original bilingual diagram of ingestion, vectorization, retrieval and grounded answers](../assets/lab-05/architecture.svg)

Figure 1. Newly authored explanatory diagram, not a screenshot or evidence of a deployed system.

You need:

* An approved Azure subscription, resource group, region, budget, and available embedding-model quota
* Azure AI Search, preferably Basic or higher for outbound managed identity, and a private Blob container
* An embedding deployment whose model and dimensions match both indexing and query-time vectorization
* Search Service Contributor for object management, Search Index Data Contributor for document loading, and Search Index Data Reader for queries, as applicable
* Storage Blob Data Contributor for your upload identity; Storage Blob Data Reader for the Search service identity reading blobs
* A standard-harness Copilot Studio agent, environment access, suitable licensing, and permission to create connections or agent flows
* Completion of [Lab 5.1](lab-05-1.md), or an administrator-provided equivalent

Contributor on a resource group does not by itself grant Search document access. Roles, networking, and authentication are independent checks. Use the [Search RBAC role definitions](https://learn.microsoft.com/en-us/azure/search/search-security-rbac), not a similarly named role selected by guesswork.

Open the [standard agents experience](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences) for the Topics, Knowledge, and agent-flow steps below. A harness is the runtime; generative versus classic orchestration is a separate setting within the standard agent experience. Prefer generative orchestration for automatic tool selection; use an explicit topic call if you need deterministic routing.

## 1. Prepare an authorized, repeatable corpus

1. Record an inventory of your approved files, expected titles, language, and intended reader permissions. Do not upload real customer information or documents you cannot redistribute.
2. For a predictable beginner exercise, create two UTF-8 text files locally with the following original, fictional contents. These invented properties are test fixtures, not hotel recommendations.
3. Name the first file `harbor.txt`:

   ```text
   Harbor Training Hotel
   City: Harbor City
   The training hotel has a rooftop garden and bicycle storage.
   The bicycle desk opens at 07:00.
   ```

4. Name the second file `forest.txt`:

   ```text
   Forest Training Lodge
   City: Pine Town
   The training lodge has a reading room and indoor pool.
   The reading room closes at 21:00.
   ```

5. In Azure portal, open the approved storage account, select Containers, and create a container named `training-documents` with anonymous access disabled.
6. Upload only these two files for the controlled test. Confirm that the blob list contains exactly `harbor.txt` and `forest.txt`. Use a separate container if you later evaluate the authorized workshop PDFs.

Keep the fixture set separate from the workshop corpus. Two input files do not imply exactly two indexed chunks; chunk count depends on splitting and extraction.

## 2. Create ingestion and vectorization

1. Open your Azure AI Search service and start the current **Import data** wizard. Older workshop UI labels say **Import and vectorize data**. Select a vectorization/RAG path, not a keyword-only import.
2. Select Azure Blob Storage and the private container. Prefer the Search service managed identity for reading storage. Configure the necessary identity and roles before running the wizard.
3. Select text extraction and chunking. A useful starting experiment is 1,000 characters per chunk with 200 characters of overlap. Record the actual unit; characters and tokens are not interchangeable.
4. Select an approved embedding deployment. Confirm its model name, deployment name, and actual output dimensions. The reviewed deployment uses `text-embedding-ada-002` with 1,536 dimensions. A different model is acceptable only if the index, embedding skill, and query vectorizer agree.
5. Name the new index `training-rag`, and record the generated names of the data source, skillset, and indexer. Do not assume generated names equal those in an older lab.
6. Review the schema before creation. Retain retrievable text and document metadata, a searchable vector field, and a semantic configuration that prioritizes the title and passage text.
7. Preserve a retrievable citation URL such as `metadata_storage_path`, with a usable authorized document link. A title alone is not a resolvable citation, and a private blob URL is not automatically accessible to every agent user.
8. Create the objects and run the indexer. Wait for its final status; inspect individual warnings and errors rather than accepting only a green overview badge.
9. Open Search explorer and retrieve a few documents. Confirm nonempty passage text, nonempty title or source identity, and a populated vector field if the field is retrievable.

The [current portal quickstart](https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors) is the preferred supported starting point. Its wizard may generate different field names; the query examples below assume you map them to `chunk`, `title`, and `text_vector`.

### Manual-object alternative and projection checks

If you need to learn the individual objects, use the official [integrated vectorization procedure](https://learn.microsoft.com/en-us/azure/search/search-how-to-integrated-vectorization) instead of copying a legacy JSON schema.

1. Create the Blob data source, then an index with an `Edm.String` key for each chunk, a filterable `parent_id`, searchable passage text, and a `Collection(Edm.Single)` vector.
2. In the skillset, split document content and embed each child passage. Configure one-to-many index projections from the passage context.
3. Map passage text, vectors, title, and citation metadata into the child index. Let projection processing manage the parent association rather than hand-mapping the parent key.
4. Set `projectionMode` to `skipIndexingParentDocuments` when the index should contain only chunks. Ensure the projection and indexer target the same intended index.
5. Attach the skillset to the indexer. Merely creating a data source and an index does not populate either vectors or text.

See [index projections](https://learn.microsoft.com/en-us/azure/search/search-how-to-define-index-projections). Do not assume the original chunk schema provides citation metadata: its title/text/vector fields need an explicit source-URL addition for clickable citations.

## 3. Compare query methods before connecting the agent

1. Open Search explorer in JSON mode. Confirm the selected index and use field names from its actual schema.
2. Run a lexical baseline:

   ```json
   {
     "search": "rooftop garden",
     "select": "title,chunk,parent_id",
     "top": 3,
     "count": true
   }
   ```

3. Run a vector-only query with a configured query-time vectorizer:

   ```json
   {
     "vectorQueries": [
       {
         "kind": "text",
         "text": "Where can I store a bicycle?",
         "fields": "text_vector",
         "k": 50
       }
     ],
     "select": "title,chunk,parent_id",
     "top": 3
   }
   ```

4. Add `"search": "bicycle storage"` to that object for hybrid retrieval. Hybrid search merges lexical and vector results using reciprocal rank fusion, not by adding unrelated raw scores.
5. To test semantic reranking, add `"queryType": "semantic"` and `"semanticConfiguration": "YOUR_CONFIGURATION_NAME"` to the hybrid object. Replace that placeholder with the real configuration. Keep meaningful search text and enough candidates for reranking.
6. Test a filter on a field actually declared filterable. Copy one returned `parent_id` and use `"filter": "parent_id eq 'COPIED_PARENT_ID'"`. Escape an embedded apostrophe by doubling it. Results must all have that same parent ID.
7. As a negative test, filter on `chunk` when it is not filterable. Expect HTTP 400 with a field-validation error, not an empty successful response.
8. Save query text, selected method, top results, latency, and expected supporting passage. Repeat the same query set after any change.

For REST or HTTP-flow requests, the document-search API version `2025-09-01` remains listed as stable; `2026-04-01` is the latest stable version in the [API-version reference](https://learn.microsoft.com/en-us/rest/api/searchservice/search-service-api-versions). Use one supported version consistently. Do not transplant preview-only schema properties into a stable request.

### Optional scoring experiment

The reviewed lab index declares an empty scoring-profile list. That is not a completed scoring-profile exercise.

1. In a separate test index or reviewed schema update, add a text-weight scoring profile that gives `title` a higher weight than `chunk`.
2. Use the same lexical query with and without `scoringProfile`. Record the profile definition and the changed ordering.
3. Compare relevance, not raw score magnitudes across BM25, hybrid, and semantic results. Keep the profile only if your labeled test set improves.

The [hybrid query guidance](https://learn.microsoft.com/en-us/azure/search/hybrid-search-how-to-query) explains candidate selection and reranking. Extra replicas do not fix a wrong vector dimension or an unusable citation.

## 4. Connect the standard agent through knowledge

1. Open the intended environment and standard agent. Confirm you are editing a disposable training agent, not a production agent.
2. Select Knowledge, Add knowledge, Featured, and Azure AI Search. Create a formal data connection using the authentication options supported by your environment.
3. Prefer Microsoft Entra ID where available. Do not paste credentials into agent instructions, index descriptions, screenshots, or this repository.
4. Select the single intended vector index and add it to the agent. Wait for knowledge status `Ready`.
5. Give the agent original instructions: answer accommodation questions only from the training documents, identify the source, and say that information is unavailable when the documents do not support a claim.
6. Disable web search and avoid unrelated knowledge during the controlled evaluation.
7. Ask the fixture questions in the test matrix. Inspect the activity trace and citations; an answer alone does not identify the route used.

The [official connection guide](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-azure-ai-search) currently contains both key-based examples and Entra-based recovery advice. Use its formal connection workflow and the authentication choice allowed by your tenant. Do not create a hand-built, unsupported knowledge connection as a workaround.

## 5. Alternative route through a controlled HTTP flow

Choose this route when the exercise requires explicit filters or query parameters. Evaluate it separately from the knowledge route so you can tell which path answered.

1. Create a standard agent flow with the agent-request trigger and a text input named `question`.
2. Add an HTTP action that sends a POST to the document-search operation for your index. Store endpoint and credentials in an approved connection/configuration facility; enable secure input/output handling where available.
3. Set JSON content type. Use an approved Entra connection/token flow, or a query key for document queries if key authentication is explicitly approved. Never expose an admin key to conversation users.
4. Construct a JSON object with the question as a value, not by concatenating unescaped user text into JSON. Set `top`, `select`, and any fixed authorization filters on the server side.
5. Parse the response's `value` array and return bounded passage text, source titles, and citation URLs. Return an explicit empty-results state if the array is empty.
6. Add the flow as an agent tool. Describe when to call it and ground the answer in its returned passages. Do not treat a successful HTTP request as proof of a supported answer.
7. For deterministic testing, invoke the flow explicitly from a topic and inspect its run. For generative routing, inspect the chosen tool in the activity trace.
8. If a custom connector is required, define this same POST operation, authenticated connection, typed input, and bounded response. Importing an operation alone does not create a real-time knowledge source.

HTTP actions, custom connectors, and connection types can have separate licensing and data-loss-prevention constraints. No flow or connector was created during this review.

## Acceptance tests and evaluation record

Exact values below belong to the original synthetic fixture only. Natural-language wording and generated scores are not exact-match contracts.

| ID    | Action                                                  | Expected assertion                                                                | Current result |
| ----- | ------------------------------------------------------- | --------------------------------------------------------------------------------- | -------------- |
| S5-01 | Inspect the fixture container                           | Exactly two named input files                                                     | Not run        |
| S5-02 | Inspect the latest indexer run                          | `status` is `success`; `itemsFailed` is `0`; readable chunks exist                | Not run        |
| S5-03 | Search `rooftop garden`                                 | A supporting Harbor passage appears in the top three                              | Not run        |
| S5-04 | Ask about bicycle-desk opening                          | Answer includes `07:00` and a Harbor citation                                     | Not run        |
| S5-05 | Apply the copied-parent filter                          | Every result has the exact selected `parent_id`                                   | Not run        |
| S5-06 | Filter on nonfilterable `chunk`                         | HTTP `400`; useful field error                                                    | Not run        |
| S5-07 | Ask for the lodge's airport shuttle price               | Explicit lack of source support; no invented price                                | Not run        |
| S5-08 | Inspect knowledge/flow trace                            | The intended source or tool was invoked; citation opens for the authorized tester | Not run        |
| S5-09 | Repeat in French                                        | Supported facts remain `07:00` and `21:00`; sources remain correct                | Not run        |
| S5-10 | Remove the tester's data permission in an approved test | Access is denied; no content leaks through a fallback                             | Not run        |

For at least ten labeled questions, record supporting-document IDs before testing. Calculate hit@3 as questions with a relevant passage in the first three results divided by questions tested. Calculate citation correctness as supported cited claims divided by cited claims inspected. Record median/p95 latency only after collecting enough timed runs, plus the sample count. Do not publish a percentage from an unexecuted test.

## Troubleshooting and cleanup

| Symptom                       | Check and safe response                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------------------- |
| Blob upload denied            | Your upload identity needs data-plane permission; refresh credentials after propagation                   |
| Indexer cannot read storage   | Check the Search identity's reader role and network path separately                                       |
| Vector length error           | Compare deployment output length, skill dimensions, and index dimensions; reindex into a compatible index |
| Empty results                 | Inspect indexer errors, extracted text, index name, filter, and query language before changing prompts    |
| Semantic error or throttling  | Check configuration name, quota, tier, and request limits; reduce test concurrency                        |
| Citations cannot open         | Correct URL mapping and reader access; do not enable anonymous blob access                                |
| Knowledge dialog fails        | Use the official connection recovery guidance with the environment administrator                          |
| Fluent but unsupported answer | Isolate knowledge sources, disable web search, inspect actual retrieval and enforce abstention            |

1. Export only sanitized test evidence: method, assertion, status, anonymized source label, and timestamps. Do not store keys, tokens, protected text, or private URLs.
2. Remove the test flow/connector or its agent association, and remove training knowledge from the disposable agent.
3. Delete only the indexer, skillset, data source, index, and fixture blobs created for this run, after confirming they are not shared.
4. If infrastructure belongs to Lab 5.1, follow its reviewed Terraform cleanup plan. Deleting an index alone does not stop Search service billing.

## Completion boundary

Static findings are verified; service behavior is not. Finish only after every required test is executed against approved resources and its actual result is recorded. The absent authenticated Copilot session and absent Search resources must be resolved by the workshop operator. No production-readiness, cost saving, or relevance improvement is claimed.
