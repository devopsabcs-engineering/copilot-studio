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

## Official references

* [PAC installation](https://learn.microsoft.com/en-us/power-platform/developer/howto/install-cli-net-tool)
* [PAC authentication](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)
* [PAC Copilot commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot)
* [PAC Copilot Studio evaluation commands](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot-studio)
* [Power Platform API permission reference](https://learn.microsoft.com/en-us/power-platform/admin/programmability-permission-reference)
* [Microsoft Power Platform VS Code extension](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.powerplatform-vscode)
