---
title: Feuille de route pour terminer l'atelier
description: Travaux restants, priorités, dépendances, responsables et critères mesurables de clôture de l'atelier.
ms.date: 2026-10-23
---

## Objectif et périmètre

[Accueil du dépôt](../../README.md) | [English](../en/completion-roadmap.md) |
[Registre de validation](validation.md) | [Dernier rapport d'exécution](backend-live-2026-10-20.md)

Le livrable de planification est terminé. L'exécution complète de l'atelier ne
l'est **pas**. Les tâches non cochées représentent des travaux à effectuer,
et non des résultats déjà observés ou promis.

La référence est le commit `94ebcd3` et les preuves conservées, pas un nouvel
inventaire cloud du 23 octobre. Le 22 octobre, 47 tests documentaires, 33 tests
de l'extension, les vérifications de dépendances et de syntaxe Python ont réussi.
Ces résultats ne certifient pas l'acceptation en environnement réel.
Cette mise à jour ne déploie rien, n'envoie aucun courriel, n'accorde aucune
permission et ne publie ni ne consulte de source protégée.

## Implémentation existante et contraintes

L'[extension Python](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/README.md)
vérifie les enregistrements récupérés contre un corpus sous licence dont l'empreinte
est fixée, puis restitue les citations par du code. Les tests locaux de transport
simulent le chargement du corpus et l'opération de réponse Azure.
Le [reçu de l'extension](../assets/runtime-2026-10-20/foundry-verified-extension.json)
conserve la version hébergée 1, un SDK Activity déployé non corrigé, une erreur
native HTTP 403 et une erreur directe authentifiée HTTP 500 avant le gestionnaire
applicatif. La réparation locale Activity `1.0.0b4` et Microsoft Agents `1.9.0`
passe sa régression. Son déploiement et les permissions aval de l'identité hébergée
restent à vérifier.

Utilisez les ressources isolées existantes et les interfaces prises en charge.
Préservez les agents d'origine, les échecs, les preuves privées et le routage
fonctionnel en version 4. Un appel SDK ne remplace pas une réponse native Copilot.
Une vérification locale ne remplace pas une exécution cloud. Ne contournez pas
la politique, n'activez pas l'accès anonyme et ne reconstituez pas les documents
protégés. Le notebook sous licence n'est pas une preuve d'équivalence juridique
ou documentaire avec ces originaux. Aucune migration d'architecture n'est nécessaire.

La permission générale de reprise et de diagnostic isolé Entra uniquement est
enregistrée dans la transmission précédente. Ne la redemandez pas. Les validations
de livraison du Product Owner, de l'équipe sécurité et du responsable technique
doivent encore être attribuables. Une permission générale ne prouve pas ces rôles.
Identifiez l'artefact exact; toute modification exige une nouvelle validation.

## Priorités, responsables et dépendances

Les responsables sont des rôles d'exécution, pas des personnes désignées ou des
approbations acquises. P0 supprime le blocage immédiat ou limite les coûts; P1 ferme
l'acceptation fonctionnelle; P2 réconcilie les preuves et la publication.

| Étape | Priorité | Responsable                         | Dépend de       | Preuve de clôture                                      |
|-------|----------|-------------------------------------|-----------------|--------------------------------------------------------|
| 1.1   | P0       | Livraison et propriétaire cloud     | Aucune          | Inventaire, coûts, artefact et validations              |
| 2.1   | P0       | Mainteneur de l'extension            | 1.1             | Réponse hébergée corrigée avec extraits exacts           |
| 3.1   | P1       | Copilot Manage et Test              | 2.1             | Réponse native, état enregistré et contrôle préservé    |
| 4.1   | P1       | Copilot Author et Test              | 3.1             | Nouvelle matrice de onze scénarios, tours complets      |
| 5.1   | P1       | Responsable des labs et Test        | 1.1             | Reçus d'acceptation des labs 0, 1, 2 et 3                |
| 6.1   | P1       | Responsable politique et lab        | 1.1             | BYOM connecté pris en charge ou exclusion explicite    |
| 7.1   | P1       | Infrastructure et responsable lab   | 1.1             | Reçus de déploiement et requêtes connectées labs 5/5.1   |
| 8.1   | P2       | Preuves et publication              | 4.1,5.1,6.1,7.1 | Preuves bilingues, nettoyage et contrôles de livraison |

Les étapes 5.1, 6.1 et 7.1 peuvent avancer indépendamment après 1.1 si leurs
ressources et sessions navigateur ne se chevauchent pas. Évitez les modifications
concurrentes d'un agent partagé. Aucune date de fin n'est annoncée tant que les
dépendances de licence, politique et validation ne sont pas résolues.

## Étapes d'implémentation et tâches exécutables

### 1.1 Fixer les limites de livraison et de coûts

Exigence : REQ-001. Entrées : inventaire privé et reçu de l'extension.

- [ ] T001 [Plan:1.1] Réinventorier l'extension isolée, le Bot, le projet, Search, les embeddings et les identités à partir des preuves privées de propriété. Comparer les identifiants, états, versions et facturation réels. Désigner un propriétaire et une échéance de revue; une balise d'expiration ne supprime rien.
- [ ] T002 [Plan:1.1] Enregistrer l'artefact, le retour arrière limité et les validations attribuables du Product Owner, de l'équipe sécurité et du responsable technique avant déploiement. Conserver les identifiants privés hors du dépôt; publier seulement une référence expurgée.

Sortie : propriété et état courant vérifiés, limites de dépenses et de livraison
explicites. Sans validation, les déploiements dépendants restent bloqués, mais les
travaux documentaires et d'inventaire indépendants peuvent continuer.

### 2.1 Déployer et démontrer la réparation SDK isolée

Exigence : REQ-002. Entrées : [instructions de l'extension](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/README.md)
et [manifeste de déploiement](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/azure.yaml).

- [ ] T003 [Plan:2.1] Réexécuter les 33 tests existants du service, les contrôles de dépendances et de syntaxe. Déployer seulement l'artefact approuvé dans le projet existant. Ajouter versions SDK résolues, version hébergée, journaux de démarrage et cible de retour arrière au reçu sans effacer l'échec précédent.
- [ ] T004 [Plan:2.1] Envoyer une requête Activity authentifiée avec enveloppe complète, dont `serviceUrl`. Vérifier une session réellement hébergée, la récupération et la sélection effectives, les extraits exacts et les comportements d'erreur/abstention. Vérifier les accès aval par l'identité hébergée, pas par les identifiants du développeur.

Sortie : l'erreur de constructeur disparaît dans l'hôte réel et la livraison
fondée sur les sources réussit. Un point de contrôle de disponibilité ne suffit
pas. Garder l'autorisation du point de terminaison inchangée pendant cette
réparation initiale pour ne pas confondre les causes.

### 3.1 Rétablir la livraison native Copilot

Exigence : REQ-003. Entrées : diagnostic enregistré inactif et route de contrôle.

- [ ] T005 [Plan:3.1] Diagnostiquer l'erreur 403 d'identifiant de tenant avec les métadonnées d'appelant et journaux pris en charge. Si nécessaire, exécuter le diagnostic Entra uniquement déjà autorisé sur le point isolé, en conservant Azure RBAC, sans accès anonyme ni permissions larges. Confier les changements gérés à Manage et le YAML à Author.
- [ ] T006 [Plan:3.1] Faire exécuter par Test un diagnostic natif et une question de contrôle inchangée. Capturer action native, corrélation hébergée, fin du tour parent et réponse affichée exacte. Désactiver ensuite le diagnostic, relire indépendamment son état inactif enregistré et vérifier la route d'origine.

Sortie : une réponse native démontre la livraison vérifiée, pas seulement un appel
Activity direct. Si Entra uniquement n'est pas pris en charge ou ne corrige pas
les métadonnées, conserver l'échec et utiliser le support officiel au lieu de
contourner l'autorisation.

### 4.1 Fermer la matrice d'acceptation des onze scénarios

Exigence : REQ-004. Entrées : questions originales et audit des tours complets dans
le [rapport d'exécution](backend-live-2026-10-20.md).

- [ ] T007 [Plan:4.1] Faire corriger par Author uniquement les écarts démontrés de citations littérales, attribution par puce, obligations conditionnelles et couverture d'exemples dans le candidat isolé. Préserver l'accueil sans source, les recherches locales, le routage hybride et le contrôle fonctionnel.
- [ ] T008 [Plan:4.1] Faire exécuter par Test les onze scénarios inchangés dans une nouvelle session native après un précontrôle acquitté. Conserver les réponses finales complètes, `DynamicPlanFinished`, les routes attendues, comparaisons de sources, attributions individuelles, pertinence, applicabilité et couverture des exemples pour chaque cas. Compter les reprises séparément.

Sortie : tous les cas et critères obligatoires passent dans cette nouvelle exécution.
Les captures fusionnées précédentes, quatre réponses extractives backend et notes
génériques de qualité ne remplacent pas cette matrice. En cas d'échec, conserver
la preuve, corriger la cause et reprendre les cas touchés et régressions de routage.

### 5.1 Terminer les labs 0, 1, 2 et 3

Exigence : REQ-005. Entrées : [table de réexécution](live-rerun-2026-10-19.md) et guides.

- [ ] T009 [Plan:5.1] Revérifier pour le [lab 0](lab-00.md) licences, capacité, politique, permissions, quota, outils et budget. Pour le [lab 1](lab-01.md), fermer l'audit historique de réponse complète, navigation de citation et fidélité des corps d'erreur du connecteur aval. Utiliser des destinataires synthétiques/approuvés; ne renvoyer un courriel que si un critère manquant l'exige.
- [ ] T010 [Plan:5.1] Pour le [lab 2](lab-02.md), vérifier la navigation réelle vers le PDF externe et les réponses connectées positives/négatives. Pour le [lab 3](lab-03.md), vérifier télémétrie sur canal publié et confidentialité requise avec corrélation événement/KQL. Un événement authentique ne prouve pas l'absence de tous les identifiants plateforme.

Sortie : chaque lab possède son reçu observé pour tous les identifiants d'acceptation
obligatoires. Conserver l'évaluation échouée initiale et expliciter toute exigence
impossible à satisfaire au lieu de déclarer une réussite complète.

### 6.1 Résoudre le conflit de politique BYOM du lab 4

Exigence : REQ-006. Entrées : [lab 4](lab-04.md), dialogue et politique observés.

- [ ] T011 [Plan:6.1] Faire établir par le propriétaire de politique si le connecteur courant prend en charge Entra sous `disableLocalAuth=true`. Sinon obtenir une exception formelle gouvernée ou une substitution/exclusion documentée et approuvée. Ne pas activer l'authentification locale ni contourner la politique par balises ou YAML.
- [ ] T012 [Plan:6.1] Avec un chemin pris en charge, faire vérifier par Test invocation directe, récupération analysée, prompt connecté, réponses fondées, résultats vides et erreurs. Enregistrer chemin retenu et preuves dans les deux guides du lab 4 et le registre.

Sortie : les critères BYOM connectés réussissent. Une exclusion approuvée modifie
le périmètre déclaré; elle n'est pas une réussite du lab original inchangé.

### 7.1 Terminer les preuves d'intégration des labs 5 et 5.1

Exigence : REQ-007. Entrées : [lab 5](lab-05.md), [lab 5.1](lab-05-1.md), reçus du pipeline privé.

- [ ] T013 [Plan:7.1] Réconcilier le déploiement Terraform corrigé avec ressources requises, versions de fournisseurs, réseaux privés et identités. Préserver les preuves plan/apply et identifier les écarts à la source inchangée; ne pas réappliquer pour reproduire une infrastructure déjà démontrée.
- [ ] T014 [Plan:7.1] Faire exécuter par Test les requêtes connectées restantes, filtres, classement et champs attendus avec les lieux indiqués par les sources. Vérifier la navigation vers les URL d'hôtels originales si requise. Sans URL dans le corpus, consigner la limite et obtenir une décision de périmètre plutôt que fabriquer des liens.

Sortie : les comportements connectés requis passent avec sources traçables et écarts
d'infrastructure documentés. Les réussites d'ingestion privée et de projection restent
des preuves de sous-système, pas de certification intégrale.

### 8.1 Réconcilier preuves, ressources et publication

Exigence : REQ-008. Entrées : nouveaux reçus et [procédure de publication](../publishing.md).

- [ ] T015 [Plan:8.1] Mettre à jour ensemble rapports anglais/français, registres, guides et reçus JSON expurgés. Préserver la chronologie et distinguer réussite, échec, blocage, exclusion et non-exécution. Supprimer uniquement les ressources jetables dont la propriété est vérifiée; sinon enregistrer propriétaire, revue des coûts et rétention explicite.
- [ ] T016 [Plan:8.1] Exécuter tests documentaires, validation canonique, export et validation wiki. Examiner destinations privées et changements humains avant publication autorisée; vérifier ensuite révisions distantes et pages des deux langues. Déclarer l'atelier terminé uniquement contre la liste finale ci-dessous.

Sortie : chaque exigence obligatoire possède une preuve actuelle, la publication
est vérifiée si effectuée et aucune ressource d'essai sans propriétaire, coût expliqué
ou décision de rétention ne reste. Une demande de suppression ne prouve pas l'absence.

## Correspondance des exigences

Ces identifiants structurent les travaux restants, sans créer de nouveaux critères.
Les guides et preuves d'acceptation conservées restent la référence.

| Exigence | Résultat restant                       | Étape | Tâches    | Preuve requise                              |
|----------|----------------------------------------|-------|-----------|---------------------------------------------|
| REQ-001  | Exécution approuvée à coûts maîtrisés   | 1.1   | T001,T002 | Inventaire et validation attribuable         |
| REQ-002  | Réparation SDK réellement hébergée      | 2.1   | T003,T004 | Activity hébergée et extraits exacts         |
| REQ-003  | Livraison native authentifiée          | 3.1   | T005,T006 | Tour complet et relecture d'état             |
| REQ-004  | Acceptation des onze scénarios          | 4.1   | T007,T008 | Nouvelle matrice et audit des sources        |
| REQ-005  | Clôture des labs 0 à 3                  | 5.1   | T009,T010 | Reçus positifs, négatifs et de confidentialité|
| REQ-006  | BYOM lab 4 pris en charge               | 6.1   | T011,T012 | Décision de politique et prompt connecté     |
| REQ-007  | Acceptation connectée labs 5 et 5.1     | 7.1   | T013,T014 | Déploiement et requêtes connectées           |
| REQ-008  | Livraison bilingue honnête et nettoyage | 8.1   | T015,T016 | Docs, publication et relectures de nettoyage |

## Vérification et liste de clôture finale

Depuis la racine du dépôt, utiliser les commandes existantes :

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s scripts -p 'test_*.py' -v
.\.venv\Scripts\python.exe scripts\validate_docs.py
.\.venv\Scripts\python.exe scripts\build_wiki.py --output .wiki-build
.\.venv\Scripts\python.exe scripts\validate_docs.py --wiki .wiki-build
```

Consulter les [instructions du service](https://github.com/devopsabcs-engineering/copilot-studio/blob/main/examples/verified-retrieval/workshop-verified-retrieval/README.md)
pour son environnement virtuel et ses tests. Les essais réels exigent navigateur
ou API pris en charge et authentifiés, ressources isolées approuvées, données sources
réelles et corrélation synthétique unique. Sans navigateur natif, les API peuvent
diagnostiquer le backend, mais l'acceptation native reste bloquée.

Avant toute déclaration de réussite complète :

* Toutes les tâches et tous les critères originaux obligatoires passent, sans
  échec obligatoire masqué par une exclusion.
* Les preuves natives et hébergées correspondent à l'artefact approuvé et préservent
  contenu exact, applicabilité, routage et comportements négatifs requis.
* Validations, rapports bilingues et reçus expurgés concordent avec les résultats;
  aucun secret, original protégé ou résultat inventé n'est publié.
* Les ressources possédées ont un nettoyage vérifié ou une rétention explicite
  à coûts maîtrisés; agents originaux et ressources étrangères restent intacts.
* La validation locale passe et toute publication revendiquée du dépôt/wiki
  a été relue indépendamment.
