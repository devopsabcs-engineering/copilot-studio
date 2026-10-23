---
title: Workshop completion roadmap
description: Prioritized remaining work, dependencies, owners, and measurable acceptance gates for workshop completion.
ms.date: 2026-10-23
---

## Goal and scope

[Repository home](../../README.md) | [Français](../fr/completion-roadmap.md) |
[Validation ledger](validation.md) | [Latest execution report](backend-live-2026-10-20.md)

The planning deliverable is complete. The workshop execution is **not complete**.
This roadmap identifies what must be done before that claim is justified.
Unchecked tasks are work to execute, not promised or observed outcomes.

The baseline is commit `94ebcd3` and the retained execution evidence, not a fresh
October 23 cloud inventory. Local verification on October 22 passed 47 documentation
tests, 33 extension tests, dependency consistency and Python syntax checks.
Those results do not establish live acceptance. No new cloud deployment, email,
permission grant, publication or protected-source access is part of this roadmap update.

## Existing implementation and constraints

The [Python extension](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/README.md)
verifies retrieved records against a pinned licensed corpus and renders quotations
in code. Local transport tests stub corpus loading and the Azure answer operation.
The retained [extension receipt](../assets/runtime-2026-10-20/foundry-verified-extension.json)
records hosted version 1, an unrepaired deployed Activity SDK, native HTTP 403,
and a separate authenticated direct HTTP 500 before the application handler.
Local Activity `1.0.0b4` and Microsoft Agents `1.9.0` pass their regression;
deployment and downstream hosted identity permissions remain unverified.

Use existing isolated resources and supported interfaces. Preserve original agents,
failed attempts, private evidence and the working version-4 route. Never substitute
an SDK call for native Copilot delivery or local checks for cloud behavior.
Do not weaken policy, enable anonymous access, reconstruct protected documents,
or claim legal/source equivalence for the licensed notebook.
No migration or new application architecture is required.

The user's general recovery and isolated Entra-only diagnostic permission is recorded
in the prior handoff. Do not ask for that same permission again. Release-specific
Product Owner, Security Team and Tech Lead sign-offs still need attributable records;
do not infer organizational roles from general permission. The exact artifact must
be identified, and changed artifacts require renewed sign-off.

## Priority, owners and dependencies

Owners below are execution roles, not assigned people or recorded approvals.
P0 removes the immediate blocker or limits ongoing cost; P1 closes runtime
acceptance; P2 reconciles evidence and publication.

| Plan item | Priority | Owner                         | Depends on       | Completion evidence                                      |
|-----------|----------|-------------------------------|------------------|----------------------------------------------------------|
| 1.1       | P0       | Release owner and cloud owner | None             | Owned-resource inventory, costs, artifact and sign-offs   |
| 2.1       | P0       | Extension maintainer          | 1.1              | Repaired hosted Activity reply with exact source records  |
| 3.1       | P1       | Copilot Manage and Test       | 2.1              | Native reply, persisted route and restored control        |
| 4.1       | P1       | Copilot Author and Test       | 3.1              | Fresh eleven-case matrix with whole-turn evidence         |
| 5.1       | P1       | Lab owner and Copilot Test    | 1.1              | Labs 0, 1, 2 and 3 acceptance receipts                     |
| 6.1       | P1       | Policy owner and lab owner    | 1.1              | Supported connected BYOM run or explicit exclusion        |
| 7.1       | P1       | Infrastructure and lab owner  | 1.1              | Labs 5/5.1 connected-query and deployment receipts        |
| 8.1       | P2       | Evidence and publication owner| 4.1,5.1,6.1,7.1  | Reconciled bilingual evidence, cleanup and release checks |

Items 5.1, 6.1 and 7.1 can proceed independently after 1.1 only when their cloud
resources and browser sessions do not overlap. Avoid concurrent changes to a shared
agent. No completion date is asserted while entitlement, policy and sign-off
dependencies remain unresolved.

## Implementation steps and executable backlog

### 1.1 Establish the release and cost boundary

Requirements: REQ-001. Input: retained ownership records and the extension receipt.

- [ ] T001 [Plan:1.1] Re-inventory the isolated extension, Bot, project, Search, embeddings and identities using the retained private ownership records. Compare actual resource IDs, provisioning state, versions and billing status. Set an owner and review deadline for each retained resource; an expiry tag is not deletion.
- [ ] T002 [Plan:1.1] Record the release artifact, scoped rollback plan and attributable Product Owner, Security Team and Tech Lead sign-offs before deployment. Keep private identifiers outside the repository; add only a sanitized approval reference to the execution report.

Exit: ownership and current resource state are verified; spending and release
boundaries are explicit. If approval is unavailable, dependent deployment stays
blocked, but independent documentation and inventory work may continue.

### 2.1 Deploy and prove the isolated SDK repair

Requirements: REQ-002. Inputs: [extension instructions](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/README.md)
and [deployment manifest](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/azure.yaml).

- [ ] T003 [Plan:2.1] Rerun the service's existing 33 tests, dependency and syntax checks; deploy only the approved extension artifact to the existing project. Record resolved SDK versions, hosted version, startup logs and rollback target in the extension receipt without erasing the old failure.
- [ ] T004 [Plan:2.1] Send an authenticated Activity request with a complete envelope, including `serviceUrl`. Verify a real hosted session, actual retrieval and selection, exact rendered source records, and explicit error/abstention behavior. Check downstream access through the hosted identity, not developer credentials.

Exit: the constructor failure is absent in the real host and source-grounded
delivery passes. HTTP readiness alone is insufficient. Keep endpoint authorization
unchanged for this initial SDK repair so authentication changes are not conflated.

### 3.1 Recover native Copilot delivery

Requirements: REQ-003. Input: the saved inactive diagnostic and existing control route.

- [ ] T005 [Plan:3.1] Diagnose the native tenant-ID 403 with supported caller metadata and scoped logs. If still necessary, execute the already-authorized Entra-only diagnostic on the isolated endpoint while retaining Azure RBAC; grant no anonymous access or broad permissions. Have Manage perform managed configuration changes and Author handle any YAML change.
- [ ] T006 [Plan:3.1] Have Test execute one native diagnostic and one unchanged control question. Capture the native action, hosted correlation, whole-parent completion and exact displayed answer. Disable the diagnostic afterward, independently read back its saved inactive state, and verify the working original route remains intact.

Exit: a native response proves verified evidence delivery, not merely a successful
direct Activity request. If Entra-only configuration is unsupported or does not
fix caller metadata, preserve the failure and escalate through supported platform
support rather than bypassing authorization.

### 4.1 Close the eleven-scenario acceptance matrix

Requirements: REQ-004. Input: the original questions and complete-turn audit in the
[execution report](backend-live-2026-10-20.md).

- [ ] T007 [Plan:4.1] Have Author correct only demonstrated quotation fidelity, per-bullet attribution, conditional-duty scope and detailed-example coverage gaps in the isolated candidate. Preserve source-free intake, local-only lookups, hybrid routing and the working control.
- [ ] T008 [Plan:4.1] Have Test run all eleven unchanged scenarios in a fresh native session after an acknowledged readiness preflight. Preserve full final replies and `DynamicPlanFinished`, expected handler routes, source comparisons, individual attribution, relevance, applicability and example-coverage results per case. Count retries separately.

Exit: every required case and criterion passes in the new run. Earlier merged
captures, four extractive backend successes and generic quality grades do not
replace this matrix. Stop on failed criteria, retain the failure, fix the cause,
and repeat affected cases plus routing regressions.

### 5.1 Complete Labs 0, 1, 2 and 3

Requirements: REQ-005. Inputs: current [rerun table](live-rerun-2026-10-19.md) and
the individual lab guides.

- [ ] T009 [Plan:5.1] Recheck [Lab 0](lab-00.md) entitlement, capacity, policy, permissions, quota, tools and budget. For [Lab 1](lab-01.md), close the historical full-answer audit, citation navigation and downstream connector error-body fidelity. Use synthetic/approved recipients; do not resend mail unless a missing criterion needs it.
- [ ] T010 [Plan:5.1] For [Lab 2](lab-02.md), verify actual external PDF source navigation and recheck connected positive/negative answers. For [Lab 3](lab-03.md), verify published-channel telemetry and the required privacy boundary with event/KQL correlation. Prior success of one genuine event does not certify absence of all platform identifiers.

Exit: each lab has its own observed receipt for all mandatory acceptance IDs.
Preserve the original failed evaluation and clarify any requirement that the
platform cannot satisfy instead of claiming a full pass.

### 6.1 Resolve the Lab 4 BYOM policy conflict

Requirements: REQ-006. Input: [Lab 4](lab-04.md) and its recorded dialog/policy evidence.

- [ ] T011 [Plan:6.1] Have the policy owner establish whether the current connector supports Entra authentication under enforced `disableLocalAuth=true`. If not, obtain a formal owner-governed exception or approve an explicitly documented substitute/exclusion. Do not toggle local auth or evade the policy through resource tags or YAML.
- [ ] T012 [Plan:6.1] When a supported path exists, have Test verify direct invocation, parsed retrieval, connected prompt execution, grounded answers, empty results and error behavior. Record the chosen path and evidence in both Lab 4 guides and the ledger.

Exit: connected BYOM criteria pass. An approved exclusion changes the declared
workshop scope; it is not a pass of the unchanged original lab.

### 7.1 Complete Labs 5 and 5.1 integration evidence

Requirements: REQ-007. Inputs: [Lab 5](lab-05.md), [Lab 5.1](lab-05-1.md) and private-pipeline receipts.

- [ ] T013 [Plan:7.1] Reconcile the corrected Terraform deployment against required resources, provider versions, private networking and identities. Preserve reviewed plan/apply evidence and identify deviations from unchanged-source deployment; do not reapply merely to reproduce already-proven infrastructure.
- [ ] T014 [Plan:7.1] Have Test execute remaining connected corpus queries, filters, ranking and expected fields using source-stated locations. Verify original hotel URL navigation where required. If the corpus lacks URLs, record a source/requirement limitation and obtain an approved scope decision rather than fabricating links.

Exit: the required connected query behaviors pass with traceable sources and
documented infrastructure deviations. Prior private ingestion and projection
passes remain valid subsystem evidence, not whole-lab certification.

### 8.1 Reconcile evidence, resources and publication

Requirements: REQ-008. Inputs: every new acceptance receipt and [publication procedure](../publishing.md).

- [ ] T015 [Plan:8.1] Update the English/French execution reports, validation ledgers, lab guides and sanitized JSON receipts together. Preserve chronological failures and distinguish passed, failed, blocked, excluded and not-run criteria. Remove only independently verified owned disposable resources; otherwise record owner, cost review date and explicit retention decision.
- [ ] T016 [Plan:8.1] Run documentation tests, canonical validation, wiki export and wiki validation. Review the private repository and wiki destinations and human changes before authorized publication; verify actual remote revisions and both language pages after publishing. Mark workshop completion only against the final acceptance checklist below.

Exit: every mandatory requirement has current evidence, publication is verified
if performed, and no unowned, unexpectedly billable or unexplained test resource
is left behind. Cleanup is never inferred from a deletion request alone.

## Requirement mapping

These IDs organize the remaining work; they are not newly invented lab criteria.
The linked lab guides and retained acceptance records remain authoritative.

| Requirement | Remaining outcome                       | Plan item | Tasks      | Required evidence                           |
|-------------|-----------------------------------------|-----------|------------|---------------------------------------------|
| REQ-001     | Owned, approved and cost-controlled run  | 1.1       | T001,T002  | Inventory and attributable release record    |
| REQ-002     | Real hosted SDK repair                  | 2.1       | T003,T004  | Hosted Activity and exact-source receipt     |
| REQ-003     | Native authenticated delivery           | 3.1       | T005,T006  | Whole-turn trace and saved-state readback    |
| REQ-004     | Complete eleven-scenario acceptance     | 4.1       | T007,T008  | Fresh per-case matrix with source audit      |
| REQ-005     | Labs 0 through 3 acceptance closure     | 5.1       | T009,T010  | Per-lab positive/negative/privacy evidence   |
| REQ-006     | Supported Lab 4 BYOM outcome             | 6.1       | T011,T012  | Policy decision and connected prompt receipt |
| REQ-007     | Labs 5 and 5.1 connected acceptance      | 7.1       | T013,T014  | Deployment and connected-query receipts      |
| REQ-008     | Honest bilingual release and cleanup    | 8.1       | T015,T016  | Validated docs, publication and cleanup reads|

## Verification and final completion checklist

Run the repository's existing commands from its root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s scripts -p 'test_*.py' -v
.\.venv\Scripts\python.exe scripts\validate_docs.py
.\.venv\Scripts\python.exe scripts\build_wiki.py --output .wiki-build
.\.venv\Scripts\python.exe scripts\validate_docs.py --wiki .wiki-build
```

Use the [service instructions](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/README.md)
for its own virtual environment and tests. For live testing, require an authenticated
supported browser or API route, approved isolated resources, actual source data and
unique synthetic correlation. If native browser access is unavailable, direct APIs
can diagnose the backend but leave native acceptance blocked.

Before declaring full completion, require all of the following:

* All required tasks and original lab acceptance criteria have passed, with no
  unresolved mandatory failure hidden by an exclusion.
* Native and hosted evidence uses the approved artifact and preserves exact
  source content, applicability, routing and required negative behaviors.
* Approval records, bilingual reports and sanitized receipts agree with actual
  outcomes; no secrets, protected originals or fabricated results are published.
* Owned resources have verified cleanup or an explicit cost-controlled retention
  decision, and original agents and unrelated resources remain intact.
* Local validation passes and any claimed repository/wiki publication has been
  independently read back.
