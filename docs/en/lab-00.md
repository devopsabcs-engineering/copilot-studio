---
title: Lab 0 - Prepare the environment
description: Verify licensing, Dataverse, governance, Azure access, tools, and quotas before running the workshop.
ms.date: 2026-10-19
---

## Goal and validation status

[All labs](index.md) | [Français](../fr/lab-00.md) | [Next: Lab 1](lab-01.md)

Prepare a controlled sandbox for the workshop. Completion means that you can open
the correct agent experience, use the required knowledge and connectors, and deploy
the Azure services within an approved budget. A signed-in portal alone is not enough.

Status: partial read-only preflight completed. Azure CLI 2.91.0 is installed and
authenticated; Microsoft.Search, Microsoft.CognitiveServices, and Microsoft.Insights
are registered in the selected subscription. Terraform was initially missing from
PATH; portable Terraform 1.16.6 has since been restored with archive checksum
verification and used for successful init, validation and a non-applying plan.
See the [actual rerun record](live-rerun-2026-10-19.md).
No end-to-end environment readiness pass is claimed.

## 1. Record your execution context

1. Open [Copilot Studio](https://copilotstudio.microsoft.com/) with your work account.
2. Select the workshop Power Platform environment. Record its friendly name, type,
   region, and owning tenant in a private run record, not a public screenshot.
3. Open the [Power Platform admin center](https://admin.powerplatform.microsoft.com/).
   Prefer a sandbox with Dataverse and a security group limited to workshop attendees.
   Do not create an environment or switch billing without administrator approval.
4. Open [Azure portal](https://portal.azure.com/), select the intended subscription,
   and confirm it belongs to the appropriate tenant. The Foundry/Copilot integration
   in Lab 6 requires a supported identity/tenant arrangement.
5. Reserve a dedicated lab resource group and an approved mailbox that you control.
   Do not use a production application, unrelated resource group, or real customer data.

If the standard-agent interface has moved, use the
[experience-switching instructions](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences).
The harness and orchestration distinction is explained in [platform changes](platform-changes.md).

## 2. Verify licensing and usable capacity

1. Ask your administrator to verify your maker entitlement or the applicable author
   configuration. A trial or a Microsoft 365 entitlement has its own restrictions.
2. Check environment-level Copilot Credits or the approved pay-as-you-go billing
   policy. Tenant purchase, user entitlement, and environment allocation are separate checks.
3. Confirm that prompts and premium connectors needed by your chosen labs are
   available to this environment and identity.
4. Record the approved spending limit and stop conditions before any deployment.

Do not repeat the original assumption that testing never requires usable capacity
or that every maker must have exactly the same licensing combination. Apply the
current rules for the selected harness, channel, and entitlement.

References checked on 2026-10-19:

* [Assign licenses and manage access](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing)
* [Standard-harness licensing and Copilot Credits](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)

## 3. Prepare Dataverse and knowledge

1. Confirm that the environment has a Dataverse database and enough file capacity.
2. In the admin center, select **Manage > Environments > your environment > Settings**.
3. Under **Product > Features**, verify the Dataverse search setting required for AI
   and agent experiences. Do not enable unrelated Dynamics 365 applications.
4. Confirm that AI prompts are permitted by environment policy if you will run Lab 4.
5. Download an authorized, current copy of the
   [Power Platform licensing guide](https://go.microsoft.com/fwlink/?LinkId=2085130).
   Record its edition and download date.
6. Check that the PDF is not encrypted or password protected before uploading it.
   Never remove a sensitivity label to force a file upload. Obtain an approved
   unprotected teaching copy from its owner instead.

The current [file-knowledge guidance](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
requires Dataverse search and does not support encrypted files. See
[Dataverse search configuration](https://learn.microsoft.com/en-us/power-platform/admin/configure-relevance-search-organization).

## 4. Review data policies and connector permissions

Ask the administrator to review the effective policies, including all policies that
apply to the environment. An environment-specific exception cannot override a more
restrictive applicable policy.

1. Keep authentication enabled. Do not unblock anonymous chat to make the workshop work.
2. Verify that file knowledge, Office 365 Users, Office 365 Outlook, Azure AI Search,
   Application Insights, and the relevant Foundry connector are allowed where needed.
3. Ensure connectors that exchange data are in the same permitted data group.
4. Create connections using a lab identity with the least privileges required.
5. Distinguish connection consent from permission to send mail or read Azure data.

Follow [data policies for agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention).
Do not disable organization-wide protections for this lab.

## 5. Verify local tools and Azure rights

Run these read-only checks in PowerShell:

```powershell
az version
az account show --query "{subscription:name,tenant:tenantId}" -o json
Get-Command terraform -ErrorAction Stop
terraform version
az provider show --namespace Microsoft.Search --query registrationState -o tsv
az provider show --namespace Microsoft.CognitiveServices --query registrationState -o tsv
az provider show --namespace Microsoft.Insights --query registrationState -o tsv
```

The original tool baselines are Azure CLI 2.50+ and Terraform 1.5+.
Those minima are not proof that current providers or preview APIs work. Use the
versions supported by the supplied configuration and record the resolved provider lock.

Contributor does not grant the ability to assign Azure roles or automatically grant
data-plane access. Ask an authorized role administrator to grant the specific roles
required for Storage, Search, model inference, and telemetry. Avoid Owner as a
default workshop role.

## 6. Confirm quota, networking, and costs

1. Check regional model availability and quota for the embedding and chat models.
2. Check the Search tier required by the actual features. Do not assume Free supports
   every vectorization, semantic, or agentic-retrieval exercise.
3. Verify that Search can reach Storage and the model endpoint using the supported
   identity and network configuration.
4. Define a cleanup owner, retention window, and resource budget. Deleting an agent
   does not remove its Azure resources.

## Acceptance checklist

| Check                          | Expected result                                     | Current evidence                                                                |
| ------------------------------ | --------------------------------------------------- | ------------------------------------------------------------------------------- |
| Correct environment            | Named workshop environment with intended access     | Not independently verified                                                      |
| Maker entitlement and credits  | Required capabilities usable under approved billing | Not independently verified                                                      |
| File knowledge                 | Supported PDF can reach Ready after upload          | Lab 1 user evidence supports a knowledge-backed outcome, not full configuration |
| DLP and connections            | Required tools allowed; no policy error             | Not independently verified                                                      |
| Azure CLI                      | Version reported and account query succeeds         | Passed read-only check                                                          |
| Resource providers             | Required providers registered                       | Search, Cognitive Services, Insights observed registered                        |
| Terraform                      | Executable and supported version                    | Missing from PATH                                                               |
| Search and telemetry resources | Approved resources available                        | None observed in the selected subscription                                      |
| Budget and quota               | Owner approval and sufficient quota                 | Not verified                                                                    |

## Evidence to capture and cleanup

Capture the environment selector with identifiers obscured, the non-sensitive
licensing/capacity status, tool versions, and the deployment plan summary. This lab
has no new portal screenshot claiming a successful preflight. The
[Lab 1 evidence gallery](evidence.md) is separate.

No cloud resources were created by this preflight. If you create temporary
connections or environments later, remove only the named workshop objects after
checking dependencies.
