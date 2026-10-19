---
title: Lab 0 - Préparer l'environnement
description: Vérifier les licences, Dataverse, la gouvernance, les accès Azure, les outils et les quotas avant l'atelier.
ms.date: 2026-10-19
---

## Objectif et état de validation

[Tous les labs](index.md) | [English](../en/lab-00.md) | [Suite : lab 1](lab-01.md)

Préparez un bac à sable contrôlé pour l'atelier. La réussite suppose de pouvoir ouvrir
la bonne expérience d'agent, utiliser les connaissances et connecteurs nécessaires et
déployer les services Azure dans le budget approuvé. Une connexion au portail ne suffit pas.

État : précontrôle partiel en lecture seule effectué. Azure CLI 2.91.0 est installé
et authentifié. Microsoft.Search, Microsoft.CognitiveServices et Microsoft.Insights
sont inscrits dans l'abonnement sélectionné. Terraform était initialement absent du
PATH ; une version portable 1.16.6 a été restaurée après vérification du SHA-256.
Elle a permis une initialisation, une validation et un plan sans apply réussis.
Consultez le [registre de réexécution réelle](live-rerun-2026-10-19.md).
La disponibilité complète de l'environnement n'est pas démontrée.

## 1. Consigner le contexte d'exécution

1. Ouvrez [Copilot Studio](https://copilotstudio.microsoft.com/) avec votre compte professionnel.
2. Sélectionnez l'environnement Power Platform de l'atelier. Notez son nom, son type,
   sa région et son locataire dans un registre privé, pas dans une capture publique.
3. Ouvrez le [centre d'administration Power Platform](https://admin.powerplatform.microsoft.com/).
   Privilégiez un environnement de bac à sable avec Dataverse et un groupe de sécurité
   limité aux participants. Ne créez pas d'environnement et ne modifiez pas la
   facturation sans l'accord de l'administrateur.
4. Dans le [portail Azure](https://portal.azure.com/), sélectionnez l'abonnement prévu
   et vérifiez son locataire. L'intégration Foundry/Copilot du lab 6 exige une
   configuration d'identité et de locataire prise en charge.
5. Réservez un groupe de ressources dédié et une boîte aux lettres approuvée que
   vous contrôlez. N'utilisez ni application de production, ni groupe de ressources
   sans rapport avec l'atelier, ni données réelles de clients.

Si l'interface des agents standard a changé de place, consultez les
[instructions de changement d'expérience](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences).
Les [changements de plateforme](platform-changes.md) distinguent le moteur et l'orchestration.

## 2. Vérifier les licences et la capacité utilisable

1. Demandez à l'administrateur de vérifier votre droit de création ou la configuration
   applicable aux auteurs. Les essais et droits Microsoft 365 ont leurs propres limites.
2. Vérifiez les crédits Copilot de l'environnement ou sa stratégie approuvée de
   paiement à l'usage. L'achat du locataire, le droit utilisateur et l'affectation
   à l'environnement constituent trois vérifications distinctes.
3. Confirmez que les prompts et connecteurs Premium des labs choisis sont disponibles
   pour cet environnement et cette identité.
4. Consignez le plafond de dépenses et les conditions d'arrêt avant tout déploiement.

Ne reprenez pas l'hypothèse ancienne selon laquelle les tests n'exigent jamais de
capacité utilisable ou chaque créateur doit disposer de la même combinaison de licences.
Appliquez les règles actuelles du moteur, du canal et du droit retenus.

Références vérifiées le 2026-10-19 :

* [Attribution des licences et gestion des accès](https://learn.microsoft.com/en-us/microsoft-copilot-studio/requirements-licensing)
* [Licences du moteur standard et crédits Copilot](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)

## 3. Préparer Dataverse et les connaissances

1. Vérifiez que l'environnement dispose d'une base Dataverse et d'une capacité de fichiers suffisante.
2. Dans le centre d'administration, sélectionnez **Gérer > Environnements > votre environnement > Paramètres**.
3. Sous **Produit > Fonctionnalités**, vérifiez la recherche Dataverse nécessaire
   aux expériences d'IA et d'agents. N'activez pas d'applications Dynamics 365 sans rapport avec l'atelier.
4. Si vous prévoyez le lab 4, confirmez que les stratégies autorisent les prompts d'IA.
5. Téléchargez une copie autorisée et actuelle du
   [guide de licences Power Platform](https://go.microsoft.com/fwlink/?LinkId=2085130).
   Consignez son édition et la date de téléchargement.
6. Vérifiez que le PDF n'est ni chiffré ni protégé par mot de passe. Ne retirez jamais
   une étiquette de confidentialité pour forcer l'importation. Demandez plutôt au
   propriétaire une copie pédagogique non protégée dont l'utilisation est approuvée.

Les [instructions actuelles sur les fichiers de connaissances](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
exigent la recherche Dataverse et n'acceptent pas les fichiers chiffrés. Consultez la
[configuration de la recherche Dataverse](https://learn.microsoft.com/en-us/power-platform/admin/configure-relevance-search-organization).

## 4. Examiner les stratégies de données et les autorisations

Demandez à l'administrateur d'examiner toutes les stratégies applicables à l'environnement.
Une exception locale ne peut pas annuler une autre stratégie applicable plus restrictive.

1. Conservez l'authentification. Ne débloquez pas la conversation anonyme pour réussir le lab.
2. Vérifiez l'autorisation des connaissances par fichier, Office 365 Users, Office 365 Outlook,
   Azure AI Search, Application Insights et du connecteur Foundry pertinent.
3. Placez les connecteurs qui échangent des données dans le même groupe autorisé.
4. Créez les connexions avec une identité de test dotée des privilèges minimaux.
5. Distinguez le consentement à une connexion du droit d'envoyer des courriels ou de lire des données Azure.

Suivez les [stratégies de données pour les agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/admin-data-loss-prevention).
Ne désactivez pas les protections de l'organisation pour l'atelier.

## 5. Vérifier les outils locaux et les droits Azure

Exécutez ces contrôles en lecture seule dans PowerShell :

```powershell
az version
az account show --query "{subscription:name,tenant:tenantId}" -o json
Get-Command terraform -ErrorAction Stop
terraform version
az provider show --namespace Microsoft.Search --query registrationState -o tsv
az provider show --namespace Microsoft.CognitiveServices --query registrationState -o tsv
az provider show --namespace Microsoft.Insights --query registrationState -o tsv
```

Les versions minimales d'origine sont Azure CLI 2.50 et Terraform 1.5.
Ces minima ne prouvent pas la compatibilité des fournisseurs actuels ou des API en préversion.
Utilisez des versions compatibles avec la configuration fournie et consignez le
verrouillage des versions de fournisseurs effectivement résolues.

Le rôle Contributor ne permet pas d'attribuer des rôles Azure et ne donne pas
automatiquement accès aux données. Faites attribuer par un administrateur habilité
les rôles nécessaires à Storage, Search, l'inférence et la télémétrie. Ne choisissez
pas Owner comme rôle par défaut.

## 6. Confirmer les quotas, le réseau et les coûts

1. Vérifiez la disponibilité régionale et le quota des modèles d'embedding et de conversation.
2. Vérifiez le niveau Search requis par les fonctions réelles. Ne supposez pas que
   Free couvre tous les exercices de vectorisation, de classement sémantique ou de recherche agentique.
3. Vérifiez que Search peut joindre Storage et le modèle avec l'identité et le réseau pris en charge.
4. Définissez un responsable du nettoyage, une durée de conservation et un budget.
   Supprimer un agent ne supprime pas ses ressources Azure.

## Liste d'acceptation

| Contrôle                        | Résultat attendu                                     | Preuve actuelle                                                                     |
| ------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Environnement correct           | Environnement nommé avec les accès prévus            | Non vérifié indépendamment                                                          |
| Droit de création et crédits    | Fonctions utilisables avec une facturation approuvée | Non vérifié indépendamment                                                          |
| Connaissances par fichier       | PDF pris en charge atteignant l'état Ready           | Le lab 1 montre un résultat fondé sur des connaissances, pas toute la configuration |
| Stratégies et connexions        | Outils autorisés, sans erreur de stratégie           | Non vérifié indépendamment                                                          |
| Azure CLI                       | Version affichée et requête de compte réussie        | Contrôle en lecture seule réussi                                                    |
| Fournisseurs de ressources      | Fournisseurs nécessaires inscrits                    | Search, Cognitive Services et Insights observés inscrits                            |
| Terraform                       | Exécutable et version compatible                     | Absent du PATH                                                                      |
| Ressources Search et télémétrie | Ressources approuvées disponibles                    | Aucune observée dans l'abonnement sélectionné                                       |
| Budget et quotas                | Accord du responsable et quotas suffisants           | Non vérifié                                                                         |

## Captures à conserver et nettoyage

Capturez le sélecteur d'environnement en masquant les identifiants, l'état non sensible
des licences et capacités, les versions des outils et le résumé du plan de déploiement.
Ce lab ne comporte aucune nouvelle capture de portail prétendant prouver un précontrôle réussi.
La [galerie du lab 1](evidence.md) est distincte.

Aucune ressource cloud n'a été créée pendant ce précontrôle. Si vous créez ensuite des
connexions ou environnements temporaires, supprimez uniquement les objets nommés de
l'atelier après vérification de leurs dépendances.
