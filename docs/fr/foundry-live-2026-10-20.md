---
title: "Résultats réels Foundry et MCP du lab 6 - 2026-10-20"
description: "Tests réels sans clé des embeddings, de la provenance Search, de MCP authentifié et de l'agent Foundry, avec échecs des citations, substitutions API et nettoyage vérifié."
ms.date: 2026-10-20
ms.topic: how-to
---

## Résultat et limites des preuves

[Guide du lab 6](lab-06.md) | [English](../en/foundry-live-2026-10-20.md) | [Registre de tous les labs](live-rerun-2026-10-19.md) | [Résultats expurgés](../assets/runtime-2026-10-19/foundry-results.json)

La poursuite payante isolée a réellement utilisé les services Foundry et Search.
Elle ne certifie pas le lab complet. Le propriétaire avait autorisé les tests
payants des labs ; cela n'implique ni nouvelle approbation de mise en production
ni validation humaine des résultats.

| Contrôle | Résultat réel | Limite |
|----------|---------------|--------|
| Agent Foundry à instructions | API `v1`, marqueur exact, 41 jetons au total | Appel du modèle/agent, pas conversation Copilot |
| Embeddings et index | 24 embeddings Ada002 réels ; trois index de huit entrées ; 1 536 dimensions | Exemples pédagogiques autorisés, pas données d'entreprise |
| Vérification du stockage | 24 vecteurs et champs originaux revérifiés sans régénération | Vecteurs explicitement récupérables |
| Recherche hybride par identité managée | Scores de reclassement sémantique présents | Ne certifie pas tous les classements |
| Provenance GA | 2 passages précis, 20 multisources et 0 non couvert ; 22 correspondances originales exactes | Autre exécution que le précédent résultat Free de 19 |
| MCP direct en préversion actuelle | Titre et contenu original complet exacts renvoyés | La découverte de l'outil seule ne comptait pas comme réussite |
| Appel Foundry monosource | Une approbation contrôlée, un appel MCP réussi, une citation originale exacte | Format et longueur demandés non respectés |
| Première demande multisource | L'agent a limité la question à une source | Cette requête inattendue n'a pas été approuvée |
| Demande multisource corrigée | Version 3 : question complète contrôlée exécutée ; trois titres demandés dans la sortie d'outil | Critère de citations finales exactes échoué |
| Point de terminaison Activity | Activity et Responses activés, version 3 épinglée, autorisation Entra uniquement relue | Pas de conversation Activity ni d'agent connecté Copilot |
| Nettoyage | Trois ressources Azure inventoriées et enfants dédiés supprimés ; absence du groupe vérifiée indépendamment | Aucun montant facturé exact annoncé |

La sortie d'outil multisource contenait deux champs de contenu originaux complets
et les trois titres demandés. Cela ne prouve pas le retour de chaque entrée
originale complète. Les trois citations finales annoncées différaient du contenu
original comme de la sortie d'outil. Le critère de citation exacte a échoué ;
cela ne prouve pas que chaque affirmation factuelle reformulée était fausse.

## 1. Isoler le test et conserver l'authentification sans clé

Utilisez un nouveau groupe approuvé, une étiquette de propriété et un manifeste
privé. La configuration testée utilisait un compte AIServices S0 et un projet
en Sweden Central, Search Basic en West US 2, GPT-4o et `text-embedding-ada-002`.
La capacité configurée était 10 pour chaque modèle. Le cycle de vie de GPT-4o a
été vérifié pour ce test ; sa réussite n'en fait pas une recommandation pour
une nouvelle application de production.

Conservez l'authentification locale désactivée. Attribuez Search Index Data Reader
à l'identité du projet sur le nouveau Search, et Cognitive Services OpenAI User
à l'identité Search sur le nouveau compte de modèles. Les droits de création et
de chargement appartiennent à l'opérateur autorisé, sur le seul service dédié.
Ne réutilisez pas de projets sans rapport et n'accordez pas de droits de données
à l'échelle de l'abonnement.

La création ARM Search a refusé l'association de `disableLocalAuth: true`
et d'un `authOptions` non nul. Retirer `authOptions` a préservé le mode sans clé.
Les états de provisionnement étaient en minuscules ; normalisez leur casse
pendant l'attente, sans ignorer les échecs/annulations ni supprimer le délai limite.

## 2. Vérifier les embeddings réels et la provenance avant MCP

1. Gardez les trois listes originales de huit entrées privées et inchangées.
2. Générez les véritables embeddings de 1 536 dimensions. Examinez chaque résultat
   de chargement, puis vérifiez les nombres de documents dans un délai borné :
   la visibilité n'est pas immédiate.
3. Préservez exactement `id`, `title` et `content`, une configuration sémantique
   et un vectoriseur par identité managée aligné sur le modèle déployé.
4. Définissez explicitement `retrievable` à `true` pour inspecter les vecteurs
   stockés. Son omission dans ce test rendait le champ non récupérable ;
   sa sélection renvoyait HTTP 400.
5. Pour les trois index dédiés, activer la récupération par modification du schéma
   a fonctionné sans suppression de documents ni nouveaux embeddings. La réponse
   était HTTP 204 ; relisez définition/données au lieu d'exiger un corps JSON.
6. Utilisez l'API GA Search `2026-04-01` pour le contrôle minimal/extractif du
   [guide du lab 6](lab-06.md). Reliez `ref_id` des passages à `id` des références
   après normalisation explicite en chaînes, en refusant les doublons normalisés.
   La réponse observée utilisait des entiers pour les passages et des chaînes
   pour les références.
7. Reliez `activitySource` à l'activité et à sa source de connaissances, puis
   `docKey` à l'entrée originale. Exigez l'égalité exacte du titre et du contenu.
   Ni un libellé produit par le modèle ni `sourceData`, parfois nul, ne prouvent
   la provenance.

Le test payant a renvoyé 22 passages correspondant exactement aux originaux.
Ces nombres sont observés, pas garantis pour de futurs classements.
La question témoin non couverte a renvoyé zéro passage.

## 3. Utiliser le schéma MCP réel, pas les arguments d'une ancienne préversion

L'adresse MCP testée suivait ce modèle :

```text
https://<owned-search>.search.windows.net/knowledgebases/<owned-kb>/mcp?api-version=2026-08-01-preview
```

Utilisez un jeton Search d'audience `https://search.azure.com/` et acceptez JSON
ou les événements SSE. Envoyez `tools/list`, vérifiez l'outil de lecture attendu
et examinez `inputSchema` avant l'appel. La préversion d'août déclarait une seule
propriété obligatoire, `query_variants` : un tableau contenant une question
naturelle complète de 400 caractères maximum.

L'exemple suivant illustre le contrat ; ce n'est pas la question protégée du test :

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "knowledge_base_retrieve",
    "arguments": {
      "query_variants": ["Quelles sources décrivent la procédure d'enquête approuvée ?"]
    }
  }
}
```

La préversion de mai déclarait `queries`. Elle signalait un modèle de planification
manquant alors que sa propre relecture de configuration montrait un modèle.
La cause de cette divergence n'a pas été établie. Envoyer `queries` à la préversion
d'août échouait également, avec une erreur exigeant `query_variants`. L'appel avec
l'argument réellement déclaré par la préversion d'août a réussi.

La base disposait d'une configuration GPT-4o sans clé pour la planification,
d'un raisonnement faible et d'une sortie extractive, relus par les API de préversion.
Ces propriétés n'appartiennent pas à la configuration GA minimale. Le contenu MCP
natif ne fournissait pas les tableaux activité/références distincts de l'API
retrieve ; aucun nombre de jetons ni trace indépendante du planificateur interne
n'est annoncé.

## 4. Créer et vérifier indépendamment la connexion du projet

La version installée d'`azd` exigeait un environnement local initialisé, même avec
l'adresse explicite du projet. Sans connexion existante, elle exigeait aussi
`AZURE_AI_PROJECT_ID` complet enregistré dans cet environnement local.

Utilisez un répertoire privé vide, pas un projet applicatif partagé.
Remplacez chaque valeur fictive par celle du nouveau manifeste dédié.
Ces commandes initialisent le contexte local et créent une connexion ;
elles n'exécutent pas `azd up` et ne provisionnent pas d'autre environnement :

```powershell
$env:AZURE_DEV_USER_AGENT = 'microsoft_foundry_skill'
azd init --minimal --environment lab6-validation --subscription '<subscription-id>' --location swedencentral --no-prompt
azd env set AZURE_AI_PROJECT_ID '<full-owned-project-ARM-ID>' --environment lab6-validation
azd ai connection create lab6-search-mcp --kind remote-tool --target '<owned-MCP-URL>' --auth-type project-managed-identity --audience 'https://search.azure.com/' --project-endpoint '<owned-project-endpoint>' --no-prompt
azd ai connection show lab6-search-mcp --project-endpoint '<owned-project-endpoint>' --no-prompt --output json
```

Définissez la variable user-agent uniquement dans le processus courant, jamais par
`azd env set`. Gardez le rattachement du projet privé. Relisez les propriétés ARM
et exigez la cible dédiée exacte, la catégorie `RemoteTool`, l'authentification
`ProjectManagedIdentity` et l'audience Search. L'appel authentifié de l'agent,
pas seulement la recherche interactive, teste ensuite cette connexion.

## 5. Créer une version actuelle et contrôler chaque approbation

Le SDK Projects `2.0.0b3` épinglé par le support refusait localement la création
avec l'API `v1`, pourtant acceptée par le service. La substitution fonctionnelle
utilisait le REST documenté
`POST /agents/<name>/versions?api-version=v1`. Le client épinglé fournissait
toujours le client OpenAI Responses ; aucun interpréteur partagé n'a été mis à jour.
L'outillage de gestion Foundry MCP avait un échec distinct de chaîne
d'identifiants ; cela ne prouvait pas l'échec de l'authentification Azure CLI.

Limitez MCP à l'adresse dédiée et à un outil de lecture. Le serveur a normalisé
la liste d'outils sous cette forme à la relecture :

```json
{
  "type": "mcp",
  "server_label": "training-kb",
  "server_url": "<owned-MCP-URL>",
  "project_connection_id": "lab6-search-mcp",
  "allowed_tools": {"tool_names": ["knowledge_base_retrieve"]},
  "require_approval": "always"
}
```

Appelez le client Responses avec un `agent_reference` explicite contenant
`name`, `version` et `type: agent_reference`. Utilisez un état neuf pour chaque
question indépendante, une sortie bornée et au plus un appel d'outil par test.

1. Examinez serveur, outil et arguments décodés de chaque `mcp_approval_request`.
2. Approuvez seulement la question complète prévue. N'approuvez pas une requête
   réduite uniquement parce qu'elle cite une source connue.
3. Envoyez `mcp_approval_response` avec le bon identifiant et
   `previous_response_id` ; examinez la sortie et l'erreur du véritable `mcp_call`.
4. Comparez les citations finales au résultat d'outil comme au texte original.
5. Réanalysez localement les réponses réussies conservées plutôt que de répéter
   les appels acceptés pour obtenir des preuves.

La citation monosource de la version 2 était une sous-chaîne originale exacte de
574 caractères. Son JSON encadré de Markdown et sa longueur ne respectaient pas
le format ni la limite demandée de 160 caractères ; ces écarts restent consignés.
La demande multisource de la version 2 n'a pas été approuvée car elle ne visait
qu'une source. Une correction bornée des instructions en version 3 a produit
la question complète contrôlée et un appel MCP réussi. Ses extraits finaux de
171, 166 et 170 caractères n'étaient pas des citations exactes.
L'acceptation de la réponse finale multisource reste donc en échec.

## 6. Distinguer la configuration Activity d'une vraie conversation

La configuration prise en charge utilisait
`PATCH /agents/<name>?api-version=v1` et le type de contenu
`application/merge-patch+json`. Elle activait `activity`, préservait `responses`,
gardait l'autorisation Entra uniquement et épinglait la version 3 avec une règle
`FixedRatio` à 100 %. Un GET indépendant a vérifié ces quatre propriétés.

Aucune requête Activity, publication Teams ni conversation d'agent connecté
Copilot n'a été exécutée. N'inventez pas d'adresse de rappel pour simuler ce test.
L'autorisation du canal exige une revue distincte ; une relecture Entra uniquement
ne prouve pas tous les prérequis d'intégration Copilot/Teams.

## 7. Préserver des preuves fidèles et retirer l'environnement payant

Le navigateur Foundry a atteint l'accueil/la route de connexion, puis signalé
un magasin IndexedDB manquant. Cela ne prouve pas des identifiants utilisateur
invalides. Aucune nouvelle capture d'exécution du produit authentifié n'a été
obtenue. La [galerie existante](evidence.md) reste utile avec ses mentions de
provenance ; les figures historiques ne sont pas renommées comme preuves de ce test.

Le nettoyage a vérifié identifiant exact du groupe, étiquette de propriété et
liste de ressources autorisées avant suppression. Azure inventoriait trois
ressources dédiées ; modèles, connexions, versions d'agent, index et autres enfants
ont été retirés avec leurs ressources parentes. Une requête indépendante
d'existence du groupe a renvoyé false.

Réponses brutes, sources, identités, adresses et jetons privés n'ont pas été publiés.
Le JSON public a été généré depuis les vrais résultats, comparé aux réponses
conservées et contrôlé contre les marqueurs d'identifiants/secrets privés.

Pour terminer le lab, rétablissez l'expérience standard Copilot prise en charge,
corrigez et rejouez le critère de réponse finale fondée, puis exécutez les cas
originaux bilingues de routage, refus d'accès, Activity et agent connecté.
Ne recréez un environnement payant que dans le périmètre autorisé et supprimez-le
après les tests. La publication documentaire ne certifie pas le lab complet.

## Références actuelles

- [Création de base Search et distinctions entre API](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Contrat retrieve et MCP](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-retrieve)
- [Outils MCP Foundry et approbations](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Versions, protocoles et autorisation Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-agent)
- [Prérequis de connexion Foundry dans Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent)
