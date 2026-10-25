---
title: Registre de validation de l'atelier
description: Preuves, vérifications effectuées, limites d'exécution et critères d'acceptation encore nécessaires pour chaque lab.
ms.date: 2026-10-25
---

## Verdict global

[Tous les labs](index.md) | [English](../en/validation.md) | [Galerie de preuves](evidence.md)

La dernière [poursuite du candidat authentifié](completion-roadmap.md#correction-du-candidat-authentifié-du-25-octobre)
résout la connexion administrateur PAC et le clonage officiel. Les recherches
littérales CTR/SAR corrigées et l'accueil sans source réussissent **3/3** en natif,
puis [encore 3/3 sur le brouillon final](../assets/runtime-2026-10-25/final-lookup-regressions.json)
après une correction ciblée des instructions SAR générales. Valeurs exactes et
attributions individuelles sont vérifiées; les instantanés ne valident pas les
citations natives. Routage SAR général et couverture réussissent, mais
[la fidélité de toute la sortie échoue encore](../assets/runtime-2026-10-25/broad-sar-corrected-native.json) :
15/16 citations exactes sur deux messages. Le schéma installé de l'action
Activity externe ne fournit aucun paramètre pris en charge de suppression/capture.
Aucune configuration non prise en charge ni modification du récupérateur protégé
n'est appliquée. La [préservation indépendante](../assets/runtime-2026-10-25/lookup-preservation.json)
confirme les 26 lignes complètes d'origine inchangées, les 28 composants prévus
du candidat, diagnostic Off/deux spécialistes On, fichiers, liaisons, date de
publication et authentification préservés. Aucune publication n'a lieu.
T007/T008 et la feuille de route restent ouverts. Les anciens états de navigateur
indisponible, mauvais tenant PAC et clonage bloqué ci-dessous sont historiques,
pas des blocages actuels; l'échec de dépendances du plugin reste non résolu.

Un [outil MCP local isolé](../assets/runtime-2026-10-25/mcp-evidence-local.json)
réussit désormais la découverte réelle du protocole et une requête SAR inchangée
avec deux documents exacts et leur provenance corrélée. L'assistant du tenant
expose OAuth manuel, mais est annulé sans connexion. Les tests locaux de jetons
signés ne prouvent pas OAuth MCP Entra réel.

Le [contrôle hébergé suivant](../assets/runtime-2026-10-25/mcp-hosted-preflight.json)
réussit maintenant démarrage App Service distinct, HTTPS/TLS et désactivation de
publication basique, refus **401** sans jeton/avec jeton invalide et découverte
correcte **200**. Deux applications possédées à tenant unique, la configuration
sortante d'identité managée limitée et un connecteur MCP officiel avec rappel
inscrit indépendamment sont persistés. La fenêtre native de consentement est
bloquée; l'autorisation normale en nouvel onglet atteint la demande de mot de
passe administrateur. Aucune réponse humaine, réussite de jeton délégué,
récupération par identité managée, liaison candidat ni question native nouvelle
n'est revendiquée. Auxiliaire/rappel temporaires sont supprimés. L'hôte B1 reste
facturable, avec estimation publique de calcul de 0,018 USD/heure, pas une facture
ni un budget approuvé. La [nouvelle préservation](../assets/runtime-2026-10-25/mcp-hosted-native-preservation.json)
confirme contenus d'origine/candidat, fichiers et liaisons inchangés;
définition version 5 et identifiants de principal/client correspondent aussi.
Fidélité complète et feuille de route entière restent ouvertes.

La [preuve réelle d'identité managée](../assets/runtime-2026-10-25/mcp-managed-identity-runtime.json)
remplace la limite de récupération sortante ci-dessus. La question SAR inchangée
renvoie `rc-002` et `ip-006` dans le conteneur applicatif App Service réel;
documents complets et texte rendu correspondent indépendamment au corpus épinglé.
Signature Microsoft, tenant/identité prévus, chaîne limitée à l'identité managée,
code déployé et préservation du récupérateur protégé sont vérifiés.
Les deux tentatives HTTP 403 antérieures restent des échecs. Un seul rôle
personnalisé limité au projet reste après suppression de trois attributions
d'essai possédées. Ses actions exactes de lecture/écriture d'agents permettent
aussi leur modification; aucune requête de modification d'agent n'est effectuée.
La [nouvelle lecture native complète](../assets/runtime-2026-10-25/mcp-managed-identity-native-preservation.json)
réussit encore. OAuth MCP délégué entrant, liaison native, fidélité complète
et matrice entière de onze cas restent non vérifiés. Aucune question native,
invocation d'outil MCP ni publication nouvelle n'est comptée.

La [récupération SAR MCP native ultérieure](../assets/runtime-2026-10-25/mcp-native-sar.json)
remplace ces limites OAuth/liaison et de fidélité SAR bornée. Le consentement
humain explicite pour tout le tenant est relu comme `AllPrincipals` avec seulement
`Evidence.Read`. Une liaison MCP enregistrée et les instructions exactes validées
par Author produisent une réponse native complète du cas 6, avec deux citations
de documents complets exactes, marqueurs individuels et recherche/référence locale
réelle. Ancienne récupération émettrice Off; validation et MCP On.
Les 26 lignes originales, toutes les autres définitions candidat et les refus
401 sans jeton/avec jeton malformé sont préservés. Aucune publication.
`DynamicPlanFinished` brut, matrice fraîche de onze cas et autres tâches restent ouverts.

La dernière [livraison Invocations vérifiée](../assets/runtime-2026-10-24/verified-invocations-delivery.json)
est hébergée en version 5 active, avec Activity préservé, 54 tests du service
et sept contrôles hébergés réussis. Les sorties SAR réelles locales/hébergées
correspondent exactement au rendu de deux documents. Refus sans jeton, limites
du parseur/corps, abstention et livraison Activity corrigée sont vérifiés;
les journaux corrélés excluent les appels de modèle pour les entrées invalides.
L'expiration du CLI et le premier HTTP 400 Activity pour version manquante
restent des échecs historiques. Lecture indépendante et doctor (11 réussites,
zéro échec, deux contrôles ignorés) établissent le service actif sans redéploiement.
Les [contrôles de préservation native](../assets/runtime-2026-10-24/native-preservation-after-invocations.json)
réussissent, mais acceptation native et autorisation SDK publiée restent ouvertes.
La page partagée est masquée et la récupération UI normale échoue; aucune nouvelle
question native ni configuration n'est soumise. Aucun jeu généré, choix de
rétention, budget chiffré ou accord organisationnel n'est inventé pendant
l'indisponibilité de l'utilisateur.

Le [suivi de protocole après publication](../assets/runtime-2026-10-25/native-protocol-followup.json)
récupère le navigateur de l'administrateur vérifié, pas la disponibilité des
opérations hébergées dans le tenant. Le clonage pris en charge est bloqué par
un skill de gestion indisponible; aucun YAML ni configuration n'est inventé.
Un [contrôle de citation CTR du candidat fraude](../assets/runtime-2026-10-25/native-lab1-navigation.json)
ouvre le dialogue de la source attendue, mais le passage affiché ne justifie
pas le seuil. Ce n'est ni le test PDF de licences du Lab 1 ni une réussite
native/matrice complète. Le nouvel échec reste conservé.

La [livraison autorisée antérieure](completion-roadmap.md#déploiement-autorisé-et-récupération-de-lauthentification)
déploie la version 3 active et ferme T003/T004 dans le périmètre hébergé :
**3/3 tests Activity réels positif, abstention et erreur d'entrée réussissent**;
38 tests de l'extension réussissent localement. L'échec de sortie vide en version 2
est conservé. Le problème de connexion AADSTS65002 a été résolu par un client
possédé PKCE sans secret, avec permissions limitées à l'utilisateur courant.
Le [test natif authentifié ultérieur](completion-roadmap.md#test-natif-authentifié-et-restauration)
utilise le jeu enregistré de deux cas et une liaison explicite de connexion :
HTTP 202, Completed, une réussite et un échec General Quality.
Réponses et correspondance question/résultat restent indisponibles; ces notes
ne valident donc pas les sources de la réponse parent complète et ne résolvent
pas l'ancien 403 natif. Le diagnostic est restauré à Inactive avec lecture
indépendante; définition exacte, rattachement d'origine et parent sont préservés.
La lecture ciblée des transcriptions est refusée pour privilège
`prvReadconversationtranscript` manquant; aucun rôle n'est élargi.
Voir [authorized-release.json](../assets/runtime-2026-10-23/authorized-release.json).
Acceptation native/matrice complète, labs restants, rétention et publication
finale restent ouvertes.

Le [rapprochement d'infrastructure indépendant](completion-roadmap.md#rapprochement-indépendant-des-outils-et-de-linfrastructure)
termine aussi la comparaison T013 sans réappliquer de ressources. PAC officiel
2.14.1 et Terraform 1.16.6 à empreinte vérifiée sont restaurés. Une copie privée
identique des 23 fichiers Terraform d'origine réussit init/validate et un plan
de 15 instances; le groupe réservé au plan est absent. D5-02/D5-03 réussissent.
L'ancien apply corrigé et son nettoyage restent distincts du modèle refusé,
des valeurs publiques/authentification et de l'identité Search absente du plan
inchangé. Aucun nouveau déploiement, réseau privé complet ni lab connecté n'est validé.

Le [point antérieur du 23 octobre](completion-roadmap.md#point-dexécution-du-23-octobre)
ajoute un inventaire actuel des ressources/coûts et des lectures authentifiées
de l'état enregistré. La réparation SDK locale passe encore 33 tests, mais reste
non déployée. Le diagnostic est Inactive; les métadonnées Foundry actuelles
sélectionnent la version 4 active inchangée du contrôle. Cela ne prouve aucune
conversation native. La [revue critère par critère](../assets/runtime-2026-10-23/independent-lab-review.json)
ne ferme aucun critère restant. Validations de livraison, propriété de rétention,
accès navigateur, politique et acceptation réelle d'origine restent non résolus.
Les preuves chronologiques ci-dessous ne constituent pas une clôture actuelle.

> [!IMPORTANT]
> Dernière poursuite : connexion Foundry externe manuelle **Connected**,
> rattachement natif et rubrique explicite persistants, inférence Responses directe
> réussie. Le premier test Activity correctif n'a pas reçu de réponse ; un test
> natif instrumenté ultérieur a reçu la vraie réponse en **6,864 secondes**.
> Transport synthétique connecté validé, non scénarios ancrés. L'observateur
> temporaire a été supprimé avec contrôles 404. Les critères d'annotations natives/
> URL éditeur avaient été ajoutés par l'assistant. La vraie recherche joint les
> 24 originaux. Après ajout de provenance canonique, **4/4 questions inchangées
> passent le contenu extractif et l'attribution backend**. Une exécution native
> indépendante réussit ensuite **4/4 questions originales en contenu affiché
> et attribution individuelle**, après correction ciblée des instructions v4.
> Cinq soumissions incluent un essai combiné non acquitté et une relance de transport
> bornée. Les résultats perdus de l'ancien lot ne sont pas reconstitués.
> Les identifiants MCP natifs restent non exposés. L'échec du DOCX original reste,
> mais le guide officiel éditeur sous licence MIT atteint **Ready**, avec égalité
> exacte des 24 enregistrements et quatre questions du notebook.
> Aucune protection retirée ni équivalence DOCX affirmée. Orchestration générative
> activée ; une vraie question CTR cite la source locale sans Foundry.
> Une QA étendue échoue ensuite sur l'accueil, trouve le CTR incomplet et s'arrête
> sur un SAR non acquitté. Après correction ciblée, les trois premiers scénarios
> exacts reçoivent une vraie réponse finale : accueil sans source, CTR complet et
> SAR conditionnel avec citations locales natives. Les échecs sont conservés ;
> ces contrôles ne certifient ni les onze scénarios naturels/locaux/hybrides ni
> l'exécution d'une rubrique d'accueil précise.
> Le retest R2 indépendant en nouvelle session s'arrête sur un Hello non
> acquitté avant toute cible notée : ses onze cas restent non évalués.
> Une lecture native ultérieure révèle une définition d'accueil vide. La saisie
> clavier normale la répare ; lecture après réouverture et vraies traces
> rubrique/actions prouvent désormais son exécution. Attente de préparation
> initiale et bouton Send normal récupèrent la livraison native, sans résultat
> navigateur externe. Les onze questions R3 reçoivent une réponse, mais six
> captures enfant ne prouvent pas la fin du parent. Les suivantes exigent
> `DynamicPlanFinished` ; les cibles répétées sont comptées séparément.
> Voir la [récupération de persistance](backend-live-2026-10-20.md#persistance-de-laccueil-et-livraison-native-récupérées).
> Le [dernier registre complet](backend-live-2026-10-20.md#tours-natifs-complets-récupérés-acceptation-encore-incomplète)
> contient les onze questions originales et leurs gestionnaires attendus.
> Preuves fusionnées, non nouvelle exécution unique des onze cas. L'audit des
> tours complets trouve citations non verbatim et marqueurs groupés ; couverture
> détaillée encore incomplète. Une variante incident échoue puis est retirée,
> avec vrai contrôle après retour. L'acceptation complète reste en échec.
> Capacité corrigée à 26 000 TPM / 26 RPM après une limitation directe prouvée.
> Une comparaison distincte GPT-4.1 a consommé 6 357 jetons mesurés, sans corriger
> l'ancrage des obligations conditionnelles. Agent/déploiement temporaires supprimés
> avec contrôles 404 indépendants ; aucune promotion vers l'agent natif.
> Search Basic, embeddings, compte/projet et deux agents sont **actifs et conservés**,
> contrairement aux anciennes
> exécutions supprimées. Le tag d'expiration ne supprime rien.
> Voir la [validation actuelle des critères d'origine](backend-live-2026-10-20.md#critères-dorigine-réconciliés-et-recherche-réelle-exercée).
> La [comparaison de modèle](backend-live-2026-10-20.md#comparaison-avec-le-modèle-complet-sans-résolution-de-lancrage)
> n'a pas corrigé la synthèse narrative. Voir la
> [récupération native et référence sous licence](backend-live-2026-10-20.md#catégories-natives-récupérées-et-référence-locale-sous-licence-prête)
> pour les réussites natives et locales, sans certification globale.

Preuves antérieures : [registre de réexécution réelle](live-rerun-2026-10-19.md).
Le propriétaire a approuvé les tests payants. Le déploiement Terraform corrigé de
15 instances, 14 contrôles modèle/recherche sans clé et un événement synthétique
Application Insights réellement corrélé par KQL ont réussi. Les ressources ont
été supprimées et leur absence vérifiée. Une autre chaîne PDF privée a réussi
25 contrôles : indexeur Blob réel, neuf projections enfants et embeddings
intégrés de 1 536 dimensions. Le dernier registre distingue son nettoyage
de celui de l'exécution précédente. L'échec SDK du lab 6 et sa restauration
isolée ont aussi été testés. Son
[exécution Foundry payante ultérieure](foundry-live-2026-10-20.md) a généré
24 embeddings réels et vérifié 22 passages récupérés. Le MCP authentifié direct
et les citations monosources de l'agent Foundry ont réussi. Les citations finales
multisources ont échoué ; Activity a été configuré sans conversation Activity/Copilot.
Cet environnement isolé a aussi été supprimé, avec absence vérifiée indépendamment.
La [reprise approuvée des citations](foundry-live-2026-10-20.md#8-reprise-approuvée-des-citations-exactes-et-échec-des-références-natives)
a réussi les trois extraits exacts deux fois, mais les références natives
étaient vides. Le modèle s'est abstenu malgré sept documents hors sujet.
Quatre nouveaux environnements successifs ont été supprimés ; les contrôles
indépendants ont confirmé quatre groupes absents et huit réponses ARM 404.
La [poursuite backend](backend-live-2026-10-20.md) s'est authentifiée à Dataverse
et a cloné l'agent réellement sauvegardé via PAC officiel. La découverte Direct
Line et l'autorisation d'évaluation PAC restent bloquées ; un clone n'est pas une
conversation. La [reprise ultérieure du navigateur](backend-live-2026-10-20.md#reprise-du-navigateur-et-trois-nouveaux-contrôles-réels)
a permis trois nouveaux contrôles Preview : recherche dans le PDF avec réponse
complète, refus d'inventer un prix et validation d'entrée incorrecte avec erreur 400
visible. L'interface Evaluate s'ouvre, sans création ni exécution d'évaluation.
Un audit indépendant du PDF conservé a ensuite réussi les cinq contrôles de
l'identité source, de l'édition, de la citation complète et de la section en
page 3 de cette nouvelle réponse. L'audit de l'ancienne réponse complète,
la navigation des citations et l'acceptation des labs connectés restent ouverts.
La [tentative d'audit historique complet du 25 octobre](../assets/runtime-2026-10-25/lab1-full-answer-audit.json)
revérifie l'empreinte du PDF d'octobre 2026, mais ne retrouve pas la réponse
complète du 19 octobre avec provenance correspondante. Le critère reste
**ouvert/indisponible**, ni réussi ni contredit; les nombres de faits sont inconnus.
Aucune réponse plus récente ni transcription tronquée n'est substituée.
L'échec distinct de navigation PDF et le critère du corps d'erreur restent
inchangés; le Lab 1 n'est pas certifié.
Après approbation explicite des crédits, une évaluation de trois cas avec
General quality a été enregistrée et soumise. Elle a été observée en attente,
sans notation ; la reprise navigateur de 11:36 UTC a échoué et son état actuel
est inconnu. Les [preuves de l'exécution approuvée](backend-live-2026-10-20.md#évaluation-approuvée-et-soumise-notation-non-observée)
ne revendiquent ni score, ni total de crédits, ni correction des permissions PAC.
L'onglet partagé suivant affichait une erreur de configuration Dataverse, mais
de nouvelles lectures authentifiées ont renvoyé HTTP 200 pour le même environnement
provisionné, l'identité et l'agent enregistré. Ce message ne prouve pas une suppression
et ne justifie pas une base de remplacement. Un diagnostic hors ligne du contrat
de citation Foundry a aussi réussi 45 contrôles : il identifie des hypothèses
JSON/titre non prises en charge, sans inventer les annotations natives absentes.
Un nouveau test réel au format pris en charge a ensuite conservé les phrases
sources, mais inventé les trois URL et encore produit zéro annotation native.
Il s'est arrêté sans correction répétée. Le cinquième environnement a été
supprimé ; les cinq groupes et dix réponses ARM 404 ont été vérifiés indépendamment.
Les tableaux suivants conservent l'état de la revue initiale,
sauf mise à jour apportée par ces registres.

La session fonctionnelle a ensuite récupéré l'évaluation d'origine terminée :
**1 réussite, 2 échecs, 7 Copilot Credits, 00:02:44**. Aucun doublon soumis.
Le [rapport des résultats](backend-live-2026-10-20.md#résultats-de-lévaluation-terminée-récupérés-dans-la-session-fonctionnelle)
conserve l'écart refus/pertinence et l'échec de complétude/citation du PDF.
Une destination Standard de création/test est désormais accessible ; ses
contrôles d'intégration ne prouvent pas la réussite des labs connectés.
Le [test connecté ultérieur du lab 3](lab-03.md#réussite-ultérieure-du-test-connecté-de-lagent)
a réellement validé l'émission par l'agent : une rubrique native exécutée,
réglages de confidentialité relus et un événement Application Insights
indépendamment associé à cinq propriétés synthétiques. Aucun émetteur externe
ni canal publié. Les clés d'identifiants conversation/canal existent encore ;
leurs valeurs sont exclues des preuves publiées.

Après approbation explicite, la
[prolongation de l'essai](../assets/runtime-2026-10-20/trial-extension.json)
a supprimé la fenêtre d'expiration et rétabli les réglages génératifs. Aucun
achat récurrent, nouvel environnement, consentement sans rapport ni activation
de recherche web. La date d'expiration n'a pas été affichée ni vérifiée.
Les [contrats d'authentification](../assets/runtime-2026-10-20/advanced-integration-contracts.json)
ont ensuite été inspectés : Search propose Entra Integrated, mais le prompt BYOM
exige une clé incompatible avec la politique imposée. La véritable
[tentative Search](backend-live-2026-10-20.md#connexion-search-sans-clé-bloquée-par-le-navigateur-hôte)
a échoué car le navigateur hôte bloquait la fenêtre de connexion. Aucun écran
de consentement, connexion ou question connectée, malgré les requêtes Azure
réussies. Le nettoyage a ensuite vérifié HTTP 404 pour le groupe, Search,
compte IA, déploiement et quatre attributions de rôles dédiés. Aucune ressource
active de ce test ne subsiste ; des frais antérieurs peuvent encore apparaître.

Une nouvelle connexion AccessKey formelle a ensuite réussi sans fenêtre OAuth,
sur un autre service Search jetable, en conservant Cognitive sans clé.
Parmi **neuf vraies questions Search connectées**, la spéculation de licences
initiale a échoué, puis les instructions natives et la branche d'abstention
explicite ont corrigé le comportement. Les régressions finales négative et
positive ont réussi ; la réponse hôtelière correspondait à la localisation
source et le cas négatif s'est abstenu. La
[chronologie complète](backend-live-2026-10-20.md#traitement-explicite-de-labsence-de-réponse-réussi)
conserve chaque échec. Un [contrôle natif ultérieur](backend-live-2026-10-20.md#le-navigateur-natif-a-confirmé-le-lecteur-pdf-de-léditeur)
a vérifié le PDF authentique à la page 3, mais pas le clic initial sur la citation
du chat. Les URL hôtelières restent absentes. Une vraie tentative formelle Foundry Entra a aussi rencontré la
fenêtre bloquée ; aucune conversation Activity. Ce nouvel environnement a
ensuite été déconnecté et supprimé avec contrôle indépendant :
[suppression distante](../assets/runtime-2026-10-20/search-accesskey-removal.json) et
[nettoyage actuel](../assets/runtime-2026-10-20/search-accesskey-cleanup.json).
Projet, rôle dédié, groupe, Search, compte IA et déploiement ont renvoyé HTTP 404
à 23:20 UTC ; la destination de gouvernance externe est restée intacte.
La rubrique corrigée non publiée subsiste sans connexion Search active.

Une [reprise via Edge externe](backend-live-2026-10-20.md#reprise-foundry-via-edge-externe)
a atteint le vrai formulaire Foundry Entra, mais la saisie du point de projet
ne persistait pas et Create restait désactivé. Zéro soumission d'authentification ;
ni rejet ni comportement de fenêtre externe testé. Le relais manuel demandé
n'était pas disponible. Aucun modèle ni appel d'inférence ajouté.
Une nouvelle lecture native a ensuite vérifié l'absence de connexion dédiée.
Les [ressources d'authentification ont été supprimées](../assets/runtime-2026-10-20/foundry-external-auth-cleanup.json)
à 23:58:49 UTC, avec projet/compte/groupe à 404 et gouvernance préservée.
L'enregistrement de récupération du compte supprimé reste présent, sans purge.
Un [contrôle supplémentaire du prérequis de saisie sans ressource](backend-live-2026-10-20.md#prérequis-supplémentaire-de-saisie-native-toujours-bloqué)
s'est arrêté avant la sonde Legacy : navigateur non mis au premier plan et
formulaire non ouvert. Un [contrôle ultérieur dans le navigateur intégré partagé](backend-live-2026-10-20.md#saisie-rétablie-dans-le-navigateur-partagé-non-authentification-externe)
a ouvert le formulaire au clavier et vérifié une sonde inoffensive, puis annulé
sans soumission. La reprise Edge externe et la levée du blocage de fenêtre
d'authentification intégré restent non prouvées. Le
[contrat publié du connecteur Inference](lab-04.md#objectifs-et-prérequis)
exige aussi une clé API, sans alternative Entra documentée pour ce connecteur.

La revue et la publication de la documentation sont distinctes de la validation
réelle des labs. L'atelier **n'est pas certifié comme entièrement réexécuté**.
Le lab 1 dispose de preuves utilisateur et d'une nouvelle exécution de son parcours
principal. Les autres labs ont désormais de vraies preuves cloud par sous-système,
mais leurs intégrations complètes d'agents connectés restent non vérifiées.

Le navigateur a d'abord rencontré une barrière d'authentification. L'utilisateur s'est
ensuite connecté et a initialisé le wiki GitHub. Cela a levé le blocage de publication,
sans créer automatiquement les ressources Search, la télémétrie, les modèles, les
index, les bases de connaissances ou les connecteurs nécessaires.

L'[exécution Search fictive](../assets/runtime-2026-10-23/lab5-synthetic-search-retry.json)
réussit aussi S5-03/S5-05/S5-06 après correction explicite de disponibilité.
Elle prouve recherche et filtrage du jeu fictif exact de deux documents, pas
l'ingestion Blob, les réponses connectées, les citations navigables ni le refus
d'identité. Les deux index jetables sont supprimés; les schémas d'origine restent inchangés.
Le [précontrôle SDK](../assets/runtime-2026-10-23/native-sdk-template-candidate.json)
prouve l'API de fichiers et la liaison existante, mais le modèle exporté perd
instructions et cinq composants. Ce n'est pas un dérivé publié fidèle.
Le [nouveau candidat de préparation](../assets/runtime-2026-10-24/native-sdk-staging-corrected-name.json)
a des fichiers, une liaison et une authentification intégrée vérifiés, mais reste
incomplet et non publié. Aucune acceptation de réponse SDK n'est déduite.
Après [reconstruction atomique vérifiée](../assets/runtime-2026-10-24/native-sdk-managed-apply-reconciled.json),
le candidat est [publié selon l'API](../assets/runtime-2026-10-24/native-sdk-publish-confirmed.json).
La tentative SDK n'envoie encore aucune question : aucun jeton Invoke silencieux.
La restauration exacte permissions/consentement réussit; publier ne ferme pas
l'acceptation des réponses natives.
La [récupération bornée suivante](../assets/runtime-2026-10-24/native-sdk-auth-consent-recovery-final.json)
obtient bien un jeton Invoke vérifié, mais le démarrage SDK ne produit qu'une
activité de frappe et aucune question. La restauration finale indépendante
réussit après des erreurs de transport; démarrage et réponse complète restent à prouver.

La [capture suivante avec en-tête](../assets/runtime-2026-10-24/native-sdk-capture-start-recovered.json)
récupère bien l'identifiant serveur et capture Hello puis le cas SAR 6 inchangé,
une fois chacun, avec HTTP 200 et flux fermés normalement. Le diagnostic désactive
l'événement de démarrage et ne valide donc pas l'accueil. Hello renvoie une demande
de précision sur l'enquête; SAR renvoie une carte Connect/Continue du connecteur
à l'exécution, pas une réponse métier. Seuls `DynamicPlanReceived`,
`DynamicPlanStepTriggered` et `DynamicPlanStepBindUpdate` sont observés :
aucun `DynamicPlanFinished` ni comparaison de sources. Connect/Continue reste
non invoqué. Restauration exacte et préservation de l'original sont vérifiées.
La capture de réponse du parent est démontrée, pas l'acceptation native complète.

Le [suivi de connexion](../assets/runtime-2026-10-24/native-sdk-connector-authorization.json)
s'arrête avant Connect car UIAutomation ne peut vérifier la session administrateur
du site, malgré le profil navigateur et l'environnement identifiés. Aucune
écriture cloud, modification de droits ou nouvelle question; les contrôles
indépendants de préservation réussissent. Vérification humaine du compte et
connexion restent requises. Ce n'est ni un échec MFA/OAuth ni un SAR terminé.

La [tentative ultérieure par page navigateur prise en charge](../assets/runtime-2026-10-24/native-sdk-browser-page-recovery.json)
vérifie bien l'administrateur exact et l'environnement cible. Une seule soumission
Create du connecteur officiel renvoie **Unable to sign in. Please try again.**
Aucun succès, Continue, nouvelle question ou événement d'exécution. Contrôles
de préservation réussis. À cette étape, le blocage est la connexion réelle du connecteur,
pas l'identité illisible du site; l'erreur générique n'en prouve pas la cause.

L'[association native Studio ultérieure](../assets/runtime-2026-10-24/native-studio-existing-connection.json)
rétablit l'autorisation par utilisateur en sélectionnant la connexion approuvée.
Les réponses SAR natives échouent ensuite en fidélité : sept citations sur neuf
et cinq sur six correspondent à leur propre groupe source; la paraphrase finale
sans guillemets n'est pas une réussite.
Le [diagnostic hébergé existant](../assets/runtime-2026-10-24/native-studio-verified-diagnostic.json)
renvoie HTTP 403 de tenant appelant; un [essai Entra seul borné](../assets/runtime-2026-10-24/native-studio-entra-only-diagnostic.json)
renvoie plutôt HTTP 400 de blueprint. Les deux diagnostics reviennent à Off.
Point/carte exacts, Entra avec BotServiceRbac, définition/identité de version 3,
manifeste source et contrôles indépendants de préservation sont vérifiés.
Aucun accès anonyme, changement de rôle, déploiement, publication ou réussite
de fidélité aux sources n'est revendiqué.
Le [nouvel essai SDK publié ultérieur](../assets/runtime-2026-10-24/native-sdk-post-studio-authorization.json)
envoie ensuite un seul cas SAR inchangé et reçoit toujours la carte Foundry
par utilisateur, sans réponse ni fin du plan. HTTP 200 et fermeture normale
ne valident pas l'autorisation. Aucun Connect/Continue; manifeste et
consentements temporaires possédés exactement restaurés, seul nouveau jeton
Invoke supprimé. Accès Maker/rafraîchissements valides et contrôles
source/candidat/fichiers/liaisons/authentification/cas original/PAC préservés.

L'[exécution privée conforme du jeu fictif](../assets/runtime-2026-10-24/lab5-private-fictional-ingestion-vector-readback.json)
ajoute deux vraies réussites S5-01/S5-02 : deux fichiers exacts chargés en privé,
indexation Blob privée sans échec/avertissement et deux passages exacts lisibles
avec vecteurs réels de 1 536 dimensions. Ressources et rôles jetables supprimés,
état Search/ARM initial vérifié préservé. Les échecs réseau, relecture et
jetons expirés/nettoyage restent conservés; aucune stratégie affaiblie.
Ces deux réussites d'ingestion ne prouvent ni réponses connectées ni navigation.

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
