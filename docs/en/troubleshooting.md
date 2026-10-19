---
title: Troubleshooting and safe recovery
description: Diagnose environment, knowledge, connector, retrieval, model, and telemetry failures without bypassing safeguards.
ms.date: 2026-10-19
---

## Start with the failing boundary

[All labs](index.md) | [Français](../fr/troubleshooting.md)

Record the lab/test ID, exact error, timestamp, environment, harness, and last successful
boundary. Avoid retrying an entire lab when a direct component test can isolate the issue.
Do not include credentials or raw customer conversations in a support ticket or screenshot.

## Environment and licensing

| Symptom                                   | Check                                                           | Safe action                                                                           |
| ----------------------------------------- | --------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Agent missing from Home                   | Environment, account, harness, filters                          | Open Agents or the standard experience before recreating anything                     |
| No Copilot Credits                        | Environment allocation, entitlement, billing policy             | Ask the administrator to verify capacity; do not assume provisioning is still running |
| Prompt or connector unavailable           | Effective data policies, environment settings, selected harness | Use an approved configuration; do not bypass policy with another account              |
| Existing agent works but new one does not | Different harness, model, instructions, or connection identity  | Compare recorded configuration instead of changing unrelated settings                 |
| Azure portal works but data call fails    | Control-plane role versus data-plane role                       | Grant only the required data permission through an authorized role administrator      |

See [Lab 0](lab-00.md) and [platform changes](platform-changes.md).

## Knowledge and email

If a file stays unavailable, check Dataverse search, file capacity, format, size, and
encryption. A protected Word file that opens for you is not automatically an uploadable
knowledge source. Never strip protection to make ingestion work.

If answers are ungrounded, start a new conversation, check the active source edition,
disable unrelated sources for the controlled test, and inspect visible retrieval.
An answer that sounds correct is not proof of source use.

If an email is missing:

1. Check the connection's actual sending mailbox.
2. Inspect the send tool's result, not only the agent's text.
3. Check Sent Items and the exact intended recipient.
4. Check the recipient's inbox and junk folder, then authorized message tracing if needed.
5. Check for duplicates before retrying. Do not send repeatedly to test delivery.

## Search and vectorization

Test in order: authorized blob access, model inference, indexer execution, direct Search
query, then Copilot Studio. For a failed indexer, inspect the per-document error and the
identity used by Search. The maker's ability to download a blob does not prove the
Search service can read it.

For empty vector results, compare:

* Embedding model and deployed model name
* Vector dimension in the index and the embedding output
* Searchable/retrievable fields and the connector's selected fields
* Semantic configuration, query type, filter expression, and selected index
* Model/endpoint availability and supported API version

A connector expecting `chunk` cannot use a `content` field by wishful mapping.
Inspect the actual output before defining a Parse value schema. Preserve source titles
and citation metadata; do not silently concatenate empty results.

## Application Insights

Verify the intended resource, supported connection-string configuration, enabled
logging, UTC time range, and the actual event/table schema. Allow ingestion time.
Do not assume an empty Live Metrics view proves that custom-event ingestion failed.
Query the relevant logs and correlate the lab event marker.

Use a deliberately emitted lab event. A query for an event name that was never emitted
cannot establish a telemetry failure. Keep sensitive activity logging off unless an
approved test specifically requires it.

## BYOM and Foundry IQ

Verify a model or Foundry agent directly before testing the Copilot integration.
Record deployment names separately from base-model names, and classic agent IDs
separately from newer agent names/versions. Check tenant identity, permissions, endpoint
format, connector support, preview API version, and actual dependency versions.

For Lab 6, inspect the notebook's local data references before running cloud cells.
If required source data or a referenced configuration file is missing, record **blocked**
instead of substituting a generic answer and calling the lab complete.

## Capture a useful failure report

```text
Lab/test ID:
Expected outcome:
Observed error and UTC timestamp:
Last successful direct component test:
Environment/harness/model/API version (private record):
Redacted screenshot or structured error:
Impact and stop condition:
Smallest next authorized action:
```

## Cleanup without collateral damage

Disconnect unused lab connections, restore the original agent configuration when
appropriate, and remove only the dedicated objects you created for the workshop.
Inspect a resource group's contents and dependencies before approving deletion.
Do not delete shared Foundry, Search, Storage, Log Analytics, or networking resources.
Retain sanitized evidence and the acceptance ledger after cleanup.
