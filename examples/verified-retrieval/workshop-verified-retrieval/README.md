---
title: Verified workshop retrieval extension
description: Deterministic quotation rendering after real source retrieval and constrained record selection
---

## Delivery contract

The existing prompt agent can paraphrase text inside quotation marks. This isolated
extension does not forward that draft answer. It verifies the completed MCP
retrieval against a SHA-256-pinned, publicly licensed Microsoft notebook, asks the
model to select only retrieved record IDs, and renders complete source paragraphs
and individual source markers in Python.

The selector cannot write quotations, financial amounts, headings or citations.
Unknown IDs, changed records, wrong source references, duplicate selections and
incomplete responses stop delivery. Valid absence of relevant evidence produces
an explicit abstention. Regulatory passages retain their whole recorded scope
and an applicability limitation.

Record selection is still model-based. Literal fidelity does not prove relevance,
legal correctness, incident-specific applicability or complete workshop acceptance.
This extension does not decrypt protected documents or change local-auth policy.

## Existing-resource configuration

Use your approved existing Foundry project, model deployment, Search service and
retrieval agent. The retained service folder name comes from Microsoft's Activity
sample; this owned test agent is named `workshop-verified-retrieval`.
Choose a unique name for another deployment.

1. Restore [requirements](src/echo-activity/requirements.txt) into the service's
   own virtual environment.
2. Copy [.env.example](src/echo-activity/.env.example) to an ignored `.env` and
   supply your approved identifiers. No keys or secrets are required.
3. Configure an isolated retrieval-only stage using
   [configure_stage.py](src/echo-activity/configure_stage.py). The script creates
   a new named agent or verifies an identical owned one; it refuses to replace a
   different existing agent. Record the returned version and pin it in your
   configuration.
4. For local development use an already authenticated Developer CLI session.
   Hosted deployments use their managed/workload identity, not a developer login.
5. Configure the same values in your local azd environment. The checked-in
   [manifest](azure.yaml) declares only the extension and an existing project.
   Do not provision a new project merely to run this example.

From the service directory, run:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -p 'test_*.py' -v
.\.venv\Scripts\python.exe main.py
```

The host exposes readiness and the Activity endpoint. Startup downloads only the
pinned public notebook and parses literal data assignments without executing
notebook code. A digest mismatch stops startup.

### Stateless Invocations contract

The same host now registers `POST /invocations`, using its public route API
without replacing the Activity adapter, lifecycle or readiness handlers.
`GET /invocations/docs/openapi.json` describes the input, output and explicit
error responses. The checked-in manifest enables both protocols; this code
change alone does not establish that a deployed version exposes Invocations.

Send a UTF-8 JSON object containing only `question`, a nonblank string of at
most 12,000 characters. The raw body is limited to 150,000 bytes, including
JSON escaping. The question is validated without rewriting it.

```json
{"question": "What are the SAR filing requirements and deadlines?"}
```

A successful response contains `text`, `record_ids`, `retrieval_response_id`
and nullable `selection_response_id`. The text is the same deterministic
renderer output used by Activity, never a second model paraphrase. No relevant
evidence returns the explicit abstention with an empty ID list and no selection
response. Requests share no conversation history or in-memory evidence state.

Malformed input, oversized bodies and unsupported media types return HTTP
400/413/415 before retrieval. Source verification or upstream failures return
502; bounded retrieval timeout returns 504. Error responses have an `error`
object containing `code`, `message` and a logged `reference`; they never return
partial evidence or successful-looking abstention for a failed dependency.

When hosted, invoke the canonical Foundry Invocations endpoint using Entra and
Azure RBAC. The manifest retains Entra plus BotServiceRbac for the existing
Activity route. The entry point defaults to loopback; the hosted manifest
explicitly sets `WORKSHOP_LISTEN_HOST=0.0.0.0` behind the Foundry gateway.
For local azd runs, override the injected binding with a loopback start command.
Do not expose the development listener publicly. Direct Invocations success is not native connected-agent
acceptance, and the public connector reference does not prove an action is
available in the current Copilot Studio catalog.

The workspace's [debug configuration](../../../.vscode/launch.json) runs the
service's own Python environment and actual entry point, not a workflow wrapper.
Configure the ignored local `.env` before starting it. The
[tasks](../../../.vscode/tasks.json) check ports 5679 and 8088 and expose the
Foundry Agent Inspector. Activity messages still require an Activity-compatible
client with a complete envelope; the inspector is not native Copilot evidence.
Stop only this service's task after debugging; the configuration deliberately
does not terminate unrelated workspace tasks.

### Optional evidence-only MCP transport

[mcp_server.py](src/echo-activity/mcp_server.py) adds a separate stateless
Streamable HTTP data tool at `/mcp`. It reuses the existing retrieval, membership
validation, record selection and deterministic renderer. It does not start
the Activity host or send conversational activities. The current Foundry
manifest and deployed version 5 are unchanged; they do not expose this MCP
entry point.

From the service directory, install and test the optional dependencies:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-mcp.txt
.\.venv\Scripts\python.exe -m unittest discover -s mcp_tests -p test_mcp_transport.py -v
.\.venv\Scripts\python.exe mcp_server.py
```

The default listener is `127.0.0.1:8000`. The only tool,
`retrieve_verified_workshop_evidence`, accepts `question` and returns structured
`text`, `record_ids`, `records`, `retrieval_response_id`,
nullable `selection_response_id`, `publisher_url` and `publisher_sha256`.
Every structured record is copied from the pinned corpus. Delivery rechecks
the rendered text, selected IDs and response provenance. Source failures,
upstream failures and timeouts are explicit MCP tool errors, not abstentions.
The HTTP wrapper rejects malformed UTF-8/JSON and parser resource limits with
400, and bodies above 150,000 bytes with 413, before retrieval.

Non-loopback binding is refused unless all five Entra settings are configured:

| Variable                    | Required value                                      |
|-----------------------------|-----------------------------------------------------|
| `WORKSHOP_MCP_TENANT_ID`     | Intended tenant UUID                                |
| `WORKSHOP_MCP_AUDIENCE`      | Dedicated API application's UUID audience           |
| `WORKSHOP_MCP_CLIENT_IDS`    | Comma-separated allowed OAuth client UUIDs           |
| `WORKSHOP_MCP_USER_IDS`      | Comma-separated allowed delegated user object UUIDs  |
| `WORKSHOP_MCP_RESOURCE_URL`  | Exact public HTTPS URL ending in `/mcp`              |

Set `WORKSHOP_MCP_HOST` and `WORKSHOP_MCP_PORT` only for the intended listener.
The [verifier](src/echo-activity/mcp_auth.py) validates RS256 signatures against
the fixed tenant's Microsoft keys, v2 issuer, exact API audience, expiry and
not-before time, tenant, allowed client, allowed user and delegated
`Evidence.Read` scope. It rejects application-only and wrong-audience tokens.
DNS-rebinding and Origin checks remain enabled. A reverse-proxy header or a
nonempty bearer string is not authentication.

A production connection needs a dedicated Entra API registration issuing v2
access tokens, its delegated scope, and an explicitly allowed confidential
connector client. Store that client's credential in the supported connection,
not this server's source or environment. The server's outbound Azure calls
must use an approved managed identity with narrowly scoped existing-resource
permissions, not a developer login. The
[Microsoft MCP onboarding procedure](https://learn.microsoft.com/en-us/microsoft-copilot-studio/mcp-add-existing-server-to-agent)
describes manual OAuth configuration and the generated redirect URL.
Do not choose anonymous/API-key authentication or weaken Storage policy.

The optional suite passes 17 protocol/authentication tests, alongside the
unchanged 54 service tests and dependency consistency check.
The actual tenant wizard exposes Streamable HTTP and manual OAuth; inspection
was cancelled without creating a connector. Local protocol/authentication tests
use generated fixture keys and mocked Microsoft key retrieval. They do not
prove a real Entra consent/token flow. One real local MCP request using the
unchanged original SAR question returned exactly two source records through the
existing Azure retriever, with no retry and no protected-agent definition change.
See [local evidence](../../../docs/assets/runtime-2026-10-25/mcp-evidence-local.json).
The [separate hosted preflight](../../../docs/assets/runtime-2026-10-25/mcp-hosted-preflight.json)
now verifies a Python 3.13 Linux B1 App Service, HTTPS/TLS, disabled FTP/basic
publishing, missing/invalid bearer 401 and protected-resource discovery 200.
An owned single-tenant API/client and official MCP connector are created; its
actual generated callback is registered and read back. Outbound credentials are
explicitly restricted to managed identity, initially with one existing-account
data role. The actual runtime continuation below replaces that assignment.
The allowlisted deployment package excludes environment files and credentials.
Client credential lifetime is seven days; local storage uses current-user DPAPI
and access-restricted transient PAC input is deleted after use.

The [actual app-container proof](../../../docs/assets/runtime-2026-10-25/mcp-managed-identity-runtime.json)
now verifies managed-identity retrieval with the original SAR question and two
exact records. Microsoft's token signature, tenant/identity, credential chain,
deployed source and unchanged retriever are verified; the full output matches
the pinned renderer independently. Earlier HTTP 403 failures are retained.
Only a project-scoped custom role with exact agent read/write data actions remains
after removing three owned trial assignments. That write permission also permits
agent authoring; the runtime makes no agent-authoring request. No account-wide
Foundry User/Owner, Storage or Search permission is added.

At that historical checkpoint, genuine delegated OAuth, candidate binding and
native whole-output acceptance remain unverified. The integrated VS Code browser
blocks consent popups; standard authorization in a new tab reaches the intended
administrator's password prompt. The user-response tool is unavailable, not an
approval. The bounded helper and temporary loopback callback are removed.
Use a popup-capable browser for the actual connector connection; approve only the
dedicated evidence scope for the current user unless the human explicitly
approves a different consent boundary. Do not supply passwords in chat.
The retained Sweden Central host remains billable at a published compute estimate
of USD 0.018/hour, not an actual bill or established numerical budget.
Fresh preservation verifies the original/candidate and current version-5
definition/principal/client IDs unchanged. A data-only tool does not itself
guarantee that a parent model will preserve quotations in its later synthesis.

The [subsequent native proof](../../../docs/assets/runtime-2026-10-25/mcp-native-sar.json)
records explicit human tenant-wide consent for `Evidence.Read` only, independent
`AllPrincipals`/Connected readbacks, real tool discovery and a saved candidate-only
MCP binding. The candidate's old emitting retrieval tool is disabled and its
parent instructions use the data-only MCP tool. One native unchanged SAR question
now returns one domain answer with two exact complete pinned-record quotations,
individual canonical markers and real local knowledge search/reference. All other
candidate definitions/states and the protected original are preserved; no
publication or Storage/network-policy change occurs. Missing/malformed bearer
controls still return 401. The full eleven-case matrix and raw completion-event
capture remain open; this bounded pass does not certify the roadmap.

The [next native matrix](../../../docs/assets/runtime-2026-10-25/mcp-native-matrix-initial.json)
passes cases 1-4, then stops on seven case-5 bullets lacking individual markers.
A saved Author repair passes fresh case 5, but
[the next SAR misattributes a renderer notice](../../../docs/assets/runtime-2026-10-25/mcp-native-source-boundary-failure.json).
The next repair fixes that boundary and preserves two exact complete MCP
quotations, yet [adds punctuation inside a local quotation](../../../docs/assets/runtime-2026-10-25/mcp-native-local-quote-failure.json).
Official native exports now retain actual completion events. Evidence calls are
counted and source-audited individually, separately from user submissions; no
failed question is automatically replayed. The backend, local source and exact
quotation criterion are unchanged. Every instruction change needs eleven fresh
cases; successes from different configurations cannot certify one matrix.

The [complete native eleven-case receipt](../../../docs/assets/runtime-2026-10-25/mcp-native-eleven-case-matrix.json)
now verifies every original case on one saved configuration. Twelve submissions
include one preserved pre-plan native stall and one explicitly counted retry after
exact preservation and normal reconnection. All thirteen agent-content exports
are byte-identical. Actual completion, seven MCP invocations, exact returned
records/renderer, intended local-source output and full semantic/attribution
reviews pass. Final MCP replies use unquoted cited paraphrases; twelve local
deterministic quotations remain exact. T008 closes, while T007 retains the
separate duplicate validation control: both actual identical replies and
topic-then-direct-action execution are retained. Original/candidate preservation
passes with no publication or backend/policy change. This is not roadmap sign-off.

The later [control-repair regression](../../../docs/assets/runtime-2026-10-25/mcp-native-control-repair-regression.json)
saves only the validation topic and proves one actual invocation/binding/reply
after a counted recovery. Its fresh regression accepts 10/11 original cases.
Case 9 retains a completed-evidence/plan failure without a parent answer and a
separate no-plan timeout; neither is accepted. Fifteen submissions include
thirteen original questions and two controls. Fourteen available agent exports
are identical; seven actual MCP calls include successful retrieval on the failed
answer. Case 2's lost official export is retained separately from its accepted
recovery. Current case 7 has two exact attributed MCP quotations and permitted
verified local evidence. Final full preservation passes, with no backend or
policy change, and the owned browser closes. T007/current acceptance remain open;
the preceding T008 pass is not reused across configurations.

## Testing and deployment boundaries

The current implementation passes 54 unit, orchestration, configuration and transport tests,
Python syntax checks and `pip check`. Four real backend cases render 12 literal,
individually attributed records. Cases 6 and 8 used the existing version-4
retriever; cases 9 and 11 used the isolated retrieval-only stage.

After explicit user deployment and credit authorization on October 23, the SDK
repair deployed as version 2. A real authenticated Activity call passed exact
source rendering through hosted managed identity credentials. Negative testing
then found that successful no-evidence MCP output can be just a newline.
The parser now treats blank text from a verified completed call as empty evidence;
missing/nontext output and malformed nonblank JSON remain explicit verification
failures. It never treats a failed tool call as an empty successful retrieval.

Five regression tests cover blank output, continued verification of later calls,
malformed output rejection, no-selection abstention and unchanged Activity delivery.
The exact failed retained response was replayed locally before deployment.
Version 3 was active at that checkpoint. Three real authenticated Activity requests passed:
unchanged original case 6 with two exact individually attributed records,
unchanged astronomy question with exact abstention, and oversized input with an
explicit error before model invocation. Authentication remains Entra plus
BotServiceRbac. These hosted results do not prove native delivery or the
eleven-scenario acceptance matrix.

See the [authorized release](../../../docs/assets/runtime-2026-10-23/authorized-release.json)
and [version-3 regression](../../../docs/assets/runtime-2026-10-23/hosted-version3-regression.json).
The earlier [version-2 failed negative check](../../../docs/assets/runtime-2026-10-23/hosted-negative-checks.json)
is preserved, not overwritten by the repair. Same-session managed identity
acquisition is observed; logs do not expose its exact principal or independently
join cloud retrieval membership. No source/legal completeness is inferred.

### Verified dual-protocol deployment

The [verified Invocations release](../../../docs/assets/runtime-2026-10-24/verified-invocations-delivery.json)
is now active version 5. Version 4 introduced both protocols; version 5 makes
JSON parser resource limits explicit HTTP 400 responses before retrieval.
Final real local and hosted original SAR questions both return exact two-record
renderer output and retrieval/selection response IDs.

Seven hosted controls pass: no-token HTTP 401, authenticated OpenAPI, blank-input
and JSON integer-limit HTTP 400, body-limit HTTP 413, no-evidence abstention and
unchanged Activity rendering. Correlated logs prove no model calls for the three
invalid authenticated requests. A first Activity control omitted the required
API version and returned HTTP 400; a separately guarded corrected request to
`/endpoint/protocols/activityprotocol?api-version=v1` passed HTTP 200.

The final deployment CLI timed out after registration; independent readback
found active version 5, and doctor returned 11 passed, zero failed, two skipped.
No deployment was repeated after that timeout. Identity, both authorization
schemes, original retriever and four resources/roles are preserved. Temporary
local hosts were stopped. Native acceptance and published-channel authorization
remain separate unresolved gates.

### Preserved pre-repair history

Hosted version 1 was active, but its native diagnostic failed with HTTP 403:
`BotServiceRbac authorization requires a valid Entra tenant id for the activity caller.`
No hosted session was observed. This does not validate the hosted identity's
downstream permissions or native quotation fidelity. Later local dotenv loading,
configuration-helper tests and license-packaging changes have not been redeployed.

The diagnostic attachment's saved Inactive state is now independently verified
through authenticated Dataverse reads, state metadata and a fresh UI snapshot.
This recovers the earlier failed browser readback without re-enabling the agent.
An Entra-only
endpoint test was proposed, retaining Azure RBAC, but no approval was obtained
and endpoint authentication was not changed. Do not enable anonymous access,
tenant-wide Bot Service access or keys to work around this failure.

One separate authenticated direct Activity attempt reached hosting and created
a session, but returned HTTP 500 before the application handler. Its logs identify
`ClaimsIdentity.__init__() got an unexpected keyword argument 'is_authenticated'`.
The deployed Activity bridge `1.0.0b1` is incompatible with Microsoft Agents `1.9.0`.
The local requirements now pin Activity `1.0.0b4` and Microsoft Agents `1.9.0`.
The regression reproduces the actual hosted identity boundary; two additional
ASGI tests exercise the real entry point and adapter, checking exact evidence
delivery and explicit validation-error delivery. Only corpus loading and the
Azure answer operation are stubbed. Local emulator authentication is not a
production authorization workaround.

The transport tests also establish that a complete Activity envelope needs
`serviceUrl`, even when `deliveryMode` is `expectReplies`. At that historical checkpoint, the cloud repair had
not been deployed or retested. The later hosted repair does not establish that the earlier native
403 is resolved or that downstream hosted permissions are sufficient.

See the [sanitized result](../../../docs/assets/runtime-2026-10-20/foundry-verified-extension.json).
The original workshop is not certified complete; resources remain live and billable.

Unit tests cover altered content, wrong sources, reference spoofing, actual Search
projection parameters, unsupported selections, per-bullet attribution, regulatory
context, non-execution of notebook code and refusal to replace a different stage.

A successful direct backend call is not native Copilot delivery. Validate the actual
Activity integration before replacing the working version-4 attachment. Likewise,
an HTTP readiness check is not proof of an authenticated Activity round trip.

Each answer can make two model requests: retrieval through a pinned prompt-agent
version, then constrained ID selection. Automatic SDK retries are disabled.
Neither request count nor target count is a monetary estimate.

## Source and license

The corpus is the public MIT-licensed
[Microsoft workshop notebook](https://github.com/Azure/Copilot-Studio-and-Azure/blob/e9ecd00dba2c25dbc8306b5be6818d22645607a3/labs/2.4-microsoft-foundry-agentic-retrieval/notebooks/foundry-IQ-agents.ipynb).
Its revision and digest are pinned in [evidence.py](src/echo-activity/evidence.py).
The Activity scaffold comes from
[Microsoft Foundry samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/python/hosted-agents/bring-your-own/activity/echo).
The publisher's [MIT notice](src/echo-activity/LICENSE) accompanies this adaptation. The protected
workshop files are not bundled or reconstructed.
