---
title: Validation du backend Copilot et du CLI - 2026-10-20
description: Lectures Dataverse authentifiées, restauration officielle de PAC, clone de l'agent sauvegardé et blocages de conversation et d'évaluation restants.
ms.date: 2026-10-26
---

## Résultat et limites

[Tous les labs](index.md) | [English](../en/backend-live-2026-10-20.md) | [Registre réel](live-rerun-2026-10-19.md)

Le [contrôle ultérieur History/source des licences](../assets/runtime-2026-10-25/lab1-history-citation-followup.json)
conserve l'historique original incomplet et un échec distinct de navigation
de citation intégrée, sans nouvelle question native ni écriture de configuration.
La [publication wiki réelle](../assets/runtime-2026-10-25/wiki-publication.json)
vérifie indépendamment destination publique, référence sans modification humaine,
envoi normal, révision distante et pages anglaises/françaises rendues.
Cet instantané honnête reste en cours; aucun déploiement d'agent ou Azure.
T009, T016, autres critères d'acceptation et gouvernance humaine restent ouverts.

## Échec du sélecteur Search OAuth natif du 26 octobre

Les [deux cohortes isolées successives par principal de service](../assets/runtime-2026-10-26/native-search-index-picker.json)
utilisent chacune une saisie manuelle du secret et un Create, avec notification
enregistrée et inventaire Connected indépendant. Les deux sélecteurs échouent :
`Something went wrong.`, HTTP 400 console et Add to agent désactivé.
Corps HTTP indisponible; cause et principal natif effectif inconnus.

La première utilise uniquement Search Index Data Reader sur son index :
lacune documentée de métadonnées, pas cause démontrée du 400. La seconde vérifie
exactement deux attributions : Reader sur son seul index et rôle personnalisé
séparé au service existant avec uniquement
`Microsoft.Search/searchServices/indexes/read` dans Actions, sans DataActions,
écriture ni operations/read. Liste directe par le bon principal et requête de
son propre témoin synthétique réussissent. Métadonnées de tous les index exposées,
pas leurs documents. L'échec natif persiste; aucun correctif démontré.

Aucune source ajoutée, liaison d'index, correspondance schéma/champs ni
disponibilité Ready. Zéro question native positive, négative ou de modèle;
ni 403 direct après révocation ni acceptation sans fuite exécutés/prouvés.
Connected et contrôles directs ne constituent ni acceptation native ni réussite
appariée partielle. Le [ticket nº 4](https://github.com/devopsabcs-engineering/copilot-studio/issues/4)
demande diagnostic pris en charge et contrat minimal de permissions.
S5-10/T014/T016 et clôture de l'atelier restent ouverts.

Les deux nettoyages indépendants vérifient zéro ressource possédée restante,
révocation/suppression des secrets et suppression des fichiers secrets protégés.
Le premier conserve l'erreur PAC de filtre d'environnement, puis sa reprise
contrôlée sur la connexion exacte, et l'erreur DNS d'instantané, puis sa
vérification distincte en lecture seule sans répéter la suppression.
Le second nettoyage contrôlé et verify-cleaned distinct n'ont aucune erreur.
Cinq agents/sept connexions/trois schémas initiaux, configuration Search complète,
rôles/définitions non possédés, rôles d'embedding, hébergement v5 et 181 fichiers
historiques restent exacts. Aucun original modifié, aucune question Activity/
Foundry, publication M365, importation ZIP, affaiblissement auth/réseau,
authentification par clé ni modification du stockage public.

## Lecture du modèle actuel du 26 octobre

Les [deux GET en lecture seule](../assets/runtime-2026-10-26/agent-endpoints-readonly.json)
renvoient des métadonnées identiques avec et sans en-tête documenté. La v5 initiale
possède déjà le nouveau modèle de point de terminaison/identité,
Activity/Invocations, Entra/BotServiceRbac et approbation `not_published`.
Configuration de protocole et sélection de version imbriquées sont présentes.
Aucune écriture ni question; échecs de l'ancienne route et T005/T006 non résolus.

La [corrélation de l'erreur conservée](../assets/runtime-2026-10-26/native-blueprint-identity-correlation.json)
trouve l'ID objet de l'utilisateur approuvé à la place du blueprint d'activité,
pas le client blueprint cible. Blueprint cible et identité d'instance restent
identiques entre v3 conservée et v5 actuelle. Aucune nouvelle requête ni question;
sélection de l'identifiant en amont et correction native non résolues.

## Reprise SP appariée interrompue du 26 octobre

Le [reçu de nettoyage SP apparié](../assets/runtime-2026-10-26/lab5-paired-sp-interrupted-cleanup.json)
compte zéro intention de question native autorisée/refusée. Des lectures finales
indépendantes vérifient la suppression du secret, identité, brouillon, quatre
rôles et ressources Azure possédés. Comparaisons des agents, connexions, schémas,
rôles d'embedding et hébergement v5 initiaux réussies; 181 fichiers historiques
inchangés. L'inventaire du portail redirige vers la connexion, donc seule l'absence
PAC/Dataverse officielle est établie. Aucune répétition de question ni modification
d'authentification pendant la reprise. Ni S5-10/T014/T016 validés ni coût finalisé.

## Historique original et permissions de transcription du 26 octobre

Le [reçu Dataverse/History en lecture seule](../assets/runtime-2026-10-26/lab1-dataverse-history.json)
conserve le défi CAE Graph et l'expiration CLI normale, puis la réussite d'une
lecture Graph vérifiée indépendamment pour l'administrateur approuvé.
La lecture administrative de l'environnement réussit aussi; aucune ne donne
l'accès aux transcriptions Dataverse. La requête de l'agent original renvoie 403
et un nouvel audit des cinq privilèges définis confirme l'absence des droits de
lecture des transcriptions et d'attribution des rôles. L'ancienne assertion
incomplète reste échouée, sans réussite rétroactive.

Les rôles directs Basic User et Environment Maker restent exacts. Aucun rôle,
paramètre de rétention ou politique de transcription modifié, aucune auto-élévation
générale ni nouvelle question. History du 19 octobre reste In progress sans réponse
complète. T009 reste bloqué; ni réponse reconstruite ni exécution plus récente substituée.

## Récupération Search Entra native du 25 octobre

Le [reçu connecté natif](../assets/runtime-2026-10-25/lab5-native-entra-connected.json)
conserve l'échec du format `ai://` documenté et la correction HTTPS/Entra
distincte réussie. Un brouillon Standard isolé non publié utilise une source
Search fictive Ready, recherche web/connaissances générales désactivées et
modèle/authentification préservés. Première cohorte 3/4, avec réponse anglaise
à la question française conservée. Après ajout et sélection du français dans
le panneau, une cohorte figée distincte réussit 4/4 : traces réelles, citations
étayées et abstention explicite sur le prix. Huit questions natives et archives
conservées, sans fusion des configurations. Une configuration exportée est
vide; les clones officiels avant/après confirment 17 fichiers inchangés.

Un vrai clic de citation ouvre le fichier source fictif publié exact, sans
fragment de section. Les trois objets logiques temporaires possédés sont
supprimés; inventaires et empreintes initiaux préservés. L'erreur de module
manquant du validateur officiel reste ouverte, sans modification de bundle
ni validation de schéma prétendue. URL hôtelières originales et refus réel
d'identité restent non vérifiés. T014 et l'atelier ne sont pas terminés.

## Erreur source native sans document renvoyé du 26 octobre

La [nouvelle reprise distincte](../assets/runtime-2026-10-26/lab5-native-denied-first-use.json)
réussit le contrôle public après retrait confirmé, attente de 600,002 secondes,
sa propre connexion neuve réussie du connecteur et contrôles récents 403 direct/
conversation. Une seule question de fermeture est exécutée. Search natif renvoie
`ConnectorRequestFailure / AzureAISearchClientError`, zéro document et zéro citation;
sa trace officielle n'expose aucun statut HTTP. La réponse complète du parent est :
« I'm sorry, I'm not sure how to help with that. Can you try rephrasing? »
L'interface signale aussi qu'aucune information n'est trouvée. Aucun fait source
n'apparaît, mais cette réponse générique ne prouve pas une gestion spécifique
des erreurs de permission.

Cette cohorte dispose d'une référence directe autorisée, pas d'une référence native
autorisée, et utilise l'administrateur approuvé, pas une identité non privilégiée
distincte. Elle ne valide pas S5-10/T014, n'attribue pas le principal effectif par
requête, n'établit pas la cause historique et ne reclasse aucun résultat antérieur.
Export/configuration officiels et contrôles indépendants du nettoyage possédé/
inventaires initiaux sont conservés; navigateur fermé normalement, aucune commande
en attente. Coût réel non finalisé.

## Échec natif isolé de retrait d'autorisation du 25 octobre

Le [reçu distinct de refus](../assets/runtime-2026-10-25/lab5-isolated-permission-removal.json)
enregistre un échec du contrôle sans divulgation, pas une réussite S5-10.
La référence native autorisée réussit sur un nouveau service Search fictif
sans clé. Après retrait de son seul rôle Reader d'index possédé, les requêtes
directes renvoient 403, mais l'unique tour natif de refus renvoie Harbor `07:00`
et sa vraie citation. La trace Search contient deux documents fictifs sans
erreur Search. Les deux configurations officielles concordent; un clone
indépendant vérifie 17 fichiers d'auteur inchangés. L'instantané existant
est récupéré après expiration de lecture, sans rejeu. Même administrateur,
pas une identité indépendante non privilégiée; principal effectif et cause
restent non établis.

Tous les objets possédés, dont service, groupe vide et rôle d'embedding
sur le compte existant, sont supprimés. Le refus CLI pour divergence route/filtre
est conservé; une suppression de première partie correctement limitée et
un 404 indépendant terminent le retrait de connexion. Agents, connexions,
compte/rôles d'embedding et schémas initiaux inchangés. Navigateur fermé normalement,
coût réel non finalisé. S5-10, T014 et acceptation complète restent ouverts.

## Récupération administrateur et candidat du 25 octobre

La [dernière poursuite du candidat](completion-roadmap.md#correction-du-candidat-authentifié-du-25-octobre)
remplace les anciens blocages de connexion, navigateur et clonage.
Authentification administrateur humaine, clone/envoi PAC officiels et lecture
persistée indépendante réussissent. Instantanés CTR/SAR restreints et accueil
réussissent 3/3 en natif, dont une seconde exécution 3/3 sur le brouillon final.
Routage SAR spécialiste et couverture finale réussissent, mais la fidélité
complète échoue avec 15/16 citations exactes sur deux messages. Les instructions
parent améliorent la synthèse ultérieure sans supprimer le défaut initial;
aucun paramètre non pris en charge de suppression externe n'est inventé.
Les 26 lignes de composants d'origine sont inchangées; 28 composants candidat,
deux rubriques possédées ajoutées, seules instructions existantes modifiées,
fichiers, liaisons et états Off/On/On sont vérifiés indépendamment.
Aucune publication n'a lieu. Autorisation du diagnostic natif/SDK d'origine et
matrice complète restent ouvertes; cela ne valide pas le rendu hébergé via
l'agent connecté. Les échecs plus anciens restent dans l'historique ci-dessous.

La [preuve MCP locale ultérieure](../assets/runtime-2026-10-25/mcp-evidence-local.json)
renvoie des preuves structurées au rendu exact sans activités de conversation,
en réutilisant le récupérateur inchangé. Un appel SAR d'origine renvoie deux
documents exacts. OAuth réel, hébergement MCP distant et liaison native candidat
ne sont pas vérifiés. L'assistant du tenant propose OAuth manuel mais est annulé
sans connexion créée; aucune ressource Azure supplémentaire n'est provisionnée
à ce point local.

Le [contrôle MCP hébergé suivant](../assets/runtime-2026-10-25/mcp-hosted-preflight.json)
déploie un App Service Linux B1 Python 3.13 distinct en Sweden Central, avec
HTTPS, TLS 1.2 et sans FTP/publication basique. Les contrôles réels sans jeton
ou avec jeton invalide renvoient 401 et la découverte OAuth correcte renvoie 200.
API/client possédés, rôle sortant limité au compte existant, connecteur MCP
officiel et rappel généré sont créés puis relus. La récupération après verrou
local de reçu évite les applications dupliquées; le premier échec local de
longueur de titre PAC reste conservé.

L'identité administrateur du navigateur/PAC est vérifiée. Le navigateur intégré
bloque le consentement contextuel du connecteur; l'autorisation normale code/PKCE
en nouvel onglet atteint plutôt la demande de mot de passe administrateur.
L'outil de réponse humaine est indisponible. Aucune réussite OAuth, récupération
sortante, liaison candidat ni nouvelle question native n'est revendiquée.
Rappel/auxiliaire temporaires sont supprimés et aucun accord utilisateur n'est
observé. L'hôte distinct reste facturable selon une estimation publique de calcul
de 0,018 USD/heure, sans facture établie, budget numérique ou responsable/date
de rétention.

La [nouvelle préservation native](../assets/runtime-2026-10-25/mcp-hosted-native-preservation.json)
vérifie encore 26 lignes d'origine/28 du candidat, contenu d'auteur, fichiers,
liaisons et états Off/On/On. La lecture confirme aussi le récupérateur protégé et
la définition/les identifiants de principal/client de la version 5 courante.
Un champ d'état d'identité supplémentaire n'est confondu ni avec un changement
d'identité ni avec une égalité d'objet entier. Aucune stratégie Storage,
publication ou acceptation globale n'est modifiée.

### Récupération sortante réelle par identité managée

La [preuve dans le conteneur applicatif](../assets/runtime-2026-10-25/mcp-managed-identity-runtime.json)
vérifie maintenant l'identité managée sortante réelle, la question SAR d'origine
inchangée, les deux documents exacts et le rendu complet. Les cinq empreintes du
code déployé et le récupérateur configuré correspondent; le récupérateur protégé
reste identique avant et après. Les échecs HTTP 403 antérieurs sont conservés.
Lectures de réponse existante et sondes de modèle inexistant distinguent droits
et inférence. Une attribution personnalisée de lecture/écriture des données
d'agents reste limitée au projet après suppression des trois attributions
d'essai possédées. L'action d'écriture permet aussi de modifier les agents,
mais aucune requête de modification d'agent n'est effectuée.

La [nouvelle préservation native complète](../assets/runtime-2026-10-25/mcp-managed-identity-native-preservation.json)
réussit encore. Aucun droit Storage/Search, changement de stratégie, jeton
conservé, question native, liaison candidat ni publication nouveau n'a lieu.
Les jetons entrants absents/invalides reçoivent toujours 401. Connexion MCP
déléguée réelle et acceptation SAR native complète restent ouvertes; la
récupération partagée directe ne les remplace pas. L'hôte reste facturable et
aucun budget numérique ni responsable de rétention n'est inventé.

### Poursuite OAuth MCP native et SAR sur le tour complet

La [poursuite native](../assets/runtime-2026-10-25/mcp-native-sar.json)
remplace la limite OAuth/SAR native antérieure. Le consentement humain explicite
pour tout le tenant est vérifié comme `AllPrincipals`, seulement `Evidence.Read`;
PAC indique Connected pour la connexion réelle. La découverte native enregistre
un composant MCP candidat, avec liaison exacte relue indépendamment.
Le candidat compte 29 composants. Seuls ses instructions et l'état actif de
l'ancienne récupération changent; texte Author exact, autres définitions,
26 lignes originales et contrôles sont vérifiés. L'ancienne définition émettrice
reste conservée, mais désactivée.

Une question SAR d'origine inchangée invoque MCP natif et recherche locale réelle,
puis produit une réponse métier unique. Les deux citations de documents complets
correspondent exactement au corpus épinglé, avec marqueurs distincts, référence
locale, délais conditionnels, exception initié, formulaire, couverture narrative/
enquête et limites d'applicabilité. La capture visible complète inclut accueil
et consentement de connexion. Jetons absents/malformés : toujours 401;
aucune publication ni modification de stratégie. L'erreur de module manquant du
bundle de gestion est conservée; interface prise en charge utilisée sans correctif
du bundle. `DynamicPlanFinished` brut, matrice fraîche complète et acceptation
des autres labs/gouvernance restent non vérifiés.

La [matrice native suivante](../assets/runtime-2026-10-25/mcp-native-matrix-initial.json)
conserve les réussites d'origine 1-4 et l'échec d'attribution individuelle du cas 5.
Une correction enregistrée réussit un cas 5 frais, mais
[échoue sur une citation source contre notice de rendu](../assets/runtime-2026-10-25/mcp-native-source-boundary-failure.json).
Le SAR corrigé suivant contient deux citations MCP complètes exactes, mais
[échoue sur un point ajouté dans une citation locale](../assets/runtime-2026-10-25/mcp-native-local-quote-failure.json).
Les exports officiels conservent maintenant les fins réelles non annulées.
Chaque appel de preuves est vérifié, sans masquer plusieurs appels ni les compter
comme nouvelles questions utilisateur. Aucune cohorte échouée ne clôt la matrice
complète ni ne modifie le backend.

La [dernière matrice native complète](../assets/runtime-2026-10-25/mcp-native-eleven-case-matrix.json)
réussit les onze cas d'origine inchangés avec douze soumissions : un blocage natif
avant plan est conservé et une reprise explicite suit la reconnexion normale.
Les treize exports du contenu agent sont identiques octet pour octet. Fins
réelles, sept appels MCP, documents épinglés, contribution locale prévue et audits
sémantiques/d'attribution complets réussissent. Les réponses MCP sont des
paraphrases vérifiées sans guillemets; douze citations locales déterministes sont
exactes. Les 26 lignes originales et 29 composants candidat restent préservés.
T008 est clos; T007 conserve le contrôle de validation dupliqué observé séparément.
Aucun déploiement, publication, nouveau rôle ou changement de stratégie n'est
déduit de cette acceptation native.

La [correction du seul contrôle](../assets/runtime-2026-10-25/mcp-native-control-repair-regression.json)
est enregistrée une fois par l'UI native et relue indépendamment. Sa reprise
comptée prouve une invocation, liaison et réponse de validation. La nouvelle
régression accepte 10/11 cas : le cas 9 termine preuves/plan sans réponse, puis
sa reprise comptée ne produit ni plan ni réponse. Aucun échec n'est masqué ou
accepté. Quinze soumissions, quatorze exports identiques du contenu agent et sept
appels MCP réels sont conservés; un appel appartient à la tentative sans réponse
parent. Le cas 7 actuel contient deux citations MCP exactes, pas zéro. Toutes les
autres lignes complètes, instructions/authentification/publication et l'original
protégé restent préservés. Le navigateur ferme; aucun déploiement backend ni
changement de stratégie. T007 et l'acceptation de configuration actuelle restent ouverts.

L'[inventaire ciblé des ressources/coûts](../assets/runtime-2026-10-25/owned-boundary-refresh.json)
lit maintenant six ressources ARM détenues, dont le site MCP et son plan B1,
avec l'administrateur approuvé vérifié. Le coût déclaré est de 11,26126391 USD
avant taxes jusqu'à l'heure limite du 25 octobre, après un HTTP 429 conservé
et une reprise réussie. Seuls deux identifiants ont des lignes publiées;
l'absence de frais ne signifie pas gratuité et les crédits Copilot sont exclus.
Aucune configuration/inférence/question. Responsable humain, date de revue,
budget chiffré et accords attribuables restent indisponibles; T001/T002 ne sont pas clos.

## Livraison hébergée à deux protocoles du 25 octobre

La [livraison Invocations vérifiée](../assets/runtime-2026-10-24/verified-invocations-delivery.json)
est active en version 5, après le transport initial réussi en version 4.
Elle préserve Activity et ajoute un contrat JSON sans état pour question/preuves,
OpenAPI authentifié et erreurs explicites bornées. Les 54 tests du service,
les dépendances et les comparaisons SAR réelles locales/hébergées avec le rendu
littéral réussissent. Sept contrôles hébergés passent, dont le refus sans jeton
et l'absence d'appel de modèle pour les entrées invalides, prouvée par les journaux
corrélés. Le HTTP 400 Activity initial pour version API manquante est conservé
avec le HTTP 200 corrigé, soumis séparément avec protection contre la répétition.

L'expiration du CLI de déploiement de version 5 est conservée : les lectures
indépendantes trouvent le service actif et doctor rapporte 11 réussites,
zéro échec, deux contrôles ignorés, sans autre déploiement. Les deux mécanismes
d'authentification, l'identité, le récupérateur version 4 et les quatre
ressources/rôles restent inchangés. La
[lecture native](../assets/runtime-2026-10-24/native-preservation-after-invocations.json)
vérifie aussi parents, définitions, liaisons, fichiers, autorisations, cache et PAC.
Aucune protection Storage/réseau n'est affaiblie.

Il s'agit du transport hébergé direct, pas d'une acceptation d'agent connecté natif
ni d'une récupération de l'autorisation SDK publiée. La page partagée reste masquée
après les tentatives normales; aucune question native ni configuration n'est
soumise. Le jeu généré supplémentaire est différé pendant l'indisponibilité de
l'utilisateur. Acceptation native/matrice, rétention et validations
organisationnelles restent ouvertes.

## Poursuite en lecture seule du 23 octobre

Ce point en lecture seule est antérieur. La livraison autorisée ci-dessous
remplace les états non déployé/utilisateur indisponible, pas les échecs conservés.

Le [point de clôture](completion-roadmap.md#point-dexécution-du-23-octobre)
conserve le rapprochement actuel des ressources possédées, les coûts retournés,
les empreintes de l'artefact exact et les contrôles locaux répétés. Il ne ferme
pas l'acceptation réelle. Le reçu
[completion-progress.json](../assets/runtime-2026-10-23/completion-progress.json)
enregistre 6,219977042 USD avant taxes pour le groupe, sous réserve du retard
de facturation et du jour partiel. Search fonctionne encore; sa balise
d'expiration ne constitue pas un nettoyage. Propriété de rétention et
validations attribuables de livraison restent en attente.

Le reçu [native-state-readback.json](../assets/runtime-2026-10-23/native-state-readback.json)
confirme que le diagnostic reste Inactive par trois GET Dataverse authentifiés
actuels. Les métadonnées Foundry actuelles confirment séparément que la cible
d'origine sélectionne la version 4 active avec sa définition de création intacte.
Aucune de ces lectures n'est une réponse native ni un déploiement de la réparation
SDK. L'extension hébergée reste en version 1 active, sans changement d'autorisation.

Le reçu [independent-lab-review.json](../assets/runtime-2026-10-23/independent-lab-review.json)
conserve les identifiants d'acceptation et échecs historiques de T009, T010 et T014.
Aucun critère restant n'est nouvellement réussi. Une tentative d'ouverture du
navigateur a expiré sans identifiant de page; ses effets restent inconnus.
Aucune nouvelle question au modèle, aucun courriel, évaluation, changement cloud,
accès à une source protégée, suppression ou publication distante n'a eu lieu.
Toutes les tâches de la feuille de route restent ouvertes.

## Réparation hébergée autorisée et récupération API native

L'autorisation explicite de déploiement/crédits de l'utilisateur est enregistrée
dans [authorized-release.json](../assets/runtime-2026-10-23/authorized-release.json).
Le candidat SDK exact a été déployé en version 2. Son test
[hosted-repair-smoke.json](../assets/runtime-2026-10-23/hosted-repair-smoke.json)
retourne de vrais extraits avec attribution individuelle.
Le reçu [hosted-negative-checks.json](../assets/runtime-2026-10-23/hosted-negative-checks.json)
conserve ensuite un nouvel échec : l'outil MCP approuvé terminé retourne un saut
de ligne non analysable en JSON. L'entrée invalide s'arrête correctement avant
toute inférence.

La correction ciblée traite seulement le texte vide d'un appel vérifié réussi
comme absence de preuve; le texte non vide mal formé reste une erreur explicite.
Cinq tests ajoutés portent la suite à 38. La réponse d'échec réelle conservée
se rejoue correctement sans nouvelle requête au modèle.
La réparation est déployée en version 3 active. Les trois tests réels de
[hosted-version3-regression.json](../assets/runtime-2026-10-23/hosted-version3-regression.json)
réussissent : cas 6 inchangé avec extraits exacts/marqueurs individuels, abstention
à la question d'astronomie inchangée et erreur d'entrée trop longue sans appel
au modèle. Les six requêtes Activity au total entre les versions 2/3 ne constituent
pas un compte de crédits facturés ou de modèles internes.
L'authentification reste Entra et BotServiceRbac. La route version 4 d'origine
est préservée; aucune réussite native n'est déduite.

L'échec de connexion navigateur Azure CLI était AADSTS65002, restriction de
préautorisation entre API Microsoft, pas un problème de rôle Azure.
Le reçu [native-api-access-recovery.json](../assets/runtime-2026-10-23/native-api-access-recovery.json)
conserve cet échec et la récupération prise en charge : un client possédé
monotenant sans secret, PKCE, consentement de lecture/écriture des opérations
maker limité à l'utilisateur courant et HTTP 200 pour la liste d'évaluations.
Aucun consentement global, rôle d'annuaire ni profil Azure n'a changé.

Initialement, l'API retourne zéro jeu de tests.
[native-canary-preparation.json](../assets/runtime-2026-10-23/native-canary-preparation.json)
conserve le CSV privé de deux cas et le prérequis d'interface restant : import
dans le bot existant, configuration du profil Microsoft Copilot Studio authentifié
et enregistrement des deux. Les vrais identifiants du jeu et de la connexion sont
requis avant l'exécution API de brouillon. Le `ConnectionError` ultérieur de
préparation ne prouve pas une régression d'authentification.
À ce stade préparatoire, le diagnostic reste Inactive et aucune évaluation n'a
encore été soumise.
T003/T004 sont terminées dans leur périmètre hébergé; acceptation native et
atelier complet restent ouverts. Les anciens échecs SDK/natifs restent inchangés.

## Test natif authentifié et restauration vérifiée

Le [point natif ultérieur](completion-roadmap.md#test-natif-authentifié-et-restauration)
remplace le prérequis de jeu manquant. Dans le contexte admin/MngEnv vérifié,
un jeu enregistré de deux cas est exécuté avec connexions authentifiées explicites
en brouillon. L'[exécution réelle](../assets/runtime-2026-10-23/native-authenticated-canary.json)
retourne HTTP 202 puis Completed avec une réussite et un échec General Quality.
Aucune soumission n'est répétée. La réponse API documentée n'expose ni les réponses
finales ni la correspondance question/résultat; l'acceptation native exacte reste
non prouvée.

La [restauration vérifiée](../assets/runtime-2026-10-23/native-canary-restoration.json)
remet le diagnostic isolé à Inactive avec sa définition exacte intacte.
Les lignes complètes du rattachement d'origine et du parent restent inchangées.
La lecture de l'endpoint confirme `@latest`, version hébergée 3 active et
Entra plus BotServiceRbac inchangés. La lecture documentée des transcriptions,
filtrée au bot et à la fenêtre du test, retourne 403 pour privilège
`prvReadconversationtranscript` manquant. La mise normale du navigateur admin
au premier plan échoue aussi; aucune touche n'est envoyée ni aucun rôle élargi.
Cette investigation conserve un échec réel d'acceptation, sans réussite de
transport natif, reproduction de l'ancien 403 de tenant ni résultat de onze cas.

## Outils indépendants et exécution Terraform

Les [tentatives prises en charge](../assets/runtime-2026-10-23/native-recovery-alternatives.json)
restaurent PAC officiel 2.14.1 et vérifient l'identité admin/MngEnv prévue.
L'appartenance Global Administrator existante n'est pas une affectation System
Administrator Dataverse. Les deux voies documentées d'auto-élévation échouent;
le client possédé exige `UserManagement.Users.Apply`, non publié.
Les rôles d'origine et l'ancien profil PAC actif sont vérifiés inchangés.
Aucun scope non pris en charge, rôle large ou consentement global n'est ajouté.

Le [rapprochement récent](../assets/runtime-2026-10-23/terraform-reconciliation.json)
termine le livrable de comparaison T013. Terraform 1.16.6 à empreinte officielle
vérifiée utilise une copie privée identique des 23 fichiers d'origine.
Init et validation retournent 0; le plan enregistré de 15 instances retourne 2.
La validation n'indique aucune erreur ni avertissement. Aucun apply, destroy
ni inscription automatique; l'absence du groupe réservé au plan est vérifiée.
L'ancien apply payant corrigé, ses écarts préservant la stratégie, la configuration
d'identité à l'exécution et son nettoyage sont conservés, pas rejoués.
Les limites modèle/sécurité/réseau du plan inchangé restent explicites.
Seuls D5-02/D5-03 gagnent des preuves récentes, pas toute la séquence connectée.

## Jeu Search fictif et contrôles de portabilité native

L'[exécution récente](../assets/runtime-2026-10-23/lab5-synthetic-search-retry.json)
réussit S5-03/S5-05/S5-06 avec le texte fictif original Harbor/Forest.
Six contrôles mesurés couvrent recherche lexicale, vectorielle naturelle,
hybride, hybride sémantique, filtrage exact du parent et HTTP 400 de champ non filtrable.
Le [premier essai](../assets/runtime-2026-10-23/lab5-synthetic-search.json)
s'arrête sur des statistiques nulles malgré deux chargements réussis, puis est
nettoyé. Le second essai explicite compte les documents par recherche réelle
et réutilise les plongements des mêmes entrées. Son index temporaire est aussi
supprimé; les trois schémas d'origine sont vérifiés inchangés.
Aucun rôle, paramètre d'authentification, index existant ni route native modifié.
Blob/indexeur, navigation des citations, réponse native, refus d'identité et
réussite globale de l'atelier ne sont pas déduits.

Les premières voies SDK disposent désormais d'un vrai clone et de fichiers
vérifiés. L'[échec d'empaquetage](../assets/runtime-2026-10-23/native-sdk-packaging.json)
et le [résultat Author](../assets/runtime-2026-10-23/native-sdk-author.json)
restent explicites. Le [précontrôle modèle/API de fichiers](../assets/runtime-2026-10-23/native-sdk-template-candidate.json)
établit une colonne de fichier prise en charge et la liaison existante, mais
le modèle omet instructions de routage et cinq composants sources.
Ces contrôles n'envoient aucune question SDK et ne prouvent pas la livraison parente complète.

L'[opération de préparation suivante](../assets/runtime-2026-10-24/native-sdk-staging-corrected-name.json)
crée un candidat non publié après correction d'un nom refusé sous le même schéma.
Ses deux fichiers relus ont les empreintes sources; la liaison autorisée est
vérifiée et authentification/accès/déclencheur valent 2/2/1.
Le parent est préservé; aucune question SDK, publication ni permission modifiée.
Les instructions de routage et cinq composants restent à reconstruire.

La [reconstruction locale](../assets/runtime-2026-10-24/native-sdk-reconstruction.json)
rédige maintenant les instructions et définitions manquantes : couverture de
26 composants, 24 définitions YAML validées, un avertissement de nom d'affichage
source et 14 opérations préparées avec contrôles des données et ETag.
Empreintes du clone et des fichiers inchangées. Aucune application en service,
publication ni acceptation de réponse n'est déduite de cette projection locale.

L'[application atomique gardée suivante](../assets/runtime-2026-10-24/native-sdk-managed-apply-reconciled.json)
réussit les 14 opérations et le contrôle indépendant des 26 composants après
rapprochement limité aux métadonnées de synchronisation. Empreintes, liaison,
authentification et lignes sources complètes sont vérifiées.
Le candidat passe d'une projection locale à une reconstruction en service
vérifiée, pas à un environnement publié ni testé par réponses.
La [capture de cette phase](../assets/runtime-2026-10-24/native-sdk-capture-reconciled.json)
contient encore zéro question et aucune réponse finale.

La [publication suivante du candidat seul](../assets/runtime-2026-10-24/native-sdk-publish-confirmed.json)
réussit selon l'état et la date de l'API indépendante malgré l'échec d'analyse
d'état PAC. Aucune republication ni modification de l'agent d'origine.
Les 26 définitions/états, fichiers, liaison et authentification/accès/déclencheur
2/2/1 restent vérifiés. La [capture SDK suivante](../assets/runtime-2026-10-24/native-sdk-capture-owned-client.json)
n'atteint ni conversation ni question : le client possédé ne reçoit aucun jeton
Invoke silencieux. Restauration application/consentement sans erreur, anciens
jetons et profil PAC conservés. Le diagnostic d'authentification reste nécessaire;
aucune réponse ni fin de tour complète n'est déclarée.

Le [diagnostic OAuth explicite](../assets/runtime-2026-10-24/native-sdk-auth-diagnostic.json)
résout ensuite l'erreur masquée : `AADSTS65001`/`consent_required`.
`prompt=none` dans le bon profil exige aussi le consentement; un essai PKCE
normal expire sans rappel. L'écouteur est fermé, aucun cookie/base de session
lu et [zéro requête SDK](../assets/runtime-2026-10-24/native-sdk-capture-recovered.json)
envoyée. La relecture finale consentement/manifeste correspond à l'état initial;
lignes sources, empreintes, liaison et publication/authentification restent vérifiées.

La [récupération suivante du consentement](../assets/runtime-2026-10-24/native-sdk-auth-consent-recovery-final.json)
vérifie un jeton Invoke après une attente unique de cinq minutes puis un
rafraîchissement forcé. Compte et ressource correspondent; les scopes OIDC
standards ne sont pas des blocages prouvés. Le SDK produit une activité de frappe,
sans démarrage terminé ni question. Des erreurs de transport affectent d'abord
la restauration; une récupération indépendante vérifie ensuite manifeste et
tous les consentements exacts, jetons Maker/rafraîchissement, lignes/fichiers/liaisons
sources et publication/authentification du candidat. Impossible d'identifier
sûrement les onglets expirés pour fermeture : ne les acceptez pas.
Le diagnostic du démarrage reste ouvert.

Le [diagnostic SDK suivant](../assets/runtime-2026-10-24/native-sdk-start-diagnostic.json)
capture l'en-tête de conversation faisant autorité et se termine normalement,
événement de démarrage désactivé. Ce réglage de diagnostic ne valide pas l'accueil.
La [capture réelle de deux tours](../assets/runtime-2026-10-24/native-sdk-capture-start-recovered.json)
envoie Hello et le cas SAR 6 inchangé sans nouvelle tentative : trois réponses
HTTP 200, démarrage inclus, et trois flux fermés normalement. Hello renvoie la
demande attendue de précision sur l'enquête. SAR renvoie l'Adaptive Card réelle
du parent demandant de connecter un compte Azure AI Foundry Agent Service,
puis Continue. Connect/Continue n'est pas invoqué. Les événements SAR réels sont
`DynamicPlanReceived`, `DynamicPlanStepTriggered` et `DynamicPlanStepBindUpdate`;
aucun `DynamicPlanFinished`, réponse métier ou comparaison de sources observé.
La liaison enregistrée ne démontre pas l'autorisation utilisateur à l'exécution.
Manifeste et tous les consentements utilisateur sont restaurés exactement,
un jeton d'accès Invoke temporaire supprimé, entrées Maker/rafraîchissement valide
conservées, et définitions/fichiers/liaisons/authentification source/candidat
ainsi que profil PAC antérieur préservés. L'acceptation native reste ouverte.

Le [suivi du connecteur](../assets/runtime-2026-10-24/native-sdk-connector-authorization.json)
vérifie profil navigateur et environnement, mais ne peut vérifier le compte
administrateur du site via UIAutomation. Arrêt avant Connect, sans nouvelle
question, modification de droits ou écriture cloud. Aucun échec MFA/OAuth observé.
Les contrôles indépendants de préservation réussissent sans erreur de vérification
ou restauration. Une vérification humaine du compte du site et le flux actuel
de connexion approuvée sont nécessaires; Continue doit attendre le succès observé.

Le [contrôle Azure du 24 octobre](../assets/runtime-2026-10-24/azure-preflight-refresh.json)
vérifie indépendamment les deux contextes Azure, quatre ressources conservées,
deux déploiements de modèles Succeeded, fournisseurs inscrits et compteurs de
quotas régionaux réels. Chat : 26/5 000; embedding : 1/1 000 (milliers de jetons/minute).
Le coût rapporté avant taxes des ressources possédées atteint 7,650361288 USD,
dont 7,373 USD pour Search, jusqu'au 24 octobre partiel. Il exclut les ressources
étrangères à l'atelier et ne représente ni facture finale ni total de crédits
Copilot. Aucune modification de configuration, inférence, facturation ou droit.
Budget/rétention et acceptation complète du lab 0 restent ouverts.
Les contrôles d'identité Azure ne vérifient pas le compte du site dans le navigateur.

Le [suivi visuel du navigateur](../assets/runtime-2026-10-24/native-sdk-connector-visual-verification.json)
inspecte une image PrintWindow limitée à la fenêtre, mais l'image blanche ne montre
aucun compte du site ou tenant lisible. Aucune action Connect/Continue; état réduit
initial restauré et contrôles indépendants de préservation réussis.

La [demande unique de focus suivante](../assets/runtime-2026-10-24/native-sdk-connector-focus-request.json)
met bien le navigateur vérifié au premier plan. Le contrôle du compte refuse
InvokePattern et les limites de capture échouent à la garde : aucune capture,
action Connect/Continue ou nouvelle question. État initial de fenêtre et contrôles
de préservation cloud, source/candidat, droits et cache vérifiés.

La [tentative par page navigateur prise en charge](../assets/runtime-2026-10-24/native-sdk-browser-page-recovery.json)
vérifie ensuite l'administrateur exact du site et la route de l'environnement.
Elle ouvre le formulaire Foundry Connect officiel et soumet Create une fois
avec le point de terminaison approuvé. Le formulaire renvoie réellement
**Unable to sign in. Please try again.** Aucun succès, Continue, nouveau SAR,
consentement accepté, publication ou modification YAML. Cette création est
une tentative d'écriture cloud. Lignes sources complètes, définitions/authentification
publiées du candidat, quatre empreintes, liaisons, application/consentements,
cache et PAC restent vérifiés préservés. Le compte illisible est remplacé par
un échec concret de connexion du connecteur, dont la cause n'est pas prouvée.

Le [gestionnaire natif Studio ultérieur](../assets/runtime-2026-10-24/native-studio-existing-connection.json)
propose la connexion approuvée existante et établit l'association réelle par
utilisateur, sans autre Create ni flux OAuth. Des réponses SAR natives arrivent,
mais trois passages entre guillemets dans deux messages ne sont pas exacts.
La paraphrase finale sans citation ne peut réussir par absence.
Autorisation du canal publié et appartenance aux résultats restent non prouvées.

Le [diagnostic hébergé existant](../assets/runtime-2026-10-24/native-studio-verified-diagnostic.json)
échoue ensuite réellement en HTTP 403 de tenant appelant BotServiceRbac.
L'[essai de point Entra seul borné](../assets/runtime-2026-10-24/native-studio-entra-only-diagnostic.json)
obtient un autre HTTP 400 de blueprint, pas une réponse réussie.
Les deux activations limitées au candidat reviennent à Off. Point/carte,
Entra avec BotServiceRbac, version hébergée 3, manifeste original et contrôles
indépendants source/candidat/application/consentements/cache sont vérifiés
préservés ou exactement restaurés, sans erreur de vérification/restauration.
Azure RBAC reste inchangé; aucun accès anonyme, déploiement ou publication.
Ces résultats remplacent le blocage de connexion Studio, pas le critère de
fidélité aux sources.
Le [nouvel essai SDK publié ultérieur](../assets/runtime-2026-10-24/native-sdk-post-studio-authorization.json)
renvoie toujours une carte de connexion par utilisateur pour un cas SAR
inchangé, malgré HTTP 200 et fermeture normale. Aucune réponse métier ou fin
de plan observée. Aucun Connect/Continue; changements temporaires
d'application/consentement possédés exactement restaurés, seul nouveau jeton
Invoke supprimé, contrôles source/candidat/fichiers/liaisons/authentification/
cas original/PAC réussis.

## Ingestion Blob fictive sous réseau privé imposé

L'[échec par réseau public](../assets/runtime-2026-10-24/lab5-blob-ingestion.json)
observe la stratégie Storage imposant Disabled au réseau public; le RBAC limité
ne contourne pas cette frontière. Vingt-cinq essais bornés renvoient 403.
Aucun indexeur ni inférence. Storage et les deux rôles limités au conteneur
sont supprimés, inventaire initial vérifié inchangé.

Le [chargement privé](../assets/runtime-2026-10-24/lab5-private-fictional-ingestion.json)
utilise un travail conteneur à identité managée/IP privée, DNS/point de terminaison
privés et Storage sans clé ni accès anonyme. Deux fichiers fictifs originaux
relus avec empreintes exactes, liste exactement `forest.txt`, `harbor.txt` :
S5-01 réussit. L'exécution est interrompue pendant l'attente du lien Search.
La récupération prend un ancien 404 pour la définition Storage et échoue avant
l'indexeur. Une course de suppression DNS asynchrone provoque une erreur initiale,
puis la zone vide possédée est supprimée et les quatre ressources initiales
retrouvées. Tous les reçus d'échec sont conservés.

La [nouvelle tentative privée](../assets/runtime-2026-10-24/lab5-private-fictional-ingestion-retry.json)
approuve le lien possédé et exécute l'indexeur privé : deux éléments traités,
aucun échec ni avertissement. La vérification renvoie 400 car le champ vectoriel
n'est pas récupérable. S5-02 n'est pas revendiqué sur le seul état.
Nettoyage et contrôles indépendants des objets/rôles/liens/ressources initiaux
réussis. Aucun document protégé, question d'agent, réponse connectée ou preuve
de navigation des sources.

L'[exécution avec relecture vectorielle corrigée](../assets/runtime-2026-10-24/lab5-private-fictional-ingestion-vector-readback.json)
réussit S5-01 et S5-02. Des jetons ARM/Search expirés interrompent initialement
relecture et nettoyage; les erreurs restent conservées. Une récupération CLI
prise en charge reprend le déploiement/chargement existant sans les répéter.
L'indexeur privé réussit avec deux fichiers, aucun échec ni avertissement.
Les deux vrais passages enfants correspondent exactement aux entrées, avec
métadonnées parent/source et vecteurs de 1 536 dimensions vérifiés. Le champ
vectoriel jetable est explicitement récupérable. Nettoyage ciblé final et
contrôles indépendants objets/rôles/liens Search/inventaire ARM réussis sans erreur
de nettoyage restante. Aucune exception de stratégie ni modification de sécurité
d'origine. Cinq critères du lab 5 réussissent, pas l'acceptation connectée
ni la feuille de route complète.

## Résultat initial du 20 octobre

L'échec du portail n'a pas arrêté l'investigation. Les appels authentifiés
Power Platform et Dataverse ont réussi. Le CLI Power Platform officiel a cloné
l'agent de l'atelier, ses deux outils et son PDF de licences téléversé.
Aucune configuration d'agent n'a été modifiée ou publiée. Aucun courriel n'a
été renvoyé et aucune nouvelle ressource Azure payante n'a été créée.

Cela prouve un parcours d'administration pris en charge, pas un parcours de
conversation complet. L'agent sauvegardé utilise le nouveau moteur CLI/GitHub
Copilot. Son clone réussi ne prouve pas l'exécution des rubriques du moteur
standard, des connaissances Search, de la télémétrie, des prompts BYOM ou des
agents Foundry connectés.

## Observations réelles des services

| Contrôle | Résultat observé | Limite d'acceptation |
|----------|------------------|---------------------|
| Environnement Power Apps prévu | HTTP 200 ; provisionnement réussi | Découverte de l'environnement uniquement |
| Dataverse `WhoAmI` | HTTP 200 | Appelant identifié, sans tous les droits de service |
| Agent connu de l'atelier | HTTP 200 | Agent et configuration exportés en privé |
| Composants limités à cet agent | Quatre enregistrements ; aucune page suivante | Deux outils connecteurs, un fichier joint et un composant de paramètres |
| Définitions sérialisées des composants | YAML dans `data` ; `content` null | Lecture des vraies définitions, sans confondre contenu null et outils absents |
| Authentification du CLI officiel | Identité Azure par défaut authentifiée et connectée | Connexion Azure CLI existante réutilisée ; aucune nouvelle inscription d'application |
| Clone officiel de l'agent | Terminé dans un chemin court | Administration/export réussis, pas un nouveau test de conversation |
| Découverte du point Direct Line | HTTP externe 400, 403/code 1002 imbriqué : `Bot does not belong to the tenant.` | Aucun point utilisable ni conversation ; cause non établie |
| Découverte des jeux d'évaluation maker | HTTP 403, `InsufficientDelegatedPermissions` ; permission `CopilotStudio.MakerOperations.Read` absente | Aucune exécution d'évaluation démarrée |

Le recognizer stocké est `CLICopilotRecognizer` et le modèle de création est
`cliagent-1.0.0`. L'authentification intégrée reste activée. Les deux outils
exportés sont **Search for users (V2)** et **Send an email (V2)**, avec
authentification de l'appelant. Identités et références de connexion restent privées.

La liste du CLI affiche l'état du composant Dataverse `Published`, tandis que
le champ `publishedon` de l'agent est null. Aucune de ces observations n'a été
prise pour la preuve d'un canal publié utilisable. L'agent existant n'a pas
été publié pour faire réussir le test.

## Restaurer le CLI officiel sans affaiblir les stratégies

1. Vérifiez l'installation existante avant de modifier les dépendances.
   Ici, `pac` était absent du PATH.
2. Essayez la distribution .NET documentée par Microsoft dans un chemin de
   session. NuGet v3 a échoué en TLS ; l'essai officiel v2 s'est bloqué et a
   été arrêté. Validation des certificats et réglages proxy sont restés intacts.
3. Utilisez la distribution officielle de l'extension VS Code Power Platform
   Microsoft lorsque son CLI intégré est disponible. Résolvez son package
   depuis les métadonnées de l'éditeur Microsoft du Visual Studio Marketplace,
   et non depuis un miroir non fiable.
4. Récupérez le package intégré par son véritable actif CDN HTTPS. La passerelle
   initiale a expiré. Le CDN acceptait les requêtes ordinaires de plages
   d'octets, permettant de récupérer seulement les packages nécessaires.
5. Vérifiez l'intégrité. L'exécutable Windows possédait une signature
   Authenticode **Valid** de **Microsoft Corporation**. CRC ZIP et longueurs
   ont été contrôlés. Cela ne prétend pas à une vérification distincte de la
   signature du package.
6. Gardez le CLI isolé. Les CLI Windows et .NET **2.13.1** ont été obtenus.
   L'outil .NET a été installé depuis le package officiel déjà téléchargé,
   avec une source NuGet exclusivement locale. Aucune installation globale
   n'était nécessaire.

Le CLI Windows .NET Framework indique que son serveur MCP n'est pas pris en
charge. Celui de l'outil .NET s'est initialisé et a fourni ses vrais schémas.
Sa découverte administrative/des évaluations ne constitue pas une conversation.

Le bundle d'administration du plugin Copilot installé a aussi échoué à cause
d'une dépendance native absente. Une restauration isolée a été tentée, mais npm
a renvoyé `EALLOWREMOTE` sous la stratégie de packages configurée. Aucun registre
alternatif ni contournement de stratégie n'a été utilisé. Le parcours PAC
fonctionnel est resté distinct.

## S'authentifier et cloner sans risque

Utilisez la véritable URL Dataverse découverte pour l'environnement prévu.
Ne la remplacez pas par le domaine du locataire et ne la déduisez pas du nom
d'affichage de l'agent. Les exemples utilisent des paramètres fictifs et
omettent les détails privés de connexion.

```powershell
$env:AZURE_TOKEN_CREDENTIALS = 'AzureCliCredential'
& $pac auth list
& $pac auth create --name 'workshop-test' --managedIdentity `
  --environment '<URL HTTPS Dataverse réelle>'
& $pac copilot clone --bot '<ID connu de l agent de l atelier>' `
  --display-name 'lab1' --output-dir '<répertoire privé court>'
```

Ici, `--managedIdentity` désigne la chaîne d'identité Azure par défaut documentée.
Elle a réutilisé l'identité Azure CLI existante ; cela ne signifie pas que le
poste a acquis l'identité managée d'une ressource Azure. Le sélecteur d'identité
limité au processus n'a pas été enregistré comme réglage de la machine.

Notez le profil PAC actif initial et restaurez-le dans `finally` après chaque
opération. Le test a préservé le profil existant et l'a réactivé après chaque
utilisation du profil nommé de l'atelier. Ne supprimez jamais tous les profils.

Le premier clone a rencontré `DirectoryNotFoundException` en écrivant un long
nom de connexion sous le chemin profond de session. Sa sortie partielle n'a pas
été comptée comme un clone réussi. La reprise dans cette destination non vide
a été refusée. Un nouveau chemin privé court a réussi ; un clone persistant
en chemin court a aussi réussi. Aucun réglage global des chemins longs ni
fichier utilisateur n'a été modifié.

## Preuves et travail restant

Configuration brute, PDF source, définitions de connexion et réponses d'identité
restent privées. Les [résultats backend expurgés](../assets/runtime-2026-10-19/backend-results.json)
ne publient que des observations ciblées, nombres et limites d'acceptation.
L'audit indépendant du lab 1 distingue identité de la source et exactitude
de la réponse : un hash PDF égal ne prouve pas chaque affirmation ou citation.

Le PDF fraîchement cloné contient **867 776 octets**. Son SHA-256 égale celui
de l'original approuvé recalculé et le hash antérieurement consigné. L'audit
indépendant a réussi **6 contrôles sur 8**, avec **2 bloqués** et aucun échec.
Il ne revendique aucun nouvel appel réel ni contrôle du contenu PDF.

Le texte complet de la réponse sauvegardée et sa correspondance avec les
cibles de citation restent nécessaires à l'audit complet du lab 1. Les captures
tronquées ne doivent pas être reconstruites en une transcription inventée.
Les six contrôles antérieurs du contenu PDF restent des preuves historiques
tant qu'ils ne sont pas réellement réexécutés.

Avant tout nouveau provisionnement payant, établissez un parcours autorisé
de création et de test d'agent standard. L'évaluation exige une identité
acceptée par cette API ; l'accès Dataverse n'a pas suffi. Ne contournez pas
le 403, ne désactivez pas l'authentification, n'élargissez pas les rôles de
manière spéculative et ne publiez pas l'agent utilisateur pour lever le blocage.

Aucune nouvelle capture produit n'est revendiquée pour cette poursuite backend.
La galerie existante préserve la provenance de ses vraies captures. Tous les
environnements payants antérieurs restent supprimés ; outils locaux et
sauvegarde privée de la source ne sont pas des ressources cloud déployées.

## Suivi : diagnostic précis des droits et essais limités

Le corps de réponse du journal officiel PAC identifie précisément l'échec
d'évaluation maker : `InsufficientDelegatedPermissions`, avec la permission
déléguée `CopilotStudio.MakerOperations.Read` absente de l'application.
Il s'agit d'une erreur API observée, pas d'une supposition concernant les
rôles Azure de l'utilisateur. Ajouter un rôle Azure plus large n'est pas
une correction justifiée. L'erreur distincte Direct Line reste inexpliquée.

La [documentation d'authentification Power Platform](https://learn.microsoft.com/en-us/power-platform/admin/programmability-authentication-v2)
exige une application dotée des permissions API adaptées et un jeton utilisateur
autorisé. Configuration d'application, consentement utilisateur et consentement
administrateur se distinguent d'une connexion Azure CLI ou Dataverse réussie.
Aucune application, permission ou autorisation globale du locataire n'a été créée.

Une demande de jeton limitée au droit de lecture observé a été tentée avec
la connexion existante. Elle n'a fourni aucun résultat de jeton utilisable
avant son arrêt. Cela ne prouve ni consentement réussi, ni jeton corrigé,
ni rejet serveur supplémentaire. La stratégie npm a aussi refusé une
restauration hors ligne des dépendances avec `EALLOWREMOTE` ; aucun
contournement de stratégie n'a été tenté.

Un Test Agent indépendant a essayé le parcours Preview du moteur actuel
historiquement vérifié, sans répéter le parcours classique cassé. L'ancien
onglet navigateur était indisponible. Une seule opération d'ouverture a expiré
sans renvoyer d'identifiant de page ; son effet final est inconnu. Aucune boucle,
question, réponse, vérification de citation ou nouvelle capture n'en a résulté.

La reprise légitime exige une session déléguée application/utilisateur autorisée
pour l'évaluation, ainsi qu'une destination standard accessible pour les tests.
Demander une permission, l'accorder et réussir l'appel API sont trois étapes
distinctes. Une vraie personne autorisée doit effectuer le consentement ou la
connexion interactive nécessaire ; une réponse automatique d'indisponibilité
ne l'autorise pas.

## Reprise du navigateur et trois nouveaux contrôles réels

Le 20 octobre, le parcours navigateur connecté est redevenu accessible.
La configuration et l'historique correspondaient au conseiller de licences
utilisé précédemment. Cela confirme la continuité avec cet agent de
l'environnement Default, pas une vérification indépendante de l'environnement
initialement visé ni d'une destination d'agent standard.

Trois nouveaux contrôles Preview ont satisfait leurs attentes limitées :

* La recherche dans le fichier chargé a renvoyé
  `Power-Platform-Licensing-Guide.pdf`, référence `turn1doc1`, avec une latence
  affichée de 4,9 secondes. La nouvelle réponse complète indique octobre 2026,
  cite une phrase d'introduction et référence le titre du fichier via `cite:1`.
* Une question sur une remise non publiée du locataire fictif Contoso a
  explicitement refusé d'inventer une remise ou un prix négocié propre au client.
* Search for users (V2), appelé une seule fois avec une recherche synthétique
  et `top=-1`, a affiché les entrées correspondantes et
  **Request validation · 400**, avec une latence affichée de 4,5 secondes.
  Aucune nouvelle tentative n'a été observée. Le message plus précis exigeant
  un nombre positif provenait de l'agent, pas du panneau d'erreur développé.

Les [preuves navigateur expurgées](../assets/runtime-2026-10-20/browser-results.json)
conservent les questions exactes, les nouvelles réponses complètes, les sorties
observées et leurs limites. La page, l'édition et la citation doivent encore
être contrôlées indépendamment dans le PDF. Un titre identique ne prouve pas
qu'une ancre de page fonctionne ; cette nouvelle réponse ne reconstitue pas
l'ancienne transcription. L'erreur de l'annuaire prouve la validation des
entrées, pas la récupération après une panne du service en aval.

Evaluate s'ouvre désormais et affiche **Create your first evaluation**, avec
un avertissement sur les Copilot Credits. Aucune évaluation n'a été créée ou
exécutée. Le formulaire d'approbation a signalé l'indisponibilité de
l'utilisateur, pas une autorisation. Cette limite du navigateur est distincte
de l'échec PAC antérieur pour permission déléguée absente, qui reste non corrigé.

Aucun courriel n'a été envoyé ; configuration, permissions, consentement,
authentification et publication de l'agent sont inchangés. Aucune ressource
Azure n'a été créée. L'inférence et la recherche Preview ont bien eu lieu ;
une estimation affichée à zéro crédit ne prouve pas une facturation nulle.
Aucun nouveau fichier de capture n'a été conservé ni ajouté à la galerie.
L'atelier reste incomplet : audit indépendant des citations, notation des
évaluations et parcours connectés Search, télémétrie, BYOM et Foundry.

## Audit indépendant de la nouvelle réponse PDF

Après la reprise, un contrôle indépendant PyMuPDF a examiné le clone PAC
officiel conservé, au lieu de demander à l'agent de se vérifier lui-même.
Les **cinq contrôles ont réussi** : le clone correspond au téléchargement
original et au SHA-256 antérieur ; l'édition, la citation complète et le nom
de section de la nouvelle réponse correspondent à la page physique 3.
Seuls les espaces ont été normalisés pour comparer la citation.
Le PDF contient 30 pages et 867 776 octets.

Les [résultats de l'audit source](../assets/runtime-2026-10-20/pdf-answer-audit.json)
remplacent la réserve précédente sur l'exactitude du contenu pour cette seule
nouvelle réponse. Ils ne vérifient ni l'ancienne réponse complète sur les offres,
ni l'ouverture du fichier et de la page attendus en cliquant sur `cite:1`.
Aucun nouveau téléchargement distant n'a été effectué pour cette comparaison
locale. La navigation des citations du lab 1 et l'acceptation complète de
l'atelier restent donc à vérifier.

## Évaluation approuvée et soumise, notation non observée

Le propriétaire a ensuite approuvé les Copilot Credits et les ressources Azure.
Le parcours Evaluate connecté a enregistré
**Read-only licensing 3 cases 2026-10-20** et soumis exactement
**une exécution**, avec un début affiché à 7 h 25.
Les trois cas utilisent le véritable évaluateur **General quality** de l'interface :

* Retrouver l'édition du guide chargé et une phrase d'introduction
* Refuser une remise et un prix négocié propres à un locataire inventé
* Rejeter un produit fictif et une capacité gratuite illimitée non documentés

General quality contrôle la pertinence et l'exhaustivité, sans comparaison à
une réponse attendue. Aucun évaluateur de correspondance exacte ni score final
n'est revendiqué. La notification réelle annonçait une mise en attente jusqu'à
disponibilité de capacité. La vue d'ensemble affichait **Waiting**, sans
réponses par cas, notes ni total de crédits. Une durée croissante et le champ
de crédits Running n'ont pas été considérés comme une preuve d'exécution.

![L'évaluation approuvée était en attente, sans notation](../assets/runtime-2026-10-20/evaluation-queued.png)

À **11:36:20 UTC**, deux essais limités de réouverture de la même exécution
ont échoué : l'interface existante a signalé `ERR_CONNECTION_RESET` ;
une nouvelle page ciblant cette même exécution s'est interrompue pendant
la redirection Microsoft. L'état actuel est donc **inconnu**. Waiting est
la dernière observation historique, pas un état nouvellement vérifié.
L'exécution soumise reste en place et peut démarrer ultérieurement.
Aucune exécution en double ni annulation n'a été demandée.

Une dernière vérification différée à **13:01:03 UTC** a rencontré la même
réinitialisation de connexion et s'est arrêtée après une navigation.
Aucun nouvel état, score ni total de crédits n'était accessible.
Le [registre de cette dernière vérification](../assets/runtime-2026-10-20/evaluation-final-recheck.json)
conserve cette observation sans modifier les preuves historiques d'attente.

Les [preuves d'évaluation](../assets/runtime-2026-10-20/evaluation-results.json)
conservent questions, évaluateur réel, état d'attente et échecs horodatés.
Configuration, authentification, permissions et consentement de l'agent sont
inchangés. L'opérateur n'a demandé ni envoyé de courriel. Sans traces terminées,
le comportement éventuel des connecteurs de l'évaluation ne peut pas être
certifié indépendamment. Ce test navigateur n'a nécessité aucune ressource Azure.

Une question distincte sur la navigation des citations a renvoyé une URI de
fichier en texte brut, sans citation cliquable exposée. Aucun fichier ni cible
de page n'a été ouvert. L'audit indépendant du contenu source reste valable,
mais la navigation des citations demeure non vérifiée. L'atelier est incomplet.

## Erreur de l'onglet restauré et preuves backend récentes

Lors de la poursuite suivante, le nouvel onglet Agents partagé a été inspecté
avant toute navigation. Il affichait **Dataverse isn't set up in this environment**
à la racine de l'agent existant, pas sur les résultats d'évaluation.
Le retour direct à l'exécution déjà soumise a expiré, puis la connexion
au navigateur a échoué. Aucun nouvel état, réponse, score ni total de crédits
n'a été obtenu. Aucune capture n'est revendiquée pour cette inspection.

Le [registre de l'onglet restauré](../assets/runtime-2026-10-20/evaluation-restored-tab.json)
conserve le message réel et distingue les événements de console conservés
des nouvelles observations. Ce seul message ne prouve ni suppression,
ni absence de base, ni nécessité de créer une infrastructure de remplacement.

De nouveaux contrôles backend en lecture seule à **17:25 UTC**, selon
l'horloge de l'hôte d'exécution, ont ensuite renvoyé :

* Découverte de l'environnement HTTP **200**, état **Succeeded**, avec
  le même point d'accès Dataverse que dans les preuves précédentes
* WhoAmI Dataverse HTTP **200**, même utilisateur et même organisation
* Agent d'atelier exact HTTP **200**, correspondant à l'agent du portail,
  avec nom et schéma inchangés

La [comparaison backend](../assets/runtime-2026-10-20/evaluation-backend-diagnosis.json)
confirme donc que l'environnement et l'agent existants restent lisibles.
Elle ne prouve pas tous les prérequis du portail et n'explique pas l'erreur
d'affichage. L'API d'évaluation précédemment refusée n'a pas été rappelée.
Aucune base, environnement, identité, permission, consentement ou configuration
d'agent n'a été modifié. L'état de l'unique évaluation soumise reste inconnu.
Rétablissez une session de portail autorisée fonctionnelle ou obtenez une voie
applicative déléguée approuvée avant d'annoncer des résultats ; ne créez pas
de base de remplacement uniquement pour faire disparaître ce message.

## Résultats de l'évaluation terminée récupérés dans la session fonctionnelle

Vers **19:13 UTC**, la session SPA connectée fonctionnelle a exposé la page
Results de l'exécution d'origine et ses détails par cas. Aucune nouvelle
exécution n'a été soumise. L'évaluation terminée a utilisé **7 Copilot Credits**
et affiché **00:02:44** : **une réussite et deux échecs**, selon General quality.

| Cas | Note réelle | Retour observé |
|-----|-------------|----------------|
| Produit fictif et capacité gratuite illimitée | Pass | Pertinent, complet et fondé sur les connaissances |
| Remise inventée propre à un locataire | Fail | Pertinence en échec ; refus d'inventer reconnu ; contrôles suivants ignorés |
| Édition du guide et phrase d'introduction | Fail | Pertinent, mais incomplet et sans références de connaissances selon l'évaluateur |

Les [preuves de l'évaluation terminée](../assets/runtime-2026-10-20/evaluation-completed.json)
conservent réponses réelles et retours de notation. Le refus suggère un possible
écart entre évaluateur et objectif du cas négatif, pas une autorisation
d'annuler l'échec enregistré. La réponse PDF contient des marqueurs visibles
et une entrée de connaissance ; cela n'invalide pas la note et ne prouve
pas la navigation des citations. Les traces complètes n'ont pas été examinées.

La même session a atteint Overview d'un agent **Standard** existant, avec
Test **Connected**, sélection Azure AI Search et paramètres Application Insights.
Ces contrôles établissent un point de départ utilisable, pas la réussite
des parcours connectés Search, télémétrie, BYOM ou Foundry.
Aucun agent existant n'a été modifié pendant cette reprise.
L'ancienne erreur de configuration n'a pas été reproduite ; sa cause
initiale reste non prouvée.

## Connexion Search sans clé bloquée par le navigateur hôte

Après prolongation approuvée de l'essai, un service Basic Search jetable et un
compte d'embeddings sans clé ont été créés. Les index distincts contenaient
30 pages du PDF de licences et trois documents hôteliers d'origine. Deux vraies
requêtes avec vectorisation en langage naturel ont retourné le texte source
exact. Le PDF de l'éditeur correspondait octet pour octet au fichier autorisé ;
aucune URL navigable d'hôtel n'était disponible ni inventée.

Dans le brouillon Standard isolé, le formulaire **Microsoft Entra ID Integrated**
a activé Create avec l'adresse HTTPS Search. Des activations distinctes prises
en charge ont retourné la même erreur :

> The connection consent pop-up window has been blocked by the browser. Please
> allow pop-ups in your browser and try again.

Aucun véritable écran de connexion ou de consentement ne s'est ouvert. Après
annulation, le sélecteur affichait **Not connected**, **No connections available**
et **Next** désactivé. Aucun index, mappage ou source n'a été sauvegardé ; zéro
question Copilot exécutée. Le blocage vient du navigateur hôte, non d'un échec
établi des droits Azure ou du point de terminaison. Les tests du vectoriseur ne
valident ni l'ancrage connecté ni la navigation des citations.

La [tentative nettoyée](../assets/runtime-2026-10-20/search-connected-attempt.json)
conserve ces limites. L'utilisateur était indisponible pour le formulaire de
reprise ; aucun consentement ni changement de sécurité n'a été déduit. Tout
provisionnement supplémentaire, dont la réutilisation Foundry, a été arrêté.
Le nettoyage dédié a été autorisé sous réserve de vérifier l'absence de connexion
distante. La suppression exige une preuve distincte. À **20:42:56 UTC**, la relecture
après navigation a vérifié Knowledge et Tools sauvegardés vides et aucune connexion
Search disponible ; l'assistant non sauvegardé a été abandonné. Cela établit la
préparation au nettoyage visible dans le portail, non un inventaire des connexions
du locataire ni une suppression Azure. Reprenez via les contrôles
normaux de fenêtres contextuelles ou une session interactive fonctionnelle ;
arrêtez si un nouveau consentement de permissions ou administrateur apparaît.

La [preuve de nettoyage](../assets/runtime-2026-10-20/search-cleanup.json)
distincte vérifie la suppression à **20:48:11 UTC**. Groupe dédié, service Search,
compte IA, déploiement d'embeddings et quatre attributions de rôles dédiées
ont renvoyé HTTP 404. Le fichier privé de connexion a été supprimé ; les identités
sans rapport et destinations de politiques externes sont restées intactes.
Aucune ressource active de ce test ne subsiste ; des frais horaires Search et de
jetons d'embeddings antérieurs peuvent encore apparaître. Le nettoyage ne
transforme pas les tests Copilot bloqués en réussites.

## Connexion formelle par clé et quatre vraies questions exécutées

Une autre voie prise en charge a utilisé le formulaire normal **Power Apps >
Connections > New connection > Azure AI Search**. Les règles héritées examinées
n'interdisaient pas les clés Search ; l'obligation sans clé Cognitive Services
est restée active. Un nouveau service jetable isolait l'accès administrateur
aux données de ce seul service. Les vecteurs en cache ont été réutilisés, sans
nouveaux jetons d'embedding documentaire. Aucune écriture manuelle YAML/API
de connexion, nouveau consentement ou modification de sécurité du navigateur.

La connexion formelle affichait **Connected** sans fenêtre OAuth, et la source
Search a atteint **Ready**. Quatre vraies questions ont été exécutées :

| Cas | Résultat réel | Limite restante |
|-----|---------------|-----------------|
| Citation de licences | Phrase complète auditée, édition octobre 2026, page physique 3 et cible PDF/page authentique conformes | Navigation par clic et page du lecteur non vérifiées |
| Produit de licences absent | Échec : absence reconnue puis droits probables extrapolés avec citations sans rapport | Corriger et retester l'exigence de preuves sources |
| Localisation hôtelière | Qatar correspond au véritable champ de localisation source | Le jeu de test attendait la ville Doha ; écart source/attente, non Qatar inventé |
| Navette hôtelière non documentée | Abstention réussie sans horaire inventé | Aucune URL externe authentique du document hôtelier |

La citation hôtelière a ouvert le contenu source interne, non un lecteur PDF
original. L'index hôtelier a été sauvegardé séparément, avec l'index de licences
exclu ; aucune contamination observée. Le portail n'exposait pas le mappage :
le schéma Azure n'est donc pas présenté comme une relecture du portail.

L'[exécution nettoyée](../assets/runtime-2026-10-20/search-accesskey-execution.json)
conserve l'échec d'origine. L'acceptation globale reste échouée en attente de
correction. À cette observation, source, connexion formelle et ressources étaient
conservées. Les preuves de suppression antérieures ne concernent que les
environnements précédents.

## Correction native de l'ancrage et trois questions de régression

L'auteur a réconcilié le brouillon réel avec PAC officiel avant de proposer
une seule propriété `additionalInstructions` sur le vrai nœud génératif classique.
Douze contrôles de schéma ont réussi, mais l'empaquetage PAC 2.13.1 a rejeté le
dossier de connaissances et le fichier de références de connexion légitimes.
Aucun fichier n'a été retiré et aucune poussée CLI effectuée.

La propriété native de personnalisation du prompt a fourni une autre voie.
Les trois paragraphes généraux exigeant des preuves ont été sauvegardés à
**22:35:50 UTC**, puis relus après navigation et réouverture à **22:37:49 UTC**.
Références sources et orchestration conservées. Trois nouvelles conversations
sur l'index de licences seul ont ensuite été exécutées :

* Le produit fictif n'a plus entraîné de droits inventés, mais un repli générique
  demandant de reformuler, sans explication spécifique aux sources.
* Une autre question sur des minutes de téléphone satellite non documentées a
  provoqué une abstention explicite, sans capacité inventée.
* La régression positive a conservé la phrase auditée complète, l'édition
  octobre 2026, la page physique 3 et la cible PDF/page authentique.

Les [preuves de correction](../assets/runtime-2026-10-20/search-portal-rework.json)
conservent l'échec d'origine, les sept questions connectées et les limites.
Le jeu hôtelier demande désormais la **localisation source, Qatar**, non une
ville déduite ; le corpus d'origine est inchangé et aucune question hôtelière
supplémentaire n'est comptée. L'ouverture directe du PDF authentique a expiré :
la navigation dans le lecteur reste non vérifiée. Le traitement de l'absence
de réponse doit encore préciser les limites des preuves sources. Ces résultats
ne certifient pas l'atelier complet ni la suppression des ressources conservées.

## Traitement explicite de l'absence de réponse réussi

La dernière correction a ajouté uniquement une branche `elseActions` à la
condition de réponse existante dans Conversational boosting. Une réponse vide
déclenche l'abstention précisant les limites des sources, puis termine le dialogue.
Réponse automatique non vide, citations, trois paragraphes d'ancrage, références
sources et réglages conservés. Repli global et traitement d'erreurs inchangés.
La sauvegarde native à **22:52:26 UTC** et la réouverture à **22:53:55 UTC**
ont vérifié la persistance ; aucune poussée CLI.

Deux nouvelles conversations sur les licences seules ont réussi. La demande
non documentée d'origine a reçu :

> I could not establish the requested information from the configured source
> evidence. I will not infer an answer.

Aucune citation ni droit inventé. La régression positive a conservé phrase exacte,
édition octobre 2026, page physique 3 et cible PDF/page authentique, avec une
seule réponse finale sans message d'abstention. Les
[preuves finales](../assets/runtime-2026-10-20/search-source-noanswer.json)
comptent **neuf questions Search connectées**, avec l'échec d'origine et le
repli générique intermédiaire conservés. Cela valide le traitement de l'absence
de preuve, non la navigation PDF externe ni l'atelier complet.

## Authentification formelle Foundry toujours bloquée

Le compte IA jetable existant ne gérait initialement pas les projets. Un PATCH
de fonctionnalité pris en charge l'a activé sans modifier l'authentification
sans clé imposée ni la sécurité réseau. Un seul projet enfant dédié avec identité
managée a été créé ; aucun nouveau rôle de projet, modèle, agent ou appel.

Avec le véritable point de terminaison renvoyé par ARM, une seule tentative
formelle **Power Apps > Connections > Azure AI Foundry Agent Service >
Microsoft Entra ID User Login** a échoué à **23:01:40 UTC**, avec la même erreur
de fenêtre bloquée. Après annulation, l'actualisation native à **23:02:28 UTC**
affichait zéro connexion Foundry, sans référence ni point enregistré dans le
brouillon. Aucun consentement, nouvel essai, extraction de jeton ou contournement
de sécurité.

La [preuve d'authentification](../assets/runtime-2026-10-20/foundry-formal-auth.json)
distingue cet échec observé des appels modèle ou Activity, non exécutés.
La suppression prise en charge de la nouvelle source/connexion Search et le
nettoyage dédié ont ensuite été autorisés. Leur suppression exige une nouvelle
preuve ; les anciens nettoyages ne couvrent pas cet environnement.

## Environnement actuel par clé déconnecté

À **23:15:35 UTC**, la relecture du portail a vérifié la source Search absente
après navigation, Tools vide et aucune permission de connexion de l'agent.
Les instructions corrigées et les deux branches de réponse restaient sauvegardées,
sans référence dédiée de point de terminaison, source ou connexion dans la rubrique.

Avant suppression, la vue native des dépendances indiquait qu'aucune application
ou aucun flux n'utilisait la connexion. Seule la connexion Search jetable nommée
a été supprimée. L'actualisation native à **23:13:27 UTC** montrait zéro connexion
Search dédiée et zéro Foundry ; les autres connexions ont été préservées.
La [preuve de suppression distante](../assets/runtime-2026-10-20/search-accesskey-removal.json)
est limitée au portail, non à un inventaire backend brut ni à une suppression
Azure. Aucune nouvelle question, authentification, navigation PDF ou publication.

Le [nettoyage Azure de cette exécution](../assets/runtime-2026-10-20/search-accesskey-cleanup.json)
a terminé à **23:20:01 UTC**. Des lectures indépendantes ont renvoyé HTTP 404
pour projet enfant, rôle dédié unique, groupe, Search, compte IA et déploiement.
La destination de gouvernance externe renvoyait HTTP 200 avant et après, sans
modification. Les fichiers éphémères de secret et de point de projet ont été
supprimés. Aucune ressource dédiée active de ce test ne subsiste ; les frais
mesurés et de diagnostics imposés peuvent encore apparaître. La rubrique
corrigée non publiée et tous les résultats historiques sont préservés.

## Le navigateur natif a confirmé le lecteur PDF de l'éditeur

Un contrôle ultérieur en lecture seule, via les contrôles d'accessibilité Windows
normaux, a trouvé le PDF déjà chargé dans la fenêtre exacte de l'espace VS Code.
L'adresse correspondait à l'URL publique vérifiée avec `#page=3`. Le document
natif indiquait **30 pages**, le numéro courant **3**, et le groupe **Page 3**
contenait **Using This Guide** et la phrase auditée complète.

La [preuve du lecteur natif](../assets/runtime-2026-10-20/native-pdf-viewer.json)
lève l'ancienne impossibilité d'observer le lecteur sans effacer les expirations.
Elle prouve le contenu accessible à la cible authentique, non l'origine de
l'onglet ni le clic initial sur la citation du chat. Aucune nouvelle question,
ressource, affirmation de hachage natif, capture publiée, extraction de jeton
ou modification de sécurité du navigateur.

## Reprise Foundry via Edge externe

Le navigateur Edge externe normal a atteint **Power Apps | Connections** via la
session SSO professionnelle existante. Le compte prévu a été vérifié sans
publier son identité. Il s'agissait d'une autre voie de navigation prise en
charge, sans contournement des fenêtres ni répétition de l'échec du navigateur
intégré.

Un nouveau compte S0 sans clé et son projet enfant à identité managée ont été
créés uniquement pour l'authentification. Aucun modèle, agent, rôle ni appel
d'inférence ajouté. Le vrai formulaire **Azure AI Foundry Agent Service**
proposait **Microsoft Entra ID User Login** et exigeait un **Azure AI Project
Endpoint**. Le nom persistait, mais le focus natif, la saisie clavier normale et
ValuePattern d'UI Automation ne conservaient pas le point de projet réel.
À **23:44:08 UTC**, le champ était vide et **Create** désactivé. Le formulaire
non soumis a été annulé.

La [preuve d'authentification native externe](../assets/runtime-2026-10-20/foundry-external-native-auth.json)
consigne **zéro invocation de Create et zéro soumission d'authentification**.
Aucun rejet d'authentification, comportement de fenêtre externe ni cause racine
n'a été établi. L'absence de connexion sauvegardée n'était pas vérifiée
indépendamment à l'arrêt de la saisie. Aucun consentement, mot de passe, MFA,
extraction de jeton, changement de sécurité ni inspection d'autres onglets.

Une inspection en lecture seule a trouvé **Azure AI Foundry Inference**, sans
exposer ses champs d'authentification. Ses choix et sa compatibilité avec le
prompt BYOM natif restent non vérifiés. Cela ne change ni le formulaire natif
observé exigeant une clé ni sa limitation face à la politique sans clé imposée.
Le relais manuel demandé n'était pas disponible ; aucune autre authentification
ni création de modèle n'a été tentée.

Une lecture ultérieure de la [référence officielle du connecteur Inference](https://learn.microsoft.com/en-us/connectors/azureaifoundryinference/)
n'a trouvé que l'authentification **Default**, avec **Target Uri** et **API Key**
obligatoires. Ce contrat publié ne documente pas d'alternative Entra. Il répond
à la question documentaire sans inventer de lecture native du formulaire ni
prouver la compatibilité avec le sélecteur de modèle du prompt. Aucun modèle
de remplacement ni passerelle n'a été provisionné sur cette base.

La navigation normale a retrouvé le document exact Connections. À **23:55:42 UTC**,
une liste actualisée non filtrée du bon environnement ne contenait aucune
connexion Foundry dédiée. Cela remplace l'ancien constat non vérifié : preuve
d'interface native, non inventaire brut du backend. Le contrôle de fermeture de
l'onglet exact n'a pas pu être identifié avec certitude ; l'onglet Power Apps
est resté ouvert pour ne pas risquer de fermer un onglet sans rapport.

Le [nettoyage d'authentification seule](../assets/runtime-2026-10-20/foundry-external-auth-cleanup.json)
s'est terminé à **23:58:49 UTC**. Les GET indépendants du projet, du compte et du
groupe ont tous renvoyé **404**. L'espace de gouvernance externe est resté à
**200** avant et après, sans modification. Le fichier privé de point de projet
a été supprimé et aucune ressource dédiée active ne subsiste. Un **enregistrement
de récupération du compte supprimé reste présent**, avec HTTP 200 ; aucune purge
autorisée ni tentée. Des frais antérieurs peuvent encore apparaître.
Toute future connexion manuelle exige un nouveau point de projet approuvé, non
celui supprimé. L'atelier complet reste incomplet.

## Prérequis supplémentaire de saisie native toujours bloqué

Après la demande de poursuite autonome, un contrôle distinct sans ressource a
été autorisé pour la méthode normale **LegacyIAccessiblePattern.SetValue**.
Aucun essai antérieur de cette méthode n'était consigné. Les demandes natives
New connection n'ont pas ouvert le formulaire et le contrôle de premier plan
de la fenêtre exacte a échoué. Arrêt avant d'atteindre le champ : **zéro sonde
de saisie Legacy**, invocation de Create, soumission ou nouvelle ressource.

À **00:06:08 UTC le 21 octobre**, une lecture native actualisée et non filtrée
montrait toujours le bon document Connections, recherche vide, aucune ligne
Foundry et aucun formulaire ouvert. La [preuve du prérequis](../assets/runtime-2026-10-20/foundry-native-input-prerequisite.json)
ne déclare pas Legacy non pris en charge ni testé. Aucun accès au presse-papiers,
aux mécanismes internes du navigateur, aux réglages de sécurité ou aux autres
onglets.

L'action requise est de mettre manuellement au premier plan l'onglet Power Apps
autorisé et d'ouvrir le formulaire Agent Service vide. L'intervention demandée
n'était pas disponible. Aucun nouveau projet n'a été créé pour répéter ce
blocage ; le nettoyage vérifié reste valide. L'acceptation réelle complète
reste bloquée, non terminée.

## Saisie rétablie dans le navigateur partagé, non authentification externe

La page Connections partagée ensuite était lisible avec les outils du navigateur
intégré. Les clics expiraient même après la mise au premier plan normale.
L'activation clavier ordinaire a ouvert New connection et le vrai formulaire
Agent Service. La sonde inoffensive `https://example.invalid` persistait après
perte du focus et activait Create. Le formulaire sélectionnait toujours
**Microsoft Entra ID User Login**.

La [preuve du navigateur partagé](../assets/runtime-2026-10-20/foundry-shared-browser-input.json)
prouve donc la saisie sur cette page intégrée et lève le besoin de mise au premier
plan manuelle pour cette seule voie. Elle ne prouve ni la reprise de saisie dans
Edge externe ni la levée du blocage de fenêtre d'authentification déjà observé
dans le navigateur intégré. Create n'a jamais été invoqué. Le formulaire a été
annulé, sa fenêtre fermée et la navigation normale est revenue aux connexions
sauvegardées. Aucune ressource, consentement, soumission ou modification de
sécurité. La seule saisie ne justifie pas un autre environnement payant et ne
compte pas comme conversation Activity connectée.

## Connexion externe manuelle réussie, réponse Activity non vérifiée

La capture Edge externe fournie à **01:07:15 UTC le 21 octobre** affichait
**Workshop Foundry Validation**, Azure AI Foundry Agent Service (Preview),
**Connected** dans le bon environnement. Le blocage d'authentification est levé
pour cette connexion seulement, sans déduire les détails du consentement.

Un nouveau compte/projet dédié sans clé a été préparé pour ce formulaire, puis
complété par un déploiement **GPT-4.1-mini 2025-04-14 Standard capacité 1** et
un agent activé **workshop-validation-specialist**, version **1**, avec Activity
et Responses. Aucun rôle ni source de recherche ajouté. Ces ressources sont
**actuellement actives et conservées pour diagnostic**. Le tag d'expiration
**04:58:55 UTC le 21 octobre** ne supprime rien automatiquement. Les preuves
de nettoyage antérieures concernent d'autres exécutions, non celle-ci.

L'agent connecté a été ajouté via la connexion existante au brouillon isolé,
puis rouvert pour vérifier la persistance. Action native :
`InvokeExternalAgentTaskAction`, `ActivityProtocolMetadata`, `SendActivityV2`,
avec le bon identifiant et les droits Invoker. Orchestration classique,
rubriques Search/télémétrie existantes et état non publié préservés.

La première question générique a produit l'abstention Search existante, non
un appel connecté. Une rubrique dédiée **Workshop Foundry connection check**
a ensuite été sauvegardée et rouverte avec zéro erreur/avertissement.
Son déclencheur exact, `workshop foundry connection check`, appelle l'action
connectée via `BeginDialog`, sans réponse de réussite codée en dur.

Un seul test correctif neuf à **01:41:26 UTC** a prouvé l'exécution de rubrique
et la liaison de cible via `DialogTracing` et `DynamicPlanStepBindUpdate`.
À **01:50:45 UTC**, aucune réponse ni erreur. C'est un échec d'observation
d'acceptation réelle, non un délai renvoyé par la plateforme ni une erreur
d'authentification établie. Envoi, exécution distante et retour restent non vérifiés.

Un diagnostic Responses direct distinct a réussi en **5,78 secondes**, avec
**I am the workshop validation specialist. Foundry connection verified.**
Coût mesuré : **75 jetons d'entrée + 13 de sortie = 88**, sans reprise.
Cela valide l'inférence pour l'identité CLI, non celle du connecteur ni le
transport Activity. Les métadonnées confirmaient déjà Activity/Responses actifs ;
aucune preuve ne justifie publication, rôle ou protocole supplémentaire.

La [preuve d'exécution connectée](../assets/runtime-2026-10-20/foundry-manual-connection-runtime.json)
préserve ces limites et l'échec initial. Le prochain diagnostic exige une
corrélation serveur connecteur/runtime pour la conversation
`46bdd592-bb45-40ae-adaf-e031960c70fa`, activité
`0da156dc-11ae-4f3a-98d8-2b81be3e3c2b`, à **01:41:26 UTC**.
La cause du blocage reste inconnue. L'atelier complet reste incomplet.

## Test synthétique Activity connecté instrumenté réussi

La corrélation serveur en lecture seule a trouvé un POST Projects accepté avec
**HTTP 202** à **01:41:30.591 UTC**, corrélation
`362a8914-f06a-4b9e-877a-ce407d2eeae5`. L'heure correspond au test bloqué,
sans identifiants natifs, chemin précis ni appelant effectif. Candidat temporel,
non preuve de cet envoi Activity ni de son résultat.

Le projet proposait Audit/Trace, sans paramètre de diagnostic. Un espace isolé
Pay-as-you-go, rétention 30 jours et plafond relu **0,023 Go/jour**, a été créé
dans le même groupe dédié ; seuls Audit/Trace du projet ont été activés.
Ce plafond n'est pas une limite de facturation stricte. Les diagnostics imposés
du compte n'ont pas été modifiés.

Une seule nouvelle conversation native instrumentée,
`84c7430d-3e15-4832-996e-1d36f82349fc`, a envoyé le déclencheur exact une fois
à **02:27:09.715 UTC**. Les traces prouvent encore la rubrique et la liaison
de cible. À **02:27:16.579 UTC**, le chat a reçu **I am the workshop validation
specialist. Foundry connection verified.**, avec visibilité confirmée.
Durée : **6,864 secondes**. La rubrique parente ne contient pas cette réponse
en dur. Le test synthétique Activity connecté réussit, non les citations/recherches.

Un événement navigateur `net::ERR_ABORTED` précédait la réponse ; il n'est donc
pas interprété comme un échec final. La requête Audit/Trace ciblée réussissait
mais renvoyait zéro ligne après observation bornée. L'ingestion et un lien causal
entre journalisation et reprise restent non vérifiés. L'ancien test sans réponse
reste conservé comme échec historique réel.

À **02:39:14 UTC**, le nettoyage du seul observateur a vérifié **404** pour
l'espace temporaire et le paramètre de diagnostic du projet. Les diagnostics
imposés du compte sont inchangés. Compte, projet, petit modèle, agent et connexion
fonctionnels restent **actifs et conservés** : pas de nettoyage complet.

Un précontrôle actuel de provenance a réussi **117 vérifications de preuve**,
sans trouver de correction distincte prise en charge pour les anciens échecs
d'annotations et d'association aux sources. Les documents intégrés n'ont pas
d'URL éditeur vérifiée : ces champs restent `null`. Une URL `citationUrl`
authentifiée n'est ni une URL éditeur ni une preuve de transmission native
par Activity. Aucun environnement de recherche, embedding ou nouveau test
connecté n'a été créé pour répéter cette stratégie en échec.

La [preuve de réussite Activity et de nettoyage observateur](../assets/runtime-2026-10-20/foundry-connected-activity-success.json)
distingue transport synthétique fonctionnel, critères multisources/citations
natives encore ouverts et conflit BYOM avec la politique sans clé.
L'atelier reste incomplet ; aucun agent d'origine ni politique modifié.

## Critères d'origine réconciliés et recherche réelle exercée

Le notebook et le guide d'installation accessibles du Lab 6 exigent des réponses
ancrées avec attribution visible, recherche par domaine et combinée, et scénarios
connectés direct/référence rapide/expertise/hybride. Ils n'exigent pas explicitement
de tableaux d'annotations natives, d'URL éditeur pour les données synthétiques
ni de citations verbatim. Ces anciens critères ajoutés par l'assistant restent
des preuves d'amélioration, non les critères d'origine. Le document principal
protégé est resté illisible, sans contournement ; ses éventuelles exigences
supplémentaires sont inconnues. L'exécution d'un vrai prompt Foundry personnalisé
au Lab 4 reste une exigence d'origine, non une amélioration facultative.

Dans ce périmètre corrigé, **workshop-retrieval-specialist** a été créé dans le
projet dédié actuel, en préservant l'agent synthétique fonctionnel. Search
**Basic, une unité**, un petit déploiement d'embeddings **GlobalStandard,
capacité 1**, trois index et un outil MCP de base de connaissances authentifié
ont été provisionnés. Les 24 enregistrements ont été joints exactement aux
originaux, huit par source. Rôles d'identité managée ciblés, ressources et versions
figurent dans le suivi de propriété/nettoyage. Authentification Cognitive sans
clé et gouvernance existante préservées.

Un second rattachement natif et une rubrique classique explicite ont été
sauvegardés puis rouverts. Quatre tentatives par domaine ont produit trois
messages natifs confirmés. Fraude, investigation et cas combiné ont atteint la
cible, sans réponse dans l'observation bornée. Livraison réglementaire non
confirmée, avec **Unable to connect** visible. Aucune réussite connectée ancrée.

Un diagnostic direct distinct a prouvé la recherche MCP des 24 originaux, puis
échoué en génération avec **rate_limit_exceeded** : limites réelles
**1 000 TPM / 1 RPM**. Erreur prouvée pour cet appel direct, non corrélée
définitivement aux blocages natifs. Après vérification du quota régional, seule
la capacité Standard est passée de **1 à 26**, relue indépendamment comme
**26 000 TPM / 26 RPM**. L'estimation prudente était de 25 529 jetons/minute pour
contexte, appels multiples et marge de sortie, non une consommation mesurée.
Aucun débit provisionné, changement de modèle/version, MCP, droits ou sécurité.

Trois régressions directes bornées ont chacune terminé sans reprise, avec
24 jointures exactes :

| Version recherche | Consommation réelle | Résultat |
|-------------------|---------------------|----------|
| 1, correction de capacité seule | 5 244 entrée + 564 sortie = 5 808 jetons | Limitation résolue ; cinq familles d'affirmations non étayées/trop larges |
| 2, règles de preuve et conditions | 5 643 entrée + 740 sortie = 6 383 jetons | Quatre familles d'erreurs de portée/attribution restantes |
| 3, adaptation extractive | 5 541 entrée + 999 sortie = 6 540 jetons | Neuf phrases sources complètes inchangées et conditions préservées ; contenu parfois non pertinent et limites d'applicabilité incomplètes |

La version 3 affichait les titres des documents d'origine, non les noms de
sources demandés. Cet écart est distinct de l'authenticité des extraits : aucun
identifiant ni URL inventé. La sortie extractive n'est pas certifiée comme
synthèse narrative complète. Les anciens échecs d'obligations, délais,
conservation et attribution restent conservés ; une génération terminée ou des
mots-clés de sources corrects ne suffisent pas à valider l'ancrage.

La [preuve de validation recherche](../assets/runtime-2026-10-20/foundry-original-lab-retrieval-validation.json)
consigne périmètre corrigé, capacité et échecs d'ancrage. Les reprises payantes
ont été arrêtées. Search, compte/projet, modèles de conversation/embeddings,
deux agents Foundry et connexions/rubriques natives restent **actifs et conservés**,
avec propriété et nettoyage suivis. Les tags ne suppriment rien. Couverture
connectée complète et vrai BYOM restent incomplets ; aucun agent d'origine ni
politique de sécurité modifié.

## Comparaison avec le modèle complet sans résolution de l'ancrage

Une comparaison portant uniquement sur le modèle a testé si les échecs de
synthèse provenaient du petit modèle. Le service a rejeté la première tentative
de remplacement avec HTTP 400 `invalid_payload` : le modèle demandé doit
correspondre à celui de l'agent référencé. Aucune réponse ni consommation
retournée. Le déploiement temporaire a été supprimé, avec absence vérifiée ;
l'agent existant n'a pas été modifié.

L'alternative prise en charge utilisait un agent temporaire distinct, copié de
la version de recherche 2, en ne changeant que son déploiement vers
**GPT-4.1 2025-04-14**. Instructions, température, outil MCP, données sources et
question combinée restaient identiques. Le quota Standard régional a été vérifié
avant création d'un déploiement à la consommation de capacité 26, sans débit
provisionné.

Un appel, sans reprise, a terminé en **24,539 secondes**, avec
**5 627 entrée + 730 sortie = 6 357 jetons**. Le résultat MCP persisté joint les
24 originaux. Les identifiants et domaines sources affichés existaient et
correspondaient aux vrais résultats, sans prouver l'ancrage de chaque affirmation.
La comparaison manuelle avec ces passages a relevé trois familles bloquantes :

* Diligence et approbations limitées aux clients/relations étendues aux transactions.
* Délai de déclaration des transactions bloquées étendu aux correspondances confirmées.
* Obligation de déclaration privée de seuils et conditions temporelles déterminants.

Les réserves générales ne corrigeaient pas les obligations affirmées trop
largement. Le grand modèle seul n'a pas résolu ces erreurs ; la configuration
n'a donc **pas été promue** vers l'agent connecté. Aucun nouvel essai payant
identique de synthèse n'a suivi.

Agent et déploiement temporaires ont été supprimés, avec contrôles indépendants
GET après suppression à 404, vérifiés le **2026-10-21 à 13:12:41 UTC**.
Version de recherche 3, agent de vérification fonctionnel, rubriques/rattachements
natifs et connexion formelle restent inchangés. Search/projet/modèles antérieurs
restent actifs ; ce nettoyage ne les a pas supprimés. Le vrai BYOM nécessite
toujours un environnement compatible approuvé par la gouvernance ; aucun
changement de politique, rôle ou consentement. La
[preuve de comparaison](../assets/runtime-2026-10-20/foundry-model-comparison.json)
conserve cet échec sans publier de passages privés.

## Provenance réparée et questions backend originales réussies

Le **2026-10-21**, les quatre questions inchangées du notebook original ont été
exécutées avec l'agent de recherche version 3. Avant correction, les extraits
étaient authentiques, mais seulement **2/4** réponses avaient l'attribution
canonique attendue. Les autres employaient de vrais titres documentaires ; une
réponse omettait certaines étiquettes. Ce n'étaient pas des documents inventés.

La réparation ajoute la métadonnée récupérable, non recherchable `source_name`
aux trois index possédés et aux **24** enregistrements. Des comparaisons
indépendantes confirment la conservation des `id`, `title`, `content`, de la
configuration sémantique et des champs vectoriels. Aucun vecteur n'a été
resoumis, aucun appel d'embedding ou de modèle effectué pendant cette mise à jour.
Version, instructions, modèle, outils et authentification de l'agent restent
inchangés. Projection demandée : `id/content/source_name`. MCP renvoie aussi le
titre sémantique original ; les titres n'ont été ni retirés du contexte ni remplacés.

Après correction, **4/4** questions passent le contrôle du contenu extractif
pertinent, des conditions déterminantes et de l'attribution canonique par
affirmation. Jointures réelles : **19 / 14 / 18 / 24**, sans imposer artificiellement
24 résultats à chaque question. Quatre requêtes, zéro relance, **21 341 jetons
Responses**, contre 19 242 avant correction. Ce n'est ni la facture totale de
l'atelier ni une mesure des Copilot Credits natifs. Le garde local rejetait
initialement le titre supplémentaire renvoyé par le fournisseur ; la réponse
déjà terminée a été récupérée sans nouvelle inférence. Six tests hors ligne
des projections passent. Une première réponse HTTP 204 valide a été reprise
avec contrôles de propriété, instantané et ETag. Les sauvegardes des projections
restent privées ; retirer le champ ajouté nécessiterait de reconstruire l'index,
ce qui n'a pas été tenté.

### Réussite native réelle et lot de catégories interrompu

Une question native distincte sur la conservation des preuves a reçu une vraie
réponse connectée en **352,940 secondes**, selon les horodatages serveur.
Paragraphe original complet, attribution, pertinence, durée de conservation et
conditions de gel juridique sont préservés. BeginDialog et liaison cible natifs
ont été capturés. L'identifiant de réponse MCP et la trace d'outil sous-jacents
ne sont pas exposés ; aucun substitut SDK n'a comblé cette absence. Aucun SLA
original de 90 secondes n'est établi.

L'ancienne conversation combinée a ensuite affiché `rate_limit_exceeded`, avec
le même identifiant que la capture initiale. La cause de cet échec est donc
établie, pas celle de tous les blocages antérieurs. Une salutation native réussit
aussi en **0,204489 seconde**, avec Greeting SendActivity/CancelAllDialogs et
sans liaison Foundry.

Le lot navigateur suivant prévoyait quatre catégories, préfixes de routage
classique explicites, sessions neuves, aucune relance et observation limitée à
450 secondes. Après reprise, son identifiant d'exécution différée n'était plus
disponible. La récupération en lecture seule montre la deuxième question
réglementaire comme activité utilisateur optimiste seulement, sans réception
serveur, trace de routage ni réponse métier confirmées. Aucun résultat de cas
terminé n'a été récupéré durablement. Atteindre le deuxième cas ne prouve pas
la réussite du premier ; aucune requête payante n'a été dupliquée.

La [preuve expurgée de récupération](../assets/runtime-2026-10-20/foundry-source-provenance-recovery.json)
distingue ces résultats. Adaptation backend extractive et réussite native ciblée
ne certifient ni synthèse narrative libre, ni routage naturel, ni matrice complète
connectée/locale/hybride. Les anciens échecs de synthèse et du grand modèle
restent des résultats historiques valides.

Le guide rapide original porte un en-tête OLE, pas un conteneur ZIP DOCX standard.
Cela ne prouve pas à lui seul un chiffrement. L'outil natif a accepté le fichier
original non transformé de **163 840 octets**. L'ingestion est passée de
**In progress** à **Error** ; le détail indique : « The file's content is either
confidential or empty. » C'est un échec réel d'ingestion, sans preuve de sa cause
exacte de protection/format. Un téléversement, zéro nouvel essai ; aucun
déchiffrement, retrait d'étiquette ni reconstruction. La source en erreur reste
dans le brouillon isolé non publié pour inspection ou remplacement autorisé.
À ce stade, une source lisible approuvée pour cet environnement était encore
nécessaire. La récupération éditeur ci-dessous lève ce prérequis sans réparer
ni convertir le DOCX.

Le vrai BYOM natif
nécessite encore un environnement et une authentification compatibles approuvés.
Le scope délégué PAC reste un problème distinct. Connexion et ressources
possédées restent actives ; les tags d'expiration ne les suppriment pas.
Aucun changement de politique, rôle ou consentement.

## Catégories natives récupérées et référence locale sous licence prête

Une exécution navigateur distincte a ensuite rétabli la livraison native réelle,
sans action dans un navigateur externe. La version 3 a répondu aux quatre
questions originales du notebook avec préfixes classiques explicites. Les
seize extraits étaient authentiques, mais deux puces de la réponse fraude
n'avaient pas leur propre attribution : **3/4** réussites du contenu affiché
et de l'attribution, non quatre. Les résultats perdus de l'ancien lot interrompu
ne sont pas reconstitués.

Une clarification ciblée des seules instructions crée la version 4 : répéter
le bon marqueur canonique pour chaque puce. Modèle, outils, température, point
de terminaison, authentification, agent de test et versions antérieures sont
conservés. Aucun appel de modèle pendant la mise à jour. La régression native
réelle réussit **4/4** questions, avec **13 extraits authentiques attribués
individuellement**, après revue de pertinence et des conditions déterminantes :

| Catégorie | Latence des activités serveur | Extraits authentiques attribués |
|-----------|-------------------------------|---------------------------------|
| Fraude | 15,718720 s | 1 |
| Réglementation | 16,774088 s | 3 |
| Enquête | 16,187563 s | 1 |
| Cas combiné | 26,940827 s | 8 |

Il y a eu **cinq soumissions métier**, pas quatre réussites au premier essai.
La première soumission combinée reste optimiste, sans horodatage serveur,
jusqu'à 17:11:09 UTC. Sa capture est conservée ; l'absence d'accusé serveur
ne prouve pas que le backend ne l'a jamais reçue. Une relance bornée, dans une
session neuve après un Hello acquitté par le serveur, reçoit la réponse combinée.
Chaque cas réussi possède identifiants utilisateur/réponse natifs, BeginDialog
et liaison cible. Les identifiants MCP/d'outil natifs sous-jacents ne sont pas
exposés. Comparer un extrait au corpus original n'est pas une jointure
indépendante aux résultats de recherche de cet appel natif. Aucun substitut SDK.

### Guide éditeur réellement ingéré

Le [dépôt officiel Microsoft](https://github.com/Azure/Copilot-Studio-and-Azure)
fournit le guide Markdown absent sous licence MIT. Sources et licence publiques
sont accessibles malgré l'erreur SAML distincte du jeton CLI authentifié.
Aucun changement SSO, de consentement ou de politique organisationnelle.
La révision `e9ecd00dba2c25dbc8306b5be6818d22645607a3` est figée. Une analyse
statique du notebook éditeur, sans exécuter son code, confirme les `id/title/content` exacts
des **24** originaux et les **quatre objets complets de questions de test**.
Le hash du notebook original a aussi été contrôlé.

La copie sous licence préserve le corps du guide, déplace son titre dans les
métadonnées initiales et ajoute provenance éditeur et avis MIT complet.
Trois tests hors ligne de vérification passent. Un téléversement natif normal,
zéro nouvel envoi, atteint **Ready**, observé à **17:31:26 UTC**. C'est une
adaptation de source amont, pas un DOCX déchiffré ou reconstruit ; aucune
équivalence au fichier illisible n'est affirmée. La source DOCX en erreur reste
disponible pour inspection.

### Test ciblé du langage naturel et des connaissances locales

Le parent isolé non publié emploie désormais l'orchestration générative et des
instructions enregistrées de routage/ancrage. Recherche web, réponses non ancrées
et raisonnement approfondi restent désactivés. Une vraie réponse native d'accueil
demande activité, tendances, montants et dates sans appeler Foundry, mais cherche
aussi les connaissances locales. Le chemin d'accueil pur sans connaissance
n'est donc pas démontré.

Une question CTR naturelle reçoit ensuite le bon seuil en espèces et
l'agrégation quotidienne en **7,247947 secondes**. La trace native de recherche
contient l'identifiant exact de la source téléversée ; la citation finale native
identifie son nom de fichier. Aucun appel Foundry n'est observé pour ces deux
questions ciblées. C'est une recherche locale réelle, pas une réponse inscrite
dans les instructions du parent. Les onze scénarios étendus et la couverture
hybride ne sont pas remplacés ni certifiés par ces deux tests.

La [preuve expurgée de récupération native](../assets/runtime-2026-10-20/foundry-native-category-recovery.json)
distingue échec d'attribution, soumission non acquittée, régression réussie et
provenance de la source sous licence. Échecs antérieurs, limites des traces
natives, blocage BYOM original et coûts des ressources actives restent visibles.
L'atelier complet n'est pas certifié terminé.

## Scénarios étendus et correction ciblée de l'accueil

Les **onze questions étendues** correspondent au document d'installation original
accessible après normalisation des espaces. Une tentative QA native distincte
emploie ces questions, pas les tests ciblés abrégés. Elle s'arrête après **trois
soumissions, zéro relance**, avec les résultats conservés suivants :

| Scénario original | Résultat réel |
|-------------------|---------------|
| 1 : Accueil vague de compte suspect | Refus au lieu de clarification ; recherche locale inutile |
| 2 : Seuil de déclaration CTR | Vraie recherche locale et citation, mais délai et formulaire attendus absents |
| 3 : Délai SAR | Aucun accusé serveur dans la fenêtre d'observation de 120 secondes |
| 4–11 | Non soumis après l'arrêt de livraison |

La [preuve QA étendue](../assets/runtime-2026-10-20/foundry-native-natural-matrix.json)
conserve deux réponses finales acquittées, le respect des quotas et l'échec
d'acceptation. Le cas SAR prouve une livraison non confirmée, pas une absence
backend ni un échec d'authentification Foundry. L'égalité des questions du support
accessible ne révèle pas d'autres exigences du document principal illisible.

La première correction enregistre le nom du composant d'accueil et tente une
définition gardée non factuelle, avec seulement clarification et annulation des
dialogues. Elle étend les instructions du parent pour demander les champs
complets des tableaux récupérés. Trois tests hors ligne du garde prévu couvrent
l'accueil vague et excluent les
questions financières précises. Aucune réponse financière n'est inscrite dans
la rubrique ou les instructions ; modèle, outils et corpus Foundry inchangés.

Une régression d'implémentation ultérieure emploie les scénarios originaux 1–3,
une fois chacun dans une même conversation native. Tous reçoivent une vraie
réponse finale acquittée :

| Scénario | Latence | Comportement vérifié |
|----------|---------|----------------------|
| Accueil | 5,390803 s | Demande activité, tendances, montants et dates ; aucun événement de recherche locale ni marqueur de routage Foundry |
| CTR | 10,748131 s | Seuil, agrégation, délai, formulaire et exemptions conditionnelles ; vraie trace et citation de source locale |
| SAR | 8,945610 s | Délais normal/sans suspect, conservation, confidentialité et formulaire ; vraie trace et citation locale |

Le texte de clarification diffère du message exact de la rubrique enregistrée.
Le comportement sans source est observé, mais l'exécution de cette rubrique
précise n'est pas établie. La
[preuve ciblée de correction](../assets/runtime-2026-10-20/foundry-native-intake-rework.json)
conserve cette distinction. Aucun résultat navigateur externe n'a été obtenu,
l'opérateur étant indisponible ; la réponse SAR intégrée ultérieure a réellement
été reçue. Ces trois contrôles d'implémentation ne certifient ni les onze
scénarios naturels/locaux/connectés/hybrides ni le lab BYOM original.

### Retest en nouvelle session arrêté avant notation

La tentative d'acceptation R2 indépendante ouvre ensuite une nouvelle session et
emploie un seul Hello comme prétest de transport. Il reste optimiste côté client,
sans accusé serveur ni réponse finale pendant **120,161 secondes**. L'arrêt
obligatoire intervient donc **avant toute question notée**. Le message d'accueil
initial ne vaut pas accusé de réception de ce prétest.

La [preuve QA R2](../assets/runtime-2026-10-20/foundry-native-natural-matrix-rework.json)
conserve **un prétest, zéro soumission cible, zéro relance cible et onze scénarios
non évalués**. Les champs de routage/citation nuls signifient non évalués, pas
absents. Les trois succès d'implémentation précédents restent réels mais ne sont
pas des réussites R2. Cette interruption n'établit ni régression ni absence
backend. Aucune configuration ni nouvelle relance cible payante n'a lieu
pendant R2.

Un contrôle navigateur externe a de nouveau été demandé, mais l'opérateur était
indisponible ; aucun résultat externe n'existe. Cette demande de transport est
dépassée par la vraie récupération interne ci-dessous, pas par un succès externe
supposé.

### Persistance de l'accueil et livraison native récupérées

Une lecture native ultérieure révèle une définition `OnRecognizedIntent` vide.
L'enregistrement du nom du composant ne prouvait pas la persistance du YAML
gardé ; cette affirmation est retirée de la preuve historique. La saisie clavier
multiligne avait accumulé l'indentation et produit des erreurs explicites.

Une saisie clavier normale ligne par ligne répare la définition. Après
enregistrement, sortie et réouverture, l'éditeur natif renvoie les 21 lignes
`OnActivity` prévues, zéro erreur et un bouton Save désactivé. La rubrique est
activée. Ses seules actions envoient une clarification non factuelle et annulent
les dialogues suivants ; cinq tests hors ligne du garde et de la lecture
préservent cette limite. La [preuve de récupération de persistance](../assets/runtime-2026-10-20/foundry-native-persistence-recovery.json)
distingue le retrait historique et la vraie réparation.

Un Hello immédiatement après enregistrement reste sans réponse. Un flux UI
distinct récupère ensuite la livraison : attendre un nouvel accueil serveur et
la frappe initiale finale, patienter dix secondes, saisir le texte, patienter
500 millisecondes puis activer le bouton Send normal avec Entrée. Le vrai Hello
et l'accueil original exact reçoivent le message enregistré et ses traces
natives de rubrique/actions. L'exécution de cette rubrique précise est désormais
prouvée pour ces tours ultérieurs, pas rétroactivement pour la première
régression. Ni le délai ni le bouton Send seul n'est établi comme cause.

### Les captures étendues exigent la fin du parent

R3 soumet une fois chacune des onze questions originales, avec un vrai Hello
par conversation. Toutes reçoivent une réponse native. Six captures initiales
s'arrêtent cependant au marqueur final d'un message enfant, sans prouver la fin
du parent. Elles sont conservées, non certifiées comme résultats d'acceptation
complets. Les captures suivantes exigent `DynamicPlanFinished` ; l'accueil
non factuel direct est prouvé par sa trace de rubrique/actions.

Les tours hybrides complets 8 et 9 incluent les preuves locales et connectées.
Le cas 10 contient une référence locale dans une étape de recherche terminée et
une étape Foundry terminée, mais le message final n'intègre pas les champs du
tableau local. Il ne prouve pas une absence de recherche locale. Le cas 11 se
termine avec Foundry seul. La clarification place les cas hybrides avant les
questions autonomes et rapides, inclut explicitement les récits SAR pour des
fraudes nommées, et distingue exigences SAR et simple délai. Ses 3 005 caractères
sont relus après rechargement complet. Aucune réponse financière, configuration
Foundry, politique d'authentification ou permission n'est modifiée.

### Tours natifs complets récupérés, acceptation encore incomplète

Le [registre des tours complets](../assets/runtime-2026-10-20/foundry-native-matrix-completion-recovery.json)
conserve désormais les identifiants serveur utilisateur/réponse pour les
**onze questions originales**. Ce sont des tours complets sélectionnés entre
exécutions nommées, pas une nouvelle exécution unique des onze cas. Toutes les
combinaisons de gestionnaires attendues sont observées :

| Scénarios originaux | Gestionnaire observé | Limite de couverture |
|---------------------|----------------------|----------------------|
| 1 | Accueil non factuel enregistré, sans recherche ni Foundry | Trace exacte de rubrique/actions |
| 2–4 | Connaissance locale, sans Foundry | Citations du fichier chargé et étapes de recherche terminées |
| 5–7 | Foundry connecté | Étapes natives déclenchées et terminées |
| 8–11 | Connaissance locale et Foundry | Deux vrais routages et preuves locales/connectées affichées |

Le contenu des exemples 1–7 est observé ; les exemples détaillés 8–11 restent
partiels ou non confirmés. Ne pas imposer de références légales non étayées,
d'obligations SAR automatiques, de priorités ou de restrictions de compte pour
imiter un exemple. Le document principal Lab 6 illisible peut contenir d'autres
critères. Les jointures indépendantes d'appartenance/version MCP restent absentes.

L'audit examine **tous les messages enfant et parent affichés**, pas seulement
le dernier, parfois réduit à une note de source. Sur 67 blocs entièrement entre
guillemets, **quatre sont reformulés ou raccourcis, non des originaux verbatim** ;
**20 n'ont pas de marqueur canonique individuel correct**. Une attribution groupée
n'est pas une attribution par bloc. Citations intégrées et paraphrases exigent
encore une revue sémantique. Le succès antérieur des quatre catégories est
conservé, sans certifier ces réponses étendues.

Le comptage reste explicite : R3 soumet 11 cibles ; le lot R4 de huit cas atteint
son dernier cas, mais son résultat différé expire avant récupération. Ce nombre
découle du flux séquentiel enregistré ; seules les métadonnées individuelles du
cas 7 sont récupérées dans la session native encore active, sans relance. Les
sept autres réponses ne sont pas reconstituées. R5 conserve ensuite dix cibles
capturées individuellement.

Une correction ciblée de complétude des incidents exécute ensuite deux cibles,
puis s'arrête avant la troisième prévue. Son cas 8 réduit à tort plusieurs
dépôts quotidiens à un par jour et invente un total agrégé exact. La variante de
3 340 caractères est rejetée. Une lecture après rechargement complet confirme
le retour à la configuration de **3 005 caractères** ; un seul contrôle exact
du cas 8 après retour reçoit les deux sources sans inventer nombre de dépôts ni
total. Cela n'établit ni causalité unique de l'instruction ni comportement futur
garanti du modèle.

Ces exécutions comptent **32 soumissions cibles**, dont les huit déduites du flux
R4, et **21 cibles réexécutées après R3**. Aucune cible n'est relancée dans une même
exécution. Les cibles ne comptent ni invocations modèle ni facturation ; QA
initiale et contrôles ciblés historiques sont exclus. Échecs originaux, captures
expirées et variante rejetée restent enregistrés.

Livraison et routage sont récupérés, **pas l'acceptation de la matrice complète**.
Il reste la couverture complète étayée et la fiabilité des citations/attributions.
Le prompt BYOM original exige toujours un environnement approuvé compatible
avec l'authentification ; les documents protégés exigent une source lisible
autorisée. Aucune politique, permission ou consentement n'est modifié.
Le brouillon reste non publié et les ressources Azure existantes facturables.

## Extension de vérification déterministe des sources

L'[implémentation isolée](https://github.com/devopsabcs-engineering/copilot-studio/tree/main/examples/verified-retrieval/workshop-verified-retrieval)
vérifie la recherche réelle contre le notebook public MIT épinglé. Le modèle ne
sélectionne que des identifiants récupérés ; le code affiche les enregistrements
entiers et leurs marqueurs individuels, sans transmettre de citations rédigées
par le modèle. Les **30 tests initiaux de l'extension**, contrôles de syntaxe et de
compatibilité des dépendances ont réussi. Quatre cas backend réels affichent
**12 passages exacts et attribués**. La pertinence de la sélection et la
complétude des incidents ne sont pas certifiées pour autant.

Le [résultat de l'extension](../assets/runtime-2026-10-20/foundry-verified-extension.json)
distingue preuve backend et échec natif. La version hébergée 1 est active.
Un diagnostic explicite, après un véritable précontrôle d'accueil, atteint sa
nouvelle action d'agent connecté, mais reçoit **HTTP 403** :
`BotServiceRbac authorization requires a valid Entra tenant id for the activity caller.`
Aucune session hébergée n'est observée. Un contrôle séparé avec le cas original 6
inchangé appelle toujours le spécialiste existant et affiche deux réponses
sourcées. Aucune fin de plan n'est capturée ; ce contrôle n'est donc pas un
nouveau succès de tour complet. Ces deux cibles sont distinctes des totaux
historiques R3–R7.

Un test Entra uniquement sur le point isolé, conservant Azure RBAC, est proposé.
La demande d'approbation ne reçoit aucune réponse humaine ; **aucun changement
d'authentification du point ni ajout manuel de rôle ou de consentement n'est
effectué pendant le diagnostic**.
Le commutateur du diagnostic affiche Disabled et une sauvegarde est tentée,
mais la lecture indépendante suivante échoue lorsque le navigateur devient
indisponible. Une lecture authentifiée ultérieure récupère cette vérification,
comme détaillé ci-dessous. Les instructions du parent original et la définition
version 4 ne sont pas modifiées.

Cette continuation crée une étape de recherche isolée, un agent hébergé et une
nouvelle ressource Azure Bot. Les identités générées par le service sont
consignées en privé pour nettoyage. Ces ressources restent actives et
facturables. Les ajouts locaux ultérieurs du script, du chargement dotenv et
du fichier de licence n'ont pas été redéployés. Ni l'extension native ni
l'atelier complet ne sont certifiés terminés ; compatibilité BYOM originale
et accès autorisé aux originaux protégés restent non résolus.

### État sauvegardé récupéré et correction du SDK Activity

Une inspection Dataverse authentifiée en lecture seule vérifie maintenant le
rattachement du diagnostic au parent attendu et son état sauvegardé
`statecode=1`, `statuscode=2`. Les métadonnées réelles nomment cet état
**Inactive** ; une nouvelle capture de l'interface montre aussi Disabled avec
Save désactivé. Une confirmation dans un navigateur externe n'est donc plus
nécessaire uniquement pour établir que ce diagnostic reste désactivé.

Une requête Activity directe authentifiée atteint l'hébergement et crée une
session, mais reçoit **HTTP 500** avant le gestionnaire de messages applicatif.
Les journaux identifient
`ClaimsIdentity.__init__() got an unexpected keyword argument 'is_authenticated'`.
Cette requête directe n'est pas un tour natif Copilot Studio. Elle utilise le
locataire et l'appelant réels du jeton Entra obtenu ; authentification du point,
rôles manuels et consentement restent inchangés.

Le pont Activity déployé `1.0.0b1` utilise un argument de constructeur supprimé.
La correction locale épingle Activity `1.0.0b4` et Microsoft Agents `1.9.0`.
Le test de régression reproduit d'abord l'erreur à la frontière réelle du SDK,
puis réussit après correction. Les **33 tests de l'extension**, contrôles de
syntaxe Python et `pip check` réussissent. Deux tests ASGI exercent le vrai
point d'entrée et l'adaptateur SDK : ils conservent exactement les preuves
affichées et signalent explicitement un rejet. Le chargement du corpus et la
génération Azure sont simulés dans ces tests locaux de transport. Ils établissent
aussi que l'enveloppe Activity exige `serviceUrl`.

Aucune version cloud corrigée n'est déployée ni retestée. La réussite locale ne
résout pas le 403 natif antérieur et ne certifie ni les permissions hébergées en
aval ni l'atelier complet. Approbations de publication et acceptation réelle
hébergée/native restent en attente.

## Références officielles

* [Installation PAC](https://learn.microsoft.com/en-us/power-platform/developer/howto/install-cli-net-tool)
* [Authentification PAC](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)
* [Commandes PAC Copilot](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot)
* [Commandes d'évaluation PAC Copilot Studio](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot-studio)
* [Référence des permissions API Power Platform](https://learn.microsoft.com/en-us/power-platform/admin/programmability-permission-reference)
* [Extension Microsoft Power Platform VS Code](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.powerplatform-vscode)
