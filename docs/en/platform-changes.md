---
title: Platform changes and safe substitutions
description: Map the original workshop to current Copilot Studio and Foundry experiences without claiming untested equivalence.
ms.date: 2026-10-19
---

## Choose equivalence by outcome

[All labs](index.md) | [Français](../fr/platform-changes.md)

Preserve the learning objective, not the exact position of a button. Record the
old step, replacement, reason, observable acceptance result, and remaining risk.
An alternative is not validated until it produces the required result.

## The biggest navigation change

The current [harness overview](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)
distinguishes the GitHub Copilot harness, standard harness, and Copilot chat harness.
The original labs largely describe the standard harness with Topics, knowledge nodes,
and prompts. Standard agents can themselves use either classic or generative orchestration.
Those orchestration modes are not the same as the harness choice.

To find the original experience, the current
[switching guide](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences)
offers three routes:

1. On Home, open the bottom sidebar **…** menu and select **Open classic experience**.
2. Select **Other ways to build** for standard agents and agent flows.
3. Open an existing agent or workflow from **Agents** or **Workflows**.

Do not recreate a working agent solely because it is absent from a different home view.
First check the selected environment, harness, and list filters.

## Migration decision table

| Original instruction                                     | Current approach or safe substitute                                                                           | Acceptance evidence                                                                |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
| Create blank agent on the old home page                  | Open the standard experience, or document an explicitly equivalent newer-harness outcome                      | Harness recorded and required tools/knowledge available                            |
| Test pane and activity map                               | Use the selected experience's Test or Preview plus visible activity/tool execution                            | Exact input, answer, retrieval/tool result, downstream effect                      |
| Billing measured in messages                             | Check current Copilot Credits and applicable harness/channel entitlements                                     | Usable environment allocation or approved billing, not only a maker license        |
| Upload licensing guide                                   | Use current authorized unencrypted edition and wait for knowledge readiness                                   | Source edition, ready state, answer checked against the PDF                        |
| Every Search lab can use Free                            | Verify required Search feature/tier/region before provisioning                                                | Indexing, retrieval, and selected features work in the approved SKU                |
| Copy an admin key into instructions                      | Use a supported secure connection and least privilege; do not expose keys in prompts or screenshots           | Successful authorized call without leaked credentials                              |
| Old Import data wizard                                   | Use the supported current import/vectorization workflow, keeping chunking and embedding dimensions consistent | Successful indexer and nonempty, relevant chunk results                            |
| Instrumentation key or connection string interchangeably | Use the supported Application Insights configuration, preferring the current connection-string field          | Correlated telemetry appears in the correct resource                               |
| Deploy a specifically named model                        | Choose a currently supported, available model accepted by the integration                                     | Deployment identifier, successful direct test, then successful integrated test     |
| BYOM replaces the entire agent model                     | Treat BYOM as a connected prompt/model call in the described lab                                              | Activity proves prompt call and output, without claiming orchestration replacement |
| Agent name equals any Agent ID                           | Distinguish classic agent identifiers, project endpoints, and versioned Foundry agents                        | Direct Foundry call and supported connector agree on the same agent                |
| Remove a working source immediately                      | Copy/export the agent first; remove or disable the old source only to isolate the new path                    | Original can be restored and the tested retrieval path is unambiguous              |

Detailed Search, telemetry, BYOM, and agentic-retrieval caveats are in their lab guides.
The table is a migration plan, not proof that every substitute ran successfully.

## Source inconsistencies that affect the sequence

The filename **Lab 3_Monitor Copilot Studio agents with Application-Insights.docx**
contains an internal heading calling it Lab 4. The filename
**Lab 4_BYOM to Copilot Studio.docx** contains an internal heading calling it Lab 3.
Use filenames as the stable identifiers for evidence and discussion.

The deployment supplement is numbered 5.1 but must precede Lab 5 when resources are
not already deployed. The Lab 6 supporting setup guide is separate from its main
Word document and notebook; review all of them before treating the package as complete.

## Document each substitution

Keep the following fields in your private run record:

```text
Lab and test ID:
Original source edition and step:
Selected environment, harness, model, and API version:
Replacement step and official reference:
Why the original step was unavailable:
Expected observable result:
Observed result and timestamp:
Redacted evidence file:
Status: passed / failed / blocked / not run
Cleanup and remaining limitations:
```

If no supported replacement preserves the objective, stop at **blocked**.
A manual answer, mock screenshot, or unrelated deployment cannot substitute for
successful retrieval, telemetry, or a connected-agent invocation.

## References reviewed

* [Harnesses in Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)
* [Access standard harness agents and agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences)
* [Generative versus classic orchestration](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions)
* [Current licensing and credits](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)
* [Supported file knowledge](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
