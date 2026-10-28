---
title: Guide de l'atelier en français
description: Parcours des labs, prérequis, captures partagées et validation fondée sur des preuves pour l'atelier Agent Factory.
ms.date: 2026-10-28
---

## Commencer ici

[English](../en/index.md) | [Accueil du dépôt](../../README.md)

Commencez par la [feuille de route](completion-roadmap.md) et le
[registre de validation](validation.md) pour l'acceptation actuelle et les critères
restants. Les huit guides bilingues sont livrés et les huit unités disposent de
preuves d'exécution ; l'exécution complète de l'atelier n'est **pas terminée**.
Le [registre de réexécution réelle](live-rerun-2026-10-19.md) conserve les premiers
essais ; la [poursuite backend](backend-live-2026-10-20.md) consigne les tests natifs
ultérieurs. Un nettoyage historique ne prouve pas la suppression des ressources
actuellement conservées.

La matrice F6 distincte compte 8 PASS, 2 PARTIAL, 0 FAIL et 2 NOT_RUN. F6-09 réussit
sous sélection explicite de langue, pas par réparation du sélecteur natif ou détection
automatique. Les dernières [réponses statiques françaises](../assets/runtime-2026-10-26/lab6-french-static-wrappers.json)
réussissent deux contrôles limités, pas une localisation complète ou une recherche
en direct. La matrice d'origine à onze scénarios reste à 10/11 : le cas 9 a échoué
deux fois, sans troisième rejeu. Ne fusionnez pas ces matrices.

Utilisez ces guides avec les supports locaux de l'atelier auxquels vous êtes autorisé
à accéder. Une vérification documentaire réussie n'est pas un déploiement cloud réussi.
La revue de ces résumés date du 2026-10-28. Les préversions et fonctions disponibles
varient selon le locataire et la région. Une mise à jour documentaire n'implique
aucune nouvelle exécution.

## Parcours des labs

| Lab | Guide                                                                    | Niveau de preuve                                          |
| --- | ------------------------------------------------------------------------ | --------------------------------------------------------- |
| 0   | [Prérequis, licences, environnement et autorisations](lab-00.md)         | Précontrôle et accès backend ; exécution standard incomplète |
| 1   | [Conseiller de licences, connaissances et outils de courriel](lab-01.md) | Parcours principal réussi ; hash PDF cloné égal ; audit des citations incomplet |
| 2   | [Azure AI Search comme source de connaissances](lab-02.md)               | Index de licences isolé et réponses connectées réussis ; navigation PDF externe/preuve de source actuelle ouvertes |
| 3   | [Supervision avec Application Insights](lab-03.md)                       | Événement natif/KQL et nettoyage réussis ; critères de canal publié/confidentialité ouverts |
| 4   | [Apporter son modèle à l'aide d'un prompt](lab-04.md)                    | Appel direct du modèle payant réussi ; prompt connecté incomplet |
| 5.1 | [Déployer l'infrastructure de recherche avancée](lab-05-1.md)            | Déploiement payant corrigé et nettoyage vérifié terminés |
| 5   | [Requêtes avancées avec Azure AI Search](lab-05.md)                      | Contrôles réels de recherche réussis ; réponse Copilot connectée incomplète |
| 6   | [Foundry IQ et recherche agentique](lab-06.md)                           | Réussites hébergées/natives limitées ; F6 8 PASS/2 PARTIAL/2 NOT_RUN ; cas 9 d'origine toujours échoué |

Exécutez le lab 5.1 avant le lab 5 si les ressources de recherche avancée n'existent
pas encore. Le lab 4 dépend de l'index Search du lab 2. Le titre interne du document
de supervision l'appelle « Lab 4 », et celui du document BYOM l'appelle « Lab 3 ».
Ces guides suivent les noms des fichiers : supervision au lab 3, BYOM au lab 4.

## Changements depuis les instructions d'origine

La documentation actuelle de Copilot Studio distingue plusieurs moteurs d'exécution,
appelés *harnesses*. Les rubriques, nœuds de connaissances et outils de prompt du
support d'origine correspondent au moteur standard. Un agent créé dans la nouvelle
expérience n'est pas automatiquement équivalent. Consultez d'abord les
[changements de plateforme](platform-changes.md).

Retenez notamment les points suivants :

* L'orchestration générative du moteur standard et le moteur GitHub Copilot sont distincts.
* Les licences actuelles utilisent les crédits Copilot plutôt que l'ancienne notion de messages.
* L'attribution d'une licence de créateur ne prouve ni la capacité de l'environnement ni le quota du modèle.
* Les fonctions d'Azure AI Search dépendent du niveau tarifaire, de la région, du modèle, de l'identité et du schéma d'index.
* Les fichiers chiffrés ou protégés par mot de passe ne sont pas acceptés comme connaissances.
* Un prompt BYOM ne remplace pas le modèle d'orchestration de l'agent.

## Preuves et exploitation

* [Registre de validation et critères d'acceptation](validation.md)
* [Feuille de route et tâches de reprise par lab](completion-roadmap.md)
* [Wiki français](https://github.com/devopsabcs-engineering/copilot-studio/wiki/FR-index) et [wiki anglais](https://github.com/devopsabcs-engineering/copilot-studio/wiki/EN-index)
* [Provenance des captures et galerie de preuves](evidence.md)
* [Dépannage, adaptations sûres et nettoyage](troubleshooting.md)
* [Publication et export reproductible vers le wiki](../publishing.md)

Pour chaque lab, démarrez une nouvelle conversation de test, consignez les entrées
et sorties exactes, capturez l'activité ou le résultat de l'outil, puis conservez la
preuve du système destinataire. N'envoyez pas de courriel à un tiers et ne créez pas
de ressources cloud sans l'accord du responsable. Les guides prévoient une boîte
de test contrôlée et un groupe de ressources dédié.
