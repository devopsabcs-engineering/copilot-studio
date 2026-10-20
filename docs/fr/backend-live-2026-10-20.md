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
| Découverte des jeux d'évaluation maker | HTTP 403 : appelant non autorisé | Aucune exécution d'évaluation démarrée |

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

## Références officielles

* [Installation PAC](https://learn.microsoft.com/en-us/power-platform/developer/howto/install-cli-net-tool)
* [Authentification PAC](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/auth)
* [Commandes PAC Copilot](https://learn.microsoft.com/en-us/power-platform/developer/cli/reference/copilot)
* [Extension Microsoft Power Platform VS Code](https://marketplace.visualstudio.com/items?itemName=microsoft-IsvExpTools.powerplatform-vscode)
