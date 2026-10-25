---
title: Feuille de route pour terminer l'atelier
description: Travaux restants, priorités, dépendances, responsables et critères mesurables de clôture de l'atelier.
ms.date: 2026-10-25
---

## Objectif et périmètre

[Accueil du dépôt](../../README.md) | [English](../en/completion-roadmap.md) |
[Registre de validation](validation.md) | [Dernier rapport d'exécution](backend-live-2026-10-20.md)

Le livrable de planification est terminé. L'exécution complète de l'atelier ne
l'est **pas**. Les tâches non cochées représentent des travaux à effectuer,
et non des résultats déjà observés ou promis.

La référence de planification est le commit `94ebcd3` et les preuves conservées.
Le 22 octobre, 47 tests documentaires, 33 tests
de l'extension, les vérifications de dépendances et de syntaxe Python ont réussi.
Ces résultats ne certifient pas l'acceptation en environnement réel.
La poursuite du 23 octobre ci-dessous ajoute un inventaire actuel en lecture
seule, sans déploiement ni nouvelle réussite d'acceptation réelle.

## Correction du candidat authentifié du 25 octobre

La connexion administrateur assistée par l'utilisateur réussit désormais. Le
[reçu de récupération du candidat](../assets/runtime-2026-10-25/candidate-authoring-recovery.json)
conserve la vérification indépendante de l'identité/environnement PAC, le clone
officiel et les envois ciblés du brouillon. Cela remplace les anciens blocages
d'authentification/clonage ci-dessous, pas l'échec de dépendances du plugin.
Aucune stratégie n'est contournée.

Le [premier test natif des recherches strictes](../assets/runtime-2026-10-25/strict-lookups-native.json)
échoue : l'orchestration choisit Search sources au lieu de la rubrique prévue.
Une lecture indépendante trouve aussi des identités CTR/SAR distinctes avec
deux dialogues CTR identiques. La cause de la copie intermédiaire reste inconnue;
les preuves ne permettent pas de l'attribuer à PAC. Cet échec reste inchangé.

Author corrige les deux rubriques avec des conditions de message étroitement
ancrées, des réponses littérales et une fin explicite de conversation. Huit tests
locaux et 31 contrôles de schéma réussissent. Les trois fichiers modifiés
correspondent au clone distant indépendant. Le
[test natif corrigé](../assets/runtime-2026-10-25/corrected-lookups-native.json)
réussit les cas CTR, délai SAR restreint et accueil sans source, une fois chacun.
Les 12 valeurs locales, attributions individuelles, conditions et avertissements
d'instantané correspondent. Ces instantanés ne sont ni une recherche réelle ni
une réparation de navigation native des citations; les traces de rubrique et
`DynamicPlanFinished` ne sont pas exposées.

La [régression SAR générale](../assets/runtime-2026-10-25/broad-sar-regression.json)
préserve le routage spécialiste mais échoue en fidélité et couverture.
Une correction des seules instructions parent réussit 33 contrôles locaux
et sept contrôles de schéma, puis est envoyée et relue exactement. Son
[test natif corrigé distinct](../assets/runtime-2026-10-25/broad-sar-corrected-native.json)
réussit routage et couverture sur deux messages visibles, mais seulement
**15/16 citations sont exactes**. Une limitation provisoire contredit aussi
l'exception d'abus interne récupérée ensuite localement. Une synthèse finale
correcte n'efface pas les erreurs déjà affichées. Le schéma installé de l'action
Activity externe ne fournit aucun paramètre pris en charge pour supprimer ou
capturer ces messages. Aucun YAML non pris en charge ni changement du
récupérateur protégé n'est appliqué. Un contrat documenté de preuves sans émission
reste un prérequis d'intégration, pas un substitut implémenté ou accepté.

Les [régressions du brouillon final](../assets/runtime-2026-10-25/final-lookup-regressions.json)
réussissent encore CTR, SAR restreint et accueil **3/3**, avec une seule réponse
finale chacun, sans paraphrase supplémentaire ni reprise. La
[préservation indépendante](../assets/runtime-2026-10-25/lookup-preservation.json)
vérifie le parent d'origine et ses 26 lignes complètes de composants inchangés.
Le candidat a exactement 28 composants : deux rubriques possédées et une
modification limitée aux instructions existantes. Diagnostic Off, deux
spécialistes On, date de publication, authentification/accès/déclencheur 2/2/1,
quatre empreintes de fichiers et deux liaisons approuvées sont préservés.
Aucune publication n'a lieu.

T007/T008 restent ouverts pour la fidélité de toute la sortie et la matrice
de onze cas. Autorisation du diagnostic hébergé natif, navigation réelle du Lab 1,
provenance de sa réponse historique, restauration du Lab 2, autres critères
connectés, propriété/budget de rétention et accords attribuables restent distincts.

## Livraison Invocations vérifiée du 25 octobre

Ce point antérieur conserve ses limites historiques de navigateur et
d'authentification; la poursuite ci-dessus les remplace pour le candidat.

La [livraison de transport vérifiée](../assets/runtime-2026-10-24/verified-invocations-delivery.json)
ajoute Invocations sans état au serveur Activity déterministe existant. La
version 4 réussit d'abord la question SAR inchangée localement et à distance.
La version 5 rejette explicitement les limites du parseur JSON; les 54 tests
du service et les contrôles de dépendances réussissent. Le CLI de déploiement
expire après l'enregistrement du service, mais des lectures indépendantes
trouvent la version 5 active; doctor retourne 11 réussites, zéro échec et deux
contrôles ignorés. Aucun déploiement n'est répété après cette expiration.

Les réponses SAR locales et hébergées finales correspondent exactement au rendu
de deux documents. Sept contrôles hébergés réussissent : HTTP 401 sans jeton,
OpenAPI authentifié, HTTP 400 pour entrée vide et limite d'entier JSON, HTTP 413
pour corps trop grand, abstention astronomique et compatibilité Activity.
Les journaux corrélés excluent les appels de modèle pour les trois entrées
authentifiées invalides. Le premier appel Activity direct omet la version API
désormais requise et retourne HTTP 400; un appel corrigé distinct, protégé contre
la répétition, retourne HTTP 200 avec rendu exact des sources. Aucune identité
native ni sémantique de charge utile n'est modifiée.

Les deux protocoles, Entra plus BotServiceRbac, l'identité hébergée, le récupérateur
d'origine en version 4 et les quatre ressources/rôles d'origine sont vérifiés.
Le [contrôle de préservation native](../assets/runtime-2026-10-24/native-preservation-after-invocations.json)
préserve aussi les deux parents, définitions, empreintes des fichiers, liaisons
approuvées, autorisations déléguées, cache possédé et profil PAC. Aucune stratégie
Storage ni configuration réseau n'est modifiée. Réponses brutes et secrets
restent privés.

T005 et l'acceptation native/matrice complète restent ouverts. La page partagée
existante reste masquée; activation normale et clics du menu de compte ne rendent
pas l'interface utilisable. Aucune nouvelle question native ni écriture de
configuration. Le jeu d'évaluation généré supplémentaire est différé pendant
l'indisponibilité de l'utilisateur, sans choix ni accord inventé. Responsable de
rétention, date de revue, budget chiffré et validations organisationnelles
attribuables restent manquants.

### Poursuite native après publication

La livraison vérifiée est poussée sur `main` au commit `1f41cd6`. La
[nouvelle investigation de protocole](../assets/runtime-2026-10-25/native-protocol-followup.json)
rétablit la visibilité normale du navigateur et vérifie indépendamment
l'administrateur attendu du site. Le catalogue montre toujours dix opérations
anciennes, sans Invocations/Responses hébergés. L'aperçu application n'expose
aucun contrat de paramètres avant configuration; il est annulé et Tools reste
vide. Ni absence côté backend ni cause de migration n'est prouvée.

Un [contrôle de citation locale native](../assets/runtime-2026-10-25/native-lab1-navigation.json)
utilise le cas CTR 2 inchangé sur le candidat fraude isolé. Réponse parent finale
visible et dialogue de source cliquable sont observés, mais le passage affiché
ne justifie pas le seuil. Il s'agit d'un défaut d'ancrage du candidat,
**pas du test d'acceptation du PDF de licences du Lab 1**. Aucun événement runtime
de fin de plan, audit de réponse historique complète ou corps d'erreur de
connecteur n'est établi. Aucune configuration n'est modifiée.

La préparation d'édition limitée au candidat est bloquée avant clonage :
Manage signale son skill requis `copilot-studio:manage-agent` indisponible.
Aucun YAML n'est inventé, aucune configuration distante modifiée ni parent
d'origine touché. T005/T007 et T009 restent ouverts; contrat du connecteur et
outillage de gestion pris en charge doivent être rétablis avant correction.

### Récupération prise en charge et contrôles des labs réels

La [récupération de gestion](../assets/runtime-2026-10-25/management-recovery.json)
retrouve les instructions installées et exécute le bundle de clonage inchangé.
Il échoue avec `MODULE_NOT_FOUND` pour `@azure/msal-node-extensions`.
PAC permet le clonage, mais son identité actuelle appartient à un autre tenant;
ni authentification ni scripts installés ne sont modifiés. L'extension expose
une commande de clonage, sans outil appelable ici. Le choix humain demandé
reste indisponible; cela n'autorise pas le contournement de la limite documentée
pour les erreurs du script.

Le [contrôle du véritable Lab 1](../assets/runtime-2026-10-25/licensing-pdf-navigation.json)
vérifie le conseiller existant et le PDF Ready. Une question inchangée recherche
le guide attendu; deux passages correspondent aux pages physiques 6–7. Le clic
sur la source PDF n'expose ni lecteur, ni détails, ni ancre observable :
l'acceptation de navigation échoue. Ce résultat ne réutilise pas le contrôle
fraude et ne certifie pas l'ancienne réponse complète.

Le [contrôle d'inventaire du véritable Lab 2](../assets/runtime-2026-10-25/lab2-source-navigation.json)
ne trouve aucun agent permis configuré et identifié sans ambiguïté; les preuves
conservées enregistrent la suppression antérieure de la source/connexion Search.
Aucun agent de substitution, question nouvelle ou clic de citation. T010 reste
bloqué, pas réussi. T009/T010 et l'édition du candidat nécessitent le rétablissement
des prérequis pris en charge; aucune source, identité, autorisation ni réussite
n'est inventée.

La récupération des dépendances retrouve ensuite le setup SessionStart et le
manifeste officiel des dépendances natives du plugin. Le répertoire de données
contient le manifeste, mais aucun des trois paquets requis. L'installation
normale et l'alternative du cache hors ligne échouent avec `EALLOWREMOTE` :
le téléchargement des paquets de type distant est désactivé. Aucun registre,
source de paquet ni stratégie n'est contourné. Ce blocage d'installation
n'autorise ni modification du bundle ni réutilisation du mauvais tenant.

L'[audit historique local du Lab 1](../assets/runtime-2026-10-25/lab1-full-answer-audit.json)
vérifie empreinte, édition et pagination du PDF approuvé conservé, mais ne retrouve
pas la réponse complète du 19 octobre avec provenance correspondante. Ni captures
partielles ni réponses plus récentes ne la remplacent. Les totaux de faits restent
inconnus; le critère historique reste indisponible, pas réussi.

La [nouvelle récupération d'authentification prise en charge](../assets/runtime-2026-10-25/supported-auth-recovery.json)
confirme indépendamment la présence du commit sur GitHub. La mise à jour
officielle du plugin réussit, mais la version 1.0.11 est déjà la plus récente.
L'authentification PAC interactive ne termine pas; l'option utilisateur seul
exige explicitement un mot de passe, qui n'est pas fourni. Deux tentatives
bornées de code appareil atteignent la page de saisie, mais clic et clavier
normaux ne la font pas avancer. Le navigateur reste masqué malgré l'activation
normale. Aucun écran MFA ni consentement n'est observé; aucune cause n'en est
déduite. Les deux processus sont arrêtés, la page partagée retourne à Agents et
les profils PAC initiaux restent intacts. Aucun code/jeton, contournement de
stratégie ni profil administrateur non vérifié n'est utilisé pour cloner.

## Précontrôle Azure indépendant du 24 octobre

Les [nouveaux contrôles Azure en lecture seule](../assets/runtime-2026-10-24/azure-preflight-refresh.json)
vérifient séparément administrateur/tenant dans les extensions Azure et Azure CLI;
ils ne prouvent pas l'identité du site dans le navigateur. Les quatre ressources
ARM conservées sont présentes. Les deux déploiements de modèles sont Succeeded
en Sweden Central. Les compteurs exacts renvoient 26 sur 5 000 pour le chat et
1 sur 1 000 pour l'embedding, libellés en milliers de jetons par minute.
Search Basic fonctionne en West US 2 avec un réplica/partition, identité système
et authentification locale désactivée. Les quatre fournisseurs requis sont
inscrits; un GET distinct vérifie Insights en minuscules après son omission
par le filtre de liste sensible à la casse.

Cost Management rapporte désormais **7,650361288 USD** avant taxes pour les
quatre identifiants de ressources conservées et leurs descendants, dont
**7,373 USD** pour Search, du 20 au 24 octobre partiel. Aucun coût de ressource
étrangère à l'atelier n'est inclus. La remontée peut être retardée : ce n'est
ni une facture finale ni un total de crédits Copilot. Aucune inférence, nouvelle
question, écriture de configuration, modification de rôle/stratégie, inscription
de fournisseur, modification de facturation ou suppression.
T001/T009 restent ouverts pour responsable, échéance, budget numérique, crédits
du tenant et autres critères d'acceptation.

Microsoft Graph vérifie indépendamment l'administrateur actuel et renvoie
quatre enregistrements de licences, dont sept plans filtrés liés à la création
en provisionnement Success. Ces attributions ne prouvent pas l'ensemble des
droits premium, les crédits du tenant ou une liaison de facturation de l'environnement.

## Ingestion fictive conforme à la stratégie

L'[essai de chargement public](../assets/runtime-2026-10-24/lab5-blob-ingestion.json)
observe la désactivation imposée du réseau public Storage et HTTP 403 malgré
le RBAC limité. Aucune exemption, clé de repli ou modification de stratégie.
Ressources et rôles temporaires supprimés, inventaire initial préservé.
L'[essai par réseau privé](../assets/runtime-2026-10-24/lab5-private-fictional-ingestion.json)
prouve ensuite S5-01 : exactement deux fichiers fictifs originaux, vérification
DNS/IP privés, identité managée et deux relectures avec empreintes exactes.
La reprise interrompue échoue avant l'indexeur; cet échec et une course de
nettoyage DNS asynchrone récupérée sont conservés. Le retour aux quatre ressources
initiales est vérifié avant une nouvelle tentative à garde distincte.
Le chargement ne prouve ni S5-02 ni réponse connectée; T014 reste ouvert.

La [vérification privée corrigée](../assets/runtime-2026-10-24/lab5-private-fictional-ingestion-vector-readback.json)
ferme désormais S5-01/S5-02. La tentative précédente, indexeur réussi mais
relecture vectorielle HTTP 400, est conservée; le champ jetable est explicitement
récupérable. La récupération CLI prise en charge reprend le travail déjà déployé,
sans nouveau déploiement/chargement, en conservant l'échec de jeton expiré et
les erreurs initiales de nettoyage. Indexation privée finale : deux fichiers,
aucun échec ni avertissement; passages exacts, métadonnées parent/source et vecteurs
réels de 1 536 dimensions vérifiés. Infrastructure, rôles et liens temporaires
supprimés; objets/rôles/liens Search et quatre ressources initiales préservés
indépendamment. Aucune stratégie Storage, configuration réseau public/clé/anonyme,
agent ou route d'origine n'est affaiblie. Avec S5-03/S5-05/S5-06, cinq critères
du lab 5 réussissent; réponses connectées, navigation, français et identité
refusée gardent T014 ouvert.

## Point d'exécution du 23 octobre

L'[inventaire et les contrôles de réparation](../assets/runtime-2026-10-23/completion-progress.json),
la [relecture de l'état enregistré](../assets/runtime-2026-10-23/native-state-readback.json)
et la [revue indépendante des labs](../assets/runtime-2026-10-23/independent-lab-review.json)
conservent les nouvelles preuves séparément des échecs antérieurs.

* T001 avance : les quatre ressources ARM existantes, les identités du compte,
  du projet et de Search, les deux déploiements de modèles et les identifiants
  de propriété conservés concordent. Search Basic fonctionne avec un réplica
  et une partition. Cost Management retourne **6,219977042 USD** avant taxes
  du 20 octobre à la période partielle du 23 octobre, dont **6,060 USD** pour
  Search. La facturation peut être retardée. La balise d'expiration n'a rien
  supprimé; le propriétaire de rétention, l'échéance de revue et la limite
  de dépenses approuvée restent à définir.
* T002/T003 avancent localement : les huit empreintes sources correspondent encore
  à `verified-retrieval-sdk-b4-20261022`. Les 47 tests documentaires existants,
  les 33 tests de l'extension, les contrôles de dépendances/syntaxe et la validation
  canonique/wiki réussissent de nouveau. L'extension hébergée reste en version 1
  active avec Entra et BotServiceRbac inchangés; la réparation SDK n'est pas déployée.
* La préparation T005/T006 avance : trois GET Dataverse authentifiés confirment
  le diagnostic Inactive et son empreinte exacte inchangée. Le rattachement
  d'origine est Active avec identité et cible concordantes. Des lectures Foundry
  actuelles distinctes confirment que la cible sélectionne la version 4 active,
  dont la définition correspond au reçu de création. Sans définition Dataverse
  historique complète du rattachement, sa comparaison octet par octet reste
  impossible. Aucune réponse native n'a été retestée.
* T009/T010/T014 ont été réconciliées critère par critère. Les réussites historiques
  de sous-systèmes restent valables dans leur périmètre, mais aucun critère
  restant n'est nouvellement fermé. La revue précise les preuves manquantes :
  navigation des citations, corps d'erreur du connecteur, canal publié,
  confidentialité et requêtes connectées.
* La requête de récupération du navigateur natif a expiré sans identifiant de page.
  Ses effets restent inconnus; cela ne prouve pas qu'aucune page ne s'est ouverte.
  Une page non partagée ne fournit pas de parcours de test natif authentifié.
* Les validations attribuables et la décision de rétention ont été demandées une
  fois; l'utilisateur était indisponible. Elles restent en attente et ne sont pas
  déduites de la permission générale de reprise. Aucune configuration cloud,
  politique, permission, agent d'origine ou fichier source n'a été modifié.
  Aucun courriel, évaluation, déploiement, suppression ou publication distante
  n'a été effectué.

À ce point en lecture seule, les seize cases restaient ouvertes : chacune exigeait davantage.
Le prochain déploiement exigeait les validations de l'artefact exact; les
contrôles natifs indépendants exigent aussi un navigateur authentifié utilisable.

## Déploiement autorisé et récupération de l'authentification

L'utilisateur a explicitement fourni toutes les validations nécessaires, dont
les déploiements Azure et l'utilisation de crédits Copilot, le **23 octobre 2026
à 16:12:49 -04:00**. Le reçu
[authorized-release.json](../assets/runtime-2026-10-23/authorized-release.json)
applique cette autorisation à la réparation isolée existante et au défaut
connexe démontré, sans inventer de signataires organisationnels.

* **T003 terminée :** le candidat SDK inchangé a été déployé en version 2.
  Le [test Activity positif authentifié réel](../assets/runtime-2026-10-23/hosted-repair-smoke.json)
  a réussi les extraits complets exacts et l'attribution individuelle. Les journaux
  de la même session montrent l'acquisition par identité managée et les appels aval.
* Les [tests négatifs de version 2](../assets/runtime-2026-10-23/hosted-negative-checks.json)
  ont révélé un vrai défaut sans preuve : un appel MCP approuvé terminé retournait
  seulement un saut de ligne, provoquant `JSONDecodeError`. L'entrée trop longue
  échouait correctement avant tout appel au modèle. Ces deux résultats sont conservés.
* L'analyseur traite désormais uniquement le texte vide d'un appel d'outil vérifié
  terminé comme une absence de preuve. Une sortie absente, non textuelle ou non vide
  mal formée échoue explicitement. Cinq régressions ajoutées portent la suite
  à **38 tests réussis**. La relecture de la réponse d'échec conservée réussit
  aussi sans nouvelle inférence. Cet artefact a été déployé en **version 3 active**,
  sans modifier Entra ni BotServiceRbac.
* **T004 terminée dans son périmètre hébergé :** [trois tests Activity réels de version 3](../assets/runtime-2026-10-23/hosted-version3-regression.json)
  réussissent : le cas 6 d'origine inchangé retourne deux extraits exacts avec
  attribution individuelle; la question d'astronomie inchangée retourne l'abstention
  exacte; l'entrée trop longue retourne l'erreur explicite sans appel au modèle.
  Ce sont trois requêtes nouvelles sans reprise, pas une acceptation native ni
  une matrice de onze cas. Les journaux n'exposent pas le principal aval exact
  et ne joignent pas indépendamment l'appartenance aux résultats cloud.
* L'erreur navigateur **AADSTS65002** provenait de la demande de permissions Power
  Platform par le client Azure CLI appartenant à Microsoft. Le consentement
  du tenant et Azure RBAC ne remplacent pas la préautorisation du propriétaire
  d'API Microsoft. Ces tentatives ont cessé. La
  [récupération par client possédé](../assets/runtime-2026-10-23/native-api-access-recovery.json)
  crée un client public monotenant sans secret, utilise PKCE et accorde seulement
  à l'utilisateur courant `MakerOperations.Read` et `MakerOperations.ReadWrite`.
  La liste d'évaluations du bot retourne **HTTP 200**, avec **zéro jeu de tests**.
  Aucun consentement global, rôle d'annuaire, secret client ou profil Azure n'a changé.
* La [préparation du test natif](../assets/runtime-2026-10-23/native-canary-preparation.json)
  produit un CSV privé de deux cas. À ce stade, le prérequis restant exige
  l'interface : importer ce fichier dans le bot existant, configurer le profil
  utilisateur Microsoft Copilot Studio authentifié et enregistrer profil et jeu
  de tests. Leurs vrais identifiants sont nécessaires à une exécution API de
  brouillon. Aucun appel de création non documenté, accès anonyme ni évaluation
  native n'a été tenté.

Le diagnostic reste Inactive et la route d'origine version 4 est préservée.
Six requêtes Activity hébergées ont été envoyées entre les versions 2 et 3;
ce nombre n'est pas un total interne de modèles, de crédits Copilot ou de coûts.
Après livraison, Cost Management retourne encore le même sous-total retardé
de 6,219977042 USD. Les ressources et la nouvelle inscription possédée sont
conservées pour les tests restants. Propriétaire/échéance de rétention et attribution
organisationnelle indépendante restent ouverts. Aucune publication distante
du dépôt ou du wiki n'a eu lieu.
La validation locale à ce stade réussit **53 tests documentaires et 38 tests de
l'extension**, les contrôles de dépendances/syntaxe, la validation canonique,
l'export wiki de 38 pages et sa validation. Ces contrôles ne certifient pas
l'acceptation native ni celle des labs restants.

## Test natif authentifié et restauration

La [configuration navigateur admin/MngEnv](../assets/runtime-2026-10-23/native-ui-setup.json)
enregistre le jeu de deux cas, avec persistance vérifiée après navigation complète.
Les sélections de compte/outil ne persistent pas dans l'interface, mais l'API
documentée de brouillon accepte des liaisons authentifiées explicites. Le
[contrôle préalable](../assets/runtime-2026-10-23/native-run-readiness.json) vérifie
l'appelant, le jeu enregistré et la liaison d'outil sans nouveaux scopes de
connectivité. L'identifiant objet du propriétaire de connexion reste non vérifié
indépendamment.

Après l'échec de chargement de la capacité optionnelle du worker, une
[transition d'état Dataverse prise en charge](../assets/runtime-2026-10-23/native-diagnostic-activate-supported.json)
active uniquement le diagnostic existant. Métadonnées d'état réelles, empreinte
exacte et contrôle de concurrence protègent l'opération. Les lignes complètes du
rattachement d'origine et du parent restent inchangées.

Une [évaluation native de brouillon authentifiée](../assets/runtime-2026-10-23/native-authenticated-canary.json)
est acceptée avec HTTP 202 et se termine le **24 octobre 2026 à 00:19:34 UTC** :
deux résultats, **une réussite et un échec General Quality**, sans nouvelle
soumission. L'échec indique abstention Yes, relevance No et completeness No.
Le propriétaire retourné et la connexion correspondent à l'appelant vérifié et
à la requête. Cela prouve l'exécution authentifiée, pas la livraison native exacte
des sources. L'API n'expose ni les réponses ni la correspondance question/résultat.
L'entrée d'intention diagnostique seule ne valide pas une recherche substantielle.

La [restauration et lecture des preuves](../assets/runtime-2026-10-23/native-canary-restoration.json)
confirment indépendamment le retour du diagnostic à Inactive, sa définition
exacte préservée et les lignes complètes du rattachement d'origine et du parent
inchangées. L'extension hébergée reste en version 3 active; son endpoint natif
sélectionne `@latest` et conserve Entra plus BotServiceRbac. La lecture documentée
des transcriptions, filtrée au bot et à la fenêtre du test, retourne
**403 : privilège `prvReadconversationtranscript` manquant**.
Le navigateur admin vérifié est retrouvé, mais sa demande normale de premier
plan échoue; aucune touche n'est envoyée. Aucun rôle, consentement, paramètre
d'authentification ou publication n'est modifié. Les métriques ne reproduisent
ni ne résolvent l'ancien 403 natif lié au tenant. T005/T006 et la matrice de onze
cas restent ouverts.

## Rapprochement indépendant des outils et de l'infrastructure

Les [alternatives prises en charge](../assets/runtime-2026-10-23/native-recovery-alternatives.json)
conservent les tentatives supplémentaires, sans réussite native. PAC officiel
**2.14.1** est restauré dans un dossier isolé ignoré par Git via le flux NuGet V2
HTTPS, après échec TLS de V3. PAC identifie indépendamment le même utilisateur
admin/MngEnv et le même environnement. L'appartenance Global Administrator ne
fournit pas le rôle Dataverse manquant. L'API documentée d'auto-élévation refuse
le client pour `UserManagement.Users.Apply`, absent du catalogue réel des
permissions publiées. PAC retourne aussi 403; ses alternatives d'affectation
échouent à résoudre l'environnement. Chaque tentative vérifie la restauration
exacte des rôles Dataverse et du profil PAC actif. Aucun nouveau consentement,
rôle ou paramètre d'authentification n'est modifié. La découverte des capacités
du MCP local officiel réussit, puis le processus est arrêté; elle ne fournit pas
la transcription manquante.

Le [rapprochement d'infrastructure T013](../assets/runtime-2026-10-23/terraform-reconciliation.json)
est terminé sans nouvel apply. Terraform **1.16.6** est restauré avec vérification
de l'empreinte officielle de l'archive. Une copie privée des **23 fichiers Terraform
d'origine** reste identique avant et après `init`, `validate` et un plan enregistré
non appliqué. Les codes sont **0, 0 et 2**, sans erreur ni avertissement de
validation, avec **15 instances proposées**. L'inscription automatique des
fournisseurs est désactivée; une lecture Azure indépendante confirme l'absence
du groupe réservé au plan. Versions résolues : AzureRM 4.45.1, AzAPI 1.15.0,
AzureAD 2.48.0, Random 3.6.1 et HTTP 3.6.3.

La comparaison conserve l'ancien apply corrigé de 15 instances et son nettoyage.
Le plan inchangé propose encore GPT-4o `2024-05-13`, déjà refusé, des valeurs
publiques/authentification locale et Search Standard sans identité attachée.
Il ne crée ni endpoint privé, ni projet Foundry, ni index de données. Les
surcharges préservant la stratégie et la vectorisation avec identité système
Search vérifiée séparément ne sont pas des propriétés du plan inchangé.
Aucune infrastructure existante n'est réappliquée. D5-02 et D5-03 disposent
désormais de preuves récentes; l'acceptation complète des labs 5.1 et 5 reste ouverte.

## Portabilité native et progrès Search fictifs

La première voie SDK obtient un vrai clone préservant les deux fichiers de
connaissances. PAC officiel 2.14.1
[refuse ensuite sa propre structure](../assets/runtime-2026-10-23/native-sdk-packaging.json);
le [contrôle Author](../assets/runtime-2026-10-23/native-sdk-author.json)
ne supprime aucun composant pour fabriquer un paquet.
Le [précontrôle distinct modèle/API de fichiers](../assets/runtime-2026-10-23/native-sdk-template-candidate.json)
vérifie les empreintes en service et une liaison existante autorisée, mais
n'exporte que 21 composants sur 26 et omet les instructions de routage parentes.
Ces premiers contrôles ne créent aucun candidat, publication ni question SDK.
Un dérivé privé complet exige encore reconstruction et vérification indépendante
de fidélité avant publication ou acceptation des réponses.

Un [candidat de préparation](../assets/runtime-2026-10-24/native-sdk-staging-corrected-name.json)
est maintenant créé et vérifié non publié. Les deux fichiers téléversés ont
les empreintes d'origine; la liaison existante est vérifiée.
L'authentification Entra intégrée et la stratégie d'accès sont préservées.
La première création refuse un nom trop long sans conserver d'agent;
le nom corrigé réutilise le même schéma. Le candidat conservé n'a encore que
21 composants, manque l'état de routage omis et n'est pas prêt pour le SDK.
Aucune publication, extension de permission ni question pendant cette phase.
Parent, composants, fichiers et référence de connexion d'origine restent inchangés.

La [reconstruction Author](../assets/runtime-2026-10-24/native-sdk-reconstruction.json)
couvre maintenant les 26 composants sources localement. Vingt-quatre définitions
YAML réussissent la validation; l'unique avertissement concerne le nom
d'affichage recommandé absent de la source, pas un comportement omis.
Quatorze opérations préparées reproduisent les 26 composants attendus,
instructions normalisées exactes et diagnostic inactif compris.
Ce sont seulement des résultats locaux : gestion doit contrôler les préconditions,
appliquer atomiquement et vérifier le candidat en service avant toute publication
ou question SDK.

Le [premier précontrôle de gestion](../assets/runtime-2026-10-24/native-sdk-managed-apply.json)
s'arrête avant envoi du lot atomique : la synchronisation de fond avance l'ETag
parent du candidat. Les 21 composants, empreintes et liaisons correspondent encore;
la source reste inchangée. Seules les métadonnées de synchronisation diffèrent.
Le [relevé de capture](../assets/runtime-2026-10-24/native-sdk-capture.json)
indique donc zéro publication, question, activité ou permission écrite.
Une actualisation limitée aux gardes de métadonnées doit revérifier tous les
champs métier avant un essai atomique distinct, jamais ignorer une modification concurrente.

L'[essai atomique rapproché](../assets/runtime-2026-10-24/native-sdk-managed-apply-reconciled.json)
réussit maintenant : les 14 sous-réponses sont HTTP 204. Une relecture indépendante
confirme les 26 composants du candidat, définitions, références et états,
instructions normalisées exactes, quatre empreintes source/candidat, liaison
et contrôles Entra. Les lignes sources complètes restent inchangées.
À ce point, le candidat n'est pas publié; le [relevé de capture](../assets/runtime-2026-10-24/native-sdk-capture-reconciled.json)
ne contient ni question, activité ni réponse finale. Publication et exécution SDK
restent distinctes, sous l'autorisation de déploiement déjà donnée par l'utilisateur.

La [publication du candidat](../assets/runtime-2026-10-24/native-sdk-publish-confirmed.json)
est maintenant confirmée indépendamment par l'API : `Succeeded` et date de
publication présente. PAC retourne 1 après un échec de son analyseur d'état;
aucune republication. Les 26 définitions/états, empreintes, liaisons et contrôles
Entra réussissent encore; parent et lignes sources complètes restent inchangés.
La [tentative de capture du client possédé](../assets/runtime-2026-10-24/native-sdk-capture-owned-client.json)
s'arrête sans jeton Invoke lors de l'authentification silencieuse : zéro
question ou activité, aucune fin déduite. Permissions d'application et consentement
utilisateur exacts sont restaurés, anciens jetons conservés et profil PAC rétabli.
Le diagnostic pris en charge et l'authentification dans le bon profil navigateur
restent des travaux distincts; publier seul ne prouve pas l'acceptation.

Le [diagnostic explicite](../assets/runtime-2026-10-24/native-sdk-auth-diagnostic.json)
identifie maintenant `AADSTS65001`, `consent_required`, sans demande de claims.
Un contrôle silencieux avec erreur et un flux PKCE `prompt=none` du client
possédé échouent pour consentement. Un flux PKCE normal dans le profil vérifié
MCAPS Main Admin ne reçoit aucun rappel dans le délai; son écouteur est fermé.
Le [relevé de récupération](../assets/runtime-2026-10-24/native-sdk-capture-recovered.json)
indique zéro requête SDK et vérifie indépendamment la restauration exacte du
consentement/manifeste, les jetons conservés et les contrôles source/candidat inchangés.
Aucun cookie ni base de session lu. Un flux expiré n'est pas une autorisation
utilisable; tout consentement supplémentaire exige un nouveau rappel actif.

Le [résultat de récupération bornée](../assets/runtime-2026-10-24/native-sdk-auth-consent-recovery-final.json)
obtient maintenant un jeton Invoke vérifié après une attente unique de cinq
minutes puis une tentative de rafraîchissement forcé. Ressource, scope, client
et compte correspondent. La même configuration inclut les scopes OIDC standards :
ils ne sont donc pas des causes prouvées de l'erreur initiale et aucun repli
OAuth simple n'est nécessaire. Le démarrage SDK renvoie une activité de frappe
sans démarrage complet utilisable; zéro question envoyée.
Le blocage passe de l'authentification à la capture du démarrage, pas à une
livraison complète du parent démontrée.

Des erreurs de transport interrompent d'abord le nettoyage; une récupération
indépendante vérifie ensuite le manifeste et tous les consentements utilisateur
du client restaurés exactement, accès Maker et rafraîchissement valide conservés,
contrôles source/candidat préservés et profil PAC antérieur actif.
UIA ne permet ni vérification complète du consentement ni identification sûre
des onglets expirés : aucun Accept/Close à l'aveugle.
N'acceptez pas les pages de consentement expirées du client possédé.

Le [diagnostic SDK avec en-tête](../assets/runtime-2026-10-24/native-sdk-start-diagnostic.json)
récupère ensuite l'identifiant de conversation fourni par le serveur. Le démarrage
désactive son événement uniquement pour le diagnostic, sans valider l'accueil,
et se termine normalement.
Les [deux captures de questions réelles](../assets/runtime-2026-10-24/native-sdk-capture-start-recovered.json)
envoient Hello et le cas SAR 6 inchangé une seule fois chacun. Les trois requêtes
renvoient HTTP 200 et leurs flux se ferment normalement. Hello produit une demande
de précision sur l'enquête; SAR produit une Adaptive Card Azure AI Foundry Agent
Service demandant de connecter le compte puis de sélectionner Continue.
Aucune de ces actions n'est invoquée. Les événements SAR observés sont
`DynamicPlanReceived`, `DynamicPlanStepTriggered` et `DynamicPlanStepBindUpdate`,
pas `DynamicPlanFinished`. Aucune réponse métier ni comparaison de sources
n'est capturée. Le blocage est désormais l'autorisation utilisateur du connecteur
à l'exécution, malgré la liaison enregistrée. Restauration exacte des droits/cache
et préservation source/candidat sont de nouveau vérifiées. T005-T008 restent ouverts.

Le [suivi d'autorisation du connecteur](../assets/runtime-2026-10-24/native-sdk-connector-authorization.json)
s'arrête avant Connect : profil navigateur et environnement sont identifiés,
mais UIAutomation ne peut vérifier le compte administrateur connecté au site.
Ce n'est pas un échec MFA ou OAuth observé. Aucune navigation Connect, soumission
Continue, nouvelle question, modification de droits ou écriture cloud.
Les contrôles indépendants source, candidat, fichiers, liaisons, application,
consentements, cache et PAC réussissent. Une personne doit vérifier visuellement
le compte MngEnv du site et terminer la connexion Foundry approuvée actuelle avant
Continue; les pages OAuth expirées ne doivent pas être acceptées.

L'[alternative visuelle limitée à la fenêtre](../assets/runtime-2026-10-24/native-sdk-connector-visual-verification.json)
ne prouve pas non plus l'identité : l'image PrintWindow inspectée est blanche,
sans compte du site ni tenant lisibles. Aucune action Connect/Continue.
L'état réduit initial du navigateur est restauré et les contrôles de préservation réussissent.

La [garde initiale de capture au premier plan](../assets/runtime-2026-10-24/native-sdk-connector-foreground-verification.json)
observe ensuite une autre fenêtre au premier plan et s'arrête sans prendre
le focus, modifier la fenêtre cible ou capturer des pixels. Aucune autre fenêtre
n'est inspectée. C'est un arrêt avant capture, pas un échec de comparaison d'identité.

La [demande unique de mise au premier plan](../assets/runtime-2026-10-24/native-sdk-connector-focus-request.json)
réussit ensuite : le navigateur vérifié est visible, non réduit et au premier plan.
Son contrôle de compte du site ne prend pas en charge InvokePattern et la garde
des limites de la zone compte refuse la capture. Aucune capture ni action Connect.
L'état réduit initial est restauré; tous les contrôles de préservation réussissent.
La vérification du compte reste obligatoire.

La [récupération par page navigateur prise en charge](../assets/runtime-2026-10-24/native-sdk-browser-page-recovery.json)
vérifie ensuite l'UPN administrateur exact dans le menu du compte du site et la
route de l'environnement cible. Le libellé du profil Edge n'est pas exposé et
ne sert pas de preuve d'identité. Une seule soumission du formulaire Foundry
Connect officiel avec le point de terminaison approuvé renvoie **Unable to sign
in. Please try again.** Aucun succès de connexion : ni Continue ni nouvelle
question SAR. La vérification d'identité du site est résolue, pas l'autorisation
du connecteur. La soumission de création compte comme une écriture cloud,
pas zéro. Les contrôles indépendants source/candidat/fichiers/liaisons/application/
consentements/cache/PAC réussissent sans erreur de vérification ou restauration.
Le message seul ne prouve pas une cause OAuth, MFA, DLP ou RBAC; le diagnostic
pris en charge reste nécessaire.

Après le signalement de connexion par l'utilisateur, le
[contrôle assisté](../assets/runtime-2026-10-24/native-sdk-human-assisted-status.json)
montre encore un formulaire vide avec Create désactivé, pas un message de succès.
Le [contrôle en lecture seule de la liste et des détails](../assets/runtime-2026-10-24/native-sdk-connection-listing-diagnostic.json)
vérifie ensuite que la connexion Foundry exacte référencée par le candidat est
**Connected** dans les deux vues, avec vérification de l'administrateur du site
et de l'environnement requis. Le propriétaire affiché est System Administrator
et la dernière modification date du 21 octobre; cela ne prouve ni une modification
par la connexion récente ni l'autorisation de la conversation suspendue.
Aucune nouvelle création, action Continue ou question SAR dans ces deux contrôles.
Les contrôles de préservation réussissent. La requête et la réponse de la
création échouée n'ont pas été conservées : sa cause reste non classée.
L'authentification du connecteur et le format du point de terminaison respectent
le contrat officiel. L'état de la connexion permet une reprise limitée à
l'exécution, pas une validation de réponse native, d'ancrage dans les sources
ou de la feuille de route complète.

La [reprise unique de la conversation initiale](../assets/runtime-2026-10-24/native-sdk-original-card-continuation.json)
envoie ensuite une seule fois la charge Retry exacte. HTTP 200 et la fermeture
normale du flux SDK renvoient l'indicateur de saisie et la même carte
d'autorisation Foundry, pas une réponse SAR. Le `streamType=final` de la carte
ne prouve ni récupération ni fin du plan : aucune citation, passage source,
événement `DynamicPlanFinished` ou fin de conversation observés.
Aucun second Retry, nouvelle question SAR, Create ou publication dans cet essai.
Le manifeste exact du client et tous les consentements de l'utilisateur sont
restaurés; seul le nouveau jeton d'accès Invoke est retiré, en conservant l'accès
Maker et la rotation valide du jeton de renouvellement. Les contrôles indépendants
source/candidat/fichiers/liaisons/authentification/PAC réussissent sans erreur
principale, de nettoyage ou de vérification. L'autorisation par utilisateur à
l'exécution reste à établir malgré l'état Connected de la connexion existante.

L'[essai instrumenté après connexion au site](../assets/runtime-2026-10-24/native-sdk-instrumented-runtime-connect.json)
utilise la cible Connect de cette nouvelle carte. Le formulaire d'exécution
vérifié propose uniquement Create, sans sélection de la connexion existante.
Entra ID User Login, le point de terminaison approuvé et les champs requis sont
vérifiés avant une seule soumission. Le PUT de connexion renvoie HTTP 201 Created,
l'interface affiche **Unable to sign in. Please try again.**, puis le DELETE
de nettoyage automatique renvoie HTTP 200. La création ne prouve pas
l'autorisation. Les identifiants de requête et de corrélation restent privés;
aucun événement de fenêtre OAuth, erreur de rappel ou corps d'erreur du service
n'est capturé. La cause de l'échec reste non classée. Aucun autre Create,
Continue ou SAR; les contrôles indépendants de préservation réussissent sans
erreur de vérification ou nettoyage. La connexion humaine propre au connecteur,
pas seulement au site, reste la prochaine limite. Ces éléments ne justifient
aucun nouveau rôle, consentement global ou changement de point de terminaison.

L'[audit supplémentaire en lecture seule](../assets/runtime-2026-10-24/native-connector-signin-audit.json)
utilise l'accès administrateur existant à Microsoft Graph v1.0, sans nouveau
consentement. Les requêtes pour l'utilisateur exact entre 19:22 et 19:25 UTC,
dont une requête non interactive distincte, ne renvoient aucun événement.
La fenêtre élargie 19:00–19:30 UTC renvoie quatre connexions Power Apps/shell
Office réussies vers 19:12, pas un code d'échec du connecteur.
Le filtre `signInEventTypes` rejeté reste consigné; `isInteractive eq false`
réussit sur v1.0 sans API bêta. La latence des journaux et la portée des requêtes
interdisent de déduire l'absence de tentative ou un blocage de fenêtre.
Le formulaire d'exécution affiche encore l'erreur de connexion. Aucune
soumission au connecteur, action Continue, question ou modification de permission
ou politique dans ce diagnostic; la cause reste non classée.

La [récupération après rechargement avec clic mesuré](../assets/runtime-2026-10-24/native-sdk-trusted-click-recovery.json)
teste une autre hypothèse après des erreurs de changement/réinitialisation réseau
du navigateur. Les métadonnées OIDC publiques du locataire renvoient HTTP 200,
sans transmission d'identifiants. Le point de terminaison approuvé et Entra User
Login sont vérifiés avant un seul clic Create par l'outil navigateur.
L'événement capturé porte `isTrusted=true` et une activation utilisateur active.
L'interface affiche pourtant Adding connection, puis Deleting connection et
la même erreur. Une absence d'activation fiable n'explique pas cette soumission.
Les erreurs réseau ne sont pas établies comme cause; la disponibilité des
métadonnées ne prouve pas l'autorisation du connecteur.
Cet essai ne capture ni l'identifiant créé ni les statuts PUT/DELETE :
l'affichage de suppression automatique ne prouve pas indépendamment l'absence
de ressource. Aucune action Continue, nouvelle question, modification de
permission ou publication ensuite. Les contrôles indépendants
source/candidat/fichiers/liaisons/consentements/cache/PAC réussissent sans erreur
de vérification ou restauration. Le diagnostic temporaire de clic est retiré.
La liste des connexions de l'utilisateur contient ensuite six lignes, dont
uniquement l'entrée Foundry initiale Connected; aucune entrée Foundry
supplémentaire ni commande de pagination observée. Cette preuve reste limitée
à la liste : l'absence de la ressource exacte n'est pas vérifiée, car
l'identifiant créé pendant l'essai n'a pas été capturé.

La [récupération par le panneau de test Studio](../assets/runtime-2026-10-24/native-studio-existing-connection.json)
établit ensuite un autre parcours pris en charge. Le cas SAR inchangé renvoie
une carte **Open connection manager**; son lien `pva-studio` réel affiche
l'outil Not Connected pour l'administrateur vérifié. Contrairement au formulaire
Connect direct, ce gestionnaire propose **Create or pick a connection**.
Une soumission associe la connexion approuvée existante, sans nouvelle connexion,
flux OAuth ou modification de permission. Le gestionnaire affiche ensuite
Connected via l'administrateur requis. Le retour à Studio réinitialise le panneau;
un seul nouveau cas SAR inchangé est envoyé après vérification de l'association.

Le parcours natif livre alors trois messages de réponse métier, sans carte
d'autorisation ni indicateur de saisie lors de la capture. Une action visible
porte le statut Completed en 25,92 secondes. Le parcours est rétabli, pas la
fidélité aux sources : sept des neuf passages cités du premier message
correspondent exactement; cinq des six du deuxième correspondent. Le dernier
message généré ne contient aucun passage entre guillemets et ne peut réussir
un contrôle de citation exacte par absence. Chaque extrait est comparé à son
propre groupe source canonique affiché dans le corpus original épinglé.
Réponses brutes et texte protégé restent privés. L'attente initiale expire car
elle suppose des enfants directs dans le fil; la capture ultérieure utilise
les articles Web Chat réellement imbriqués. Ni l'absence d'indicateur de saisie
ni le statut de l'outil ne prouvent un événement protocolaire de fin du plan.
L'autorisation du canal publié et la matrice complète de onze cas restent
non prouvées.

Le [diagnostic hébergé existant](../assets/runtime-2026-10-24/native-studio-verified-diagnostic.json)
est ensuite activé uniquement sur le candidat et invoqué une fois par la
connexion native rétablie. Il renvoie HTTP 403, `ConnectorRequestFailure` :
BotServiceRbac exige un identifiant de tenant Entra valide pour l'appelant
Activity. L'outil affiche Failed et zéro jeton, sans réponse métier.
Le diagnostic revient à Off; parent original, définitions/authentification du
candidat, liaisons de fichiers, application/consentements, cache possédé et
profil PAC sont vérifiés indépendamment.

L'[essai Entra seul borné déjà autorisé](../assets/runtime-2026-10-24/native-studio-entra-only-diagnostic.json)
modifie ensuite uniquement la liste d'autorisation du point isolé, en conservant
Azure RBAC, sans jamais activer d'accès anonyme. Une seule question native
dépasse l'erreur de tenant mais renvoie HTTP 400 : l'identifiant de blueprint
de l'appelant Activity ne correspond pas au résumé de l'agent hébergé.
Ce nouvel échec ne valide ni fidélité aux sources ni cause de migration d'identité.
Le diagnostic du candidat revient à Off; les deux autres spécialistes restent On.
Point/carte exacts, Entra avec BotServiceRbac, définition/identité de version 3
et octets du manifeste original sont vérifiés restaurés, sans erreur de
vérification ou restauration. Aucun déploiement, nouvelle version, publication,
changement de corpus ou de rôle. La fenêtre maximale de cinq minutes se termine
plus tôt après l'essai. La prochaine étape est l'examen pris en charge du
contrat protocole/connecteur, pas une nouvelle création de connexion ni le
retrait permanent de BotServiceRbac.

Le [contrôle natif du contrat en lecture seule](../assets/runtime-2026-10-24/native-connector-operation-contract.json)
observe dix actions après **See all**. La référence publique décrit des actions
hébergées Invocations/Responses, mais aucune n'apparaît dans ce catalogue;
cela ne prouve pas leur absence côté service. L'action Activity par application
propose la connexion approuvée, mais son aperçu est annulé avant
**Add and configure**. La liste des outils reste vide et le diagnostic Off.
Le [guide d'intégration natif officiel](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-foundry-agent)
exige Activity, déjà exposé par le point réel. Aucun correctif officiel vérifié
pour cette erreur exacte ni cause de migration d'identité n'est établi.
Aucune identité appelante ou charge Activity n'est remplacée.

Le [nouvel essai SDK publié après association Studio](../assets/runtime-2026-10-24/native-sdk-post-studio-authorization.json)
envoie exactement un cas SAR inchangé, sans reprise. Démarrage et question
renvoient HTTP 200; les deux flux possédés se ferment normalement. Les cinq
activités contiennent frappe, trois événements de démarrage/liaison de plan
et carte Foundry **Connect your account**, pas de réponse métier ni fin du plan.
L'association Studio ne prouve donc pas l'autorisation du canal publié.
Aucun Connect, Continue, nouvelle connexion ou publication ne suit.
Portée du manifeste possédé et consentement limité à l'utilisateur sont
exactement restaurés. Seul le nouveau jeton d'accès Invoke est supprimé;
accès Maker et entrées de rafraîchissement valides sont conservés.
Définitions source/candidat, fichiers, liaisons, authentification, cas original
et profil PAC passent les contrôles, sans erreur primaire, de restauration
ou de vérification finale.

L'[exécution Search fictive réelle](../assets/runtime-2026-10-23/lab5-synthetic-search-retry.json)
ferme S5-03/S5-05/S5-06, pas T014. Elle teste le texte original Harbor/Forest,
la vectorisation de requêtes sans clé en 1 536 dimensions, la recherche
lexicale/vectorielle/hybride/sémantique et les deux assertions de filtrage.
L'échec initial de disponibilité par statistiques reste conservé; le second
essai utilise un comptage de recherche réel. Les deux index temporaires sont
supprimés; les trois schémas existants sont vérifiés inchangés.
Ces contrôles par chargement direct ne prouvaient pas l'acceptation Blob/indexeur;
la vérification privée ultérieure ci-dessus valide S5-01/S5-02.
Les réponses connectées, citations navigables, cohérence française et refus
d'identité restent ouverts.

## Implémentation existante et contraintes

Le reçu suivant décrit les échecs antérieurs. La livraison autorisée de version 3
ci-dessus remplace seulement son état de déploiement, pas ses preuves historiques.

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

La permission générale de reprise et l'autorisation explicite ultérieure de
déploiement/crédits sont enregistrées ci-dessus. Ne les redemandez pas.
L'attribution indépendante des rôles Product Owner, équipe sécurité et responsable
technique n'est pas établie par cette déclaration. Conservez cette distinction
dans T002, les artefacts exacts et le retour arrière limité.

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

- [x] T003 [Plan:2.1] Réexécuter les tests du service, les contrôles de dépendances et de syntaxe. Déployer l'artefact autorisé par l'utilisateur dans le projet existant. Conserver versions SDK résolues, version hébergée, journaux et retour arrière sans effacer l'échec précédent. Terminé : versions 2 et 3 déployées; les 38 tests actuels réussissent.
- [x] T004 [Plan:2.1] Envoyer des requêtes Activity authentifiées avec enveloppes complètes, dont `serviceUrl`. Vérifier sessions réelles, récupération/sélection, extraits exacts et comportements d'erreur/abstention avec les identifiants hébergés. Terminé : tests positif, abstention et entrée invalide de version 3 réussis; acceptation native et appartenance indépendante aux résultats restent exclues.

Sortie : l'erreur de constructeur disparaît dans l'hôte réel et la livraison
fondée sur les sources réussit. Un point de contrôle de disponibilité ne suffit
pas. Garder l'autorisation du point de terminaison inchangée pendant cette
réparation initiale pour ne pas confondre les causes.

### 3.1 Rétablir la livraison native Copilot

Exigence : REQ-003. Entrées : diagnostic enregistré inactif et route de contrôle.

- [ ] T005 [Plan:3.1] Résoudre le contrat natif de protocole/identité avec les métadonnées d'appelant et journaux pris en charge. L'essai Entra seul borné est exécuté et exactement restauré : HTTP 403 devient HTTP 400 de blueprint, sans livraison réussie. Conserver Azure RBAC et BotServiceRbac, sans accès anonyme ni permissions larges. Confier les changements gérés à Manage et le YAML à Author.
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

- [x] T013 [Plan:7.1] Réconcilier le déploiement Terraform corrigé avec ressources requises, versions de fournisseurs, réseaux privés et identités. Préserver les preuves plan/apply et identifier les écarts à la source inchangée; ne pas réappliquer pour reproduire une infrastructure déjà démontrée. Rapprochement terminé : nouveaux init/validate/plan des sources inchangées, écarts réseau/identité/modèle explicites et ancien apply corrigé/nettoyage conservés; aucun nouveau déploiement ni réussite globale du lab.
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
