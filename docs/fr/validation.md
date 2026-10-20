---
title: Registre de validation de l'atelier
description: Preuves, vérifications effectuées, limites d'exécution et critères d'acceptation encore nécessaires pour chaque lab.
ms.date: 2026-10-19
---

## Verdict global

[Tous les labs](index.md) | [English](../en/validation.md) | [Galerie de preuves](evidence.md)

Dernières preuves : [registre de réexécution réelle](live-rerun-2026-10-19.md).
Le propriétaire a approuvé les tests payants. Le déploiement Terraform corrigé de
15 instances, 14 contrôles modèle/recherche sans clé et un événement synthétique
Application Insights réellement corrélé par KQL ont réussi. Les ressources ont
été supprimées et leur absence vérifiée. Une autre chaîne PDF privée a réussi
25 contrôles : indexeur Blob réel, neuf projections enfants et embeddings
intégrés de 1 536 dimensions. Le dernier registre distingue son nettoyage
de celui de l'exécution précédente. L'échec SDK du lab 6 et sa restauration
isolée ont aussi été testés. Les tableaux suivants
conservent l'état de la revue initiale, sauf mise à jour apportée par ce registre.

La revue et la publication de la documentation sont distinctes de la validation
réelle des labs. L'atelier **n'est pas certifié comme entièrement réexécuté**.
Le lab 1 dispose de preuves utilisateur et d'une nouvelle exécution de son parcours
principal. Les autres labs ont désormais de vraies preuves cloud par sous-système,
mais leurs intégrations complètes d'agents connectés restent non vérifiées.

Le navigateur a d'abord rencontré une barrière d'authentification. L'utilisateur s'est
ensuite connecté et a initialisé le wiki GitHub. Cela a levé le blocage de publication,
sans créer automatiquement les ressources Search, la télémétrie, les modèles, les
index, les bases de connaissances ou les connecteurs nécessaires.

## Définition des états

| État                             | Signification                                                                               |
| -------------------------------- | ------------------------------------------------------------------------------------------- |
| Exécution utilisateur observée   | Les preuves fournies montrent un résultat précis, pas une nouvelle exécution de l'assistant |
| Contrôle en lecture seule réussi | Un outil a directement observé un prérequis ciblé ou une condition du dépôt                 |
| Procédure revue                  | Le parcours a été comparé aux recommandations officielles ; son exécution reste nécessaire  |
| Contrôle statique                | Un fichier ou une propriété du code a été examiné sans exécuter d'opération cloud           |
| Bloqué                           | Un prérequis, droit, environnement ou problème d'intégration empêche la réussite            |
| Non exécuté                      | Aucun résultat d'exécution n'est disponible                                                 |

Une étape indisponible ou non testée reste bloquée ou non exécutée. Une capture d'un
document Word, un schéma généré ou une réponse plausible ne peut pas améliorer cet état.

## État de la revue initiale

Le tableau suivant conserve la revue d'origine. Consultez le
[tableau actuel d'exécution par lab](live-rerun-2026-10-19.md) pour les résultats ultérieurs.

| Lab                | Résultat actuel                                                                            | Preuves requises pour une réussite complète                                                                             |
| ------------------ | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------- |
| [0](lab-00.md)     | Précontrôle partiel ; disponibilité complète non établie                                   | Environnement, droits/capacité, stratégies, accès aux données, quotas, Terraform et budget vérifiés                     |
| [1](lab-01.md)     | Exécution utilisateur observée : outil d'envoi et message reçu ; tests négatifs incomplets | Nouvelle exécution contrôlée : réponse fondée, résolution du destinataire, envoi, réception et tests négatifs           |
| [2](lab-02.md)     | Procédure revue ; recherche intégrée complète non démontrée                                | Indexeur réussi, résultats Search pertinents non vides et réponse Copilot avec les sources attendues                    |
| [3](lab-03.md)     | Procédure revue ; ingestion de télémétrie non démontrée                                    | Événement volontaire corrélé à l'interaction du lab et visible dans la bonne requête de journaux                        |
| [4](lab-04.md)     | Procédure revue ; appel du modèle connecté non démontré                                    | Test direct, résultats analysés, appel du prompt, réponse fondée et traitement explicite du vide et des erreurs         |
| [5.1](lab-05-1.md) | Revue statique du déploiement ; aucun apply                                                | Fournisseurs compatibles, plan revu, apply approuvé, ressources et configuration privée attendues                       |
| [5](lab-05.md)     | Revue des sources et statique ; résultats avancés non observés                             | Corpus indexé, requêtes exécutées, champs, classement et filtres attendus consignés                                     |
| [6](lab-06.md)     | Revue des sources et statique ; agent connecté non démontré de bout en bout                | Données/configuration complètes, SDK/API pris en charge, recherche directe, agent Foundry et connexion Copilot vérifiés |

## Contrôles effectués pendant cette session

| Contrôle                               | Résultat observé                                                                                          | Limite de portée                                                                                              |
| -------------------------------------- | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Inventaire des sources                 | Labs 0 à 6, supplément 5.1 et fichiers complémentaires trouvés                                            | Ne prouve pas que le support exécutable est complet                                                           |
| Accès aux documents Word               | Extraction locale des documents ZIP lisibles et lecture des formats composés avec Word installé           | Documents protégés non republiés                                                                              |
| Numérotation                           | Titres internes de supervision/BYOM contraires aux noms des fichiers                                      | Les guides suivent les noms des fichiers                                                                      |
| Azure CLI                              | Version 2.91.0 installée ; requête du compte sélectionné réussie                                          | Aucune conclusion pour tous les abonnements ou locataires                                                     |
| Inscription des fournisseurs           | Search, Cognitive Services et Insights observés Registered                                                | Ne prouve ni droits, ni capacité, ni réseau, ni déploiement réussi                                            |
| Ressources de l'abonnement sélectionné | Absence corrigée par contrôle explicite : 9 comptes Cognitive, 4 projets, 7 composants Insights sans rapport, 0 Search avant tests jetables | Tests Search Free et nettoyage vérifié dans le dernier registre réel |
| Exécutable Terraform                   | Absent du PATH                                                                                            | Aucun init, validate, plan ou apply annoncé                                                                   |
| Navigateur Copilot                     | Connexion réussie et accueil visible, puis page durablement vide en ouvrant l'agent                       | Le conseiller de licences n'a pas pu être ouvert ; aucune nouvelle question n'a été envoyée                   |
| Accès de publication GitHub            | Dépôt privé créé ; wiki activé puis initialisé par le propriétaire                                        | Dépôt et wiki exigent des commits et vérifications distantes distincts                                        |
| Pièces jointes du lab 1                | Résultat de l'outil et courriel reçu conservés sous forme d'extraits                                      | Pas d'audit indépendant des en-têtes de transport ou du contenu des licences                                  |
| Recommandations actuelles              | Références Microsoft Learn consultées pour les adaptations                                                | Une vérification documentaire n'est pas un test réel                                                          |
| Notebook du lab 6                      | 11 cellules de code sur 11 valides syntaxiquement ; 24 enregistrements intégrés identifiés                | Syntaxe et données présentes ne prouvent ni compatibilité des API, ni inférence, ni recherche, ni intégration |
| Exemples des labs avancés              | Quatre exemples JSON vérifiés, schémas SVG analysés et identifiants de tests alignés entre langues        | Exemples et schémas ne démontrent pas l'exécution cloud                                                       |

La revue avancée a aussi relevé des lacunes d'identité et de réseau Terraform,
le provisionnement Foundry désactivé, la cohérence requise des dimensions d'embedding,
des évolutions d'API et de SDK ainsi que des réinitialisations destructrices à corriger
ou encadrer explicitement avant l'exécution. Consultez les détails des labs 5.1, 5 et 6
au lieu d'appliquer le support d'origine sans adaptation.

### Constats sur le support avancé à traiter

1. La configuration Terraform désactive le module Foundry : ce chemin ne provisionne
   donc pas le projet Foundry annoncé.
2. Le module Search n'applique pas les options d'adresses IP autorisées et d'Entra
   comme attendu, et l'identité de service requise n'est pas attachée. Examinez les
   ressources effectives et les rôles avant de considérer cette configuration comme
   une base d'identité et de réseau.
3. Le supplément de déploiement utilise des embeddings de 1 536 dimensions, tandis
   que le lab 6 en attend 3 072. Ces configurations ne rendent pas les index interchangeables.
   Alignez la sortie du modèle, le champ d'index et l'embedding de requête pour le lab choisi.
4. Les contrats de SDK, ARM et MCP en préversion exigent une vérification de
   compatibilité. Le parcours d'agent connecté exige le contrat Activity et l'agent
   du nouveau portail pris en charge.
5. Le code de réinitialisation du notebook supprime des objets à nom fixe ; le
   nettoyage final est commenté. N'exécutez pas ces cellules sur un projet partagé.

Le notebook référence aussi un fichier Markdown de référence rapide absent.
Le support contient plutôt `data\quick_reference_guide.docx`. Changer l'extension
ne convertit pas un document ; obtenez une source autorisée dans le format attendu.

## Contrôles de documentation et d'outillage

Les vérifications hors ligne sont reproductibles avec :

```powershell
python -m py_compile scripts\build_wiki.py scripts\validate_docs.py scripts\test_docs.py
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts\build_wiki.py --output .wiki-build
python scripts\validate_docs.py --wiki .wiki-build
```

Les contrôles hors ligne ont réussi pour la version de publication : compilation
Python, sept tests unitaires, 28 fichiers Markdown de référence, 13 paires français/anglais,
29 figures PNG avec provenance et 30 fichiers Markdown exportés pour le wiki.
Aucun lien local rompu ni image ou provenance manquante n'a été trouvé. Le dépôt
initialement vide ne disposait d'aucun linter ou build de paquet préconfiguré.

La publication finale est acceptée seulement après leur réussite et la concordance
des commits locaux et distants du dépôt et du wiki. Ces contrôles valident le livrable
documentaire, pas l'exécution cloud. La [procédure de publication](../publishing.md)
décrit l'export et la maintenance.

## Validation réelle restante

1. Confirmez environnement, moteur, crédits, droits, quotas, stratégies, budget
   approuvé et responsable du nettoyage.
2. Préservez l'agent fonctionnel du lab 1 avant de modifier ses connaissances ou rubriques.
3. Provisionnez uniquement les ressources dédiées et approuvées de Search et de
   télémétrie nécessaires. Ne réutilisez pas de ressources de production sans rapport.
4. Exécutez les matrices de tests des guides dans l'ordre des dépendances.
5. Capturez les nouvelles preuves masquées avec entrée, résultat, horodatage,
   édition de source, version du modèle/API et effet destinataire si applicable.
6. Corrigez l'étape en échec la plus ciblée, retestez-la, puis retestez le parcours intégré.
7. Actualisez les deux registres et distinguez un test partiel d'un lab entièrement réussi.

La phase documentaire initiale n'a créé aucune ressource facturable. Les tests
payants approuvés ensuite et leur nettoyage figurent explicitement au registre.
Aucune stratégie de facturation ni application sans rapport n'a été modifiée.
Conservez l'état bloqué plutôt que de déduire une intégration réussie de sous-systèmes validés.
