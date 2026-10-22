---
title: Copilot backend and CLI validation - 2026-10-20
description: Actual authenticated Dataverse reads, official PAC recovery, saved-agent clone, and the remaining conversation and evaluation barriers.
ms.date: 2026-10-22
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

A subsequent read of the [official Inference connector reference](https://learn.microsoft.com/en-us/connectors/azureaifoundryinference/)
found only **Default** authentication with required **Target Uri** and **API
Key** fields. This published contract does not document an Entra alternative.
It resolves the documentation question without inventing a native form readback
or proving compatibility with the prompt's model selector. No replacement model
or gateway was provisioned on that basis.

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

## Additional native input prerequisite remained blocked

After the request to continue autonomously, a separate no-resource check was
authorized for the normal **LegacyIAccessiblePattern.SetValue** input method.
That method had no recorded earlier attempt. Native New connection requests
did not open the form, and the exact-window foreground guard failed. The check
stopped before reaching the endpoint control: **zero Legacy input probes**,
Create invocations, authentication submissions or new resources.

At **00:06:08 UTC on 21 October**, fresh unfiltered native readback still showed
the correct Connections document, blank search, no Foundry rows and no open
form. The [prerequisite receipt](../assets/runtime-2026-10-20/foundry-native-input-prerequisite.json)
does not label Legacy input unsupported or claim it was tested. No clipboard,
browser internals, security settings or unrelated tabs were accessed.

The required next action is to manually foreground the existing authorized
Power Apps tab and open the blank Agent Service form. The requested intervention
was unavailable. No fresh project was provisioned merely to repeat this blocker;
the previously verified cleanup remains valid. Full runtime acceptance is still
blocked, not complete.

## Shared browser recovered form input, not external authentication

The subsequently shared Connections page was readable through the integrated
browser tools. Pointer clicks timed out even after normal bring-to-front.
Ordinary keyboard activation opened New connection and the real Agent Service
form. The harmless `https://example.invalid` endpoint probe persisted after
blur and enabled Create. The form still selected **Microsoft Entra ID User
Login**.

The [shared-browser receipt](../assets/runtime-2026-10-20/foundry-shared-browser-input.json)
therefore proves working input on this shared integrated page, superseding the
need for manual foregrounding on that route only. It does not prove recovered
external Edge input or removal of the previously observed integrated-browser
authentication pop-up restriction. Create was never invoked. The form was
canceled, its dialog closed, and normal navigation returned to saved Connections.
No resource, consent, authentication submission or security change occurred.
The working input alone does not justify another paid environment or count as
a connected Activity conversation.

## Manual external connection succeeded; Activity response remains unverified

The user's external Edge screenshot at **01:07:15 UTC on 21 October** showed
**Workshop Foundry Validation**, Azure AI Foundry Agent Service (Preview),
**Connected** in the intended environment. This supersedes the authentication
blocker for this connection only. Consent details are not inferred.

A fresh owned keyless account/project was prepared for that manual form, then
extended with one **GPT-4.1-mini 2025-04-14 Standard capacity 1** deployment and
one enabled **workshop-validation-specialist**, version **1**, supporting
Activity and Responses. No new roles or retrieval sources were added.
These resources are **currently live and held for diagnosis**. Their
**04:58:55 UTC on 21 October** expiry tag is not automatic deletion. Earlier
cleanup receipts concern different runs and do not prove this run deleted.

The connected agent was added through the existing connection in the isolated
draft, then reopened to verify persistence. The native action is
`InvokeExternalAgentTaskAction`, `ActivityProtocolMetadata`, `SendActivityV2`,
with the correct agent ID and Invoker credentials. Classic orchestration,
existing Search/telemetry topics and unpublished status were preserved.

The first generic prompt produced the existing source-aware Search abstention,
not a connected invocation. A dedicated **Workshop Foundry connection check**
topic was then saved and reopened with zero checker errors/warnings. Its exact
trigger, `workshop foundry connection check`, invokes the existing connected
action through `BeginDialog`; it contains no hardcoded success response.

One fresh corrective test at **01:41:26 UTC** proved topic execution and target
binding through native `DialogTracing` and `DynamicPlanStepBindUpdate`.
At **01:50:45 UTC**, no response or error had appeared. This is a failed runtime
acceptance observation, not a platform-returned timeout or proven authentication
failure. Dispatch, downstream execution and callback delivery remain unverified.

One distinct direct Responses diagnostic completed in **5.78 seconds** and
returned **I am the workshop validation specialist. Foundry connection verified.**
It consumed **75 input + 13 output = 88 tokens**, with zero retries. This verifies
backend inference for the CLI identity, not the connector identity or Activity
transport. Live metadata already showed enabled Activity/Responses; no evidence
supports a missing publish step or a speculative role/protocol change.

The [connected runtime receipt](../assets/runtime-2026-10-20/foundry-manual-connection-runtime.json)
preserves these boundaries and the historical initial failure. The next diagnostic
is server-side connector/runtime correlation for conversation
`46bdd592-bb45-40ae-adaf-e031960c70fa`, prompt activity
`0da156dc-11ae-4f3a-98d8-2b81be3e3c2b`, at **01:41:26 UTC**. The stall's root
cause is unknown. The full workshop remains incomplete.

## Instrumented connected Activity smoke passed

Read-only server correlation found a Projects POST accepted with **HTTP 202**
at **01:41:30.591 UTC**, correlation
`362a8914-f06a-4b9e-877a-ce407d2eeae5`. Its timing matches the earlier stalled
test, but it lacks the native identifiers, endpoint path and effective caller.
It is a temporal candidate, not proof of that Activity dispatch or its outcome.

The owned project exposed Audit/Trace categories but had no project diagnostic
setting. One isolated Pay-as-you-go workspace with 30-day retention and a
provider-read-back **0.023 GB/day** cap was therefore created in the same owned
group, and only the project's Audit/Trace collection was enabled. The cap is
best effort, not a hard spending limit; account policy logging was untouched.

One new instrumented native conversation, `84c7430d-3e15-4832-996e-1d36f82349fc`,
sent the exact trigger once at **02:27:09.715 UTC**. Native tracing again proved
the explicit topic and connected target binding. At **02:27:16.579 UTC** the
actual chat received **I am the workshop validation specialist. Foundry connection
verified.**, independently confirmed visible. Elapsed time: **6.864 seconds**.
The parent topic contains no hardcoded success response. This passes the
synthetic connected Activity smoke; it does not certify retrieval or citations.

A browser `net::ERR_ABORTED` event preceded the reply, so it is not treated as
a failed final result. The scoped Audit/Trace query succeeded but still returned
zero matching rows after bounded ingestion observation. Diagnostic ingestion
and a causal role for logging in the recovery remain unverified. The earlier
no-reply test is retained as a real historical failure.

At **02:39:14 UTC**, observer-only cleanup independently verified **404** for
the temporary workspace and project diagnostic setting. Account policy logging
remained unchanged. The working account, project, small model, agent and formal
connection remain **live and retained**; this is not full environment cleanup.

A separate current-provenance preflight passed **117 evidence checks**, but
found no distinct supported repair for the earlier native annotation and source
association failures. Original inline documents have no verified publisher URLs:
these remain `null`. A documented authenticated `citationUrl` lookup is not a
publisher URL or proof of native metadata forwarding through Activity. No new
retrieval environment, embedding call or connected retrieval prompt was created
merely to repeat that failed strategy.

The [Activity success and observer-cleanup receipt](../assets/runtime-2026-10-20/foundry-connected-activity-success.json)
separates working synthetic transport from the still-open multi-source quotation/
native-citation gate and the BYOM keyless-policy mismatch. The workshop remains
incomplete; no original agent or security policy was changed.

## Original lab acceptance reconciled and real retrieval exercised

The accessible original Lab 6 notebook and setup guide require source-grounded
answers with visible source attribution, domain-specific and combined retrieval,
and connected direct/quick-reference/expertise/hybrid scenarios. They do not
explicitly require native annotation arrays, external publisher URLs for the
synthetic records, or verbatim quotations. Those earlier assistant-added gates
remain useful enhancement evidence, not substitutes for original lab acceptance.
The protected main Lab 6 document remained unreadable and was not bypassed;
additional requirements there are unknown. Genuine custom Foundry prompt
execution in Lab 4 remains an original requirement, not an optional enhancement.

Under that corrected scope, a separate **workshop-retrieval-specialist** was
created in the current owned project, preserving the working synthetic smoke
agent. Minimal Search **Basic, one unit**, a small embedding deployment
**GlobalStandard, capacity 1**, three source indexes and an authenticated
knowledge-base MCP tool were provisioned. The 24 original records joined
exactly to their source data, eight per knowledge source. Scoped managed-identity
roles and every added resource/version were added to ownership/cleanup tracking.
Keyless Cognitive authentication and existing governance were preserved.

A second native attachment and explicit classic topic were saved and reopened.
Four domain submission attempts produced three confirmed native messages.
Fraud, investigation and combined cases reached the retrieval-agent target but
returned no answer during bounded observation; regulatory delivery was
unconfirmed with **Unable to connect** visible. No grounded connected-domain
pass was claimed.

A distinct direct-agent diagnostic proved completed MCP retrieval of all 24
original records, then failed final generation with **rate_limit_exceeded**.
The actual deployment limit was only **1,000 TPM / 1 RPM**. This error is
proven for that direct call, not definitively correlated to the native stalls.
Available regional quota was verified, then only Standard capacity changed
**1 to 26**, independently read back as **26,000 TPM / 26 RPM**. The conservative
planning estimate was 25,529 tokens/minute for context, multiple model requests
and output margin; it is not measured token consumption. No provisioned
throughput, model/version, MCP, authentication or security change accompanied it.

Three bounded direct regressions each completed without retries and with 24
exact source joins:

| Retrieval version | Actual usage | Result |
|-------------------|--------------|--------|
| 1, capacity-only fix | 5,244 input + 564 output = 5,808 tokens | Rate error resolved; five unsupported/overbroad assertion families |
| 2, generic evidence/condition rules | 5,643 input + 740 output = 6,383 tokens | Four remaining scope/record-attribution failure families |
| 3, extractive evidence adaptation | 5,541 input + 999 output = 6,540 tokens | Nine unchanged complete source sentences; conditions preserved, but some irrelevant material and incomplete applicability limits |

Version 3 displayed original document titles rather than the requested
knowledge-source labels. That mismatch is recorded separately from quotation
authenticity: it did not fabricate record IDs or URLs. Extractive output is not
certified as the full requested narrative synthesis. Earlier unsupported
obligation, deadline, retention-scope and attribution findings remain failures;
completed inference or correct source-name keywords alone do not pass grounding.

The [retrieval validation receipt](../assets/runtime-2026-10-20/foundry-original-lab-retrieval-validation.json)
records the actual scope correction, capacity fix and failed grounding gates.
Further paid prompt retries stopped. The Search service, account/project,
chat and embedding deployments, both Foundry agents and native connections/topics
remain **live and retained**, with cleanup ownership recorded. Expiry tags do not
delete them. Full connected scenario coverage and original BYOM execution remain
incomplete; no original agent or security policy was changed.

## Full-model comparison completed but did not resolve grounding

A model-only comparison tested whether the remaining synthesis failures came
from the smaller model. The service rejected an initial override request with
HTTP 400 `invalid_payload`: a request model must match its referenced agent.
No completion or usage was returned. Its temporary deployment was deleted and
absence verified; the existing agent was not changed.

The supported alternative used a separate temporary agent copied from retrieval
version 2, changing only its model deployment to **GPT-4.1 2025-04-14**.
Instructions, temperature, MCP tool, source data and the combined-case prompt
were unchanged. Regional Standard quota was checked before creating a
capacity-26 pay-per-token deployment; no provisioned throughput was used.

One invocation, with no retries, completed in **24.539 seconds** and used
**5,627 input + 730 output = 6,357 tokens**. Persisted MCP output joined all
24 original records. Displayed record/source locators existed and matched the
actual source domains, but that did not establish claim-level grounding.
Manual comparison with those actual passages found three blocking families:

* Customer/relationship-scoped due diligence and approval were generalized to transactions.
* A blocked-transaction reporting deadline was extended to confirmed screening matches.
* Mandatory filing lost material institution/amount thresholds and timing context.

General caveats did not retract the affirmative overbroad duties. A larger model
alone did not resolve these failures, so the configuration was **not promoted**
to the connected agent. No further identical paid synthesis attempts followed.

Both the temporary comparison agent and deployment were deleted, with independent
GET-after-delete 404 checks verified at **13:12:41 UTC on 2026-10-21**.
Existing retrieval version 3, the working smoke agent, native topics/attachments
and formal connection were unchanged. The earlier Search/project/models remain
live, not deleted by this comparison cleanup. Original BYOM still requires a
governance-approved compatible environment; no policy, role or consent was changed.
The [model-comparison receipt](../assets/runtime-2026-10-20/foundry-model-comparison.json)
preserves this failed acceptance result without publishing private passages.

## Source provenance repaired and original backend questions passed

On **2026-10-21**, the four unchanged questions from the original notebook were
run against retrieval agent version 3. Before the metadata repair, quoted content
was authentic, but only **2/4** answers passed canonical knowledge-source
attribution. The other answers used authentic document titles, and one omitted
some labels. These were attribution gaps, not invented documents.

The repair added retrievable, nonsearchable `source_name` metadata to three owned
indexes and all **24** records. Independent comparisons verified preservation of
original `id`, `title` and `content`, semantic configuration and vector fields.
Vector values were not resubmitted; the update made no embedding or model calls.
Agent version, instructions, model, tools and authentication were unchanged.
The requested projection is `id/content/source_name`; MCP also returns the
original semantic title. Titles were neither removed from context nor replaced.

After repair, **4/4** original questions passed relevant, condition-preserving
extractive content and canonical claim-level attribution. Actual source joins
were **19 / 14 / 18 / 24**, not an artificial requirement for 24 on every query.
Four requests, zero retries, consumed **21,341 Responses tokens**; the baseline
used 19,242. These are measured response usage, not complete workshop billing
or a measurement of native Copilot Credits. A local projection guard initially
rejected the provider's additional title; the already completed response was
recovered without another inference. Six offline projection tests passed.
An initial valid HTTP 204 update was recovered using ownership/snapshot/ETag
guards. Projection backups remain private; removing the additive schema field
would require an index rebuild, which was not attempted.

### Genuine native success and interrupted category batch

A separate native evidence-preservation question received a real connected
reply in **352.940 seconds**, measured between server activity timestamps.
The complete original paragraph, correct source label, relevance, retention and
legal-hold conditions passed. Native BeginDialog and target binding were captured.
Its underlying MCP response ID/tool trace was not exposed and was not replaced
with an SDK proxy. No original 90-second acceptance SLA was established.

The earlier combined conversation later displayed `rate_limit_exceeded`, with
its conversation ID matching the original capture. This establishes that one
failure's cause, not the cause of every earlier stall. A native greeting also
passed in **0.204489 seconds**, with Greeting SendActivity/CancelAllDialogs and
no Foundry binding.

That subsequent four-category browser batch used explicit classic routing
prefixes, fresh sessions, no resubmits and a 450-second observation limit.
After continuation, its deferred execution handle was unavailable. Read-only
recovery showed the second regulatory prompt only as an optimistic user activity,
without confirmed server delivery, route trace or domain reply. No completed
case results were durably recovered. Reaching case two does not certify case
one; no duplicate paid requests were sent to reconstruct missing evidence.

The [sanitized recovery receipt](../assets/runtime-2026-10-20/foundry-source-provenance-recovery.json)
records these distinct outcomes. This establishes an extractive backend
adaptation and one focused native domain success, not unrestricted narrative
synthesis, natural routing or the full connected/local/hybrid matrix. Earlier
synthesis and full-model failures remain valid historical results.

The original quick-reference file has an OLE compound header rather than a
standard DOCX ZIP container. That header alone does not prove encryption.
The normal native uploader accepted the original unmodified **163,840-byte**
file. Ingestion changed from **In progress** to **Error**; Status information
reported: "The file's content is either confidential or empty." This is an
actual ingestion failure, not proof of its precise protection/format cause.
One upload, zero reuploads; no decryption, label removal or reconstruction.
The failed source remains in the isolated unpublished draft for owner inspection
or authorized replacement. At that checkpoint, a readable source approved for
this environment was still needed. The later publisher-source recovery below
addresses that prerequisite without repairing or converting the DOCX.

Original native prompt BYOM still needs an approved compatible
environment/authentication route. PAC's delegated scope remains a separate
authorization issue. The working connection and owned resources remain live;
expiry tags do not delete them. No policy, role or consent was changed.

## Native categories recovered and licensed local knowledge ready

A later, separate browser run recovered genuine native delivery without an
external-browser action. Version 3 answered all four original notebook questions,
using explicit classic routing prefixes. Sixteen excerpts were authentic, but
the fraud reply left two bullets without their own source markers: **3/4**
displayed-content and attribution passes, not four. This does not recover the
missing results of the earlier interrupted batch.

One targeted instructions-only clarification created retrieval agent version 4:
repeat the correct canonical source marker for every bullet. Model, tools,
temperature, endpoint, authentication, smoke agent and earlier versions were
preserved. The update made no model calls. Its actual native regression passed
**4/4** questions, with **13 authentic, individually attributed excerpts** and
manual review of relevance and material conditions:

| Category | Server activity latency | Authentic attributed excerpts |
|----------|-------------------------|-------------------------------|
| Fraud | 15.718720 s | 1 |
| Regulatory | 16.774088 s | 3 |
| Investigation | 16.187563 s | 1 |
| Combined | 26.940827 s | 8 |

There were **five expertise submissions**, not four uninterrupted first-attempt
passes. The first combined submission remained optimistic, without a server
timestamp, through 17:11:09 UTC. Its capture is retained; absence of server
acknowledgement does not prove the backend never received it. One bounded
reattempt, in a fresh session after a server-acknowledged Hello, received the
combined reply. Every passing case has native user/reply IDs, BeginDialog and
target binding. The underlying native MCP response/tool IDs remain unexposed.
Matching excerpts to the original corpus is not an independent join to that
native invocation's retrieval membership. No SDK proxy fills that gap.

### Actual publisher guide ingested

The official [Microsoft workshop repository](https://github.com/Azure/Copilot-Studio-and-Azure)
provides the missing Markdown guide under an MIT license. Public source and
license reads succeeded despite the authenticated CLI token's separate SAML
error; no SSO, consent or organization policy was changed.
Revision `e9ecd00dba2c25dbc8306b5be6818d22645607a3` was pinned. Static parsing
of the publisher notebook, without executing its code, verified exact `id/title/content` matches for
all **24** original records and exact matches for all **four full test-query
objects**. The original notebook hash was independently checked.

The licensed upload preserves the guide body, moves its title to frontmatter,
and appends publisher provenance and the complete MIT notice. Three offline
verification tests pass. One normal native upload, zero reuploads, reached
**Ready**, observed at **17:31:26 UTC**. This is an upstream-source adaptation,
not a decrypted or reconstructed DOCX, and equivalence to that unreadable file
is not claimed. The original failed DOCX source remains available for inspection.

### Natural local-knowledge canary

The isolated unpublished parent now uses generative orchestration and saved
routing/source instructions. Web search, ungrounded responses and deep reasoning
remain off. A real native intake reply asked for activity, patterns, amounts and
timing, without calling Foundry, but also searched local knowledge. It does not
demonstrate the intended pure no-knowledge greeting path.

A subsequent natural CTR lookup answered the cash threshold and daily aggregation
correctly in **7.247947 seconds**. Native search tracing includes the exact
uploaded source ID; the final native reply citation identifies the uploaded
filename. No Foundry invocation was observed for these two canary questions.
This is genuine local retrieval, not an answer copied into parent instructions.
It does not replace the eleven expanded scenarios or certify hybrid coverage.

The [sanitized native recovery receipt](../assets/runtime-2026-10-20/foundry-native-category-recovery.json)
preserves the failed citation case, unacknowledged submission, successful
regression and licensed-source provenance separately. Earlier failures, the
native trace boundary, original BYOM blocker and live-resource charges remain
visible. The full workshop is not certified complete.

## Expanded scenario checks and focused intake rework

All **eleven expanded question texts** match the accessible original setup
document after whitespace normalization. A separate native QA attempt used those
questions, not the shorter canary substitutes. It stopped after **three
submissions, zero replays**, preserving these results:

| Original scenario | Actual outcome |
|-------------------|----------------|
| 1: Vague suspicious-account intake | Refusal instead of clarification; unnecessary local search |
| 2: CTR filing threshold | Genuine local retrieval and citation, but missing expected deadline and form |
| 3: SAR deadline | No server acknowledgement within the 120-second observation window |
| 4–11 | Not submitted after the delivery stop |

The [expanded QA receipt](../assets/runtime-2026-10-20/foundry-native-natural-matrix.json)
records two acknowledged final replies, compliant quota pacing and the failed
acceptance gate. The SAR observation proves unconfirmed delivery, not backend
absence or a Foundry authentication failure. Matching the accessible setup
questions does not reveal additional requirements in the unreadable main DOCX.

The initial targeted rework saves the intake topic component name and attempts
a guarded, nonfactual definition containing only a clarification message and
dialog cancellation. It extends parent instructions to request complete
retrieved table fields. Three offline tests of the intended guard cover
vague intake and prevent interception of specific financial questions. No
financial answers were embedded in the topic or instructions, and the Foundry
model, tools and corpus were unchanged.

A subsequent implementation regression used the exact original scenarios 1–3,
once each in one native conversation. All received real server-acknowledged
final replies:

| Scenario | Latency | Verified behavior |
|----------|---------|-------------------|
| Intake | 5.390803 s | Requests activity, patterns, amounts and timing; no local-search event or Foundry route marker |
| CTR | 10.748131 s | Threshold, aggregation, deadline, form and conditional exemptions; actual local source trace and citation |
| SAR | 8.945610 s | Standard/no-suspect deadlines, retention, confidentiality and form; actual local source trace and citation |

The clarification wording differs from the registered topic's exact message.
Its source-free behavior is observed, but execution of that particular topic
is not established. The
[focused rework receipt](../assets/runtime-2026-10-20/foundry-native-intake-rework.json)
preserves that distinction. No external-browser result was obtained because the
operator was unavailable; the later embedded SAR reply was genuinely received.
These three implementation checks do not certify the full eleven-scenario
natural/local/connected/hybrid matrix or the original BYOM lab.

### Fresh-session retest stopped before scoring

The independent R2 acceptance attempt then used a fresh test session and one
literal Hello transport preflight. It remained client-optimistic without server
acknowledgement or final reply for **120.161 seconds**, so the mandatory stop
occurred **before any scored question**. The startup greeting is not an
acknowledgement of that preflight.

The [R2 QA receipt](../assets/runtime-2026-10-20/foundry-native-natural-matrix-rework.json)
records **one preflight, zero target submissions, zero target replays and eleven
unassessed scenarios**. Null route/citation fields mean unassessed, not absent.
The three earlier implementation successes remain valid observations but are
not R2 passes. This interruption establishes neither a regression nor backend
absence. No configuration changes or additional paid target retries occurred
during R2.

An external-browser check was requested again, but the operator was unavailable;
there is no external validation result. That transport request is superseded by
the genuine internal recovery below, not by an assumed external success.

### Intake persistence and native delivery recovered

Later native readback exposed an empty default `OnRecognizedIntent` definition.
The earlier component-name save did not prove that guarded YAML persisted; that
claim is retracted in the historical receipt. Multiline keyboard entry had
accumulated indentation and produced explicit parse errors.

Normal line-by-line keyboard editing repaired the definition. After saving,
leaving and reopening, the native editor returned the intended 21-line
`OnActivity` definition, zero parse errors and a disabled Save button. The topic
is enabled. Its only actions send a nonfactual clarification and cancel further
dialog processing; five offline guard/readback tests preserve that boundary.
The [persistence recovery receipt](../assets/runtime-2026-10-20/foundry-native-persistence-recovery.json)
records the retraction and the genuine repair separately.

An immediate post-save Hello still received no reply. A distinct UI workflow
then recovered delivery: require a new server greeting and final startup typing,
wait ten seconds, fill the input, wait 500 milliseconds, and activate the normal
Send button with Enter. Both the real Hello preflight and the exact original
intake scenario received the registered literal response and native topic/action
traces. Execution of this particular topic is now proven for those later turns,
not retroactively for the earlier focused regression. Neither the delay nor the
Send button alone is established as the cause of recovery.

### Expanded captures require whole-parent completion

R3 submitted each of the eleven original questions once, with one real Hello
preflight per conversation. All received native responses. Six early captures
stopped on a child message's stream-final marker, however, which does not prove
that the parent turn finished. Those captures are retained, not certified as
complete acceptance results. Later captures require `DynamicPlanFinished`;
direct nonfactual intake instead has its actual topic/action trace.

Completed hybrid turns 8 and 9 include local and connected evidence. Case 10
has a local-source reference in a completed search step and a completed Foundry
step, but the final displayed message does not integrate the local table facts.
It is not evidence of absent local retrieval. Case 11 completes with Foundry
alone. The routing clarification orders hybrid cases before standalone and
quick lookups, explicitly includes named-fraud SAR narratives, and separates
SAR filing requirements from deadline-only questions. Its 3,005 characters were
read back after a full reload. No financial answers, Foundry configuration,
authentication policy or permissions were changed.

### Complete native turns recovered, acceptance still incomplete

The [complete-turn ledger](../assets/runtime-2026-10-20/foundry-native-matrix-completion-recovery.json)
now preserves matching server user/reply identifiers for **all eleven original
questions**. These are selected complete turns across named rounds, not a
single fresh eleven-case run. All expected handler combinations are observed:

| Original scenarios | Observed handler | Coverage boundary |
|--------------------|------------------|-------------------|
| 1 | Registered nonfactual intake, no search or Foundry | Exact topic/action trace |
| 2–4 | Local knowledge, no Foundry | Uploaded-filename citations and completed search steps |
| 5–7 | Connected Foundry | Native triggered and finished execution steps |
| 8–11 | Local knowledge and Foundry | Both actual routes and displayed local/source evidence |

The original example content for 1–7 is observed; the detailed examples for
8–11 remain partial or unconfirmed. Do not force unsupported legal references,
automatic SAR conclusions, priorities or account restrictions merely to imitate
an example. The unreadable main Lab 6 document may contain additional criteria.
Native MCP membership/version joins are still not independently exposed.

The audit evaluates **all displayed child and parent messages**, not only the
last message, which can contain just a source note. Across 67 fully quoted
blocks, **four are paraphrased or shortened rather than verbatim originals**;
**20 lack a correct individual canonical marker**. Grouped attribution is not
called per-block attribution. Inline quotations and paraphrases still require
semantic review. The earlier four-category success is retained, but it does
not certify these expanded responses.

Execution accounting remains explicit: R3 has 11 targets; the eight-case R4
batch reached its final case, but its deferred result expired before retrieval.
That batch count follows the recorded sequential control flow; only case 7's
individual metadata was recovered from the still-active native session, without
replay. The seven other answer bodies were not reconstructed. R5 then preserved
ten individually captured targets.

A narrowly scoped incident-completeness attempt subsequently ran two targets,
then stopped before its planned third. Its case 8 incorrectly collapsed
multiple daily deposits into one per day and invented an exact aggregate total.
The 3,340-character variant was discarded. Full-reload readback verified
restoration of the prior **3,005-character** configuration; one exact post-rollback
case 8 canary completed with both sources and without inventing a deposit count
or total. This is not a claim that the instruction alone caused the regression
or that future model behavior is guaranteed.

These rounds account for **32 target submissions**, including the eight inferred
from R4 control flow, and **21 reexecuted targets after R3**. There were no
within-round target retries. Targets are not model-invocation or billing counts;
historical initial QA and focused checks are outside these totals. Original
failures, expired captures and the rejected variant remain recorded.

Delivery and routing are recovered, **not full matrix acceptance**. Remaining
work includes complete source-backed example coverage and reliable quotation/
attribution handling. Original native prompt BYOM still requires an approved
authentication-compatible environment, and protected original documents require
an authorized readable source. No policy, role or consent change was made.
The draft remains unpublished and existing Azure resources remain billable.

## Deterministic source-verification extension

The [isolated implementation](https://github.com/devopsabcs-engineering/copilot-studio/tree/main/examples/verified-retrieval/workshop-verified-retrieval)
now verifies actual retrieval against the pinned public MIT notebook, constrains
the model to selecting retrieved record IDs, and renders whole source records
with individual source markers in code. It does not forward model-written
quotations. All **30 extension tests**, syntax checks and dependency compatibility
checks pass. Four real backend cases render **12 exact attributed records**.
Selection relevance and complete incident coverage are not thereby certified.

The [extension receipt](../assets/runtime-2026-10-20/foundry-verified-extension.json)
distinguishes backend proof from native failure. Hosted version 1 is active.
One explicit diagnostic, after a genuine intake preflight, reached its new
connected-agent action but returned **HTTP 403**:
`BotServiceRbac authorization requires a valid Entra tenant id for the activity caller.`
No hosted session was observed. A separate unchanged original case 6 still
invoked the existing specialist and displayed two source replies; no whole-plan
completion was captured, so this control is not a new complete-turn PASS.
These two additional targets are separate from the historical R3–R7 totals.

An Entra-only test on the isolated endpoint was proposed, retaining Azure RBAC.
The approval request received no human answer; **no endpoint authentication,
role or consent change was made**. The diagnostic switch showed Disabled and
Save was attempted, but subsequent independent readback failed when browser
access became unavailable. Confirm its saved Disabled state externally before
another native test. The original parent instructions and version-4 definition
were not changed.

This continuation created an isolated retrieval stage, a hosted agent and a new
Azure Bot resource, with service-generated identities recorded privately for
cleanup. These resources remain live and billable. Later local helper, dotenv
and license-packaging changes have not been redeployed. Neither the native
extension nor the full workshop is certified complete; original BYOM
compatibility and authorized access to protected originals remain unresolved.

## Official references

* [PAC installation](https://learn.microsoft.com/en-us/power-platform/developer/howto/install-cli-net-tool)
* [PAC authentication](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)
* [PAC Copilot commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot)
* [PAC Copilot Studio evaluation commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot-studio)
* [Power Platform API permission reference](https://learn.microsoft.com/en-us/power-platform/admin/programmability-permission-reference)
* [Microsoft Power Platform VS Code extension](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.powerplatform-vscode)
