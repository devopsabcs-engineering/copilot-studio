---
title: "Lab 02: Ground an agent with Azure AI Search"
description: "Build a vector retrieval pipeline, connect it to a standard Copilot Studio agent, and verify grounding without claiming an unperformed live test."
ms.date: 2026-10-20
ms.topic: tutorial
---

## Lab 02: Ground an agent with Azure AI Search

[Workshop index](index.md) | [Français](../fr/lab-02.md) | [Next: monitoring](lab-03.md)

Use an Azure AI Search index to retrieve passages from an approved licensing guide.
Keep retrieval, answer generation, and document provenance separate so you can test
each layer. Allow about 90 minutes, excluding resource approval and indexing delays.

> [!IMPORTANT]
> Status: **Retrieval pipeline tested; complete Copilot integration blocked**.
> On 2026-10-19, sign-in succeeded and the Copilot Studio home shell was visible.
> Subsequent Agents navigation and reloads returned a blank page, preventing
> inspection of the licensing agent or a fresh knowledge question. The current
> original Azure subscription inventory reported no Search or Application Insights.
> A later explicit-subscription recheck corrected the latter: seven unrelated
> Application Insights components exist and were left unchanged. A disposable Free
> Search service was then used for actual indexing and retrieval, but not the
> integrated vectorizer or Copilot connection at that checkpoint. A later approved
> paid run verified real embeddings and managed-identity query vectorization.
> A further private hotel-corpus test passed 25 checks: three original PDFs,
> nine Search-projected child chunks, integrated embeddings and hybrid retrieval.
> Licensing-corpus isolation and the Copilot connection remain unverified. See the
> [latest runtime results](live-rerun-2026-10-19.md). The original review was scoped to
> that subscription, not proof that no connection exists elsewhere. Documentation
> checks are not runtime passes. The original review created no resources or agent changes.

### Objectives and acceptance criteria

Latest result: the later formal AccessKey route did connect. Actual licensing
answer/edition/quotation/page/source-target checks and final source-aware
abstention passed after a recorded initial failure and two native corrections.
The [nine-question chronology](backend-live-2026-10-20.md#source-aware-no-answer-handling-passed)
does not certify external PDF viewer navigation. The keyless Cognitive policy
remained enforced; Search keys were permitted on this isolated service.

The later October 20 attempt created a licensing-only index of 30 source pages,
separate from the hotel index, and passed an actual query vectorizer check.
The connected Standard-agent test then stopped at the hosting browser's blocked
Entra sign-in pop-up: no connection, field mapping, source or question was saved.
This supersedes the earlier index-isolation uncertainty, not the connected-agent
acceptance boundary. See the
[actual connection failure](backend-live-2026-10-20.md#keyless-search-connection-blocked-by-the-hosting-browser).

* Create a private document container and an index containing retrievable text.
* Use integrated vectorization for both ingestion and natural-language queries.
* Connect one vector index through a supported Copilot Studio data connection.
* Prove that answers use the intended source, not a competing uploaded file.
* Record positive, negative, and isolation tests with sanitized evidence.

### Prerequisites and safety boundary

1. Complete Lab 01 and obtain maker access to its agent in a development environment.
2. Open the standard-agent experience. From the Copilot Studio home page, use
   **… > Open classic experience**, or open your existing standard agent from
   **Agents**. The standard harness supports both classic and generative
   orchestration. Opening the classic experience does not itself select classic
   orchestration. See [harnesses][harness] and [switching experiences][experience].
3. Obtain an approved Azure subscription, region, resource group, budget, and
   permission to provision resources and assign roles. A maker license alone
   does not provide Azure permissions. Obtain approval before incurring costs.
4. Confirm that tenant data policies permit the Azure AI Search connector and
   that the environment can reach the resource endpoints.
5. Obtain a current, publicly distributable licensing guide from the publisher.
   Record its title, publication date, download date, and source URL. Do not
   redistribute the PDF unless its terms permit it. Licensing answers are
   educational, not a substitute for contractual licensing advice.
6. Save a solution export or approved backup of the agent, its knowledge list,
   instructions, and orchestration setting. Use a disposable copy for isolation
   tests. Do not remove production knowledge sources.

### Original workflow and current substitutions

The original Lab 2 describes storage, embeddings, indexing, and an agent connection.
The updated route retains that architecture but changes these assumptions:

* Replace a default **Free** Search service with **Basic or higher** for the
  managed-identity route in the current portal quickstart. Free vector search
  availability does not mean this complete wizard and identity route is supported.
* Use **Import data**, **Import data (new)**, or **Import and vectorize data** as
  offered by your portal, then the Blob Storage RAG/vectorization workflow.
* Use a supported embedding deployment such as `text-embedding-3-small` or
  `text-embedding-3-large`, not a chat model. Availability, quota, dimensions, and
  model lifecycle must be checked in the selected subscription and region.
* Replace broad Contributor grants with the specific identities and data roles
  below. Do not grant Storage Blob Data Owner for a read-only indexer.
* Prefer the connector's **Microsoft Entra ID Integrated** connection. Do not
  paste an endpoint/key into an unsupported knowledge configuration.
* Treat semantic ranking as an optional configured feature, not a synonym for
  vectorization or a prerequisite for every vector query.

The [current knowledge article][knowledge] lists key-based authentication, but
also warns that unsupported connections can break the environment-level connection
dialog and recommends formal data connections with Entra ID for recovery.
The [connector reference][connector] documents the available authentication types;
its managed-identity connection type is restricted to Logic Apps. That restriction
does not prevent the Search service using its own identity to read blobs and call
the embedding model.

### Exercise 1: Prepare the document and storage

1. In Azure portal, open **Storage accounts > Create**, if no approved lab account
   exists. Select the approved subscription and lab resource group.
2. Choose a unique name and approved region. Use a standard general-purpose v2
   account; LRS is a cost-conscious workshop option when policy permits it.
   Review network, encryption, and public-access settings before deployment.
3. Under **Data storage > Containers**, create a container named
   `licensing-docs` with anonymous access disabled.
4. Upload the approved PDF. Check that its size is nonzero and that you can open
   it using an authorized identity. Do not publish a SAS token in your evidence.
5. If you need upload rights, request **Storage Blob Data Contributor** on the
   narrowest appropriate scope. Azure resource Contributor alone is not a Blob
   data-plane role.

![Original storage-account creation screen](../assets/lab-02/image3.png)

*Original workshop screenshot, not a new execution. Use the current approved
subscription, region, and security settings rather than copying visible values.*

![Original private-container creation screen](../assets/lab-02/image9.png)

*Original workshop screenshot, not a new execution. Keep the container private.*

### Exercise 2: Configure embeddings and Search access

1. Ask the resource owner for an approved Azure OpenAI embedding deployment, or
   obtain approval to create one. The current [portal quickstart][vectors]
   specifies a compatible Azure OpenAI resource with a custom subdomain, created
   through Azure portal for this route. A Cognitive Services inventory entry
   does not prove that a compatible model is deployed.
2. In Foundry, inspect the deployment's actual model, version, deployment name,
   region, and available quota. Record the deployment name without recording keys.
3. Create or select a **Basic or higher** Azure AI Search service. Review cost
   before creation. Use a region compatible with the selected model and wizard.
   A preference for colocating resources does not override model availability.
4. On Search, enable role-based access and its system-assigned identity.
5. On Storage, grant that Search identity **Storage Blob Data Reader** for the
   approved container or account scope supported by your indexing configuration.
6. On Azure OpenAI, grant that identity **Cognitive Services OpenAI User**.
   Do not substitute broad Cognitive Services Contributor by default.
7. For the person building and testing the pipeline, follow the quickstart's
   Search roles: **Search Service Contributor**, **Search Index Data Contributor**,
   and **Search Index Data Reader**. Keep ingestion/write access separate from
   subsequent query-only connections.
8. For the connector identity, use **Search Index Data Reader** for querying.
   If index enumeration/configuration requires **Search Service Contributor**,
   have the administrator approve that additional management-plane access.
   Reevaluate connector permissions after setup.

> [!WARNING]
> The current portal wizard requires public endpoint access during setup.
> Do not disable an enterprise firewall or private endpoint to complete a lab.
> If policy prevents this route, stop and request an approved private-network
> implementation. A successful portal wizard does not prove Copilot Studio can
> reach the resulting service.

### Exercise 3: Import, vectorize, and inspect the index

1. Open the Search resource and start its import/vectorization wizard.
2. Select **Azure Blob Storage** and the approved storage account and container.
   For the folder filter, use the intended document folder or leave it empty if
   the container contains only workshop documents.
3. Select managed-identity authentication. Choose the embedding deployment from
   Exercise 2 and acknowledge its usage charges.
4. Keep this exercise text-only. Skip optional image enrichment. Review generated
   names for the data source, skillset, index, and indexer before creating them.
5. Wait for the indexer execution to finish. Open its execution history. Expect
   a successful run, at least one processed source document, and no failed items.
   The number of chunks need not equal the number of PDFs.
6. Open the index schema. Record the actual text, title, identifier, and vector
   field names. Verify that text/title fields used by the agent are retrievable.
7. Check that the vector field has a vector-search profile associated with an
   appropriate query vectorizer. Index-time embeddings alone are insufficient
   for a natural-language vector query.
8. In Search explorer, use the text-to-vector/vector query mode offered by the
   portal to ask a licensing question. Confirm that returned passages contain
   relevant text from your document. Do not assume that a successful keyword
   query proves vectorization.
9. If enabling semantic ranking, configure it separately and check supported
   region, tier, and billing. Preserve a baseline vector query for comparison.

![Original Blob Storage import wizard](../assets/lab-02/image19.png)

*Original workshop screenshot, not a new execution. Wizard labels and generated
index fields can differ in the current portal.*

### Exercise 4: Connect and isolate the knowledge source

1. In the standard agent, open **Knowledge > Add knowledge > Featured >
   Azure AI Search**. Some navigation surfaces call this **Data sources**.
2. Create a formal data connection. Prefer **Microsoft Entra ID Integrated**
   and authenticate with the approved query identity. Use the endpoint format
   requested by the connection dialog; do not invent a URI scheme.
3. Confirm successful connection creation. Select the actual vector index name,
   then **Add to agent**. This knowledge connection supports one vector index.
4. Wait for the knowledge status to become **Ready**. Record the index name,
   connection type, and readiness state, never the key or token.
5. In your disposable agent copy, temporarily remove or disable the original
   uploaded PDF and other overlapping knowledge. Record how to restore them.
6. For a strict grounding test, turn off general knowledge and web information
   where those settings are available. Save the prior values.
7. Start a fresh test conversation and open the activity map. Ask the positive
   question below, inspect the retrieved source, and compare its factual claims
   with the saved PDF edition.

![Original Azure AI Search knowledge selection](../assets/lab-02/image23.png)

*Original workshop screenshot, not a new execution. Use the supported connection
dialog and your own index, not any identifier shown in the source image.*

### Validation plan and exact expected results

Execute these tests only after the prerequisites are available. Generated wording
is nondeterministic; the listed observable assertions are the acceptance criteria.

* `SRCH-01`: Inspect indexer history. Expect a successful run with at least one
  processed document and zero failed items. Save the sanitized run summary.
* `SRCH-02`: Ask, “Which Power Apps licensing options does the indexed guide
  describe?” Expect at least one relevant retrieved chunk and an answer whose
  licensing claims can each be traced to that guide edition. Capture the activity
  map and citation/source information; an answer alone is insufficient.
* `SRCH-03`: Ask, “What does this guide say about the fictional product
  WorkshopNebula-999?” Expect no invented product entitlement. The agent must
  state that the source does not establish the answer or decline to answer.
  A nearest-neighbor result may still exist; that is not proof of relevance.
* `SRCH-04`: In the disposable copy, disable the Search knowledge source and
  restart the conversation with competing sources still disabled. Expect that
  the activity map cannot report retrieval from that disabled source. Restore
  Search afterward. If the answer remains grounded, investigate another path.
* `SRCH-05`: Inspect evidence files. Expect no credentials, SAS URLs, personal
  identifiers, protected PDF excerpts, or unrelated resource information.

### Troubleshooting and recovery

* If the indexer returns 403, check the Search identity's Blob reader and OpenAI
  user roles, endpoint access, and role propagation. Do not respond by assigning
  subscription Owner.
* If embeddings fail, inspect deployment availability, quota, selected dimensions,
  skillset configuration, and index vector dimensions. Recreate only disposable
  lab artifacts if the schema cannot be corrected safely.
* If natural-language search fails but keyword search works, check the query
  vectorizer, vector field, profile, and model access rather than the agent prompt.
* If the knowledge source is not Ready, inspect the connection identity, index
  visibility, connector policies, and metadata processing state.
* If the connection dialog fails immediately, do not create repeated endpoint/key
  variants. Escalate the environment-level data connection issue to the owner.
  Microsoft's recovery options include resetting external access or recreating
  an affected disposable agent; neither is an automatic workshop cleanup step.
* If an answer uses the old file, restart the conversation and inspect all
  agent-level and topic-level knowledge sources before retesting.

### Rollback, cleanup, and evidence

1. Restore the original knowledge sources, general-knowledge/web settings, and
   orchestration mode from the saved configuration. Validate the original Lab 01
   question in a fresh conversation before using the agent again.
2. Remove only the workshop knowledge connection if no later lab needs it.
   Preserve the index and embedding deployment for Lab 04 when approved.
3. After all dependent labs, delete only specifically approved lab resources:
   indexer, skillset, data source, index, uploaded document/container, and
   dedicated deployments/services. Never delete a shared resource group.
4. Revoke lab-only role assignments and unused connections. Rotate any exposed
   key through the owner's process. Deleting a blob alone might not remove its
   indexed chunks; verify deletion detection or remove the lab index.
5. Record date, guide edition, orchestration setting, index schema summary,
   query assertions, indexer result, sanitized screenshots, and cleanup result.
   Record each runtime case as **Not run** until observed.

The completed review verified the official routes, authentication distinctions,
wizard tier requirement, embedding options, and role separation. Index creation,
connector readiness, retrieval quality, citations, and cleanup remain unverified
in the live tenant. Unblocking requires a working agent authoring page with maker
access, approved Search infrastructure, model deployment/quota, and authorized
data connections. Authentication is no longer the observed blocker; the agent's
existing knowledge and tools could not be inspected through the blank page.

### Official references checked

These Microsoft Learn pages were fetched during the 2026-10-19 review.

* [Azure AI Search knowledge source][knowledge]
* [Azure AI Search connector and its authentication/action reference][connector]
* [Portal vector-search quickstart and current prerequisites][vectors]
* [Semantic ranker concepts][semantic]
* [Copilot Studio harnesses][harness]
* [Access the standard-agent experience][experience]

[knowledge]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-azure-ai-search
[connector]: https://learn.microsoft.com/en-us/connectors/azureaisearch/
[vectors]: https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors
[semantic]: https://learn.microsoft.com/en-us/azure/search/semantic-search-overview
[harness]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
[experience]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences
