---
title: Registre de validation de l'atelier
description: Preuves, vérifications effectuées, limites d'exécution et critères d'acceptation encore nécessaires pour chaque lab.
ms.date: 2026-10-26
---

## Verdict global

[Tous les labs](index.md) | [English](../en/validation.md) | [Galerie de preuves](evidence.md)

### Acceptation du lab 6 réconciliée, 2026-10-26

La [correspondance documentaire T017](../assets/runtime-2026-10-26/lab6-acceptance-crosswalk.json)
est livrée avec le [guide actualisé](lab-06.md), sans acceptation du lab entier.
F6-01/02/03 sont PASS historiques hors ligne, pas des réussites d'exécution.
F6-04 est PASS; F6-05 est PASS au niveau du document avec la limite d'extrait
ci-dessous. F6-07 est PASS et F6-08 est PASS pour la réponse uniquement;
F6-06/12 sont PARTIAL; F6-09 est PASS sous sélection explicite; F6-10/11 sont NOT_RUN.
Les douze lignes conservent provenance, pointeurs publics et limites.
Au point de contrôle hors ligne initial du 2026-10-26, F6-04/05 étaient NOT_RUN et F6-08 était PARTIAL;
la réconciliation n'avait soumis aucune question ni tentative réelle.

Le [contrôle multisource exact](../assets/runtime-2026-10-26/lab6-multisource-native.json)
réussit F6-07 : une question, un appel MCP natif terminé, deux enregistrements
vérifiés dans le corpus figé et deux groupes applicables, procédures d'enquête et
conformité réglementaire. Comparaison attribuée, aucune règle inventée et plan
terminé non annulé sont prouvés. Cette preuve MCP prospective ne joint pas les
résultats d'outil du spécialiste original historique.

Le [reçu de réparation du routage](../assets/runtime-2026-10-26/lab6-intake-routing-repair.json)
conserve F6-06 FAIL initial : l'accueil non ancré correspondait à `hi` dans `Which`.
Seule cette condition a changé, avec `^...$` et `reviewing a case`; le contrôle du
sujet natif sauvegardé réussit. Une cohorte distincte comprend quatre questions,
quatre conversations et aucune relance interne. F6-06 réussit désormais la recherche
MCP étayée, avec deux enregistrements vérifiés et un plan terminé, mais reste PARTIAL :
l'appel de l'agent enfant Foundry original est non prouvé. Les régressions F6-04/05
réussissent dans leurs limites existantes. F6-09 FAIL est conservé : ancrage et
traçabilité centrale réussis, mais prose finale anglaise. La version du composant
du sujet reste `NOT_ESTABLISHED`; aucune publication d'agent n'a eu lieu.

La [tentative avec langue configurée](../assets/runtime-2026-10-26/lab6-language-configured-attempt.json)
ajoute `fr-FR` secondaire, sans changer `en-US` primaire. Le nouvel envoi anglais
affiche `Cannot send empty message` : une intention/un clic, zéro question acceptée
observée en 240 secondes, acceptation serveur `NOT_ESTABLISHED`. Le français n'est
ni sélectionné ni envoyé; cette tentative est NOT_RUN et ne remplace pas le FAIL
terminé. Langue de session et restauration anglaise restent non vérifiées.
Détection automatique et localisation complète des sujets statiques ne sont pas
prouvées. La publication ne soumet aucune question.

Le [contrôle ultérieur en texte français](../assets/runtime-2026-10-26/lab6-french-locale-native.json)
prouve la livraison, pas l'acceptation française : une question acceptée après
vérification du vrai champ et du compteur `60/2000`, mais activité et réponse ont
la locale `en-US` et la prose reste anglaise. Un appel MCP terminé retourne trois
enregistrements vérifiés, dont les deux entrées centrales de la base anglaise
antérieure. Corpus, instructions et modèle sont inchangés, mais le français
secondaire a été ajouté après cette base. Le plan non annulé termine en
71,232 secondes de réception serveur à réponse (76,134 secondes depuis Send).
Aucune nouvelle question anglaise ni relance. Les deux boutons de langue
exposent encore `aria-checked=false` après un contrôle clavier natif sans question.
Ce F6-09 historique reste FAIL, sans cause de sélection prouvée. L'échec de livraison précédent
et le NOT_RUN conditionnel restent conservés.

La [réparation prise en charge des traductions](../assets/runtime-2026-10-26/lab6-french-localization-repair.json)
utilise PAC officiel `2.14.1` via le proxy NuGet d'entreprise existant, sans modifier
l'authentification ni TLS. L'import français natif réussit; des exports indépendants
prouvent les 155 valeurs anglaises inchangées et 97 valeurs d'exécution traduites
persistantes après normalisation des libellés/déclencheurs. L'énumération Windows
à chemins étendus vérifie les 39 fichiers principaux identiques et 22 traductions
ajoutées; le sous-ensemble précédent de 35 fichiers à chemins courts était incomplet.
Après rechargement complet,
les deux langues restent `aria-checked=false` et une nouvelle session sans question
accueille en anglais. À ce point de contrôle, la question française reste NOT_RUN;
le dernier F6-09 terminé à ce point de contrôle était FAIL. Traduction statique complète et cause de sélection
restent non prouvées; voir [#5](https://github.com/devopsabcs-engineering/copilot-studio/issues/5).

La [cohorte ultérieure de sélection explicite](../assets/runtime-2026-10-26/lab6-language-switch-native.json)
réussit F6-09 : `System.User.Language` exécuté et relu vaut French; la question
inchangée reçoit une prose française et un plan ancré terminé, tandis que les
`Activity.Locale` envoyée/répondue restent `en-US`. La régression anglaise réussit;
F6-06 global reste PARTIAL, car la route d'enfant Foundry original n'est pas prouvée.
Deux conversations neuves contiennent cinq messages acceptés : deux questions de
domaine et trois contrôles déterministes, sans relance. Chaque question termine un
appel MCP; l'anglais retrouve une entrée et le français deux, dont une entrée ATO
centrale commune. Le retour à l'anglais est prouvé dans la seconde conversation.
Les 1 288 fichiers historiques gardent leurs empreintes/dates; un clone complet neuf
vérifie 63 fichiers hors jeton et 22 traductions inchangés. Réparation du sélecteur,
détection automatique et preuve continue des versions restent non prouvées.
Les anciens FAIL/NOT_RUN et l'attente échouée d'écho du collecteur sont conservés;
aucun message n'est rejoué.

Les [deux textes statiques français ultérieurs](../assets/runtime-2026-10-26/lab6-french-static-wrappers.json)
réussissent leurs contrôles natifs ciblés : une conversation neuve, quatre messages
acceptés (deux consultations et deux contrôles de langue), quatre clics Send et zéro
relance. Les réponses CTR/SAR correspondent exactement aux ressources françaises
corrigées, avec les 12 citations littérales et références individuelles inchangées.
Ces instantanés ne sont pas une recherche en direct; zéro invocation native de
recherche/MCP/Foundry. `System.User.Language` français et retour à l'anglais sont
prouvés; les `Activity.Locale` envoyées/répondues restent `en-US`. La valeur persistante
est remise à l'anglais, pas effacée. Un téléversement conserve les deux corrections.
Les contrôles stricts d'égalité et de modification de deux seuls fichiers échouent
et restent des échecs : l'audit en lecture seule explique 41 positions réordonnées
avec les 42 phrases Escalate conservées, un composant français matérialisant un repli
existant et les métadonnées administratives. Le clone passe de 64 à 65 fichiers;
le contrôle après exécution préserve 64 fichiers hors jeton, 23 traductions françaises
et 50 composants. Les 158 ressources anglaises/153 françaises et 1 814 fichiers
historiques restent exacts à ce contrôle. L'échec UTF-8 strict sur BOM est conservé;
la validation compatible BOM relit les mêmes fichiers, sans export ni message
supplémentaire. Cette cohorte distincte ne prouve ni localisation statique complète,
ni réparation du sélecteur, ni détection automatique, ni achèvement de T017.

Le [contrôle exact d'historique privé](../assets/runtime-2026-10-26/lab6-private-history-native.json)
est F6-08 PASS pour la réponse uniquement : une question, sans relance ni Hello
supplémentaire, sur la même configuration prospective figée que F6-04/05. La réponse
finale complète reconnaît que les preuves configurées n'établissent pas l'historique
du client privé et refuse toute inférence, sans événement inventé ni substitution
par le corpus fictif. Message final natif et repli terminal `EndDialog`/état sans
réponse terminé sont prouvés, mais la clôture du plan reste non prouvée :
aucun `DynamicPlanFinished` en 240 secondes. Une recherche locale terminée retourne
trois enregistrements. Le libellé MCP n'a pas d'invocation/sortie corrélée; les nombres
réels d'appels MCP et Foundry sous-jacents sont `NOT_ESTABLISHED`, pas zéro.
Ce cas est distinct du cas 9 de la matrice originale, sans équivalence d'architecture
ni achèvement T017/atelier. La publication ne soumet aucune question.

Les [deux contrôles natifs exacts](../assets/runtime-2026-10-26/lab6-intake-local-native.json)
consignent la cohorte antérieure : deux questions, une par conversation neuve, sans
question préliminaire ni relance. F6-04 a terminé la clarification avec
`activityProcessed=true`, sans recherche ni appel de preuve Foundry/MCP
(0,118 seconde entre réception serveur et réponse finale). F6-05 a terminé un
`SearchAndSummarizeContent` local et un `DynamicPlanFinished` non annulé, sans
appel de preuve Foundry/MCP (70,618 secondes). Account Takeover est étayé au niveau
du document par un autre fragment réellement récupéré de la même source;
l'extrait de citation affiché ne contient pas la ligne ATO. Le support du fragment
cité exact, la fidélité de l'extrait et la qualité globale des citations ne sont
pas prouvés. Cette configuration prospective figée du spécialiste original
existant, adaptée à MCP, utilise le Markdown éditeur MIT réellement Ready,
sans équivalence avec la configuration historique; l'ingestion DOCX reste Error.
Après contrôle, racine/paramètres, empreinte des instructions, versions des
sources, empreintes éditeur et archives sont inchangés, sans second export complet.
Ces tests n'ont rien modifié/publié ni créé de ressource. La publication ne soumet
aucune question. Aucun nouvel export ou secret n'est requis pour ces deux contrôles.

Spécialiste original natif 4/4, extension diagnostique hébergée et candidat MCP
de données sont des routes distinctes. Les correspondances au corpus ne joignent
pas indépendamment les résultats de l'outil natif du spécialiste.
L'[ancien candidat 11/11](../assets/runtime-2026-10-25/mcp-native-eleven-case-matrix.json)
comprend une relance explicite. La [cohorte actuelle après contrôle est à 10/11](../assets/runtime-2026-10-25/mcp-native-control-repair-regression.json);
cas 9 échoué deux fois, cause non prouvée, aucun troisième essai.
Conservez échecs et citations historiquement réussies, sans substitution entre cohortes.

Accueil, connaissances locales, expertise étayée, multisource, trois jeux de
données et nettoyage sont fondés sur les sources. Syntaxe/disposition, variantes
ciblées et contrôles français/client privé/identité refusée/sans Activity sont
des validations du guide, pas de nouvelles exigences originales universelles.
Le libellé F6-05 apparaît dans les instructions; son exécution n'était pas prouvée
au point initial hors ligne, avant le nouveau reçu. Les autres variantes non
exécutées limitent la reproductibilité, sans imposer de répéter
les comportements sources vérifiés. Les exigences supplémentaires du document
principal protégé restent UNKNOWN, sans contournement ni reconstruction.
Annotations natives, URL éditeur et citations verbatim ne sont pas des critères
originaux universels; les anciens tests gardent leurs vrais résultats.

Le refus Search du lab 5 ne prouve pas le refus Foundry F6; HTTP 400 de blueprint
ne prouve pas le test sans Activity suivi de réparation.
La [réparation hébergée v3 T003/T004 réussit 3/3](../assets/runtime-2026-10-23/hosted-version3-regression.json);
la [v5 hébergée reste conservée](../assets/runtime-2026-10-26/agent-endpoints-readonly.json)
sans certification native. Les anciens nettoyages ne prouvent que leurs propres
inventaires clos, pas zéro ressource actuelle ni facture finale.
T017 reste non cochée, l'atelier incomplet. Reprenez un seul critère non résolu
avec périmètre autorisé et prérequis pris en charge, pas des labs entiers.
La chronologie et le tableau initial ci-dessous restent historiques, sans
remplacer cette réconciliation actuelle.

### Chronologie des exécutions antérieures

La [sonde Search intégrée](../assets/runtime-2026-10-26/native-search-integrated-popup.json)
emploie le choix natif Microsoft Entra ID Integrated et l'espace `ai://`
documenté. Un seul Create rencontre l'erreur explicite de popup de consentement
bloquée; OAuth ne se termine pas, Next reste désactivé et le sélecteur ne tourne
jamais. Aucun statut/corps HTTP du sélecteur ni principal natif établi.
[VS Code documente le blocage des popups](https://code.visualstudio.com/docs/debugtest/integrated-browser#_navigation);
l'OAuth normal dans un navigateur externe pris en charge est le prochain
prérequis, pas une autre question ni un élargissement de permissions.
Le nettoyage vérifie sept connexions initiales et aucune connexion de sonde
persistante, sans suppression devinée. Deux instantanés complets de 64 fichiers
à chemins longs conservent 63 fichiers hors jeton, 22 traductions françaises et
49 composants. Zéro source ajoutée, question, enregistrement, publication ou
écriture Azure; aucun audit continu de l'état externe. Ce n'est pas une
correction de l'échec antérieur par principal de service. S5-10/T014/T016 et
l'acceptation de recherche native/refus apparié restent ouverts.

Les [deux nouvelles cohortes Search OAuth par principal de service](../assets/runtime-2026-10-26/native-search-index-picker.json)
enregistrent chacune Connected après un Create, puis échouent au sélecteur :
`Something went wrong.`, HTTP 400 console, Add to agent désactivé.
Data Reader sur le seul index manque de lecture des métadonnées; l'ajout séparé
de l'Action `Microsoft.Search/searchServices/indexes/read` au service, sans
DataActions, écriture ni operations/read, réussit liste directe/requête du propre
témoin synthétique, pas le sélecteur natif. Ses deux attributions sont vérifiées.
Corps HTTP indisponible, cause et principal natif non établis; aucun correctif
inféré. Zéro source et zéro question native positive/négative/de modèle; aucune
liaison, correspondance, disponibilité, 403 direct après révocation ni acceptation
sans fuite. Connected/contrôles directs ne valent pas acceptation native ou
appariée partielle. Les deux nettoyages indépendants laissent zéro ressource
possédée et retirent secrets et fichiers protégés; contrôles initiaux et 181
fichiers préservés. Les erreurs PAC de filtre et DNS du premier restent
consignées avec reprise séparée; second nettoyage/vérification sans erreur.
Le [ticket de diagnostic nº 4](https://github.com/devopsabcs-engineering/copilot-studio/issues/4)
suit la question du contrat pris en charge. S5-10/T014/T016 restent ouverts.

Le [contrôle du modèle actuel](../assets/runtime-2026-10-26/agent-endpoints-readonly.json)
renvoie deux GET réussis et identiques. L'hébergement v5 initial expose déjà le
nouveau point de terminaison, avec Activity/Invocations et Entra/BotServiceRbac
inchangés; approbation `not_published`. Aucune écriture ni question. La nouvelle
documentation ne prouve aucune correction native ni n'efface les six échecs
de l'ancienne route; T005/T006 restent ouverts.

La [corrélation locale des ID](../assets/runtime-2026-10-26/native-blueprint-identity-correlation.json)
localise l'écart historique: blueprint d'activité égal à l'ID objet de l'utilisateur
approuvé, résumé égal au blueprint cible inchangé. Aucun nouvel essai natif,
remplacement d'identité ni correctif pris en charge n'est revendiqué.

La [cohorte SP appariée interrompue](../assets/runtime-2026-10-26/lab5-paired-sp-interrupted-cleanup.json)
compte zéro intention de question native autorisée/refusée. Secret, identité,
brouillon, quatre rôles et ressources Azure possédés sont indépendamment absents
après nettoyage. Inventaires initiaux et 181 fichiers historiques préservés.
L'inventaire du portail natif redirige vers la connexion; les preuves PAC/Dataverse
ne prouvent pas l'absence dans le portail. Ni acceptation native appariée ni coût
finalisé revendiqués; S5-10, T014 et T016 restent ouverts.

Le [suivi Search Entra natif](../assets/runtime-2026-10-25/lab5-native-entra-connected.json)
réussit S5-04/S5-07/S5-08/S5-09 sur le jeu fictif isolé. La cohorte initiale
3/4 conserve sa réponse anglaise à la question française. Une cohorte distincte
4/4 avec français activé vérifie récupération native réelle, faits exacts,
abstention sur le prix et citations individuelles. Le français est sélectionné
dans le panneau, pas déduit de la locale cliente `en-US` enregistrée.
Un clic natif réel ouvre le fichier source immuable sans fragment de section.
Une configuration de diagnostic est vide; les clones officiels avant/après
confirment les 17 fichiers d'auteur inchangés. Brouillon, connexion et index
possédés supprimés, objets initiaux préservés. Ni PDF hôtelier original,
ni identité refusée, ni lab complet validés; T014 reste ouvert.

La [reprise native contrôlée du 26 octobre](../assets/runtime-2026-10-26/lab5-native-denied-first-use.json)
pose une seule question de fermeture au premier usage, après authentification
neuve réelle, attente de 600 secondes et contrôle de preuve réussi.
Search direct renvoie 403; Search natif signale `ConnectorRequestFailure /
AzureAISearchClientError`, sans statut HTTP exposé, avec zéro document/citation.
Le parent demande génériquement de reformuler, sans erreur spécifique aux
permissions vérifiée. Aucun fait source n'est renvoyé dans cette unique réponse.
Ce n'est ni une acceptation native autorisée puis révoquée appariée, ni une identité
indépendante; S5-10/T014 restent ouverts. Nettoyage et inventaires initiaux sont
vérifiés indépendamment; les résultats antérieurs sont inchangés.

Le [test isolé de retrait d'autorisation](../assets/runtime-2026-10-25/lab5-isolated-permission-removal.json)
échoue à S5-10. Seul un nouveau rôle Reader de test est retiré sur un service
Search distinct sans clé. Les requêtes directes renvoient 403, mais une nouvelle
conversation native renvoie `07:00`, la vraie citation Harbor et deux documents
fictifs dans sa trace Search. Même administrateur approuvé, pas une identité
indépendante non privilégiée; principal natif effectif et cause non établis.
L'instantané officiel est récupéré après expiration de lecture sans rejouer
la question. Les deux configurations concordent et les 17 fichiers restent
inchangés. Objets possédés supprimés, originaux préservés et navigateur fermé.
Coût réel non finalisé. Le 4/4 antérieur ne devient pas une réussite d'isolation;
T014 et la feuille de route complète restent ouverts.

Le [contrôle Dataverse/History du 26 octobre](../assets/runtime-2026-10-26/lab1-dataverse-history.json)
vérifie l'accès Graph rétabli de l'administrateur approuvé, pas les droits de
transcription Dataverse. La requête de métadonnées limitée à l'agent original
renvoie 403; le nouvel audit manque encore des privilèges de lecture des
transcriptions et d'attribution des rôles. Rôles et politiques inchangés.
L'exécution History originale affiche uniquement accueil et question, In progress.
Ni rejeu, reconstruction de réponse ni auto-élévation générale; T009 reste ouvert.

La [récupération ultérieure de l'historique des licences](../assets/runtime-2026-10-25/lab1-history-citation-followup.json)
retrouve la question originale exacte, mais aucune réponse historique complète,
même après une actualisation. Un clic de citation dans un autre historique
terminé n'expose ni destination ni PDF et ne remplace pas l'audit original.
Aucune nouvelle question ni écriture de configuration; T009 reste ouvert.
L'[instantané wiki vérifié](../assets/runtime-2026-10-25/wiki-publication.json)
réussit comparaison avec la référence sans écrasement humain, publication
normale et contrôles rendus des deux langues. La destination est publique,
sa visibilité inchangée. Ces progrès ne ferment ni T016 ni les critères
restants d'acceptation et de rétention.

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

La [première tentative de matrice](../assets/runtime-2026-10-25/mcp-native-matrix-initial.json)
réussit les cas 1-4 et s'arrête aux sept puces non attribuées du cas 5. Une
correction enregistrée réussit un cas 5 frais, puis le
[SAR suivant échoue sur une notice de rendu mal attribuée](../assets/runtime-2026-10-25/mcp-native-source-boundary-failure.json).
La correction suivante supprime cette erreur, mais
[échoue sur un point ajouté dans une citation locale](../assets/runtime-2026-10-25/mcp-native-local-quote-failure.json).
Les événements génératifs de fin réels sont maintenant conservés. Deux appels
de preuves dans un tour sont comptés séparément de son unique soumission
utilisateur. Les contrôles stricts de citation sont inchangés; aucune matrice
complète après correction ne réussit encore.

La [dernière exécution complète des onze cas](../assets/runtime-2026-10-25/mcp-native-eleven-case-matrix.json)
réussit maintenant les cas d'origine sur une configuration enregistrée immuable.
Douze soumissions incluent un blocage conservé du cas 7 et une reprise distincte
après lecture exacte et reconnexion normale. Huit fins génératives réelles, trois
fins de topics déterministes, sept appels MCP réels, contribution locale prévue
et audits complets des réponses/sources sont conservés. Douze citations locales
restent exactes; les réponses MCP finales utilisent des paraphrases sans
guillemets, attribuées individuellement. T008 est clos pour cette exécution, pas la
feuille de route. Le contrôle de validation distinct produit deux réponses
identiques par topic puis action directe; sa correction T007 reste ouverte.

La [correction et régression suivantes](../assets/runtime-2026-10-25/mcp-native-control-repair-regression.json)
prouvent une invocation/liaison/réponse réelle de validation après une reprise
comptée, sans réponse codée en dur. La nouvelle régression accepte 10/11 cas.
Le cas 9 termine recherches et plan sans réponse parent; sa reprise ne produit
ni plan ni réponse. Les deux échecs restent conservés. Quinze soumissions
comprennent treize questions d'origine et deux contrôles. Les quatorze exports
disponibles du contenu agent concordent; les sept appels MCP réels incluent
la recherche réussie sans réponse finale. L'export perdu du cas 2 n'est accepté
qu'après sa reprise distincte. Le cas 7 actuel comporte deux citations MCP
exactes attribuées et un contexte local supplémentaire permis et vérifié.
Préservation finale complète et fermeture du navigateur réussissent.
T007/l'acceptation de configuration actuelle restent ouverts; l'ancien résultat
T008 ne certifie pas cette configuration.

L'[inventaire ciblé du 25 octobre](../assets/runtime-2026-10-25/owned-boundary-refresh.json)
lit six ressources ARM détenues, dont le site MCP isolé et son plan B1.
L'échec de facturation HTTP 429 est conservé avant une reprise réussie comptée.
Le coût déclaré est de 11,26126391 USD avant taxes; seuls deux identifiants ont
des lignes publiées. Ce n'est ni la dépense complète ni une facture finale,
et les crédits Copilot sont exclus. Aucune modification, inférence ou question
native. L'indisponibilité renvoyée par le formulaire n'attribue aucun responsable,
date de revue, budget chiffré ou accord de rôle. T001/T002 restent ouverts.

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
de l'état enregistré. À ce jalon antérieur, la réparation SDK locale passait
33 tests sans être déployée. T003/T004 ont ensuite déployé la réparation et
réussi 3/3 contrôles hébergés v3; la dernière v5 reste conservée sans certification
native. Le diagnostic était Inactive; les métadonnées Foundry de ce jalon
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
