---
title: "Atelier 6 : Recherche Foundry IQ et évaluation d'agents connectés"
description: "Examinez un notebook de recherche multisource, adaptez les API Foundry actuelles et évaluez un agent standard Copilot Studio sans confondre contrôle statique et preuve réelle."
ms.date: 2026-10-20
ms.topic: tutorial
---

## Objectif et état des preuves

[Index des ateliers](index.md) | [English](../en/lab-06.md) | [Recherche Search](lab-05.md) | [Revue d'infrastructure](lab-05-1.md)

Distinguez quatre responsabilités : Copilot Studio gère la conversation ; un agent Foundry connecté effectue le travail approfondi ; une base de connaissances Search récupère des passages de plusieurs sources ; un modèle rédige la réponse. Model Context Protocol (MCP) expose l'outil de recherche à l'agent Foundry. Prévoyez 120 à 180 minutes après la fourniture des ressources et la revue de compatibilité par un administrateur.

> [!WARNING]
> La nouvelle connexion externe manuelle est **Connected** et l'inférence Responses
> directe réussit. La liaison de cible Activity native a réussi, sans réponse
> connectée observée. Le nouveau compte/projet, modèle Standard capacité 1 et agent
> restent **actifs pour diagnostic** ; le tag d'expiration ne supprime rien.
> Les anciennes preuves de suppression ne couvrent pas cette exécution.
> Voir les [limites actuelles](backend-live-2026-10-20.md#connexion-externe-manuelle-réussie-réponse-activity-non-vérifiée).

> [!IMPORTANT]
> Des tests réels de dépendances complètent désormais la première revue syntaxique.
> L'environnement actuel a échoué sur une importation parmi 15 : la classe de
> raisonnement de la cellule 14 a quitté `indexes.models` dans le SDK Search 12.0.0. Un environnement
> isolé restauré aux versions du support a réussi les 15 importations. Les 24
> enregistrements ont aussi passé les contrôles locaux de champs et d'identifiants.
> Une recherche cloud GA gratuite a ensuite indexé les 24 enregistrements dans trois
> sources : 2 passages précis, 17 multisources et zéro pour la question non couverte.
> Les 19 passages correspondaient exactement aux originaux. Un test payant ultérieur
> a généré les 24 embeddings, vérifié vecteurs/champs stockés et comparé exactement
> 22 passages récupérés. La recherche MCP authentifiée et un appel d'outil par
> l'agent Foundry monosource ont réussi. Les citations finales multisources ont
> échoué ; Activity a été configuré sans conversation Activity/Copilot.
> Consultez les [résultats Foundry et la procédure API actuelle](foundry-live-2026-10-20.md).

La reprise approuvée ultérieure a produit **3/3 citations sources exactes dans
chacune de deux exécutions**, mais les références natives étaient vides.
Le modèle s'est abstenu malgré sept documents hors sujet récupérés.
Les quatre environnements jetables successifs ont été supprimés, avec absence
vérifiée indépendamment. Consultez les
[limites de la reprise](foundry-live-2026-10-20.md#8-reprise-approuvée-des-citations-exactes-et-échec-des-références-natives) ;
cela ne certifie pas l'acceptation Copilot/Activity connecté.
Le dernier test au format pris en charge a encore produit zéro annotation
native et trois URL de documents inventées. Les phrases sources restaient
fidèles, avec des espaces Markdown finaux. Le cinquième environnement a aussi
été supprimé ; les cinq groupes et dix lectures ARM compte/Search ont été
vérifiés absents/404 indépendamment. Aucune correction répétée n'a suivi.

Copilot Studio est devenu utilisable pour les véritables tests de recherche et
d'envoi du Lab 1, puis Preview est redevenu vide par intermittence. Un inventaire
ultérieur explicitement limité à l'abonnement a trouvé sept composants Application
Insights sans rapport, corrigeant la première mention d'absence. Ils n'ont pas été
réutilisés. Les ressources Search Free isolées ont été supprimées après les tests.
Le compte Foundry payant, son projet, ses modèles, Search et sa connexion MCP
ont ensuite été testés puis supprimés, avec absence du groupe vérifiée
indépendamment. Une future exécution connectée exige un nouvel environnement
autorisé ; aucune adresse active n'est volontairement conservée.

Le texte protégé, le code du notebook et ses exemples intégrés ne sont pas republiés. Les quatre figures proviennent uniquement du document d'accompagnement non protégé consacré à Copilot, avec masquage des données sensibles. Ce sont des captures historiques du support, pas des preuves d'exécution nouvellement capturées.

## 1. Confirmer les prérequis et choisir la bonne expérience

La vraie tentative ultérieure de connexion Foundry de premier niveau a utilisé
un projet dédié réel, mais la fenêtre de consentement était bloquée par le
navigateur hôte. Un seul essai, sans consentement ni connexion sauvegardée.
Aucune conversation Activity connectée n'est comptée. L'environnement jetable
a ensuite été supprimé avec contrôles indépendants. Voir
[l'échec d'authentification](backend-live-2026-10-20.md#authentification-formelle-foundry-toujours-bloquée)
et le [nettoyage](../assets/runtime-2026-10-20/search-accesskey-cleanup.json).

Une [reprise via Edge externe](backend-live-2026-10-20.md#reprise-foundry-via-edge-externe)
a atteint le vrai formulaire Entra, mais la saisie du point restait vide et
Create désactivé. Aucune soumission d'authentification. Il s'agit d'un blocage
de saisie automatisée, non d'un rejet externe ou d'une réussite d'agent connecté.
Le relais manuel était indisponible ; aucun modèle ni appel d'inférence ajouté.
Une nouvelle lecture native a vérifié l'absence de connexion dédiée.
Le [nettoyage d'authentification seule](../assets/runtime-2026-10-20/foundry-external-auth-cleanup.json)
a vérifié projet/compte/groupe à 404 ; l'enregistrement de récupération du compte
reste présent sans purge. Un futur essai exige un nouveau point approuvé.

Un [contrôle supplémentaire de saisie sans ressource](backend-live-2026-10-20.md#prérequis-supplémentaire-de-saisie-native-toujours-bloqué)
n'a pu mettre le navigateur au premier plan ni ouvrir le formulaire. Arrêt
avant toute sonde Legacy, sans soumission d'authentification. Un
[contrôle ultérieur dans le navigateur intégré partagé](backend-live-2026-10-20.md#saisie-rétablie-dans-le-navigateur-partagé-non-authentification-externe)
a ouvert le formulaire au clavier et vérifié une saisie inoffensive, puis annulé.
Cela ne prouve ni la reprise Edge externe ni la levée du blocage de fenêtre
d'authentification intégré.

Après prolongation approuvée de l'essai, la vraie fenêtre Microsoft Foundry du
brouillon Standard isolé proposait **Microsoft Entra ID User Login** et exigeait
un Azure AI Project Endpoint, sans champ de clé. Les exigences officielles
imposent toujours un agent du nouveau portail compatible Activity. Le sélecteur
d'identifiant en aval et la conversation n'ont pas été exercés durant cette
inspection en lecture seule. Cela établit une interface de connexion sans clé,
non la réussite d'un agent connecté. Voir les
[contrats observés](../assets/runtime-2026-10-20/advanced-integration-contracts.json).

1. Terminez la création d'un agent standard et l'[atelier 5](lab-05.md), ou obtenez une infrastructure Search équivalente et autorisée.
2. Ouvrez l'[expérience des agents standard](https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences). Les étapes Connaissances, Agents et volet de test suivantes visent le harnais standard.
3. Distinguez l'orchestration du harnais : un agent standard peut utiliser l'orchestration générative ou classique. Utilisez la générative pour sélectionner l'agent selon ses métadonnées, ou invoquez-le explicitement depuis une rubrique pour un test déterministe.
4. Confirmez que l'environnement Copilot et le projet Foundry appartiennent au même locataire Microsoft Entra prévu. Utilisez la même identité professionnelle si la politique l'autorise. Un locataire identique ne donne pas automatiquement les droits.
5. Demandez à l'administrateur un nouveau projet Microsoft Foundry, un modèle pris en charge, un déploiement de plongements et Azure AI Search dans une région compatible avec les fonctions choisies.
6. Confirmez les droits de gestion d'objets Search, de chargement et de recherche. L'identité utilisée par la connexion Foundry doit pouvoir interroger Search ; votre requête interactive réussie ne prouve pas les droits du projet.
7. Confirmez les rôles de création d'agents et de connexions Foundry. Le guide MCP actuel cite Foundry User pour les agents et Foundry Project Manager pour une connexion d'authentification MCP ; certains portails affichent encore les anciens noms Azure AI.
8. Faites approuver les coûts Search/modèles, les droits sur les sources, les chemins réseau et l'utilisation des préversions avant l'exécution.

![Capture originale masquée du point d'entrée de création dans Copilot Studio](../assets/lab-06/image1.png)

Figure 1. Capture originale masquée du document d'accompagnement, `image1.png`. Repère visuel uniquement : choisissez l'expérience standard actuelle sans supposer que la page historique est inchangée.

## 2. Inventorier le package et corriger les hypothèses de chemin

Le package examiné contient `requirements.txt` et `.env.example` à la racine, `notebooks\foundry-IQ-agents.ipynb`, `data\quick_reference_guide.docx` et un document d'installation. Ces ressources privées ne sont pas copiées dans ce dépôt.

1. Obtenez le dossier complet autorisé auprès de l'animateur. Gardez-le séparé de ce dépôt de documentation.
2. Vérifiez que les dépendances et le modèle d'environnement sont à la racine, pas dans `notebooks`.
3. Confirmez le fichier fourni `data\quick_reference_guide.docx`. Le support d'installation mentionne `data\copilot_knowledge\quick_reference_guide.md`, absent du package examiné.
4. N'attendez pas 24 fichiers de données séparés. Le notebook contient trois listes intégrées de huit entrées. Ces 24 éléments sont des enregistrements d'exemple, pas un corpus d'entreprise automatiquement synchronisé.
5. Copiez `.env.example` vers un `.env` privé uniquement dans une copie de travail autorisée. Ne placez ni secrets ni adresses privées dans une sortie partagée.
6. Vérifiez le répertoire de travail du noyau. Le chargeur lit `.env` dans le parent du répertoire courant, et non de manière fiable à partir du fichier notebook. Un noyau démarré à la racine peut chercher un niveau trop haut.
7. Positionnez le noyau dans le dossier `notebooks` autorisé avant le chargement, ou faites revoir une correction du chemin dans la copie de travail. Vérifiez le chemin résolu sans afficher les valeurs.

| Variable                          | Signification et validation                                                                           |
| --------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `AI_FOUNDRY_PROJECT_ENDPOINT`     | Adresse du plan de données du nouveau projet Foundry prévu                                            |
| `AZURE_AI_MODEL_DEPLOYMENT_NAME`  | Nom réel du déploiement autorisé, pas seulement nom du catalogue                                      |
| `AZURE_AI_SEARCH_ENDPOINT`        | Adresse du service Search prévu ; le message de validation l'abrège à tort en `AZURE_SEARCH_ENDPOINT` |
| `AZURE_OPENAI_ENDPOINT`           | Adresse de ressource adaptée au client de plongements                                                 |
| `EMBEDDING_MODEL_DEPLOYMENT_NAME` | Déploiement produisant exactement les dimensions du schéma                                            |
| `PROJECT_RESOURCE_ID`             | Identifiant Azure complet du type réel de projet utilisé pour créer la connexion                      |

Ne confondez pas adresse du projet, adresse Search, identifiant de ressource ARM et identifiant d'agent. Ils servent des API différentes.

## 3. Résoudre la compatibilité avant Run All

> [!WARNING]
> Ne sélectionnez pas Run All sur un service Search partagé. Des cellules précoces suppriment la base de connaissances, les sources et les index portant les noms configurés. Utilisez un espace de noms ou service jetable approuvé, examinez les cibles et obtenez l'accord de l'animateur avant ces cellules.

| Élément examiné                                                                                | Signification                                                                           | Décision nécessaire                                                                                                                                       |
| ---------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `azure-ai-projects==2.0.0b3` et `azure-search-documents==11.7.0b2`                             | Versions instantanées de SDK en préversion épinglées                                    | Reproduire seulement en environnement isolé approuvé, ou migrer une copie avec les exemples actuels ; l'analyse syntaxique ne prouve pas la compatibilité |
| Message initial de disponibilité                                                               | La première cellule n'installe ni ne vérifie les packages                               | Contrôler l'environnement réel ; une icône de succès imprimée n'est pas une preuve                                                                        |
| Plongement par défaut `text-embedding-3-large`, dimension `3072`                               | Différent des 1 536 dimensions du déploiement de l'atelier 5.1                          | Fournir un modèle compatible autorisé ou revoir ensemble schéma, modèle et dimensions                                                                     |
| Conversation par défaut `gpt-4o`                                                               | Une chaîne par défaut ne garantit pas un déploiement ; GPT-4 est soumis au cycle de vie | Choisir un déploiement disponible pris en charge et rejouer les tests de qualité                                                                          |
| API de plongement `2024-02-01`                                                                 | Distincte des API Search et agents Foundry                                              | Vérifier le modèle retenu ; ne pas remplacer globalement toutes les versions                                                                              |
| URL MCP Search avec `2025-11-01-Preview`                                                       | Orthographe et contrat historiques de préversion                                        | Aligner URL, SDK et schéma avec une version prise en charge ; changer casse ou date ne suffit pas                                                         |
| Raisonnement minimal et sortie extractive                                                      | Search renvoie des passages sans planification LLM dans cette configuration             | Ne pas affirmer qu'une planification Search automatique à plusieurs étapes est démontrée                                                                  |
| Requête ARM déclarant `Microsoft.MachineLearningServices/workspaces/connections` en préversion | Une déclaration de l'époque hub/workspace peut ne pas correspondre au nouveau projet    | Vérifier identifiant réel et procédure de connexion actuelle avant l'envoi                                                                                |
| Échec de connexion seulement signalé                                                           | Les cellules suivantes peuvent continuer sans connexion                                 | Arrêter sur un statut non réussi et contrôler la connexion indépendamment                                                                                 |
| MCP `require_approval` à `never`                                                               | Outil de recherche autorisé sans demande d'approbation                                  | Limiter au point Search en lecture seule autorisé ; ne pas étendre aux outils d'écriture                                                                  |
| Instructions demandant des libellés de sources                                                 | Un libellé rédigé par le modèle ne prouve pas une citation issue de la recherche        | Examiner résultats d'outil et passages, pas seulement la réponse                                                                                          |
| Suppressions finales commentées                                                                | Exécuter la dernière cellule ne supprime pas les ressources                             | Effectuer un nettoyage distinct approuvé et vérifier la suppression réelle                                                                                |

Le [guide actuel des bases de connaissances](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base) distingue `2026-04-01` stable, minimal/extractif, et les fonctions `2026-08-01-preview`, telles que planification LLM et synthèse. La [liste des API](https://learn.microsoft.com/en-us/rest/api/searchservice/search-service-api-versions) mentionne encore `2025-11-01-preview` ; cela ne prouve pas sa compatibilité avec les clients Python épinglés.

Le modèle Foundry extérieur peut décider comment appeler un outil même si Search utilise une récupération minimale. Il s'agit de couches d'orchestration différentes. Aucun gain de pertinence, de temps de recherche ou de conformité n'est démontré par les ressources locales.

Consultez le [démarrage rapide de recherche agentique](https://learn.microsoft.com/en-us/azure/search/search-get-started-agentic-retrieval), le [guide des connexions de projet](https://learn.microsoft.com/en-us/azure/foundry/how-to/connections-add) et le [guide MCP](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol) pour la compatibilité. Ne copiez pas d'identifiants externes et n'accordez pas de droits sur tout l'abonnement pour contourner un écart.

### Variante GA testée pour le point de contrôle de récupération

L'exécution réelle a utilisé l'API REST Search `2026-04-01` plutôt que de migrer
tous les SDK du notebook en préversion. Les requêtes ci-dessous reproduisent ce
contrat ; les noms d'objets sont illustratifs. Le service temporaire a été
supprimé. Utilisez uniquement un service jetable approuvé et les données locales
autorisées de l'atelier. N'envoyez pas ces PUT à des objets partagés existants :
PUT peut remplacer leur définition. Ce parcours ne crée ni agent Foundry ni
connexion MCP.

1. Chargez les trois listes originales de huit entrées dans trois index distincts.
   Chaque entrée doit garder ses champs `id`, `title` et `content`. Configurez
   une configuration sémantique `training-semantic` utilisant titre et contenu ;
   vérifiez huit chargements réussis par index et 24 au total. Aucun plongement
   généré ni déploiement de modèle externe n'est nécessaire pour cette variante.
2. Pour chaque index, envoyez
   `PUT /knowledgesources/<source-name>?api-version=2026-04-01` au point de
   terminaison Search approuvé avec du JSON et l'authentification autorisée.
   Le nom de source doit être identique dans le chemin et le corps. Adaptez les
   noms de source et d'index pour chacune des trois sources.

```json
{
  "name": "fraud-ks",
  "kind": "searchIndex",
  "searchIndexParameters": {
    "searchIndexName": "fraud-index",
    "semanticConfigurationName": "training-semantic",
    "sourceDataFields": [
      {"name": "id"}, {"name": "title"}, {"name": "content"}
    ]
  }
}
```

3. Envoyez `PUT /knowledgebases/workshop-training-kb?api-version=2026-04-01`.
   Exigez HTTP 200 ou 201 et vérifiez les trois noms de sources renvoyés.
   N'ajoutez pas les anciennes propriétés de raisonnement ou de mode de sortie
   propres à la préversion.

```json
{
  "name": "workshop-training-kb",
  "description": "Isolated workshop retrieval test",
  "knowledgeSources": [
    {"name": "fraud-ks"},
    {"name": "compliance-ks"},
    {"name": "investigation-ks"}
  ]
}
```

4. Envoyez
   `POST /knowledgebases/workshop-training-kb/retrieve?api-version=2026-04-01`
   avec le corps suivant. Exigez HTTP 200. Gardez les réponses brutes dans un
   espace privé pour comparaison ; publiez seulement des assertions expurgées.

```json
{
  "intents": [
    {"type": "semantic", "search": "fraud investigation compliance"}
  ],
  "knowledgeSourceParams": [
    {"knowledgeSourceName": "fraud-ks", "kind": "searchIndex"},
    {"knowledgeSourceName": "compliance-ks", "kind": "searchIndex"},
    {"knowledgeSourceName": "investigation-ks", "kind": "searchIndex"}
  ]
}
```

5. Vérifiez les champs racine `response`, `activity` et `references`.
   Analysez le texte de réponse comme une liste JSON de passages contenant
   `ref_id`, `title` et `content`. Associez références et passages par identifiant
   de référence, puis reliez le `docKey` de chaque référence à l'entrée originale
   de la source correspondante. Exigez l'égalité exacte du titre et du contenu ;
   ne dépendez pas de `sourceData`, qui était nul dans les références observées.
6. Recommencez avec le titre exact de la première entrée de fraude, puis
   `zqxvunicornasteroidorchard`. L'exécution observée a renvoyé 2, 17 et 0 passages
   pour les requêtes précise, multisource et sans correspondance respectivement.
   Ces nombres sont des observations, pas une garantie de classement futur.
   Le cas multisource couvrait les trois sources ; les 19 passages renvoyés
   correspondaient aux originaux. Arrêtez sur champ absent, chargement échoué,
   statut HTTP non réussi, source incorrecte ou texte modifié.
7. Supprimez uniquement les ressources jetables appartenant à la session après
   collecte des preuves, puis vérifiez indépendamment leur absence. Les
   [résultats cloud expurgés](../assets/runtime-2026-10-19/free-cloud-results.json)
   consignent l'exécution réelle et le nettoyage.

Cela prouve une récupération Search multisource minimale et extractive, pas la
planification LLM, la synthèse de réponses, les plongements sémantiques générés,
l'appel d'outil Foundry ni une conversation avec un agent connecté Copilot.

## 4. Exécuter par points de contrôle et distinguer les couches testées

La poursuite payante a exécuté les points de contrôle embeddings, Search, MCP et
agent Foundry ci-dessous, avec des résultats d'acceptation mixtes. La
[procédure API actuelle](foundry-live-2026-10-20.md) consigne les substitutions,
la réussite monosource et l'échec des citations finales multisources.
La séquence originale d'agent connecté Copilot reste non exécutée.

1. Faites préparer un environnement dédié et revoir les dépendances épinglées ou leur migration testée. Installez uniquement dans cet environnement, jamais dans un interpréteur système partagé.
2. Sélectionnez cet environnement comme noyau. Vérifiez les versions avant toute cellule ; l'analyse syntaxique Python 3.14.3 ne certifie pas ce runtime pour les anciennes dépendances.
3. Chargez la configuration et confirmez les six paramètres. Authentifiez l'utilisateur selon le parcours Azure CLI approuvé. N'affichez pas les jetons.
4. Inspectez les trois listes intégrées. Les nombres attendus sont `8`, `8` et `8`. Leur contenu reste pédagogique, pas un conseil financier ou juridique.
5. Examinez les noms ciblés par la cellule de réinitialisation/suppression. Arrêtez-vous si un objet appartient à une autre session.
6. Créez les trois index dans le périmètre jetable. Examinez clés, texte interrogeable, dimensions vectorielles et configurations sémantiques.
7. Produisez les plongements et chargez les entrées. Examinez chaque résultat individuel : un appel par lot sans exception peut contenir des échecs. Vérifiez huit documents dans chaque index d'essai non modifié, soit 24.
8. Créez une source par index, puis une base qui référence les trois. Confirmez les définitions renvoyées plutôt qu'un message imprimé.
9. Testez directement la recherche avant l'agent. Vérifiez passages, identifiants de sources et contrôle d'accès. Un index rempli ne prouve pas que l'API de base de connaissances fonctionne.
10. Créez la connexion MCP de projet approuvée avec la méthode actuelle adaptée au projet. Confirmez cible, audience du jeton Search, identité et droits. Arrêtez dès qu'une création échoue.
11. Créez une version d'agent Foundry avec le modèle autorisé et une liste d'outils de recherche restreinte. Conservez nom/identifiant stable et version active dans un espace privé.
12. Testez directement l'agent avec une question monosource puis multisource. Notez appels d'outils et références réelles. Utilisez une conversation neuve pour chaque cas indépendant afin d'éviter la contamination par les réponses précédentes.
13. Excluez des preuves publiques les identifiants de conversation et les corps complets des échanges. Conservez plutôt assertions assainies et mesures de temps.

## 5. Activer le protocole nécessaire à Copilot Studio

La [procédure actuelle d'agent connecté](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent) exige le point de terminaison du **protocole Activity**. Responses et A2A, exposés par défaut, ne suffisent pas.

Le test payant a activé Activity en préservant Responses, épinglé la version 3
et relu une autorisation Entra uniquement. Cela ne prouve ni une conversation
Activity ni l'autorisation propre au canal exigée par Copilot ou Teams.

1. Confirmez la création de l'agent dans la nouvelle expérience de portail/projet Foundry. La documentation du connecteur avertit que l'ancien portail peut produire `404 - Version not found`.
2. Suivez [Configurer et partager l'agent](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-agent) pour activer Activity par l'API REST ou le SDK pris en charge. C'est une modification distincte à faire approuver, pas un bouton disponible dans la capture historique.
3. Confirmez l'identité entrante et le schéma d'autorisation. Les rôles actuels incluent Foundry Agent Consumer pour l'invocation et Foundry User pour la création.
4. Vérifiez la version active de l'adresse stable. Épinglez-la si les réexécutions du notebook ne doivent pas changer automatiquement le comportement connecté.
5. Ne concluez pas à un échec parce que la vue Endpoints n'affiche encore que Responses et A2A : le guide officiel Copilot documente cette omission.
6. Consignez un test Activity réussi avant de déclarer l'intégration terminée.

## 6. Configurer l'agent standard Copilot Studio

1. Dans l'environnement approuvé, créez un agent standard jetable avec un nom et une description génériques de formation.
2. Enregistrez ses détails avant les connaissances ou l'agent connecté.

![Capture originale masquée de la zone de détails de l'agent](../assets/lab-06/image4.png)

Figure 2. Capture originale masquée du document d'accompagnement, `image4.png`. Elle illustre la zone de détails, pas un agent configuré avec succès pendant cette revue.

3. Ajoutez un fichier de référence approuvé aux connaissances. Utilisez le DOCX autorisé si permis, ou créez un court fichier original définissant `ATO` comme `Account takeover`. Ne copiez pas de contacts privés ni de tableaux réglementaires non vérifiés dans un jeu public.
4. Attendez l'état `Ready`. Désactivez le web et retirez les sources sans rapport pendant l'évaluation contrôlée.
5. Rédigez des instructions originales : clarifier les demandes vagues, répondre aux définitions à partir du glossaire, appeler l'agent connecté pour les scénarios détaillés, signaler les preuves absentes et exiger une revue humaine avant toute décision réelle.
6. Dans Agents, choisissez Ajouter un agent, Se connecter à un agent externe, puis Microsoft Foundry.

![Capture originale masquée des choix de connexion à un agent externe](../assets/lab-06/image10.png)

Figure 3. Capture originale masquée du document d'accompagnement, `image10.png`. Menu historique fourni comme repère ; la disponibilité actuelle dépend de l'environnement d'agent standard.

7. Créez ou sélectionnez la connexion Foundry autorisée avec l'adresse du projet. Renseignez l'identifiant attendu par le connecteur actuel pour l'agent stable et décrivez clairement la différence entre recherche approfondie et simple glossaire.
8. L'ancien support appelle « Agent Id » la chaîne du nom de l'agent. Le notebook affiche séparément nom, version et identifiant. Vérifiez contrat et métadonnées actuels ; ne devinez ni UUID ni ancien identifiant d'assistant classique.
9. Enregistrez et testez. Examinez la carte d'activité pour prouver l'utilisation des connaissances locales ou de l'agent connecté.
10. Laissez l'agent non publié sauf exercice distinct autorisé. Enregistrer et tester n'autorise pas une mise en production.

## Matrice d'acceptation et assertions exactes

Utilisez seulement des situations fictives non identifiantes. Le contenu financier du notebook autorisé est pédagogique, pas une référence juridique actuelle. N'évaluez pas les réponses sur des seuils réglementaires codés en dur ni sur l'âge d'un client fictif.

| ID    | Entrée ou contrôle                                                 | Chemin attendu et assertion mesurable                                                   | Résultat actuel                  |
| ----- | ------------------------------------------------------------------ | --------------------------------------------------------------------------------------- | -------------------------------- |
| F6-01 | Analyser les cellules sans les exécuter                            | `11` cellules analysées ; zéro erreur syntaxique                                        | Réussi sur Python 3.14.3         |
| F6-02 | Examiner les listes intégrées                                      | Exactement `8 + 8 + 8 = 24` entrées                                                     | Vérifié par analyse AST statique |
| F6-03 | Examiner les fichiers                                              | Dépendances/environnement racine et vrai DOCX présents ; MD imbriqué absent             | Vérifié localement               |
| F6-04 | « Bonjour, j'ai besoin d'aide pour examiner un cas »               | Demande de précisions ; `0` appel d'agent connecté                                      | Non exécuté                      |
| F6-05 | « Que signifie ATO ? »                                             | Glossaire source pour `Account takeover` ; `0` appel connecté                           | Non exécuté                      |
| F6-06 | « Quels signes examiner pour une prise de contrôle de compte ? »   | Appel d'agent et d'outil ; passage pertinent sur les indices présent                    | Non exécuté                      |
| F6-07 | « Comparez la conservation des preuves à la politique pertinente » | Au moins deux groupes de sources applicables dans les résultats ; aucune règle inventée | Non exécuté                      |
| F6-08 | « Qu'a fait notre client privé hier ? »                            | Aucun événement privé inventé ; absence d'accès/preuve signalée                         | Non exécuté                      |
| F6-09 | Rejouer F6-06 dans l'autre langue en conversation neuve            | Sens étayé et traçabilité identiques ; formulation non figée                            | Non exécuté                      |
| F6-10 | Retirer l'accès d'une identité de test autorisée                   | Refus d'accès ; aucun passage interdit dans la réponse                                  | Non exécuté                      |
| F6-11 | Connecter sans Activity dans un test négatif isolé                 | HTTP `400` avec erreur de protocole Activity ; corriger puis retester                   | Non exécuté                      |
| F6-12 | Vérifier le nettoyage                                              | Connexion, version d'agent, connaissances et index de formation supprimés selon accord  | Groupe Foundry/Search dédié supprimé et absence vérifiée ; aucun objet Copilot créé |

Pour chaque cas réel, notez chemin, sources, résultat des assertions, justification des citations, latence et erreur assainie. La justesse du routage est le nombre de cas bien routés divisé par les cas exécutés. Évaluez séparément les citations. Un libellé rédigé par le modèle ou un succès HTTP ne remplace pas un passage récupéré.

## Dépannage et collecte de preuves

![Capture originale masquée de la gestion de l'authentification des connexions](../assets/lab-06/image14.png)

Figure 4. Capture originale masquée du document d'accompagnement, `image14.png`. Elle illustre la gestion des connexions, sans prouver une connexion authentifiée dans cette session.

| Symptôme                                                     | Vérification et action                                                                                            |
| ------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| ImportError d'une classe d'agent ou de base de connaissances | Confirmez versions SDK et génération d'API ; les bêtas n'exposent pas toutes les mêmes classes                    |
| Configuration absente malgré `.env` rempli                   | Vérifiez répertoire du noyau et chargement depuis son parent ; corrigez dans une copie approuvée                  |
| Message `AZURE_SEARCH_ENDPOINT` manquant                     | Le code lit `AZURE_AI_SEARCH_ENDPOINT` ; distinguez message trompeur et vraie variable                            |
| Dimensions incompatibles                                     | Notebook `3072`, déploiement atelier 5.1 `1536` ; alignez modèle et schéma                                        |
| Avertissement de connexion puis erreur d'outil               | Arrêtez au premier échec ; vérifiez type réel de ressource, droits et existence                                   |
| Search 403 uniquement depuis l'agent                         | Contrôlez identité du projet/de connexion, rôle de lecteur, audience et réseau                                    |
| Connecteur 400 mentionnant Activity                          | Activez Activity via SDK/REST ; Responses/A2A ne suffisent pas                                                    |
| `404 - Version not found`                                    | Vérifiez nouvelle/ancienne expérience Foundry et identifiant de l'agent stable                                    |
| Agent connecté jamais choisi                                 | Différenciez descriptions, confirmez orchestration standard, inspectez la trace ou appelez une rubrique explicite |
| Source ou réponse inattendue                                 | Nouvelle conversation, examen de recherche, retrait des doublons et exigence de sources                           |
| Ressources restantes après la dernière cellule               | Les suppressions sont commentées ; suivez le nettoyage approuvé                                                   |

Capturez de nouvelles preuves seulement après autorisation et accès effectif. Masquez identités, locataire, adresses privées, contenu et identifiants. Ajoutez date, action et résultat observé. Ne présentez jamais les quatre figures historiques comme preuves des tests F6-04 à F6-12.

## Nettoyage et limite de validation

1. Retirez ou déconnectez l'agent Foundry de formation dans Copilot Studio avant de supprimer son arrière-plan. Préservez les connexions partagées.
2. Supprimez seulement les versions et conversations approuvées. Vérifiez la version active de l'agent stable avant toute suppression.
3. Retirez la connexion MCP dédiée si aucun autre agent ne l'utilise.
4. Supprimez la base Search avant ses sources, puis les sources avant les index dédiés.
5. Confirmez la disparition des trois index et de leurs 24 entrées d'exemple. Retirez uniquement les fichiers ou connaissances créés pour cette session.
6. Fermez clients et noyaux locaux, puis retirez `.env` et sorties sensibles selon la politique de conservation.
7. Supprimez l'infrastructure dédiée uniquement avec le [plan de nettoyage 5.1](lab-05-1.md) approuvé. Search, modèles et Foundry peuvent rester facturés après suppression des objets du notebook.

La revue statique, la restauration des dépendances et plusieurs contrôles cloud
sont terminés. Le [registre Foundry payant](foundry-live-2026-10-20.md) distingue
transport et citations monosources réussis des citations finales multisources
échouées. Les cas de routage Copilot F6-04 à F6-11 et une conversation Activity
réelle restent non exécutés. La navigation Copilot standard échouait encore ;
le navigateur Foundry signalait aussi une erreur de magasin IndexedDB.
Ces observations ne prouvent pas des identifiants utilisateur invalides.
Toutes les ressources isolées ont été retirées. Ne certifiez pas le lab complet
avant la réussite effective des critères restants.
