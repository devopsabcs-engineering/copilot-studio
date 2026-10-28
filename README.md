---
title: Foundry and Copilot Studio Agent Factory workshop
description: Illustrated English and French lab guides, validation evidence, and current-platform adaptations.
ms.date: 2026-10-28
---

## English | Français

Work through the original workshop with updated navigation, explicit acceptance tests,
shared screenshots, and an honest distinction between observed results and procedures
that still need a live run.

Parcourez l'atelier d'origine avec des chemins de navigation actualisés, des tests
d'acceptation explicites, des captures partagées et une distinction claire entre les
résultats observés et les procédures qui restent à exécuter.

* [English workshop guide](docs/en/index.md)
* [Guide de l'atelier en français](docs/fr/index.md)
* [Validation record in English](docs/en/validation.md)
* [Registre de validation en français](docs/fr/validation.md)
* [Actual rerun record](docs/en/live-rerun-2026-10-19.md)
* [Registre de réexécution réelle](docs/fr/live-rerun-2026-10-19.md)
* [English wiki](https://github.com/devopsabcs-engineering/copilot-studio/wiki/EN-index)
* [Wiki en français](https://github.com/devopsabcs-engineering/copilot-studio/wiki/FR-index)
* [Publication and maintenance / Publication et maintenance](docs/publishing.md)
* [Remaining-work roadmap](docs/en/completion-roadmap.md)
* [Feuille de route des travaux restants](docs/fr/completion-roadmap.md)

> [!IMPORTANT]
> Bilingual documentation is delivered for all eight lab units. All eight have
> execution evidence; none is unstarted. The workshop runtime is **not complete**.
> Lab 1 includes received-email evidence; later labs also have scoped live results,
> not just documentary checks. Read the validation ledger and roadmap for each gate.
>
> La documentation bilingue des huit unités est livrée. Toutes disposent de preuves
> d'exécution ; aucune n'est non commencée. L'exécution complète de l'atelier
> n'est **pas terminée**. Le lab 1 inclut un courriel reçu ; les labs suivants ont
> aussi des résultats réels de portée limitée, pas seulement des vérifications
> documentaires. Consultez le registre et la feuille de route pour chaque critère.

## All eight labs / Les huit unités

| Unit / Unité | English guide | Guide français |
| ------------ | ------------- | -------------- |
| 0 | [Environment, licensing and permissions](docs/en/lab-00.md) | [Environnement, licences et autorisations](docs/fr/lab-00.md) |
| 1 | [Licensing advisor and email tools](docs/en/lab-01.md) | [Conseiller de licences et outils de courriel](docs/fr/lab-01.md) |
| 2 | [Azure AI Search knowledge](docs/en/lab-02.md) | [Connaissances Azure AI Search](docs/fr/lab-02.md) |
| 3 | [Application Insights monitoring](docs/en/lab-03.md) | [Supervision Application Insights](docs/fr/lab-03.md) |
| 4 | [Bring your own model in a prompt](docs/en/lab-04.md) | [Apporter son modèle dans un prompt](docs/fr/lab-04.md) |
| 5.1 | [Deploy the Search infrastructure](docs/en/lab-05-1.md) | [Déployer l'infrastructure Search](docs/fr/lab-05-1.md) |
| 5 | [Advanced Search queries](docs/en/lab-05.md) | [Requêtes Search avancées](docs/fr/lab-05.md) |
| 6 | [Foundry IQ and agentic retrieval](docs/en/lab-06.md) | [Foundry IQ et recherche agentique](docs/fr/lab-06.md) |

Run 5.1 before 5 when the approved infrastructure is absent. Lab 4 depends on
Lab 2's Search index. The guides follow source filenames: monitoring is Lab 3,
BYOM is Lab 4, despite the reversed internal titles in the original material.

Exécutez 5.1 avant 5 si l'infrastructure approuvée manque. Le lab 4 dépend de
l'index Search du lab 2. Les guides suivent les noms des fichiers sources :
supervision au lab 3, BYOM au lab 4, malgré les titres internes inversés du support.

## Current results and limits / Résultats actuels et limites

The original eleven-scenario matrix remains **10/11** after controls: case 9 failed
twice, with no third replay. The separate F6 matrix is **8 PASS, 2 PARTIAL, 0 FAIL,
2 NOT_RUN**, with scoped rather than whole-lab passes. F6-09 passes under an explicit
language override; native picker behavior, automatic detection and general French
acceptance are not proven.

La matrice d'origine à onze scénarios reste à **10/11** après contrôles : le cas 9
a échoué deux fois, sans troisième rejeu. La matrice F6 distincte compte **8 PASS,
2 PARTIAL, 0 FAIL, 2 NOT_RUN**, pour des réussites limitées, non pour le lab entier.
F6-09 réussit sous sélection explicite de langue ; le sélecteur natif, la détection
automatique et l'acceptation générale du français ne sont pas prouvés.

The latest [French static-wrapper receipt](docs/assets/runtime-2026-10-26/lab6-french-static-wrappers.json)
covers two static replies under that override, not live retrieval or full static
localization. All 12 quotation/reference pairs are preserved. Earlier failures and
strict localization-map/two-file guard failures remain recorded. Use the
[English roadmap](docs/en/completion-roadmap.md) and
[validation ledger](docs/en/validation.md) to resume only unresolved criteria.

Le dernier [reçu des réponses statiques françaises](docs/assets/runtime-2026-10-26/lab6-french-static-wrappers.json)
couvre deux réponses sous cette sélection, pas une recherche en direct ni la
localisation statique complète. Les 12 paires citation/référence sont conservées.
Les échecs antérieurs et ceux des contrôles stricts de correspondance de traduction
et de modification de deux fichiers restent consignés. La
[feuille de route française](docs/fr/completion-roadmap.md) et le
[registre de validation](docs/fr/validation.md) permettent de reprendre uniquement
les critères non résolus.

## Prerequisites and safe use / Prérequis et usage sûr

Use authorized local workshop material, a development environment with maker
access, suitable licensing and capacity, approved connector policies, and the
standard agent experience where required. Azure exercises also need an approved
subscription, roles, quota and budget. A maker license or documentation test does
not prove cloud readiness or runtime acceptance. Obtain approval before creating
resources or sending mail; use a controlled test mailbox and retain sanitized evidence.

Utilisez les supports locaux autorisés, un environnement de développement avec
droits de créateur, des licences et capacités adaptées, des stratégies de connecteurs
approuvées et l'expérience d'agent standard lorsque requise. Les exercices Azure
exigent aussi un abonnement, des rôles, des quotas et un budget approuvés. Une licence
de créateur ou un test documentaire ne prouve ni la préparation cloud ni l'acceptation
d'exécution. Faites autoriser toute création de ressources ou tout envoi de courriel ;
utilisez une boîte de test contrôlée et conservez des preuves expurgées.

## Wiki and maintenance / Wiki et maintenance

The wiki mirrors the canonical repository guides. Start at
[EN-index](https://github.com/devopsabcs-engineering/copilot-studio/wiki/EN-index)
or [EN-completion-roadmap](https://github.com/devopsabcs-engineering/copilot-studio/wiki/EN-completion-roadmap).
Edit source Markdown, not generated wiki pages. Follow the
[publication procedure](docs/publishing.md) to validate, export and verify both languages;
source and wiki publication are separate operations.

Le wiki reflète les guides de référence du dépôt. Commencez par
[FR-index](https://github.com/devopsabcs-engineering/copilot-studio/wiki/FR-index)
ou [FR-completion-roadmap](https://github.com/devopsabcs-engineering/copilot-studio/wiki/FR-completion-roadmap).
Modifiez les sources Markdown, pas les pages wiki générées. Suivez la
[procédure de publication](docs/publishing.md) pour vérifier, exporter et contrôler
les deux langues ; les publications du dépôt et du wiki sont distinctes.

## Scope / Périmètre

The source material is the Word lab collection in the local
*Workshop - Foundry and Copilot Studio Agents with Microsoft Agent Factory* folder.
This repository contains original explanations derived from that workshop, not copies
of its protected Word files, notebooks, Terraform state, or credentials.

Les sources sont les documents Word du dossier local de l'atelier. Le dépôt contient
des explications originales adaptées de ces documents, et non des copies des fichiers
Word protégés, des notebooks, des états Terraform ou des identifiants.

The repository was created private; the
[October 25 publication checkpoint](docs/assets/runtime-2026-10-25/wiki-publication.json)
records public visibility with the wiki enabled. Recheck visibility before publishing;
do not change it during documentation maintenance. Source figures are teaching
illustrations, not new execution evidence. The three marked Lab 1 crops record the
user's observed run; later sanitized runtime receipts document their own scoped checks.
Keep protected originals, credentials and private evidence out of both publication surfaces.

Le dépôt a été créé privé ; le
[point de publication du 25 octobre](docs/assets/runtime-2026-10-25/wiki-publication.json)
constate sa visibilité publique et l'activation du wiki. Vérifiez la visibilité avant
publication, sans la modifier pendant la maintenance documentaire. Les figures d'origine
illustrent la procédure et ne prouvent pas une nouvelle exécution. Les trois extraits
identifiés du lab 1 documentent l'exécution observée par l'utilisateur ; les reçus
expurgés ultérieurs documentent leurs propres contrôles limités. Excluez les originaux
protégés, les identifiants et les preuves privées des deux supports de publication.
