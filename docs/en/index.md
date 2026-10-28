---
title: Workshop guide in English
description: Lab sequence, prerequisites, shared screenshots, and evidence-based validation for the Agent Factory workshop.
ms.date: 2026-10-28
---

## Start here

[Français](../fr/index.md) | [Repository home](../../README.md)

Start with the [completion roadmap](completion-roadmap.md) and
[validation ledger](validation.md) for current acceptance and remaining gates.
All eight bilingual lab guides are delivered and all eight lab units have execution
evidence; the workshop runtime is **not complete**. The
[actual rerun record](live-rerun-2026-10-19.md) preserves earlier runs; the
[backend continuation](backend-live-2026-10-20.md) records later native tests.
Historical cleanup does not prove that currently retained resources are deleted.

The separate F6 matrix is 8 PASS, 2 PARTIAL, 0 FAIL and 2 NOT_RUN. F6-09 passes
under an explicit language override, not native picker repair or automatic detection.
The latest [French static wrappers](../assets/runtime-2026-10-26/lab6-french-static-wrappers.json)
pass two scoped static checks, not full localization or live retrieval.
The original eleven-scenario matrix remains 10/11: case 9 failed twice, without
a third replay. These matrices must not be merged.

Use these guides alongside your authorized local workshop material. Do not treat a
successful documentation check as a successful cloud deployment. The last review
date for these summaries is 2026-10-28; each tenant can expose different previews
and regional capabilities. No new runtime run is implied by a documentation update.

## Lab sequence

| Lab | Guide                                                               | Evidence level                            |
| --- | ------------------------------------------------------------------- | ----------------------------------------- |
| 0   | [Prerequisites, licensing, environment, and permissions](lab-00.md) | Preflight and backend access; standard runtime incomplete |
| 1   | [Licensing advisor, knowledge, and email tools](lab-01.md)          | Core live path passed; cloned PDF hash matched; citation audit incomplete |
| 2   | [Azure AI Search as knowledge](lab-02.md)                           | Licensing-only index and connected answer checks passed; external PDF navigation/current-source proof open |
| 3   | [Application Insights monitoring](lab-03.md)                        | Native agent event/KQL correlation and cleanup passed; published-channel/privacy gates open |
| 4   | [Bring your own model with a prompt](lab-04.md)                     | Direct paid model call passed; connected prompt incomplete |
| 5.1 | [Deploy the advanced-search infrastructure](lab-05-1.md)            | Corrected paid deployment and verified cleanup completed |
| 5   | [Advanced querying with Azure AI Search](lab-05.md)                 | Real retrieval checks passed; connected Copilot answer incomplete |
| 6   | [Foundry IQ and agentic retrieval](lab-06.md)                       | Hosted/native scoped passes; F6 8 PASS/2 PARTIAL/2 NOT_RUN; original case 9 still failed |

Run 5.1 before 5 if the advanced-search resources do not already exist. Lab 4
depends on the Search index from Lab 2. The supplied monitoring document has an
internal title that calls it Lab 4, and the BYOM document calls itself Lab 3.
These guides follow the source filenames: monitoring is Lab 3 and BYOM is Lab 4.

## What changed since the original instructions

The current Copilot Studio documentation distinguishes several agent harnesses.
The original workshop's Topics, knowledge nodes, and prompt tools refer to the
standard harness. A new agent in the newer experience is not automatically an
equivalent replacement. Read [platform changes](platform-changes.md) first.

In particular:

* Standard-harness generative orchestration and the GitHub Copilot harness are different concepts.
* Current licensing uses Copilot Credits, not the original message terminology.
* A successful maker license assignment does not prove environment capacity or model quota.
* Azure AI Search feature availability depends on tier, region, model, identity, and index schema.
* File knowledge does not support encrypted or password-protected files.
* BYOM prompt integration does not replace the agent's orchestration model.

## Evidence and operation

* [Validation ledger and acceptance gates](validation.md)
* [Completion roadmap and per-lab resume tasks](completion-roadmap.md)
* [English wiki](https://github.com/devopsabcs-engineering/copilot-studio/wiki/EN-index) and [French wiki](https://github.com/devopsabcs-engineering/copilot-studio/wiki/FR-index)
* [Screenshot provenance and evidence gallery](evidence.md)
* [Troubleshooting, safe substitutions, and cleanup](troubleshooting.md)
* [Publication and repeatable wiki export](../publishing.md)

For each lab, start a fresh test conversation, record the exact input and output,
capture the visible activity/tool result, and retain the relevant downstream evidence.
Do not send email to a third party or create cloud resources without the lab owner's
approval. These guides use a controlled test mailbox and a dedicated resource group.
