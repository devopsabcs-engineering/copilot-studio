---
title: Screenshot provenance and execution evidence
description: Distinguish the user's successful Lab 1 run from historical teaching figures and future validation captures.
ms.date: 2026-10-20
---

## Evidence classes

[All labs](index.md) | [Français](../fr/evidence.md) | [Validation ledger](validation.md)

The same image files are shared between English and French. Each lab supplies captions
and explanations in its own language. The screenshot inventory is recorded in the
[machine-readable provenance manifest](../assets/manifest.json).

| Class           | Meaning                                                               | Can establish a new pass                               |
| --------------- | --------------------------------------------------------------------- | ------------------------------------------------------ |
| User evidence   | Cropped copies of the two attachments supplied with the request       | Supports the observed Lab 1 run, within visible limits |
| Source figure   | Screenshot embedded in the original, readable workshop documents      | No; illustrates the earlier procedure                  |
| Live validation | A new capture with run ID, timestamp, test input, and observed result | Only for the specific test shown                       |
| Diagram         | Original explanatory drawing, not a portal capture                    | No                                                     |

No historical figure has been relabeled as a new successful execution. Where a protected
source has no publishable figure, the guide uses original text or a labeled diagram,
not an invented screenshot.

## Lab 1 proof chain

The request and the agent/tool result come from the first attachment. The received
email comes from the second attachment. Together they support the user's report that
the agent sent a licensing summary and that the corresponding message arrived.

![User request from the first attachment](../assets/lab-01/evidence-request.png)

The user asks for an email about Power Apps licensing. This is the input, not the result.

![Send tool and success response from the first attachment](../assets/lab-01/evidence-agent-result.png)

The visible send-tool activity and response support an attempted/completed send.
The recipient address is redacted. This alone would not establish mailbox delivery.

![Received message from the second attachment](../assets/lab-01/evidence-email-received.png)

The matching subject and body in Outlook establish the downstream outcome visible
in the provided screenshot. The message header shows 2026-10-19 at 1:19 PM in the
displayed mailbox; its time zone and transport headers were not independently examined.

These images do not prove every directory lookup, exact guide version, permission
setting, citation, absence of duplicates, or production reliability. License names
visible in the email remain historical output, not a current entitlement guarantee.

## Historical figure map

| Guide              | Figure count                            | Original document                                                  | Purpose                                                            |
| ------------------ | --------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| [Lab 1](lab-01.md) | 10 source figures plus 3 evidence crops | Lab 1_Create an agent in Copilot Studio.docx                       | Agent, file knowledge, directory search, email setup               |
| [Lab 2](lab-02.md) | 4 source figures                        | Lab 2_Use Azure AI Search in Copilot Studio.docx                   | Storage, container, import wizard, knowledge selector              |
| [Lab 3](lab-03.md) | 4 source figures                        | Lab 3_Monitor Copilot Studio agents with Application-Insights.docx | Resource selection, telemetry settings, custom event, flow diagram |
| [Lab 4](lab-04.md) | 4 source figures                        | Lab 4_BYOM to Copilot Studio.docx                                  | Prompts, inputs, parsing, topic completion                         |
| [Lab 6](lab-06.md) | 4 source figures                        | Lab 6 supporting COPILOT_STUDIO_SETUP.docx                         | Environment, agent details, external agent, connection state       |

The initial publication includes 29 PNG figures: 26 source figures and 3 user-evidence
crops. Source IDs in the manifest map as follows: 01 to Lab 1, 02 to Lab 2, 03 to
monitoring, 04 to BYOM, and 08 to the Lab 6 supporting setup guide.
Additional live evidence, if captured, is listed individually in the manifest.

## Approved evaluation submission

![One submitted evaluation queued for capacity, with account details masked](../assets/runtime-2026-10-20/evaluation-queued.png)

After explicit credit approval, one evaluation containing three read-only cases
was saved and submitted on October 20. This screenshot records the actual queued
notification and one total run. It does not show completed answers or grades.
Account/navigation details are masked; an oversized privacy mask also covers
part of the capacity sentence. No obscured text was reconstructed.
See the [backend continuation](backend-live-2026-10-20.md) for the latest result.

## Privacy and preservation

The two original attachments remain unchanged in their read-only attachment locations.
Published derivatives crop out browser addresses, unrelated tabs, inbox messages,
and unnecessary chrome. Selected tenant/resource/account metadata is masked in
source figures. Every derivative has a bilingual provenance footer.

No protected Word document, raw mailbox export, connection secret, Azure key,
Terraform state, or notebook output containing credentials is included.
The repository is private; changing its visibility requires a separate publication review.

## Capture protocol for the remaining tests

1. Assign a run ID and a test ID before executing the step.
2. Capture the exact input, visible tool/retrieval result, and outcome. For email,
   retain downstream receipt; for telemetry, retain the matching query row.
3. Record the source guide edition, environment, harness, model, and API version
   in a private run record.
4. Crop to the relevant application area. Mask names, tenant IDs, keys, endpoints,
   unrelated messages, and any sensitive prompt/response data.
5. Add provenance to the manifest and the same image link to both language guides.
6. Update the validation ledger with the test actually completed, not the whole
   lab unless every required acceptance condition passed.
