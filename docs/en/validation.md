---
title: Workshop validation ledger
description: Evidence, completed checks, runtime limitations, and the acceptance criteria still required for each workshop lab.
ms.date: 2026-10-19
---

## Overall verdict

[All labs](index.md) | [Français](../fr/validation.md) | [Evidence gallery](evidence.md)

Documentation review and publication are separate from live lab validation.
The workshop is **not certified as fully rerun**. Lab 1 has user-provided evidence
of its email outcome. The remaining labs have source/documentation/static checks and
explicit acceptance procedures, but do not have a demonstrated complete cloud pass.

The browser initially reached an authentication barrier. The user then signed in
and initialized the GitHub wiki. That removed the publication barrier; it did not
automatically create Search, telemetry, models, indexes, knowledge bases, or connectors.

## Status definitions

| Status                 | Meaning                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------- |
| Observed user run      | The provided evidence shows a specific outcome; not a new assistant rerun             |
| Read-only check passed | A tool directly observed a narrow prerequisite or repository condition                |
| Procedure reviewed     | The source workflow was compared with official guidance; execution is still needed    |
| Static check           | A local file or code property was inspected without executing its cloud operations    |
| Blocked                | A prerequisite, permission, environment, or supported integration prevents completion |
| Not run                | No execution result is available                                                      |

An unavailable or untested step remains blocked/not run. A screenshot from a Word
document, a generated diagram, or a plausible agent answer cannot upgrade that status.

## Per-lab acceptance ledger

| Lab                | Current result                                                                      | Required evidence before a full pass                                                                            |
| ------------------ | ----------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| [0](lab-00.md)     | Partial read-only preflight; complete environment readiness not established         | Environment, entitlement/capacity, policy, data permissions, quota, Terraform, and budget verified              |
| [1](lab-01.md)     | Observed user run: send tool and received message; not every negative test executed | New controlled run with grounded answer, recipient resolution, send result, receipt, and negative tests         |
| [2](lab-02.md)     | Procedure reviewed; no demonstrated complete retrieval run                          | Successful indexer, nonempty relevant Search results, connected Copilot answer with expected sources            |
| [3](lab-03.md)     | Procedure reviewed; no demonstrated telemetry ingestion                             | Deliberate event correlated to a recent lab interaction and visible in the intended log query                   |
| [4](lab-04.md)     | Procedure reviewed; no demonstrated connected-model run                             | Direct model test, parsed retrieval, prompt invocation, grounded answer, explicit empty/error behavior          |
| [5.1](lab-05-1.md) | Static deployment review; no apply performed                                        | Compatible providers, reviewed plan, approved apply, expected resources and private configuration               |
| [5](lab-05.md)     | Source/static review; advanced query results not observed                           | Supplied corpus indexed, required queries executed, expected fields/ranking/filter behavior recorded            |
| [6](lab-06.md)     | Source/static review; end-to-end connected-agent run not observed                   | Complete data/configuration, supported SDK/API, direct retrieval, Foundry agent and Copilot connection verified |

## Checks performed in this session

| Check                                    | Observed result                                                                                    | Scope limitation                                                                              |
| ---------------------------------------- | -------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------- |
| Source inventory                         | Labs 0–6 and supplement 5.1 found, plus supporting files                                           | Does not prove the runtime package is complete                                                |
| Word source access                       | Readable ZIP-based documents extracted locally; compound-format files read through installed Word  | Protected source documents are not republished                                                |
| Lab numbering                            | Monitoring/BYOM internal titles contradict their filenames                                         | Guides consistently follow filenames                                                          |
| Azure CLI                                | Installed version 2.91.0; selected account query succeeded                                         | No claim about every subscription or tenant                                                   |
| Provider registration                    | Search, Cognitive Services, Insights observed Registered                                           | Registration does not prove role rights, capacity, network access, or deployment success      |
| Selected-subscription resource inventory | Cognitive Services resources present; no Search service or Application Insights component returned | Scoped to the selected subscription and current identity                                      |
| Terraform executable                     | Not found on PATH                                                                                  | No terraform init, validate, plan, or apply claimed                                           |
| Copilot browser                          | Sign-in succeeded and Home was visible; agent navigation then returned a persistent blank page     | Licensing advisor could not be opened; no new knowledge question was submitted                |
| GitHub publication access                | Private repository created; wiki enabled and initialized by the owner                              | Repository and wiki require separate commits and remote verification                          |
| Lab 1 attachments                        | Send-tool/result crop and matching received-email crop preserved                                   | No independent transport-header or licensing-content audit                                    |
| Current product guidance                 | Official Microsoft Learn references checked for the documented substitutions                       | Documentation checks are not runtime tests                                                    |
| Lab 6 notebook                           | 11 of 11 code cells syntax-valid; 24 inline records identified                                     | Syntax and data presence do not prove API, inference, retrieval, or integration compatibility |
| Advanced-lab examples                    | Four JSON examples checked; SVG diagrams parsed; acceptance IDs aligned between languages          | Examples and diagrams do not prove cloud behavior                                             |

The advanced-lab review also identified Terraform identity/network gaps, disabled
Foundry provisioning, embedding-dimension consistency requirements, API/SDK drift,
and destructive reset behavior that must be resolved or consciously gated before a
live run. Consult the detailed findings in Labs 5.1, 5, and 6 rather than applying the
original package unchanged.

### Advanced-package findings that need action

1. The supplied Terraform configuration disables the Foundry module, so the
   advertised Foundry project is not provisioned by that path.
2. The Search module does not apply the supplied allowed-IP/Entra options as expected,
   and the required service identity is not attached. Review effective resources and
   role assignments before treating the configuration as an identity/network baseline.
3. The deployment supplement uses 1,536-dimensional embeddings while Lab 6 expects
   3,072. These are different configuration expectations, not interchangeable indexes.
   Align the model output, index field, and query embedding for the selected lab.
4. Preview SDK, ARM, and MCP contracts require compatibility reconciliation. The
   connected-agent route requires the supported Activity/new-portal agent contract.
5. Notebook reset code deletes fixed-name objects; the final cleanup is commented
   out. Do not run reset cells against a shared project.

The notebook also references a quick-reference Markdown file that is absent.
The package supplies `data\quick_reference_guide.docx` instead. Renaming an extension
does not convert a document; obtain an authorized source in the expected format.

## Documentation and tooling gates

The offline gates are reproducible using:

```powershell
python -m py_compile scripts\build_wiki.py scripts\validate_docs.py scripts\test_docs.py
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts\build_wiki.py --output .wiki-build
python scripts\validate_docs.py --wiki .wiki-build
```

The offline checks passed for the publication snapshot: Python compilation, six
unit tests, 28 canonical Markdown files, 13 English/French page pairs, 29 manifested
PNG figures, and 30 exported wiki Markdown files. There were no broken local links
or missing image/provenance entries. No pre-existing linter or package build was
configured in the initially empty repository.

The final publication is accepted only after these checks succeed and the remote
repository/wiki commits match the local published commits. These checks validate the
documentation deliverable, not cloud execution. See
[publication procedure](../publishing.md) for export details and maintenance.

## Remaining live validation work

1. Confirm the selected workshop environment, harness, credits, permissions, quota,
   data policies, approved budget, and cleanup owner.
2. Preserve the working Lab 1 agent before changing its knowledge or topics.
3. Provision only the dedicated, approved Search and telemetry resources required
   by the selected labs. Do not reuse unrelated production resources.
4. Execute the test matrices in each guide in dependency order.
5. Capture new, redacted evidence with input, result, timestamp, source edition,
   model/API version, and downstream outcome where applicable.
6. Fix the smallest failing boundary, retest it, then retest the integrated path.
7. Update both language ledgers and distinguish partial tests from a complete lab pass.

No billable Azure resources, new billing policy, external email, or agent configuration
changes were performed by the documentation work. Stop at blocked rather than
inventing a pass if the required authorized environment is unavailable.
