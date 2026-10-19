---
title: Workshop guide in English
description: Lab sequence, prerequisites, shared screenshots, and evidence-based validation for the Agent Factory workshop.
ms.date: 2026-10-19
---

## Start here

[Français](../fr/index.md) | [Repository home](../../README.md)

Use these guides alongside your authorized local workshop material. Do not treat a
successful documentation check as a successful cloud deployment. The last review
date is 2026-10-19; each tenant can expose different previews and regional capabilities.

## Lab sequence

| Lab | Guide                                                               | Evidence level                            |
| --- | ------------------------------------------------------------------- | ----------------------------------------- |
| 0   | [Prerequisites, licensing, environment, and permissions](lab-00.md) | Partial read-only preflight               |
| 1   | [Licensing advisor, knowledge, and email tools](lab-01.md)          | User-provided execution evidence          |
| 2   | [Azure AI Search as knowledge](lab-02.md)                           | Procedure review; live run blocked        |
| 3   | [Application Insights monitoring](lab-03.md)                        | Procedure review; live run blocked        |
| 4   | [Bring your own model with a prompt](lab-04.md)                     | Procedure review; live run blocked        |
| 5.1 | [Deploy the advanced-search infrastructure](lab-05-1.md)            | Static review; deployment not run         |
| 5   | [Advanced querying with Azure AI Search](lab-05.md)                 | Static/procedure review; live run blocked |
| 6   | [Foundry IQ and agentic retrieval](lab-06.md)                       | Static/procedure review; live run blocked |

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
* [Screenshot provenance and evidence gallery](evidence.md)
* [Troubleshooting, safe substitutions, and cleanup](troubleshooting.md)
* [Publication and repeatable wiki export](../publishing.md)

For each lab, start a fresh test conversation, record the exact input and output,
capture the visible activity/tool result, and retain the relevant downstream evidence.
Do not send email to a third party or create cloud resources without the lab owner's
approval. These guides use a controlled test mailbox and a dedicated resource group.
