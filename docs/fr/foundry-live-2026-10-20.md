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

## 8. Reprise approuvée des citations exactes et échec des références natives

Après la nouvelle approbation Azure, quatre environnements jetables ont été
testés successivement, jamais simultanément. Chacun utilisait un nouveau groupe
étiqueté avec manifeste de propriété, un compte/projet Foundry sans clé,
Search Basic et GPT-4o/Ada002 de capacité 10. Seuls des rôles limités aux
nouvelles ressources ont été ajoutés ; aucun droit global d'abonnement,
permission applicative ou consentement n'a été modifié.

L'ancien échec conservé a été revérifié : les trois prétendues citations étaient
des reformulations, pas une simple différence d'échappement. Les tentatives
suivantes ont révélé trois problèmes distincts de compatibilité :

1. Le MCP natif en effort low signalait toujours un modèle de planification
   manquant malgré la relecture de configuration. Ce parcours reste non résolu.
2. La recherche minimal fonctionnait, mais le SDK Projects 2.3.0 installé
   n'exposait pas `AgentReference`. Des dictionnaires explicites de référence
   d'agent ont résolu cette incompatibilité SDK.
3. Le schéma réel de l'outil MCP minimal exigeait des requêtes courtes.
   Les trois requêtes par titre ont d'abord été refusées par l'ancien contrôle
   d'approbation exigeant une question complète. Instructions et contrôle ont
   été alignés sur un appel unique contenant les trois titres exacts approuvés.

Des instructions d'extraction explicite, plutôt que de résumé, ont ensuite
produit deux vraies réponses du modèle avec **3/3 citations exactes chacune**.
Les six citations correspondent aux enregistrements originaux et aux sorties
d'outil, avec identifiants, titres et URL de documents de l'index Search
vérifiés indépendamment. Les extraits comportaient 80, 109 et 144 caractères.
Les deux réponses étaient du JSON valide sans bloc Markdown. Chaque réponse
d'outil multisource contenait 24 documents, tous conformes au corpus.
Aucune réponse de remplacement déterministe n'a été substituée.

L'acceptation complète de sortie a néanmoins **échoué deux fois** :
chaque champ `citation` ne contenait que des espaces et les tableaux
d'annotations du texte de sortie étaient vides. Provenance indépendante et
titres corrects ne remplacent pas des références natives. Le contrôle non
couvert a produit la vraie réponse `{"sources":[]}` ; l'abstention du modèle
a réussi, mais l'outil a renvoyé **sept documents hors sujet**. La réussite
technique du MCP ne prouve pas l'absence de documents récupérés.

Les [preuves de reprise expurgées](../assets/runtime-2026-10-20/foundry-quote-recovery.json)
séparent fidélité des extraits, références natives, abstention et précision
de recherche. Textes sources et réponses complètes restent privés.
Aucun agent utilisateur, Activity ou Copilot connecté n'a été modifié
ni testé pendant cette poursuite.

Les quatre groupes dédiés ont été supprimés. La vérification indépendante
de **12:55:32 UTC** a confirmé quatre groupes absents et **huit réponses ARM 404**
pour les quatre paires compte/Search. Seules les ressources du manifeste ont
été supprimées. L'absence ARM ne certifie ni suppression réversible du
fournisseur ni politique de conservation des inférences. L'usage observé est de
**16 184 jetons de réponse d'agent**, **13 288 jetons d'embeddings** et
96 embeddings, soit quatre lots des mêmes 24 enregistrements uniques.
Les métadonnées de raisonnement MCP sont consignées séparément ; ni montant
facturé ni total complet de planification interne n'ont été observés.

La fidélité des extraits est rétablie dans ce test limité. Les références
natives, la recherche sans résultat, le planificateur low et l'acceptation
d'agent connecté restent ouverts. Aucun environnement payant n'est conservé
intentionnellement.

## 9. Diagnostic du contrat de citation avant un nouveau test

Une relecture hors ligne des vraies réponses conservées a réussi **45 contrôles**,
sans appel cloud ni modèle. Elle confirme six associations sources exactes,
six champs JSON de citation vides et zéro annotation native. Dans chaque
réponse d'outil normalisée, les 24 titres externes des documents étaient des URL.
Le titre humain et l'identifiant d'origine figuraient dans `document.content`
décodé en JSON, pas dans ces champs externes.

Le [diagnostic du contrat](../assets/runtime-2026-10-20/foundry-citation-contract.json)
identifie une hypothèse incorrecte du test précédent : ni une correspondance
numérique de marqueurs natifs choisie manuellement, ni l'égalité entre leur
libellé source et ce titre interne n'étaient établies par la réponse réelle
ou le contrat public. L'API utilisait le format texte ; le JSON strict venait
des instructions, pas d'un schéma imposé. Même renseigné, un champ de citation
rédigé par le modèle ne prouverait pas une annotation native du service.

La documentation Microsoft actuelle décrit les annotations natives pour
Foundry IQ MCP, y compris avec la recherche minimal/extractive.
Il est donc incorrect de les déclarer globalement non prises en charge.
Les réponses conservées n'en contiennent toujours aucune ; omission du modèle
et post-traitement du service ne peuvent pas être départagés.

La correction à tester consiste à produire des sections en langue naturelle,
avec citations textuelles inchangées et référence native hors de chaque extrait,
plutôt que des marqueurs construits dans du JSON. Les contrôles de titre,
d'identifiant, d'URL d'outil et d'exactitude restent obligatoires.
Les libellés natifs doivent suivre le service réel ; une URL MCP de repli
documentée ne suffit pas sans métadonnées d'annotation et association unique
à l'enregistrement original. Ce diagnostic hors ligne ne transforme pas
la correction proposée en réussite réelle.

* [Connecter les agents Foundry à IQ](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/foundry-iq-connect)
* [Chaîne de recherche minimal/extractive](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-pipeline)
* [Contrat d'effort de raisonnement](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort)

## 10. Nouveau test réel au format pris en charge, échec et arrêt

La correction issue du diagnostic hors ligne a été testée dans **un seul**
nouvel environnement jetable, avec la configuration minimal/extractive
fonctionnelle et le SDK installé. Seuls les instructions de sortie de l'agent
de test et le validateur ont changé : sections en langue naturelle, titre et
identifiant originaux exacts, vraie URL d'outil, phrase d'ouverture inchangée
et référence native hors de chaque extrait. L'ancienne hypothèse imposant
un libellé natif lié au titre interne dans du JSON n'a pas été appliquée.

Une réponse multisource et un contrôle non couvert ont été exécutés.
Le transport multisource a réussi et les 24 documents récupérés correspondaient
au corpus original. Les trois titres demandés et identifiants étaient corrects.
La relecture indépendante a confirmé les phrases d'ouverture comme sous-chaînes
originales inchangées, chacune suivie de deux espaces de saut de ligne Markdown.
Ces espaces expliquent l'échec de comparaison stricte de la ligne entière ;
les échecs stricts ont été conservés, pas convertis silencieusement en réussites.

Les échecs substantiels d'attribution persistent :

* **0/3** URL de la réponse correspondent aux véritables URL d'outil ;
  les trois adresses de documents ont été inventées par le modèle.
* Les annotations natives réelles Responses restent à **0**, avec **0/3**
  associations natives aux sources. Aucun lien ou marqueur rédigé par le modèle
  n'a été compté comme métadonnée.
* Le contrôle non couvert s'est abstenu, mais l'outil a encore renvoyé
  **sept** documents. La recherche sans résultat n'a pas réussi.

Les [résultats au format pris en charge](../assets/runtime-2026-10-20/foundry-supported-citation-retest.json)
conservent donc **FAIL** pour l'acceptation complète des sources et références
natives. Cela établit un échec pour la configuration/fournisseur testés,
pas une absence globale de prise en charge ni une cause interne prouvée.
Aucune nouvelle réponse multisource, correction de prompt ou création
d'environnement n'a suivi le constat de métadonnées absentes.

Le nouveau groupe dédié a été supprimé. Des contrôles indépendants ont confirmé
son absence et celle des quatre groupes précédents, plus **dix réponses ARM 404**
pour les comptes/Search. Aucune ressource étrangère ni aucun agent utilisateur
existant n'a été modifié. Aucune conversation Activity ou Copilot connecté
n'a été exécutée. L'usage observé de ce test est de **8 324 jetons Responses**
et **3 322 jetons d'embeddings**. Le MCP direct a signalé séparément
**3 466 jetons de raisonnement** ; l'usage interne complet et le montant
facturé n'étaient pas observables. Ce n'est pas un total de facturation.

La suite exige une investigation fournisseur/configuration distincte et bornée,
fondée sur les vraies réponses conservées, pas de nouveaux tests payants
identiques. Les critères d'agent connecté et de l'atelier complet restent ouverts.

## Références actuelles

- [Création de base Search et distinctions entre API](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Contrat retrieve et MCP](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-retrieve)
- [Outils MCP Foundry et approbations](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/tools/model-context-protocol)
- [Versions, protocoles et autorisation Foundry](https://learn.microsoft.com/en-us/azure/foundry/agents/how-to/configure-agent)
- [Prérequis de connexion Foundry dans Copilot Studio](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent)
