---
title: Lab 1 - Build and verify a licensing advisor
description: Illustrated setup for file-grounded answers and email tools, with the user's successful send and received-email evidence.
ms.date: 2026-10-19
---

## Goal, prerequisites, and evidence

[All labs](index.md) | [Français](../fr/lab-01.md) | [Prerequisites](lab-00.md) | [Next: Search](lab-02.md)

Create a Power Platform licensing advisor, ground its responses in an approved
licensing guide, and send a summary to a controlled test mailbox. The original
workshop estimates 45 minutes; allow more time for licensing, consent, and indexing.

You need a permitted maker environment, file knowledge, Office 365 Users and Outlook
connections, a supported licensing PDF, and a mailbox you own or are authorized to use.

Status: the user supplied two screenshots of a successful run. The first shows a
send-email tool result and the agent's success message; the second shows the received
message. This supports the requested end-to-end email outcome for that run.
It does not prove every original configuration step, citation accuracy, or a new run
performed by this assistant.

## 1. Choose the equivalent agent experience

1. Open [Copilot Studio](https://copilotstudio.microsoft.com/) and select the intended environment.
2. To follow the original Topics/Knowledge/Tools workflow, open the standard-agent
   experience. If the new home page looks different, use
   [Access standard agents and agent flows](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences).
3. Create a blank agent only if the lab environment permits it. Name it
   **Power Platform Licensing Advisor**, and describe its scope as explaining
   licensing from approved Microsoft documentation.
4. Record the harness, model, and orchestration mode actually selected. Keep a
   supported default model unless the exercise explicitly needs another.
5. If you reproduce the outcome with a newer harness, label it an equivalent
   outcome, not a byte-for-byte reproduction of the original UI.

![Original blank-agent entry point](../assets/lab-01/image2.png)

Original workshop screenshot, with privacy masking. It is navigation guidance,
not evidence that this assistant created an agent.

![Original agent details configuration](../assets/lab-01/image3.png)

Original workshop screenshot: the name and description communicate the intended scope.

## 2. Define a grounded, bounded behavior

In the agent's instructions, describe the following behavior in your own wording:

* Answer Power Platform licensing questions from the approved guide and cite the source.
* State the guide's edition; do not call an old PDF the latest policy.
* Explain uncertainty and refer purchasing or compliance decisions to the licensing owner.
* Do not invent pricing, plan entitlements, availability, or contractual advice.
* Resolve the recipient before sending mail; ask for clarification if several directory users match.
* Send only to an approved test mailbox after the recipient and subject are confirmed.
* Report a mail success only after the send tool returns success.

The original sample's per-user/per-app comparison is not a permanent licensing rule.
Validate all plan names and rights against the actual guide edition. Do not turn the
license list visible in the supplied email into an authoritative 2026 licensing table.

## 3. Add the licensing PDF and wait for readiness

1. Download the [official licensing guide](https://go.microsoft.com/fwlink/?LinkId=2085130)
   and record its edition, source URL, and download date.
2. Open **Knowledge > Add knowledge**. Upload the approved, unencrypted PDF.
3. Give it a meaningful description, for example a description that identifies the
   guide edition and says it is the source for Power Platform licensing questions.
4. Wait until the source is usable, such as **Ready** in the standard experience.
   A completed upload is not the same as a completed index.
5. Save the configuration. If ingestion fails, check Dataverse search, storage
   capacity, supported format, file size, and encryption before retrying.

![Original Add knowledge file-upload interface](../assets/lab-01/image5.png)

Original workshop screenshot: select or drop the file rather than adding an unrelated website.

![Original knowledge description and Save action](../assets/lab-01/image7.png)

Original workshop screenshot, with author metadata masked. The January 2026 filename
is historical; use the edition approved for your run.

Follow the current [file-upload guidance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload).
It explicitly excludes encrypted or password-protected files.

## 4. Isolate the knowledge test

1. For a strict grounding exercise, disable general knowledge and web information
   where those switches are available in the selected standard experience.
2. Do not assume those switches replace all instructions and tool controls in every harness.
3. Start a fresh conversation in **Test your agent** or **Preview**.
4. Ask: `What Power Apps licensing options are described in the uploaded guide? Cite the guide.`
5. Inspect the activity or tool view. Verify retrieval from the intended source,
   then compare the answer with the relevant page in the PDF.
6. Ask a question that the PDF cannot answer, such as an unpublished discount for
   your tenant. The agent should explain that the source does not establish it.

![Original general-knowledge and web-information switches](../assets/lab-01/image9.png)

Original workshop screenshot. Labels and availability depend on the agent experience.

The current [generative-orchestration documentation](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions)
explains how the standard harness selects knowledge and tools. Activity views are
useful for visible execution evidence, not a substitute for checking the answer.

## 5. Add directory lookup and email tools

1. Open **Tools > Add a tool**. In newer layouts, expand the connector choices if needed.
2. Select **Office 365 Users > Search for users (V2)**. Create or select the approved connection.
3. Describe the tool as resolving a user's directory profile and email address.
4. Expose **Search term** as an input. Test that your intended recipient can be
   resolved uniquely. Do not accept the first result when the name is ambiguous.
5. Add **Office 365 Outlook > Send an email (V2)** using an approved mailbox connection.
6. Configure the recipient, subject, and body inputs according to the UI.
   For this lab, prefer a fixed approved test recipient or explicit confirmation.
7. If the body is HTML, ensure the connector accepts the intended format.
   Keep the completion response consistent with the actual tool result.
8. Save and review the connection identities. The identity that owns the connection
   matters; do not assume mail is sent as the person currently chatting.

![Original Tools page and Add a tool entry point](../assets/lab-01/image13.png)

Original workshop screenshot.

![Original directory-search connector selection](../assets/lab-01/image14.png)

Original workshop screenshot: select the Microsoft Office 365 Users connector.

![Original Search term input](../assets/lab-01/image17.png)

Original workshop screenshot: the name or search string is an input, not an inferred email address.

![Original Outlook send-email connector selection](../assets/lab-01/image18.png)

Original workshop screenshot: this is an action with a real external side effect.

![Original email inputs and completion response](../assets/lab-01/image19.png)

Original workshop screenshot. Dynamically generated recipients require safeguards;
the screenshot is not a recommendation to send to arbitrary addresses.

Current reference: [Add tools to custom agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-tools-custom-agent).
If policy blocks the connector, obtain an administrator-approved configuration.
Do not substitute a personal Outlook connection or bypass data policies.

## 6. Execute one controlled send

1. Start a new conversation so that earlier recipient choices do not leak into this test.
2. Ask for a summary to be sent to your approved test user. Specify the mailbox
   explicitly if the display name is not unique.
3. Confirm the recipient and subject before the tool runs. If a connector requests
   consent, review its identity and scope before selecting **Connect**.
4. Observe the send tool's completion. If it fails, retain the error and do not
   accept a success-shaped natural-language response.
5. Check **Sent Items**, then the recipient's inbox. Match the subject and content
   to the test, and record timestamps. An agent saying "sent" is not delivery proof.
6. Do not repeat the send automatically if delivery is delayed; check for duplicates first.

The provided run used the request below. The original typo and exact wording are
retained in the image as evidence, not as an instruction to use that particular user.

![User-supplied request to send a licensing summary](../assets/lab-01/evidence-request.png)

User-supplied execution evidence, cropped from the first attachment.

![User-supplied send-tool result and licensing summary](../assets/lab-01/evidence-agent-result.png)

User-supplied execution evidence. The recipient is redacted. The visible success
message alone would not prove receipt.

![User-supplied received Outlook message](../assets/lab-01/evidence-email-received.png)

User-supplied execution evidence. The received message has the subject
**Power Apps License Types Overview** and a matching licensing summary.
Unrelated inbox content and browser chrome have been excluded.

## Acceptance tests and interpretation

| ID    | Test                                      | Required result                                           | Observed evidence                                                                     |
| ----- | ----------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| L1-01 | Ask a supported licensing question        | Source-grounded answer consistent with the approved guide | User screenshot shows a summary and source mention; full accuracy audit not performed |
| L1-02 | Ask an unsupported pricing question       | No invented tenant-specific price                         | Not executed                                                                          |
| L1-03 | Resolve a unique controlled recipient     | Verified intended mailbox, no guessing                    | Final recipient visible in original; lookup execution not proven by the crops         |
| L1-04 | Ask to send one summary                   | Send tool completes successfully                          | Send tool and success response shown                                                  |
| L1-05 | Verify downstream delivery                | Matching message in the controlled inbox                  | Received-email screenshot provided                                                    |
| L1-06 | Use an ambiguous name                     | Clarification before sending                              | Not executed                                                                          |
| L1-07 | Block or fail a connection in a safe test | Clear failure; no false success and no duplicate email    | Not executed                                                                          |

## Troubleshooting and cleanup

If the file is unavailable, wait for indexing and check the supported-file requirements.
If the answer cites the web despite your test setup, inspect the actual harness,
enabled sources, and selected tools rather than repeatedly rewriting the question.
If a user is not found, verify directory permissions and use an unambiguous test identity.
If mail is absent, compare the connection mailbox, Sent Items, recipient, spam folder,
and any administrator message-trace evidence. Do not claim a missing message was delivered.

Keep the agent for Lab 2. Retain a copy or export before changing its knowledge.
After the workshop, remove only the test messages and connections you own and no
longer need. Keep the redacted evidence and test record; never commit mailbox tokens,
connection credentials, or raw inbox screenshots.
