---
title: Lab 0 - Prepare the environment
description: Verify licensing, Dataverse, governance, Azure access, tools, and quotas before running the workshop.
ms.date: 2026-10-23
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

### October 23 prerequisite refresh

The [current prerequisite receipt](../assets/runtime-2026-10-23/lab-prerequisite-refresh.json)
reconfirms Azure CLI 2.91.0 and registration of Cognitive Services, Search,
Insights and Storage. Regional quota metadata reports 26/5000 allocated units
for Standard GPT-4.1-mini and 1/1000 for GlobalStandard text-embedding-3-small.
These are the API's `Count` units, not measured throughput or guaranteed runtime
availability. No quota allocation was changed.

At that checkpoint, the process resolved az, azd and Python, but not Terraform or PAC on
PATH. That is not proof they are uninstalled; the historical portable Terraform
plan remains historical. Current Search Basic is retained and running.
User authorization for deployment and paid testing is recorded in the
[authorized release](../assets/runtime-2026-10-23/authorized-release.json).
Maker entitlement/credit allocation, effective DLP, current file readiness,
published-channel telemetry, retention ownership and a numerical spending boundary
remain distinct unclosed requirements. This refresh does not certify all of Lab 0.

The [later tool recovery](../assets/runtime-2026-10-23/native-recovery-alternatives.json)
restores official PAC 2.14.1 and verifies the intended admin/MngEnv identity.
The [independent Terraform check](../assets/runtime-2026-10-23/terraform-reconciliation.json)
restores checksum-verified Terraform 1.16.6 and passes original-source init,
validation and a saved plan. Both tools use explicit isolated executable paths;
global PATH is not changed. These results close the missing-tool observation,
not entitlement, policy, budget or native-answer acceptance.

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
| Correct environment            | Named workshop environment with intended access     | Admin/MngEnv, owned bot and environment verified through UI/API/PAC                |
| Maker entitlement and credits  | Required capabilities usable under approved billing | Authenticated draft evaluation executes; tenant credit allocation remains unverified |
| File knowledge                 | Supported PDF can reach Ready after upload          | Lab 1 user evidence supports a knowledge-backed outcome, not full configuration |
| DLP and connections            | Required tools allowed; no policy error             | Not independently verified                                                      |
| Azure CLI                      | Version reported and account query succeeds         | Passed read-only check                                                          |
| Resource providers             | Required providers registered                       | October 24: Search, Cognitive Services, Insights and Storage registered          |
| Terraform                      | Executable and supported version                    | Verified portable 1.16.6; original-source init/validate/plan pass                   |
| Search and telemetry resources | Approved resources available                        | Search Basic running; published telemetry/privacy acceptance remains unverified  |
| Budget and quota               | Owner approval and sufficient quota                 | October 24: chat 26/5,000 and embedding 1/1,000; retention/budget limits open |

The [October 24 read-only receipt](../assets/runtime-2026-10-24/azure-preflight-refresh.json)
matches deployed models to their exact Sweden Central quota meters, labeled
thousands of tokens per minute, and verifies both deployments are Succeeded.
The four retained ARM resources report USD 7.650361288 before tax, including
USD 7.373 Search, through the partial October 24 period. Reporting may lag;
this is not a final invoice or Copilot-credit total. No inference, provider
registration or configuration change is performed. Tenant credits, budget,
retention and other Lab 0 acceptance criteria remain open.

A separate Microsoft Graph read verifies the exact administrator's object ID
and account, then returns four license records. Seven filtered maker-related
plans have provisioning status Success. These assignments do not prove full
standard-harness/premium entitlement, tenant credit allocation or an environment
pay-as-you-go binding. No additional grant is requested.

## Evidence to capture and cleanup

Capture the environment selector with identifiers obscured, the non-sensitive
licensing/capacity status, tool versions, and the deployment plan summary. This lab
has no new portal screenshot claiming a successful preflight. The
[Lab 1 evidence gallery](evidence.md) is separate.

No cloud resources were created by this preflight. If you create temporary
connections or environments later, remove only the named workshop objects after
checking dependencies.
