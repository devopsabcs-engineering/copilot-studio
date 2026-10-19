---
title: Changements de plateforme et adaptations sûres
description: Adapter l'atelier aux expériences actuelles de Copilot Studio et Foundry sans annoncer une équivalence non testée.
ms.date: 2026-10-19
---

## Choisir l'équivalence par le résultat

[Tous les labs](index.md) | [English](../en/platform-changes.md)

Préservez l'objectif pédagogique plutôt que la position exacte d'un bouton. Consignez
l'étape d'origine, son remplacement, la raison, le résultat d'acceptation observable
et le risque restant. Une solution de remplacement n'est validée qu'après avoir
produit le résultat requis.

## Le principal changement de navigation

La [présentation actuelle des moteurs](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)
distingue les moteurs GitHub Copilot, standard et Copilot chat. Les labs d'origine
décrivent principalement le moteur standard avec rubriques, nœuds de connaissances
et prompts. Les agents standard peuvent eux-mêmes utiliser l'orchestration classique
ou générative. Ces modes ne correspondent pas au choix du moteur.

Pour retrouver l'expérience d'origine, le
[guide de changement d'expérience](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences)
propose trois chemins :

1. Depuis l'accueil, ouvrez le menu **…** en bas de la barre latérale et choisissez **Open classic experience**.
2. Sélectionnez **Other ways to build** pour les agents et flux du moteur standard.
3. Ouvrez un agent ou un flux existant depuis **Agents** ou **Workflows**.

Ne recréez pas un agent qui fonctionne parce qu'il n'apparaît pas dans une autre vue
d'accueil. Vérifiez d'abord l'environnement, le moteur et les filtres de liste.

## Tableau de décisions de migration

| Instruction d'origine                                       | Approche actuelle ou adaptation sûre                                                             | Preuve d'acceptation                                                                     |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| Créer un agent vide dans l'ancien accueil                   | Ouvrir l'expérience standard ou documenter un résultat équivalent explicite avec un autre moteur | Moteur consigné et outils/connaissances disponibles                                      |
| Volet de test et carte d'activité                           | Utiliser Test ou Aperçu et l'activité visible de l'expérience choisie                            | Entrée exacte, réponse, recherche/outil et effet destinataire                            |
| Facturation en messages                                     | Vérifier les crédits Copilot et droits du moteur/canal                                           | Affectation utilisable ou facturation approuvée, pas seulement une licence de créateur   |
| Importer le guide de licences                               | Utiliser l'édition actuelle approuvée non chiffrée et attendre sa disponibilité                  | Édition, état prêt et réponse comparée au PDF                                            |
| Free pour tous les labs Search                              | Vérifier fonctions, niveau et région avant le déploiement                                        | Indexation, recherche et fonctions retenues opérationnelles dans le niveau approuvé      |
| Copier une clé d'administration dans les instructions       | Utiliser une connexion sécurisée prise en charge avec des privilèges minimaux                    | Appel autorisé réussi sans divulgation d'identifiants                                    |
| Ancien assistant Import data                                | Employer le parcours actuel pris en charge, avec découpage et dimensions cohérents               | Indexeur réussi et fragments pertinents non vides                                        |
| Clé d'instrumentation ou chaîne de connexion indifféremment | Utiliser la configuration actuelle d'Application Insights et son champ de chaîne de connexion    | Télémétrie corrélée dans la bonne ressource                                              |
| Déployer un modèle nommé précisément                        | Choisir un modèle disponible et pris en charge par l'intégration                                 | Identifiant de déploiement, test direct puis test intégré réussis                        |
| BYOM remplace le modèle de tout l'agent                     | Traiter BYOM comme un appel de prompt/modèle connecté dans ce lab                                | Activité prouvant l'appel et la sortie, sans annoncer le remplacement de l'orchestration |
| Le nom d'agent vaut pour tout Agent ID                      | Distinguer identifiants classiques, points de terminaison de projet et agents Foundry versionnés | Appel Foundry direct et connecteur pris en charge visant le même agent                   |
| Retirer immédiatement une source fonctionnelle              | Copier/exporter l'agent avant de retirer ou désactiver une source pour isoler la nouvelle        | Restauration possible et chemin de recherche sans ambiguïté                              |

Les guides détaillent les réserves propres à Search, la télémétrie, BYOM et la recherche
agentique. Ce tableau décrit une stratégie de migration, pas une exécution réussie
de chaque adaptation.

## Incohérences des sources qui modifient le parcours

Le fichier **Lab 3_Monitor Copilot Studio agents with Application-Insights.docx**
porte un titre interne « Lab 4 ». Le fichier **Lab 4_BYOM to Copilot Studio.docx**
porte un titre interne « Lab 3 ». Utilisez les noms des fichiers comme identifiants
stables dans les preuves et échanges.

Le supplément de déploiement est numéroté 5.1, mais doit précéder le lab 5 quand les
ressources n'existent pas encore. Le guide de configuration complémentaire du lab 6
est distinct du document Word principal et du notebook. Examinez l'ensemble avant
de considérer le support comme complet.

## Documenter chaque adaptation

Conservez les champs suivants dans votre registre privé :

```text
Lab et identifiant de test :
Édition de la source et étape d'origine :
Environnement, moteur, modèle et version d'API :
Étape de remplacement et référence officielle :
Raison de l'indisponibilité de l'étape d'origine :
Résultat observable attendu :
Résultat observé et horodatage :
Fichier de preuve masqué :
État : réussi / échoué / bloqué / non exécuté
Nettoyage et limites restantes :
```

Si aucune adaptation prise en charge ne préserve l'objectif, indiquez **bloqué**.
Une réponse manuelle, une fausse capture ou un déploiement sans rapport ne peuvent
pas remplacer une recherche réussie, de la télémétrie ou l'appel d'un agent connecté.

## Références examinées

* [Moteurs de Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview)
* [Accès aux agents et flux du moteur standard](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences)
* [Orchestration générative et classique](https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-generative-actions)
* [Licences et crédits actuels](https://learn.microsoft.com/en-us/microsoft-copilot-studio/billing-licensing)
* [Fichiers de connaissances pris en charge](https://learn.microsoft.com/en-us/microsoft-copilot-studio/knowledge-add-file-upload)
