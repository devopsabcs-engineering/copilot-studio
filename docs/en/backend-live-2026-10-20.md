---
title: Copilot backend and CLI validation - 2026-10-20
description: Actual authenticated Dataverse reads, official PAC recovery, saved-agent clone, and the remaining conversation and evaluation barriers.
ms.date: 2026-10-20
---

## Result and boundaries

[All labs](index.md) | [Français](../fr/backend-live-2026-10-20.md) | [Live ledger](live-rerun-2026-10-19.md)

The portal failure did not end the investigation. Authenticated Power Platform
and Dataverse calls succeeded, and the official Power Platform CLI cloned the
saved workshop agent, its two tools and its uploaded licensing PDF.
No agent configuration was changed or published. No email was resent and no
new paid Azure resource was created.

This proves a supported management route, not a completed conversation route.
The saved agent uses the newer CLI/GitHub Copilot harness. Its successful clone
does not establish that standard-harness Topics, Search knowledge, telemetry,
BYOM prompts or connected Foundry agents have been exercised.

## Actual service observations

| Check | Observed result | Acceptance boundary |
|-------|-----------------|---------------------|
| Intended Power Apps environment | HTTP 200; provisioning succeeded | Environment discovery only |
| Dataverse `WhoAmI` | HTTP 200 | Caller identified, not every service permission granted |
| Known workshop agent | HTTP 200 | Existing agent and configuration exported privately |
| Components scoped to that agent | Four records; no continuation page | Two connector tools, one file attachment and one settings component |
| Serialized component definitions | YAML in `data`; `content` null | Read actual definitions rather than treating null content as missing tools |
| Official CLI authentication | Default Azure identity authenticated and connected | Existing Azure CLI login reused; no new app registration |
| Official agent clone | Completed in a short path | Management/export passed, not a new runtime test |
| Direct Line endpoint discovery | Outer HTTP 400, nested 403/code 1002: `Bot does not belong to the tenant.` | No endpoint or conversation obtained; cause not established |
| Maker evaluation test-set discovery | HTTP 403, `InsufficientDelegatedPermissions`; missing `CopilotStudio.MakerOperations.Read` | No evaluation run started |

The agent's stored recognizer is `CLICopilotRecognizer` and its template is
`cliagent-1.0.0`. Integrated authentication remains enabled. The two exported
tools are **Search for users (V2)** and **Send an email (V2)** with invoker
authentication. Connection identities and references remain private.

The CLI list displays the Dataverse component state as `Published`, while the
agent record's `publishedon` field is null. Neither observation was treated as
proof of a usable published channel. The existing agent was not published to
make the test pass.

## Recover the official CLI without weakening policy

1. Check the existing installation before changing dependencies. In this run,
   `pac` was absent from PATH.
2. Try Microsoft's documented .NET tool distribution in a session-local path.
   NuGet v3 failed TLS; the official v2 attempt stalled and was stopped.
   Certificate validation and proxy settings were not disabled.
3. Use the official Microsoft Power Platform VS Code extension distribution
   when its bundled CLI is available. Resolve its package through the Visual
   Studio Marketplace's Microsoft publisher metadata, not an untrusted mirror.
4. Retrieve the bundled package through its actual HTTPS gallery CDN asset.
   The initial package gateway timed out. The CDN honored ordinary byte-range
   requests, allowing only the required bundled packages to be retrieved.
5. Verify package integrity. The Windows executable had a **Valid**
   Authenticode signature from **Microsoft Corporation**. ZIP CRC and byte
   lengths were checked. This is not a claim that a separate package-signature
   verification was performed.
6. Keep the CLI isolated. Both Windows and .NET CLI **2.13.1** were obtained.
   The .NET tool installed from the already downloaded official bundle using
   a local-only NuGet source. No global tool installation was required.

The Windows .NET Framework CLI reports that its MCP server is unsupported.
The .NET tool's MCP server initialized and returned its actual tool schemas.
Its management/evaluation discovery is not itself agent conversation evidence.

The installed Copilot plugin's management bundle also failed on a missing
native dependency. A session-local restore was attempted, but npm returned
`EALLOWREMOTE` under the configured package policy. No alternate registry or
policy override was used. The working PAC route was kept separate.

## Authenticate and clone safely

Use the actual Dataverse URL discovered for your intended environment.
Do not substitute a tenant domain or infer a URL from the agent's display name.
The examples use placeholders and omit private connection details.

```powershell
$env:AZURE_TOKEN_CREDENTIALS = 'AzureCliCredential'
& $pac auth list
& $pac auth create --name 'workshop-test' --managedIdentity `
  --environment '<actual Dataverse HTTPS URL>'
& $pac copilot clone --bot '<known workshop bot ID>' `
  --display-name 'lab1' --output-dir '<short private output directory>'
```

Here `--managedIdentity` means the documented default Azure identity chain.
It successfully reused the existing Azure CLI identity in this run; it does
not imply that this workstation acquired an Azure resource's managed identity.
The process-only credential selector was not persisted as a machine setting.

Record the original active PAC profile and restore it in `finally` after
each operation. This run preserved the existing profile and restored it after
each use of the uniquely named lab profile. Never clear all profiles.

The first clone hit `DirectoryNotFoundException` when writing a long connection
filename below the deep session path. Its partial output was not counted as a
successful clone. A retry into that nonempty destination was rejected.
A fresh, short private path then completed; a persistent short-path clone also
completed. No system-wide long-path setting or user file was changed.

## Evidence handling and remaining work

Raw configuration, source PDF, connection definitions and identity responses
are private. The [sanitized backend results](../assets/runtime-2026-10-19/backend-results.json)
publish only narrow observations, counts and failed acceptance boundaries.
The independent Lab 1 evidence audit distinguishes source identity from answer
accuracy: a matching PDF hash cannot prove that every answer claim or citation
is correct.

The freshly cloned PDF contains **867,776 bytes**. Its SHA-256 equals both the
freshly hashed approved original and the previously recorded source hash.
The independent audit passed **6 of 8 checks**, with **2 blocked** and none
failed. It made no new live call or PDF content-check claim.

The complete saved supported-answer text and citation-target mapping are still
needed for a full Lab 1 citation audit. Existing clipped screenshots must not
be reconstructed into an invented transcript. The six earlier PDF content
checks remain historical evidence unless actually rerun.

Before additional paid provisioning, establish an authorized standard-agent
authoring and test route. Evaluation requires an identity accepted by that API;
Dataverse access alone did not provide it. Do not bypass the observed 403,
disable authentication, broaden roles speculatively, or publish the existing
user agent to work around the barrier.

No new product screenshot is claimed for this backend-only continuation.
The existing gallery preserves its real screenshot provenance. All earlier
paid test environments remain deleted; the local tools and private source
backup are not cloud deployment resources.

## Follow-up: exact authorization diagnosis and bounded retries

The official PAC diagnostic response body identifies the maker-evaluation
failure precisely: `InsufficientDelegatedPermissions`, with the application
missing the delegated permission `CopilotStudio.MakerOperations.Read`.
This is an observed API error, not a guess that the user lacks an Azure
subscription role. Assigning a broader Azure role is not a justified fix.
The separate Direct Line tenant-membership error remains unexplained.

The [Power Platform authentication guidance](https://learn.microsoft.com/en-us/power-platform/admin/programmability-authentication-v2)
requires an application with the relevant API permissions and an appropriately
authorized user token. Application configuration, user consent and admin consent
are distinct from an existing successful Azure CLI or Dataverse login.
No application, permission grant or tenant-wide consent was created in this test.

A token request for only the observed read scope was attempted using the
existing login. It returned no usable token result before the attempt was
stopped. That is not evidence of successful consent, a corrected token, or
an additional server rejection. The configured npm policy also rejected an
offline dependency-restore attempt with `EALLOWREMOTE`; no policy override
was attempted.

An independent Test Agent tried the historically verified current-harness
Preview route, rather than repeating the broken classic route. The previous
browser tab was unavailable. One browser-open operation timed out without
returning a page ID; its eventual effect is unknown. No retry loop, prompt,
answer, citation check or new screenshot resulted.

The next legitimate recovery is an authorized delegated application/user
session for evaluation, plus an accessible standard-agent test destination.
Requesting a permission, granting it and successfully exercising the API must
be recorded as separate steps. A real authorized person must complete any
required consent or interactive sign-in; an automated unavailable-user response
does not authorize it.

## Browser recovery and three new runtime checks

On October 20, the signed-in browser route became accessible again. Saved
configuration and conversation history matched the earlier workshop licensing
advisor. This confirms continuity with that Default-environment agent, not
independent verification of the originally intended environment or a standard
agent destination.

Three fresh Preview checks passed their narrow expectations:

* Uploaded-file retrieval returned `Power-Platform-Licensing-Guide.pdf`,
  reference `turn1doc1`, with a displayed latency of 4.9 seconds. The complete
  new answer identifies October 2026, quotes an introductory sentence and
  cites the uploaded-file title through `cite:1`.
* A fictional Contoso unpublished-discount question explicitly refused to
  invent a tenant-specific discount or negotiated price.
* Search for users (V2), called once with a synthetic search term and `top=-1`,
  displayed the matching input and **Request validation · 400**, with a
  displayed latency of 4.5 seconds. No retry was observed. The more specific
  positive-number error text came from the agent, not the expanded error panel.

The [sanitized browser evidence](../assets/runtime-2026-10-20/browser-results.json)
preserves exact prompts, complete new answers, observed tool output and limits.
The uploaded PDF's actual page, edition and quotation still require an
independent source audit. A title match does not establish a working page anchor,
and the new answer does not reconstruct the earlier historical transcript.
The directory result proves request validation, not downstream outage recovery.

Evaluate now opens and displays **Create your first evaluation**, alongside a
Copilot Credits warning. No evaluation was created or run. The approval form
received an unavailable-user response, not authorization. This browser boundary
is distinct from the earlier PAC missing delegated-permission failure, which
has not been repaired.

No email, agent configuration, permission, consent, authentication or publication
was changed, and no Azure resource was provisioned. Preview inference and retrieval
did run; a displayed zero-credit estimate does not prove zero billing.
No new screenshot file was retained, so none is claimed in the published gallery.
The full workshop remains incomplete, including independent citation auditing,
evaluation grading and the connected Search, telemetry, BYOM and Foundry paths.

## Independent audit of the new PDF answer

After runtime recovery, an independent PyMuPDF check inspected the retained
official PAC clone, rather than asking the agent to verify itself.
All **five checks passed**: the clone matches the original download and prior
SHA-256, and the new answer's edition, complete quotation and named section
match physical page 3. Only whitespace was normalized for the quotation check.
The PDF has 30 pages and contains 867,776 bytes.

The [source-audit results](../assets/runtime-2026-10-20/pdf-answer-audit.json)
supersede the earlier unverified-content boundary for this one new answer.
They do not audit the historical full licensing-plan response or prove that
clicking `cite:1` opens the intended file/page. No fresh remote download was
performed in this local comparison. Full Lab 1 citation navigation and full
workshop acceptance therefore remain open.

## Approved evaluation submitted, grading not observed

The owner subsequently approved Copilot Credits and Azure resources.
The signed-in Evaluate route saved **Read-only licensing 3 cases 2026-10-20**
and submitted exactly **one run** at the displayed 7:25 AM start time.
All three cases use the actual UI's **General quality** grader:

* Retrieve the uploaded guide's edition and one introductory sentence
* Refuse an invented tenant-specific discount and negotiated price
* Reject an unsupported fictional product and unlimited-free-capacity claim

General quality checks relevance and completeness; it does not compare against
an expected response. No exact-match grader or completed score is claimed.
The actual notification said the evaluation was queued and would start when
capacity became available. The overview showed **Waiting**, with no per-case
responses, grades or credit total. A ticking duration and a credits field
labeled Running were not treated as proof of execution.

![The approved evaluation was queued, not graded](../assets/runtime-2026-10-20/evaluation-queued.png)

At **11:36:20 UTC**, two bounded attempts to reopen the same run failed:
the existing shell reported `ERR_CONNECTION_RESET`; a fresh same-run route
aborted during the Microsoft sign-in redirect. Current state is therefore
**unknown**. Waiting is the last historical observation, not a freshly verified
status. The submitted run remains in place and may execute later.
No duplicate run was created or cancellation attempted.

One final elapsed-time recheck at **13:01:03 UTC** encountered the same shell
connection reset and stopped after one navigation. No new status, grade or
credit total was accessible. The [final recheck record](../assets/runtime-2026-10-20/evaluation-final-recheck.json)
preserves that observation without changing the historical queued-run evidence.

The [evaluation evidence](../assets/runtime-2026-10-20/evaluation-results.json)
preserves the prompts, UI grader, queued state and timestamped recovery failures.
Agent configuration, authentication, permissions and consent were unchanged.
No email was requested or sent by the operator. Without completed traces,
the evaluation's eventual connector behavior cannot be independently certified.
No Azure resource was needed for this browser evaluation.

A separate citation-navigation question returned plain file-URI text instead
of an exposed clickable citation. No file or page target was opened. This
does not invalidate the independent source-content audit, but citation
navigation remains unverified. The workshop is not complete.

## Restored tab error versus fresh backend evidence

On the next continuation, the newly shared Agents tab was inspected before
navigation. It rendered **Dataverse isn't set up in this environment** at
the existing agent's root, not the evaluation-results route. Returning directly
to the same submitted run timed out; the subsequent browser connection failed.
No new evaluation state, response, grade or credit total was obtained.
No screenshot is claimed for this inspection.

The [restored-tab record](../assets/runtime-2026-10-20/evaluation-restored-tab.json)
preserves the actual message and distinguishes retained console events from
new observations. The setup message alone does not establish deletion,
database absence or a need to provision a replacement.

Fresh read-only backend checks at **17:25 UTC**, recorded by the execution-host
clock, then returned:

* Environment discovery HTTP **200**, provisioning **Succeeded**, with the
  same Dataverse endpoint as the earlier evidence
* Dataverse WhoAmI HTTP **200**, matching the historical user and organization
* Exact saved workshop bot HTTP **200**, matching the supplied portal agent,
  with unchanged name and schema

The [backend comparison](../assets/runtime-2026-10-20/evaluation-backend-diagnosis.json)
therefore confirms that the existing environment and agent remain readable.
It does not prove every portal prerequisite or diagnose the rendering failure.
The known-denied evaluation API was not called again, and no database,
environment, identity, permission, consent or agent configuration was changed.
The single submitted evaluation's current state remains unknown. Restore a
working authorized portal session or obtain an approved delegated application
route before claiming run results; do not create a replacement database merely
to suppress this portal message.

## Completed evaluation recovered from the working session

At approximately **19:13 UTC**, the working signed-in SPA session exposed the
exact original run's Results page and per-case drawers. No new run was submitted.
The completed run used **7 Copilot Credits** and displayed duration **00:02:44**:
**one pass and two failures** under General quality.

| Case | Actual grade | Observed feedback |
|------|--------------|-------------------|
| Fictional product and unlimited-free-capacity claim | Pass | Relevant, complete and based on knowledge sources |
| Invented tenant-specific discount | Fail | Relevance failed; feedback explicitly acknowledged refusal to invent a price; further checks skipped |
| Guide edition and introductory quotation | Fail | Relevant, but incomplete and missing knowledge citations according to the grader |

The [completed evaluation evidence](../assets/runtime-2026-10-20/evaluation-completed.json)
preserves actual responses and grader feedback. The refusal result suggests
a grader/objective mismatch for this negative case, not permission to override
its recorded failure. The PDF answer contains visible citation markers and a
knowledge-source entry; those do not invalidate the grader result or establish
working citation navigation. Full execution traces were not inspected.

The same working session reached an existing **Standard** agent's Overview
with Test status **Connected**, Azure AI Search knowledge selection and
Application Insights settings. Those controls establish a usable starting
surface, not completed connected Search, telemetry, BYOM or Foundry tests.
Existing agents were not modified during this recovery. The earlier setup
error was not reproduced; its original cause remains unproven.

## Keyless Search connection blocked by the hosting browser

After the approved trial extension, a single disposable Basic Search service and
keyless embedding account were created. Separate indexes held 30 licensing PDF
pages and three original hotel documents. Two real natural-language vectorizer
queries returned exact-source text. The licensing publisher PDF matched the
approved file byte-for-byte; no navigable hotel URLs were available or invented.

The isolated Standard draft's **Microsoft Entra ID Integrated** connection form
enabled Create with an HTTPS Search endpoint. Distinct supported activation
attempts returned the same error:

> The connection consent pop-up window has been blocked by the browser. Please
> allow pop-ups in your browser and try again.

No actual sign-in or consent screen opened. After canceling, the knowledge
selector showed **Not connected**, **No connections available**, and disabled
**Next**. No index, field mapping or knowledge source was saved, and zero Copilot
questions ran. This is a hosting-browser blocker, not an established Azure
permission or endpoint failure. Vectorizer smoke tests do not pass the connected
grounding or citation-navigation gates.

The [sanitized attempt](../assets/runtime-2026-10-20/search-connected-attempt.json)
preserves these boundaries. The user was unavailable for the browser-recovery
form; no consent or browser-security change was inferred. Further provisioning,
including Foundry reuse, was stopped and owned-resource cleanup was released,
subject to verifying remote connection absence. Deletion requires its separate
receipt. At **20:42:56 UTC**, navigation readback verified empty saved Knowledge,
empty Tools and no available Search connection; the unsaved wizard was discarded.
This establishes portal-visible cleanup readiness, not a tenant-wide connection
inventory or Azure deletion. Resume only through normal browser pop-up controls or a working
interactive sign-in session, and stop if new permission/admin consent appears.

The separate [cleanup receipt](../assets/runtime-2026-10-20/search-cleanup.json)
verified deletion at **20:48:11 UTC**. The owned group, Search service, AI account,
embedding deployment and all four owned resource-scoped role assignments returned
HTTP 404. The private connection handoff was removed; unrelated principals and
external policy destinations were untouched. No active resources from this test
remain, although historical hourly Search and embedding-token charges may settle
later. Cleanup does not turn the blocked Copilot tests into passes.

## Formal access-key connection executed four real questions

A later supported alternative used the normal top-level **Power Apps >
Connections > New connection > Azure AI Search** form. The reviewed inherited
rules did not prohibit Search key authentication; the Cognitive Services
keyless requirement remained enabled. A new disposable Search service isolated
the admin key's service-wide data-plane access. Cached vectors were reused,
with zero new document-embedding tokens. No manual YAML/API connection writes,
new consent or browser-security override was used.

The formal connection read back **Connected** without an OAuth pop-up, and the
Search knowledge source reached **Ready**. Four actual questions ran:

| Case | Actual result | Remaining boundary |
|------|---------------|--------------------|
| Licensing quotation | Complete audited sentence, October 2026 edition, physical page 3 and authentic publisher PDF/page target matched | Browser click-through and viewer page not verified |
| Unsupported licensing product | Failed: acknowledged absence, then guessed likely entitlements with unrelated guide citations | Source-evidence-only behavior needs correction and retest |
| Hotel location | Answer Qatar matched the source's actual location field | Original fixture expected city Doha; source/fixture mismatch, not fabricated Qatar |
| Unsupported hotel shuttle | Passed abstention without invented departure times | No authentic external hotel document URL |

The hotel citation opened an in-product source-content dialog, not an original
PDF viewer. The hotel index was saved separately with the licensing index
excluded; no licensing contamination was observed. Field mapping was not exposed
in the portal, so Azure schema evidence is not presented as portal readback.

The [sanitized execution](../assets/runtime-2026-10-20/search-accesskey-execution.json)
retains the original failure. Overall acceptance remains failed pending rework.
At this observation, the new source, formal connection and resources were still
retained. Earlier deletion receipts apply only to the previous environments.

## Native grounding correction and three regression questions

The author reconciled the live draft with official PAC before proposing a
single `additionalInstructions` property on the actual classic generative-answer
node. Twelve schema checks passed, but PAC 2.13.1 offline packaging rejected
the legitimate connected workspace's knowledge directory and connection-reference
file. No files were stripped and no CLI push occurred.

The supported native portal prompt property provided another authoring route.
The three general evidence-only instruction paragraphs were saved at
**22:35:50 UTC** and verified after navigating away and reopening at
**22:37:49 UTC**. Source references and orchestration were preserved.
Three fresh licensing-only questions then ran:

* The original fictional-product negative stopped inventing entitlements, but
  returned a generic rephrasing fallback rather than a source-specific explanation.
* A distinct unsupported satellite-phone entitlement explicitly abstained and
  invented no capacity.
* The positive regression preserved the full audited sentence, October 2026
  edition, physical page 3 and authentic publisher PDF/page target.

The [rework evidence](../assets/runtime-2026-10-20/search-portal-rework.json)
keeps the original failure, seven total connected questions and remaining
limitations separate. The hotel fixture now asks for the source-stated
**location, Qatar**, not an inferred city; the original corpus was not edited
and no additional hotel question was counted. A separate direct browser open
of the authentic PDF timed out, so viewer navigation remains unverified.
Source-aware no-answer handling still needs correction. These outcomes do not
certify the entire workshop or imply that the retained resources were deleted.

## Source-aware no-answer handling passed

The final correction added only an `elseActions` branch to the existing
answer condition in the real Conversational boosting topic. It sends a
source-aware abstention for an empty answer, then ends the dialog. The nonempty
automatic-answer path, citations, three grounding paragraphs, source references
and settings were preserved. Global fallback and error handling were not changed.
Native save at **22:52:26 UTC** and reopening at **22:53:55 UTC** verified
persistence; no CLI push occurred.

Two fresh licensing-only tests passed. The original unsupported request received:

> I could not establish the requested information from the configured source
> evidence. I will not infer an answer.

It had zero citations and no invented entitlement. The positive regression
retained the exact audited sentence, October 2026 edition, physical page 3 and
authentic publisher PDF/page target, with one final answer and no abstention
message. The [final no-answer evidence](../assets/runtime-2026-10-20/search-source-noanswer.json)
records **nine total connected Search questions**, retaining the original failure
and intermediate generic fallback. This passes the source-aware no-answer gate,
not external PDF navigation or the whole workshop.

## Foundry formal authentication remained blocked

The existing disposable AI account initially lacked project management. A
supported feature-only PATCH enabled it while preserving enforced keyless
authentication and network security. One owned child project with managed
identity was created; no new project roles, models, agents or inference queries.

Using the actual ARM-returned project endpoint, exactly one formal **Power Apps >
Connections > Azure AI Foundry Agent Service > Microsoft Entra ID User Login**
attempt failed at **23:01:40 UTC** with the same hosting-browser pop-up error.
The dialog was canceled. Native refresh at **23:02:28 UTC** showed zero Foundry
connection rows, with no saved Foundry reference or endpoint in the draft.
No consent, retry, token extraction or browser-security override followed.

The [Foundry authentication receipt](../assets/runtime-2026-10-20/foundry-formal-auth.json)
distinguishes this observed failure from model or Activity-protocol execution,
neither of which ran. The new Search source/connection and owned environment
were then released for supported removal and scoped cleanup. Their deletion
requires a fresh receipt; earlier cleanup records do not cover this environment.

## Current access-key environment disconnected

At **23:15:35 UTC**, supported portal readback verified the owned Search knowledge
source absent after navigation, Tools empty and no agent connection permissions.
The revised grounding instructions and both answer branches remained saved,
without owned endpoint/source/connection references in that topic.

Before deletion, the formal connection's native dependency view stated it was
not used by any apps or flows. Only the named disposable Search connection was
deleted. Native refresh at **23:13:27 UTC** showed zero owned Search matches and
zero Foundry rows; other connections were preserved. The
[removal receipt](../assets/runtime-2026-10-20/search-accesskey-removal.json)
is portal-scoped evidence, not raw backend enumeration or proof of Azure deletion.
No new prompt, sign-in attempt, PDF navigation or publication occurred.

The separate [current-run Azure cleanup](../assets/runtime-2026-10-20/search-accesskey-cleanup.json)
completed at **23:20:01 UTC**. Independent GETs returned HTTP 404 for the owned
child project, sole scoped role, group, Search service, AI account and embedding
deployment. The external governance destination returned HTTP 200 before and
after and was untouched. Ephemeral secret and project-endpoint handoffs were
removed. No owned active resources from this run remain; historical metered
and policy-routed diagnostic charges may still settle. The corrected unpublished
topic and all historical results remain preserved.

## Native host confirmed the publisher PDF viewer

A later read-only check through normal Windows accessibility controls found the
publisher PDF already loaded in the exact VS Code workspace host. The browser
address matched the previously verified public PDF URL with `#page=3`. Its native
document reported **30 pages**, its page-number control was **3**, and the
**Page 3** group contained **Using This Guide** and the complete audited sentence.

The [native viewer receipt](../assets/runtime-2026-10-20/native-pdf-viewer.json)
supersedes the earlier inability to observe the PDF viewer, without erasing those
timeouts. It proves accessible viewer content at the authentic target, not the
origin of that tab or the original chat citation's click-through. No new agent
question, resource, byte-hash claim, published screenshot, token extraction or
browser-security change was involved.

## External Edge Foundry recovery stopped before submission

The normal external Edge browser reached **Power Apps | Connections** through
the existing organizational SSO session. The intended account matched without
publishing its identity. This was a different supported browser route, not a
pop-up override or a repeat of the integrated-browser authentication failure.

One new keyless S0 account and managed-identity child project were provisioned
for authentication only. No models, agents, roles or inference calls were added.
The real **Azure AI Foundry Agent Service** form offered **Microsoft Entra ID User
Login** and required an **Azure AI Project Endpoint**. The display name persisted,
but normal native focus, keyboard input and UI Automation ValuePattern did not
retain the actual endpoint. At **23:44:08 UTC**, the endpoint readback was empty
and **Create** was disabled. The unsubmitted form was canceled.

The [external native-auth receipt](../assets/runtime-2026-10-20/foundry-external-native-auth.json)
records **zero Create invocations and zero authentication submissions**. No
authentication rejection, external-browser pop-up behavior or root cause was
established. Saved-connection absence was not independently verified when input
stopped. No consent, password, MFA, token extraction, browser-security change or
inspection of unrelated tabs occurred.

A read-only inspection found an **Azure AI Foundry Inference** candidate, but its
authentication fields were not exposed. Its authentication choices and
compatibility with native prompt BYOM remain unverified. This does not overturn
the observed key-only prompt dialog or the enforced keyless-policy limitation.
The requested manual handoff was unavailable; no further authentication or
model provisioning was attempted.

Normal navigation recovered the exact Connections document. At **23:55:42 UTC**,
a fresh unfiltered list in the intended environment contained no owned Foundry
connection. This supersedes the earlier unverified-list disposition; it is
native UI evidence, not a raw backend enumeration. The exact individual tab
close control could not be confidently identified, so the Power Apps tab was
left open rather than risking unrelated tabs.

The [auth-only cleanup](../assets/runtime-2026-10-20/foundry-external-auth-cleanup.json)
completed at **23:58:49 UTC**. Independent project, account and group GETs all
returned **404**. The external governance workspace remained **200** before and
after, untouched. The private endpoint handoff was removed and no live owned
resources remain. A **soft-deleted account recovery record remains** with HTTP
200; no purge was authorized or attempted. Historical charges may still settle.
Any future manual connection requires a fresh approved project endpoint, not
the deleted endpoint. The full workshop remains incomplete.

## Official references

* [PAC installation](https://learn.microsoft.com/en-us/power-platform/developer/howto/install-cli-net-tool)
* [PAC authentication](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)
* [PAC Copilot commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot)
* [PAC Copilot Studio evaluation commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot-studio)
* [Power Platform API permission reference](https://learn.microsoft.com/en-us/power-platform/admin/programmability-permission-reference)
* [Microsoft Power Platform VS Code extension](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.powerplatform-vscode)
