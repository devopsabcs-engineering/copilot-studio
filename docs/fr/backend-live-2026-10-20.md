---
title: Validation du backend Copilot et du CLI - 2026-10-20
description: Lectures Dataverse authentifiées, restauration officielle de PAC, clone de l'agent sauvegardé et blocages de conversation et d'évaluation restants.
ms.date: 2026-10-20
---

## Résultat et limites

[Tous les labs](index.md) | [English](../en/backend-live-2026-10-20.md) | [Registre réel](live-rerun-2026-10-19.md)

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

## Références officielles

* [Installation PAC](https://learn.microsoft.com/en-us/power-platform/developer/howto/install-cli-net-tool)
* [Authentification PAC](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)
* [Commandes PAC Copilot](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot)
* [Commandes d'évaluation PAC Copilot Studio](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot-studio)
* [Référence des permissions API Power Platform](https://learn.microsoft.com/en-us/power-platform/admin/programmability-permission-reference)
* [Extension Microsoft Power Platform VS Code](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.powerplatform-vscode)
