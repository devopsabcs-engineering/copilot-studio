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

## Testing and deployment boundaries

The current implementation passes 33 unit, orchestration, configuration and transport tests,
Python syntax checks and `pip check`. Four real backend cases render 12 literal,
individually attributed records. Cases 6 and 8 used the existing version-4
retriever; cases 9 and 11 used the isolated retrieval-only stage.

Hosted version 1 is active, but its native diagnostic failed with HTTP 403:
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
`serviceUrl`, even when `deliveryMode` is `expectReplies`. The cloud repair has
not been deployed or retested. It does not establish that the earlier native
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
