---
title: Registre de réexécution réelle - 2026-10-19
description: Recherche PDF et livraison de courriel réellement testées, plan Terraform exécuté, échec SDK reproduit, restauration isolée et conditions cloud restantes.
ms.date: 2026-10-19
---

## Périmètre et résultat actuel

[Tous les labs](index.md) | [English](../en/live-rerun-2026-10-19.md) | [Registre de validation](validation.md)

| Lab | État de l'exécution réelle | Limite d'acceptation restante |
|-----|----------------------------|------------------------------|
| 0 | Identité, rôles, modèles Azure et Terraform portable vérifiés | Autorisation de ressources payantes dédiées |
| 1 | Recherche, refus, annuaire, livraison, clarification, activité de connecteur échouée et hash du PDF téléchargé vérifiés | Audit complet des citations et sortie HTTP brute du connecteur |
| 2 | Véritables indexation documentaire et recherche Search par solution Free | Ingestion Blob, embeddings intégrés et connexion Search Copilot |
| 3 | Inventaire corrigé ; télémétrie sans rapport restée privée | Configuration de l'agent, événement synthétique et preuve KQL corrélée |
| 4 | Procédure BYOM actuelle revue | Appel de modèle autorisé et prompt connecté |
| 5 | 17 assertions réelles Search sur les hôtels réussies | Embeddings sémantiques, découpage et réponse Copilot sourcée |
| 5.1 | Init, validate et plan Terraform de 15 instances réussis | Apply payant d'origine non autorisé ; solution Free temporaire déployée puis nettoyée |
| 6 | 24 enregistrements, 3 index/sources, recherche minimale réelle et 19 passages exacts | Modèle/agent Foundry, MCP, Activity et parcours d'agent connecté Copilot |

Il s'agit du suivi d'exécution demandé après la première revue documentaire.
Les contrôles ci-dessous ont réellement été exécutés. Ils ne signifient pas que
l'ensemble de l'atelier a réussi. Les
[résultats structurés et nettoyés](../assets/runtime-2026-10-19/results.json)
conservent versions, nombres et erreur observée, sans identifiants de locataire,
chemins privés, secrets ou état Terraform.

## Lab 0 - Précontrôle réel de l'environnement

Azure CLI s'est authentifié dans l'abonnement d'atelier sélectionné. L'identité courante
dispose de droits de création et d'attribution de rôles ; les rôles observés comprennent
Owner et Foundry User au niveau de l'abonnement. Cela vérifie cette identité, pas les
droits de tous les participants.

Le nouvel inventaire limité explicitement à cet abonnement a retourné **neuf comptes
Cognitive Services, quatre projets Foundry, sept composants Application Insights et
zéro service Search**, avant les tests isolés. Cela corrige la mention précédente
d'absence d'Application Insights. Ces ressources servent d'autres applications ;
leur existence et les droits techniques n'autorisent ni leur réutilisation ni
l'export de leur télémétrie. Elles n'ont pas été modifiées.
L'inventaire réel des modèles dans eastus2 indiquait
`text-embedding-3-large` version `1` à l'état GenerallyAvailable et les anciennes
versions GPT-4o à l'état Deprecating. La présence d'un modèle et de quotas est un
prérequis, pas la preuve d'un déploiement réussi.

Terraform était absent du PATH. Une version portable **Terraform 1.16.6** a été
restaurée dans le répertoire privé d'outils de la session. Le SHA-256 de l'archive
a été comparé aux sommes publiées par HashiCorp. Aucune installation globale ni
modification du PATH de la machine n'a été effectuée.

## Lab 1 - Outils enregistrés et actualisation de l'agent

L'utilisateur a fourni l'écran de l'agent enregistré et partagé sa page directe.
L'image montre les outils d'envoi et d'annuaire ainsi que le PDF de licences.
C'est une preuve de configuration, pas un nouveau test de connaissances ou d'envoi réussi.

![Configuration enregistrée de l'agent, des outils et des connaissances fournie par l'utilisateur](../assets/runtime-2026-10-19/saved-tools-user-evidence.png)

La configuration visible utilise **GPT-5.5 Chat**, **Send an email (V2)**,
**Search for users (V2)**, le PDF et **Search all websites**.
Une réponse correcte ne prouverait donc pas, à elle seule, l'utilisation exclusive
du PDF. Le test réel doit examiner l'activité de recherche et d'outils sélectionnée.

### Résultats de la nouvelle exécution

La nouvelle page Preview s'est actualisée correctement et est restée interactive.
Le test a utilisé l'agent et les connexions existants ; les outils enregistrés
ont été conservés. Aucune nouvelle connexion ni autorisation n'a été nécessaire.
La liste Agents identifiait le moteur **GitHub Copilot**. Le test valide donc
un parcours principal équivalent dans la nouvelle expérience, pas une recréation
de l'ancienne interface de rubriques des agents standard.

1. La recherche dans le PDF chargé a été exécutée. La réponse a identifié
   **octobre 2026**. Cela démontre l'activité de recherche, pas un audit indépendant
   de chaque affirmation de licence ni la désactivation globale de la recherche web.
2. Une question sur une remise propre au locataire a été refusée, sans remise inventée.
3. **Search for users (V2)** a retourné un seul compte d'atelier correspondant et vérifié.
4. **Send an email (V2)** s'est terminé sans erreur en **1,6 seconde**.
5. Le message correspondant a été vérifié dans **Inbox** et **Sent Items**.
   Outlook affichait **14 h 44**. Son objet unique était
   **Lab1 live rerun 2026-10-19 1844Z - Licensing summary**.

La question couverte a été saisie exactement en anglais :

> What Power Apps licensing options are described in the uploaded Power-Platform-Licensing-Guide.pdf? Cite the uploaded guide and identify its edition. Do not search the web or use general knowledge for this test.

Elle demande les options Power Apps du PDF chargé, sa citation et son édition,
sans recherche web ni connaissances générales.

La question non couverte a été saisie exactement en anglais :

> Using only the uploaded licensing guide, what exact unpublished discount percentage and negotiated final Power Apps Premium price has Microsoft approved specifically for our Contoso tenant for next month? If the guide cannot establish that, say so. Do not invent a tenant-specific quote or search the web.

Elle demande une remise confidentielle et un prix négocié propres au locataire
Contoso pour le mois suivant, en exigeant de signaler l'absence de preuve dans
le guide et de ne rien inventer.

Il s'agit de nouveaux résultats observés dans le navigateur, distincts des captures
antérieures de l'utilisateur. Le
[registre nettoyé du Lab 1](../assets/runtime-2026-10-19/lab1-live-results.json)
conserve ces observations sans publier les identifiants de compte ou de locataire.
Le courriel de test a déjà été livré. Ne le renvoyez pas pour obtenir une autre capture.

Le parcours principal de recherche, d'annuaire, d'envoi et de réception a été exécuté.
À ce premier point de contrôle, l'ambiguïté et la panne de connexion n'avaient
**pas été exécutées**. Le suivi sûr ci-dessous décrit ensuite une clarification
conversationnelle réussie et une tentative d'erreur de connecteur non vérifiée indépendamment.
Cette réexécution ne signifie pas que tous les labs de l'atelier ont réussi.

### Nouvelles captures et limites

Les images suivantes sont des extraits nettoyés de la nouvelle exécution, pas des
captures du support initial ou fournies par l'utilisateur. Un problème de capture
lié au DPR de 1,5 a tronqué le bord droit des images d'origine. Aucun texte manquant
n'a été reconstitué. Les identifiants de compte et les messages sans rapport ont été exclus.
Ces images partielles illustrent l'activité observée ; ce ne sont pas des transcriptions
complètes. Les objets de courriel sont notamment tronqués. L'objet complet et les
résultats de livraison ci-dessus proviennent des observations dans le navigateur.

#### Recherche et refus de la question non couverte

![Nouvelle activité réelle Searched knowledge, capture partielle](../assets/runtime-2026-10-19/lab1-live-knowledge.png)

L'exécution a invoqué **Searched knowledge**. La sortie détaillée observée pendant
le test identifiait le PDF chargé avec la référence `turn1doc1` ; cette sortie complète
n'est pas visible dans l'extrait.

![Nouveau refus réel d'un prix négocié propre au locataire, capture partielle](../assets/runtime-2026-10-19/lab1-live-unsupported.png)

La réponse a refusé d'établir un prix négocié propre au locataire à partir du guide.

#### Exécution des outils d'annuaire et d'envoi

![Nouvelle réponse d'annuaire avec une correspondance et une latence de 2,7 secondes](../assets/runtime-2026-10-19/lab1-live-directory.png)

L'annuaire a retourné une correspondance. Les champs de boîte aux lettres ont été
exclus de l'image.

![Nouvel extrait détaillé de l'outil d'envoi et latence de 1,6 seconde, destinataire exclu](../assets/runtime-2026-10-19/lab1-live-send.png)

L'extrait détaillé montre le corps réellement transmis et la latence **1.6s**.
L'outil n'a retourné ni identifiant de message ni accusé de livraison. La réception
a été vérifiée séparément dans Outlook, sans la déduire de la réponse de l'agent.

#### Réception et éléments envoyés

![Nouveau message Inbox à 14 h 44, objet partiel](../assets/runtime-2026-10-19/lab1-live-inbox.png)

![Nouveau message Sent Items à 14 h 44, objet partiel](../assets/runtime-2026-10-19/lab1-live-sent.png)

Les deux dossiers ont été vérifiés pour le même objet unique et le même résumé.
Seules les lignes de message utiles sont incluses ; les autres courriels sont exclus.

## Lab 5.1 - Commandes Terraform réellement exécutées

Le support Terraform d'origine a été copié dans un répertoire privé d'exécution.
Les sources de l'atelier n'ont été ni modifiées ni publiées.

1. `terraform init -backend=false -input=false` a réussi.
2. `terraform validate` a réussi.
3. La validation JSON a retourné `valid: true`, zéro erreur et zéro avertissement.
4. Une surcharge locale a fixé `resource_provider_registrations = "none"` pour
   empêcher les inscriptions automatiques pendant le plan.
5. `terraform plan -input=false -refresh=false -detailed-exitcode` a réussi avec
   le code **2** : plan valide contenant des modifications, pas un échec.
6. Le plan enregistré contient **15 instances prévues**. Aucun apply n'a été exécuté.

| Type de ressource                  | Nombre |
|------------------------------------|--------|
| Compte Cognitive                   | 1      |
| Déploiements de modèles             | 2      |
| Groupe de ressources               | 1      |
| Attributions de rôles               | 6      |
| Service Search                     | 1      |
| Compte de stockage                 | 1      |
| Identité attribuée par utilisateur | 1      |
| Réseau virtuel                     | 1      |
| Identifiant aléatoire local         | 1      |

Les fournisseurs résolus sont AzureRM **4.45.1**, AzAPI **1.15.0**, AzureAD **2.48.0**,
Random **3.6.1** et HTTP **3.6.2**. Un verrouillage a été produit dans la copie privée.
Le plan brut et l'état ne sont pas des livrables publiés.

Ces résultats valident l'initialisation, la compatibilité des fournisseurs et schémas,
ainsi que la génération du plan. Ils ne valident ni déploiement, ni disponibilité
dans la région configurée, ni propagation des rôles, indexation, réseau ou intégrations.
Le support non modifié propose toujours un service Search Standard payant et les
anciens modèles décrits dans le [guide de déploiement](lab-05-1.md).

## Lab 5 - Contrôles réels de lisibilité des entrées

Les trois PDF d'hôtels fournis ont été ouverts avec l'analyseur PDF installé et
leur texte extrait localement. Chacun est non chiffré et contient une page.
Les contrôles des villes Doha, Rome et Tokyo ont réussi, avec respectivement
**774**, **767** et **743** caractères extraits. Consultez les
[résultats nettoyés](../assets/runtime-2026-10-19/hotel-input-results.json).

Cela prouve que les fichiers sont lisibles et non vides, pas leur ingestion dans
Azure ni les résultats attendus des requêtes avancées.

## Lab 6 - Test réel de compatibilité des dépendances

Seules les instructions d'importation du notebook ont été exécutées. Les appels cloud,
réinitialisations, créations d'agents et cellules de nettoyage ont été exclus.

### Échec reproduit dans l'environnement actuel

Avec `azure-search-documents==12.0.0` et `azure-ai-projects==2.3.0`, **14 importations
sur 15** ont réussi. L'importation de la cellule 14 a échoué :

```text
cannot import name 'KnowledgeRetrievalMinimalReasoningEffort'
from 'azure.search.documents.indexes.models'
```

C'est une incompatibilité SDK reproduite, pas une simple hypothèse de revue.
Aucun remplacement silencieux ou réponse de recherche artificielle n'a été utilisé.

### Restauration des versions du support et nouveau test

Un environnement virtuel distinct a été créé sans modifier l'interpréteur partagé.
Les dépendances ont été restaurées aux versions fixées dans le support :

```text
azure-ai-projects==2.0.0b3
azure-search-documents==11.7.0b2
azure-identity==1.25.1
azure-core==1.38.0
openai==2.16.0
python-dotenv==1.2.1
requests==2.32.5
```

Les **15 importations sur 15 ont réussi** après restauration. Cette base locale
fonctionne pour le code fourni, sans prouver que les contrats en préversion restent
compatibles avec les services Azure actuels. Cette vérification cloud reste à faire.

Un contrôle supplémentaire a vérifié que le SDK actuel expose
`KnowledgeRetrievalMinimalReasoningEffort` dans
`azure.search.documents.knowledgebases.models`, et non `indexes.models`.
`KnowledgeBase` et `KnowledgeSourceReference` restent dans `indexes.models` ;
`KnowledgeRetrievalOutputMode` n'existe dans aucun des deux espaces inspectés.
Changer une seule importation ne constitue donc pas une migration complète.
Le test REST GA ci-dessous ne confond pas restauration des importations et
compatibilité de tous les anciens contrats de préversion.

Les trois jeux de données intégrés ont aussi été évalués localement sans exécution
des cellules cloud. Ils contiennent chacun huit enregistrements, soit **24 au total**.
Chaque enregistrement possède des chaînes `id`, `title` et `content` non vides, avec
des identifiants uniques dans chaque jeu. Le contenu protégé lui-même n'est pas republié.

## Conditions d'exécution restantes

### Suivi sûr du Lab 1 et contrôle indépendant de la source

La question d'ambiguïté demandait quelles informations étaient nécessaires lorsque
plusieurs collègues s'appelaient Alex, en interdisant les connecteurs. La réponse
a demandé une adresse, un nom complet, un contexte ou un UPN avant toute action.
Le **contrôle conversationnel de clarification** a réussi ; cela ne prouve pas
le blocage d'ambiguïté lors d'un véritable envoi. Aucun autre courriel n'a été envoyé.

Une recherche en lecture seule du propre compte avec `top=-1` a été tentée.
L'agent a annoncé HTTP 400 et `Top parameter should be a positive number.`, sans
nouvel essai. La sortie n'était initialement pas accessible. Après la nouvelle
connexion de l'utilisateur, **History a exposé l'entrée du connecteur
`SearchforusersV2`, son activité rouge en échec et l'état Failed de la conversation**.
L'entrée observée était la chaîne `top: "-1"`, avec le propre compte vérifié
et la chaîne `isSearchTermRequired: "true"`. L'activité a duré **4,62 secondes**.
L'appel contrôlé et son indicateur d'échec sont ainsi vérifiés indépendamment,
mais pas le code HTTP ni le corps d'erreur : aucune section Output n'était exposée.
HTTP 400 et le message cité restent annoncés par le modèle.
La gestion d'une authentification expirée n'a pas été testée. Aucun test, recherche
d'annuaire ou envoi n'a été répété pour récupérer cette preuve.

![Activité de connecteur en échec récupérée dans History, identifiants exclus](../assets/runtime-2026-10-19/lab1-live-failed-activity.png)

Une copie locale indépendante de `Power-Platform-Licensing-Guide.pdf` a été trouvée
dans Downloads. Sa couverture indique réellement **octobre 2026**. Les pages PDF
6 et 7 étayent le résumé : Premium par utilisateur, paiement à l'utilisation par
application et droits inclus limités. La page 30 mentionne la fin de commercialisation
de l'offre par application en janvier 2026. Six contrôles exacts ont réussi.
Le fichier local comporte 30 pages ; son SHA-256 figure dans les
[résultats de contrôle](../assets/runtime-2026-10-19/licensing-source-check.json).
L'inspection connectée a ensuite ouvert la véritable source chargée, observé son
état **File / Ready** et cliqué sur **Download**. L'utilisateur a confirmé
l'enregistrement dans Downloads. Le nouveau fichier comptait **867 776 octets**,
avec modification à **17 h 38 min 43 s, heure locale**. Son SHA-256 correspondait
à la copie déjà contrôlée :
`e1b4789118ff8f1bb633683d6fbeb750b80c25b16760d036eff247e477a524d6`.
Les six contrôles de source ont été réexécutés avec succès. Cette correspondance
repose sur la **provenance du téléchargement confirmée par l'utilisateur et le hash
du fichier**, sans événement de téléchargement du navigateur, nom Content-Disposition
ou hash côté serveur capturé. Elle ne constitue ni un audit complet des citations
ni une vérification des conditions commerciales applicables aujourd'hui.

![Couverture réelle du PDF local de licences, pas une capture du portail](../assets/runtime-2026-10-19/licensing-local-cover.png)

### Exécution Azure réelle au niveau gratuit

Au lieu de créer des ressources payantes, la réexécution a utilisé un service
**Search Free**, **semanticSearch=free** et **knowledgeRetrieval=free** isolés.
La [documentation des niveaux Search](https://learn.microsoft.com/en-us/azure/search/search-sku-tier)
et celle de la [facturation de recherche agentique](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-enable-disable)
confirment le niveau gratuit limité et le rejet des requêtes dépassant l'allocation,
sans bascule automatique vers un forfait payant.
Aucun compte Storage, appel de modèle externe, niveau Search payant ni ressource
sans rapport n'a été utilisé. Les clés sont restées en mémoire du processus et
n'ont pas été écrites dans les preuves publiques.

La première tentative dans **eastus2** a échoué avec `InsufficientResourcesAvailable`.
Le service Free de **westus2** a fonctionné. Une première requête sémantique a retourné
HTTP 400 : `queryLanguage` n'est pas accepté par l'API Search **2026-04-01**.
La suppression de ce paramètre et la réexécution réelle ont résolu l'échec.
La tentative échouée est conservée dans les
[résultats cloud nettoyés](../assets/runtime-2026-10-19/free-cloud-results.json),
au lieu d'être remplacée par un récit de réussite uniquement.

#### Recherche d'hôtels : données réelles et assertions mesurées

Les trois PDF fournis ont été extraits localement et chargés comme **trois documents
textuels entiers**, pas comme passages issus d'un indexeur Blob. Chaque statut
individuel de chargement a réussi.

* Le nombre exact de documents était **3** ; les requêtes lexicales Doha, Rome et
  Tokyo ont chacune retourné uniquement l'hôtel correspondant.
* Le filtre Rome n'a retourné que Rome ; les trois facettes de ville comptaient
  chacune **1** document.
* `rooftop garden` avec `searchMode=any` a retourné Tokyo, mais `searchMode=all`
  n'a rien retourné. Le corpus fourni contient rooftop, mais pas garden.
* `bicycle storage` exigeant tous les termes n'a rien retourné : aucun PDF ne contient
  bicycle. L'exemple du support n'est donc pas automatiquement un test positif.
* Les requêtes vectorielle et hybride ont classé Tokyo en premier avec des
  **caractéristiques explicites de ville à trois dimensions, codées one-hot**.
  Ce ne sont **pas des embeddings sémantiques**, ni une preuve de pertinence sémantique.
* Une véritable requête sémantique a retourné Tokyo en premier avec un score de
  reclassement non nul. Le profil `title-boost` a aussi été exécuté ; aucune
  amélioration de pertinence n'est revendiquée.
* Un filtre sur `content`, non filtrable, a retourné **HTTP 400**.
  Une requête sans identifiants a retourné **HTTP 403**, pas les documents.

Ces tests valident réellement les API d'indexation et de recherche. Ils ne valident
ni ingestion Storage, projections de passages, embeddings intégrés, identité managée,
URL de citation, ni connexion Search Copilot Studio des Labs 2 et 5 d'origine.

#### Lab 6 : recherche réelle dans trois sources

L'index d'hôtels propre à l'exécution a été supprimé pour respecter la limite de trois
index Free. Les trois jeux du notebook ont ensuite été chargés dans trois nouveaux
index : **8 + 8 + 8 = 24 enregistrements**, avec vérification de chaque chargement
et du nombre final. Trois véritables sources de type index Search et une base
de connaissances référençant les trois ont été créées.

L'exécution a utilisé le **contrat REST GA minimal/extractif 2026-04-01** :
aucune configuration LLM, planification, génération d'embeddings ou synthèse de réponse.
La [documentation de recherche minimale](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-set-retrieval-reasoning-effort)
et le [contrat GA des bases](https://learn.microsoft.com/en-us/azure/search/agentic-retrieval-how-to-create-knowledge-base)
expliquent ce remplacement pris en charge du notebook de préversion.

1. Une question précise de fraude a retourné **2 passages et 2 références**, depuis
   la source des schémas de fraude.
2. La requête multisource `fraud investigation compliance` a retourné **17 passages
   et 17 références provenant des trois sources**.
3. Une requête sans rapport, constituée d'un mot inventé, a retourné **0 passage
   et 0 référence**.
4. Les trois sources figuraient dans l'activité de chaque requête.
5. Les titres et contenus des **19 passages retournés correspondaient exactement
   aux enregistrements indexés**, reliés par le `docKey` de chaque référence.
   `sourceData` était nul ; la validation n'a pas supposé qu'il contenait le document.

La dernière exécution a réussi **34 contrôles HTTP, schéma et dénombrement**, ainsi
que les trois contrôles exacts de forme et de contenu ci-dessus. Les données et
réponses complètes restent privées ; seuls nombres, assertions et métadonnées
de test sont publiés. Cela prouve la recherche de connaissances Search, **pas**
un agent Foundry, une connexion MCP, un point Activity ou un agent connecté Copilot.

#### Nettoyage et limites restantes

Les **quatre** groupes isolés des tentatives de capacité, d'hôtels initiale,
d'hôtels corrigée et multisource ont tous été supprimés. Leur absence a été vérifiée
après chaque suppression. Seuls les groupes portant exactement l'étiquette de
l'exécution et ne contenant aucune ressource inattendue pouvaient être nettoyés.
Aucun service, agent, connexion ou boîte existants n'a été supprimé.

Aucune ressource facturable n'a été créée ou appliquée. Les demandes de budget
n'ont reçu aucune réponse humaine ; une réponse automatique d'indisponibilité
n'est pas interprétée comme une approbation. L'outil de prix n'a retourné aucun tarif
pour les requêtes de niveaux Search tentées. Aucun tarif ni plafond garanti n'est donc supposé.

Le déploiement payant d'origine, la chaîne Storage/vectoriseur, la télémétrie corrélée
de l'agent, le prompt BYOM connecté et les agents connectés Foundry/Copilot nécessitent
encore un périmètre dédié et des dépenses autorisées. Les ressources de production
existantes ne sont pas des substituts sans accord de leur propriétaire.
Les tests gratuits et vérifications de source ci-dessus sont réels, mais
**l'ensemble de l'atelier n'est pas certifié réussi**.

## Éléments restés intacts

### Dernier contrôle d'accès

Une tentative limitée antérieure a ouvert l'URL Preview exacte de l'agent existant.
Elle a redirigé vers la connexion Microsoft (`login.microsoftonline.com`) ; le
navigateur a retourné `ERR_ABORTED (-3)` sans identifiant de page utilisable.
L'utilisateur s'est ensuite reconnecté et a partagé l'agent. Le **suivi entre
21 h 35 et 21 h 44 UTC a réussi**, permettant l'inspection de History et du
fichier chargé. Le blocage d'authentification est résolu pour cette période
d'observation.
Aucune authentification, autorisation ou sélection de compte n'a été contournée.

### Interface de création inspectée après la connexion

Le [registre nettoyé du suivi](../assets/runtime-2026-10-19/signed-in-followup.json)
conserve l'inspection en lecture seule. Le modèle sélectionné est resté
**GPT-5.5 Chat** ; aucun nouvel identifiant de moteur ou numéro de version du
produit n'était exposé.

* Menu de mode : **Build, Preview, Evaluate, Monitor**
* Paramètres : **Agent details, AI & behavior, Safety & access, Greeting & prompts**
* Ajout d'outil : **Featured, MCP, Connectors, Workflows**
* Agents connectés : seuls les agents publiés peuvent être connectés ; le sélecteur
  affichait **Classic agent connections are not supported**

Les rubriques conventionnelles, la configuration Application Insights, un point
de modèle personnalisé dans son menu et un point Foundry dans le sélecteur d'agents
n'étaient **pas exposés dans les contrôles inspectés**. Il s'agit d'un constat
local à cette interface, pas d'une indisponibilité globale. Cela explique pourquoi
la supervision, le prompt BYOM et la connexion Foundry de l'agent standard d'origine
ne peuvent pas être déclarés reproduits en inspectant simplement cet agent.
Save est resté désactivé au niveau ARIA et les dialogues ont été annulés.
Aucune configuration, connexion, sélection de modèle, création d'agent ou publication
n'a été modifiée.

Un inventaire en lecture seule a trouvé **23 déploiements de modèles réussis
répartis sur huit des neuf comptes Cognitive Services**. Cela établit des métadonnées,
pas l'autorisation d'envoyer les données d'atelier vers d'autres applications,
la gratuité des appels, la compatibilité des points d'accès ou la réussite BYOM.
Aucun appel d'inférence ni lecture de clé de ces comptes existants n'a été effectué.

Les documents Word, le notebook et les sources Terraform d'origine sont inchangés.
Les ressources de production ou d'autres usages n'ont pas été modifiées. Les preuves
initiales d'envoi et de réception du lab 1 restent des preuves historiques utilisateur,
distinctes de tout nouveau test exécuté par l'assistant.
