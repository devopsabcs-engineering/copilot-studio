---
title: "Lab 03 : Superviser un agent avec Application Insights"
description: "Configurer la télémétrie d’un agent, examiner les propriétés d’un événement avec KQL et distinguer revue documentaire et preuve d’exécution."
ms.date: 2026-10-19
ms.topic: tutorial
---

## Lab 03 : Superviser un agent avec Application Insights

[Index de l’atelier](index.md) | [English](../en/lab-03.md) | [Précédent : Search](lab-02.md) | [Suite : BYOM](lab-04.md)

Collectez la télémétrie d’un agent dans Azure Monitor Application Insights, puis
vérifiez un événement synthétique sans collecter le contenu des conversations.
Prévoyez environ 60 minutes, hors autorisations et délai d’ingestion.

> [!IMPORTANT]
> Statut : **Monitor natif inspecté réellement ; parcours Application Insights/KQL bloqué**.
> Le Monitor connecté n'affichait aucune donnée du 13 au 19 octobre et limitait
> l'accès aux transcriptions. Preview History exposait indépendamment les activités
> antérieures d'annuaire, d'envoi et de recherche échouée, sans les réexécuter.
> Le menu classique existe, mais sa destination n'a pas chargé pendant l'inspection.
> Les sept ressources Application Insights sans rapport sont restées intactes.
> Aucun réglage de télémétrie, émission d'événement ou appel KQL n'a été exécuté.
> Consultez les [résultats et captures réels](live-rerun-2026-10-19.md).

### Exercice d'observation dans l'expérience actuelle

1. Sur l'agent existant, choisissez **Monitor** dans Build/Preview/Evaluate/Monitor.
2. Consignez les dates et la présence réelle de données. La période observée était
   **Last 7 days, 10/13/26-10/19/26**, soit du 13 au 19 octobre.
3. Ouvrez **Sessions > See all**. L'identité courante voyait zéro ligne et une
   restriction d'accès aux transcriptions. N'augmentez pas les droits et ne publiez
   pas simplement pour supprimer ce bandeau.
4. Inspectez la conversation déjà enregistrée par **Preview > History**.
   Les activités d'annuaire, d'envoi et d'annuaire échoué duraient **2,73 s,
   1,63 s et 4,62 s**. Ne renvoyez pas le courriel pour obtenir une preuve de supervision.
5. Séparez Monitor/History de la procédure Azure ci-dessous. Un agrégat vide ne
   prouve ni consommation nulle ni taux de réussite réel nul.

L'en-tête Monitor affichait zéro session, durée moyenne nulle, 0 % de réussite
et zéro crédit avec **No data yet**. La conversation History indiquait séparément
**90,33 crédits estimés**. Ces portées diffèrent ; il ne faut ni inventer une
facturation ni déclarer gratuite l'exécution de l'agent.

### Objectifs et prérequis

* Connecter un agent de développement à Application Insights lié à un espace de travail.
* Émettre un événement inoffensif avec un identifiant de cas reproductible.
* Interroger la table adaptée à la portée de télémétrie sélectionnée.
* Séparer l’activité du volet de test de celle des canaux publiés.
* Expliquer pourquoi un tableau de bord, un résultat vide ou un décompte
  d’utilisateurs ne prouve pas la qualité des réponses.

Vous avez besoin d’un accès créateur à une copie jetable de l’agent du Lab 01
ou 02, d’un abonnement approuvé, des droits de configuration d’Application
Insights et de son espace Log Analytics, ainsi que des droits de lecture des
journaux. Faites approuver coût, conservation, résidence des données et accès
avant toute collecte. Utilisez seulement des entrées fictives.

Ouvrez un agent utilisant le **moteur standard** par **… > Open classic
experience** ou la liste des agents existants. Ce changement d’interface ne
modifie pas l’orchestration : le moteur standard accepte l’orchestration
classique ou générative. Ces réglages de télémétrie par agent ne constituent
pas une procédure pour le moteur GitHub Copilot. Consultez les
[moteurs d’exécution][harness] et l’[accès aux agents standard][experience].

### Numérotation corrigée et approche actuelle

Le titre interne de la source de supervision indique « Lab 4 ». Il s’agit du
Lab 03 dans cet atelier, conformément à l’ordre des fichiers. BYOM est le Lab 04.

* Remplacez « clé d’instrumentation ou chaîne de connexion » par le champ
  **Connection string** de **Settings > Advanced > Application Insights**.
  L’introduction de l’article actuel mentionne encore la clé, mais ses étapes
  numérotées demandent explicitement la chaîne de connexion.
* Utilisez Application Insights lié à un espace Log Analytics approuvé. Créer un
  nouvel espace peut ajouter des frais et des obligations de gouvernance.
* Retrouvez les réglages **Enable logging**, **Log conversation details**,
  **Log sensitive Activity properties** et **Node execution events** disponibles
  dans le tenant. Les anciennes captures peuvent afficher **Log Activity** ou
  **Log node tools**.
* Gardez les détails de conversation et les propriétés sensibles désactivés.
  Identifiants, noms, messages et arguments d’outils peuvent contenir des données personnelles.
* Gardez le classeur **Copilot Studio Dashboard** facultatif. La vue est documentée
  en préversion ; sa présence dans la galerie n’est pas un critère de réussite.
* Distinguez événements par agent et traces OpenTelemetry au niveau de
  l’environnement. La [vue d’ensemble de la télémétrie][overview] indique
  `customEvents` pour les premiers et `dependencies` pour les secondes.

### Exercice 1 : Préparer Application Insights

1. Exportez la copie jetable de l’agent ou réalisez une sauvegarde approuvée.
   Consignez sa configuration de télémétrie sans placer de secrets dans le dépôt.
2. Dans Azure portal, cherchez une ressource Application Insights approuvée et
   liée à un espace de travail. À défaut, obtenez l’accord avant **Create a
   resource > Application Insights**.
3. Choisissez l’abonnement, le groupe et la région autorisés. Sélectionnez
   l’espace Log Analytics prévu ou un nouvel espace explicitement approuvé.
4. Vérifiez coût d’ingestion/conservation, droits et réseau. Ne modifiez pas la
   conservation d’un espace partagé pour terminer cet exercice.
5. Après création, ouvrez la vue d’ensemble et repérez **Connection string**.
   Transférez-la directement dans le champ approuvé de l’exercice 2, sans la
   faire apparaître dans une capture ou une note partagée.
6. Ouvrez **Logs** depuis la ressource Application Insights. Confirmez votre accès
   et déterminez si l’éditeur est limité à cette ressource ou à l’espace de
   travail. Consignez la portée sans divulguer son identifiant privé.

![Écran d’origine de création d’Application Insights](../assets/lab-03/image1.png)

*Capture de l’atelier d’origine, pas d’une nouvelle exécution. Original workshop
screenshot, not a new execution. La création exige une autorisation ; adaptez
l’espace de travail et la région aux règles de votre organisation.*

### Exercice 2 : Configurer la collecte sur l’agent

1. Dans l’agent standard, ouvrez **Settings > Advanced > Application Insights**.
2. Saisissez la chaîne de connexion complète, pas seulement la clé d’instrumentation.
3. Activez **Enable logging**. Laissez **Log conversation details** et **Log
   sensitive Activity properties** désactivés.
4. Activez **Node execution events** seulement si le test contrôlé le nécessite.
   Conservez la valeur initiale pour le retour arrière.
5. Enregistrez et ouvrez une nouvelle conversation de test. Les tests dans
   Copilot Studio peuvent produire de la télémétrie sans publication. Publier
   ou tester un canal réel exige une autorisation distincte et ne fait pas
   partie de cette revue.

![Réglages d’origine de la télémétrie de l’agent](../assets/lab-03/image4.png)

*Capture de l’atelier d’origine, pas d’une nouvelle exécution. Original workshop
screenshot, not a new execution. La configuration actuelle utilise une chaîne
de connexion et peut présenter d’autres libellés.*

### Exercice 3 : Ajouter un événement contrôlé

1. Dans la copie jetable, créez une rubrique nommée `Workshop telemetry check`.
2. En orchestration classique, ajoutez l’expression de déclenchement `run
   workshop telemetry check`. En orchestration générative, décrivez précisément
   la rubrique pour la limiter à une demande explicite de ce contrôle. Ne
   changez pas le mode d’orchestration pour reproduire une capture.
3. Ajoutez le nœud **Log custom event** depuis le menu des nœuds. Si le tenant
   ne le propose pas, consignez cette limite sans le remplacer par un connecteur
   sans rapport ou une requête externe.
4. Nommez l’événement `WorkshopTelemetryCheck`. Fournissez cet enregistrement
   de propriétés synthétiques dans l’éditeur de formules si nécessaire :

   ```powerfx
   {
       WorkshopId: "cs-lab-03",
       EnvironmentName: "Workshop",
       TopicName: "TelemetryCheck",
       TestCaseId: "MON-01"
   }
   ```

5. Ajoutez ensuite un message contenant exactement `Telemetry check requested.`
6. Terminez la rubrique et enregistrez. Déclenchez-la une fois dans une nouvelle
   conversation, suivez son parcours et relevez l’heure UTC.
7. N’insérez ni message utilisateur, rôle, nom, adresse électronique, clé ou
   extrait du guide. `EnvironmentName` est une étiquette de test choisie, pas
   une affirmation sur le stade de déploiement réel.

![Écran d’origine de création de l’événement](../assets/lab-03/image5.png)

*Capture de l’atelier d’origine, pas d’une nouvelle exécution. Original workshop
screenshot, not a new execution. Le nouvel événement utilise des propriétés
fictives et un marqueur d’atelier distinct.*

### Exercice 4 : Examiner les événements avec KQL

Attendez l’ingestion, puis exécutez la requête de découverte depuis **Application
Insights > Logs**. Commencez sans filtre sur un nom supposé : un nœud personnalisé
peut apparaître dans une enveloppe de plateforme telle que `OnLogEvent`, au lieu
du libellé que vous avez choisi.

```kusto
customEvents
| where timestamp > ago(1h)
| project timestamp, name, customDimensions
| order by timestamp desc
| take 50
```

Repérez l’événement proche de l’heure UTC enregistrée et développez
`customDimensions`. Déterminez le libellé et la structure réellement observés.
Si les propriétés du nœud sont des dimensions de premier niveau :

```kusto
customEvents
| where timestamp > ago(1h)
| where tostring(customDimensions.WorkshopId) == "cs-lab-03"
| project timestamp, name,
    TestCaseId=tostring(customDimensions.TestCaseId),
    TopicName=tostring(customDimensions.TopicName),
    DesignMode=tostring(customDimensions.designMode)
| order by timestamp desc
```

Si les propriétés sont imbriquées, adaptez le chemin à la structure observée.
Un résultat vide avec ce filtre pratique ne prouve pas l’absence d’émission.
Ne présentez pas une structure fixe comme validée sans l’avoir capturée.

À la portée **Log Analytics workspace**, les événements Application Insights
utilisent `AppEvents` et les colonnes `TimeGenerated`, `Name` et `Properties`.
Utilisez cette requête plutôt que de remplacer uniquement le nom de table :

```kusto
AppEvents
| where TimeGenerated > ago(1h)
| project TimeGenerated, Name, Properties
| order by TimeGenerated desc
| take 50
```

Si plusieurs applications partagent l’espace, ajoutez le filtre de ressource de
l’application approuvée avant d’interpréter les résultats. N’exportez pas les
lignes d’autres applications. La [référence AppEvents][appevents] confirme
ces colonnes.

Pour exclure les événements du volet de test à la portée Application Insights :

```kusto
customEvents
| where timestamp > ago(1d)
| where tostring(customDimensions.designMode) == "False"
| summarize EventCount=count() by bin(timestamp, 1h)
```

Cette dernière requête peut légitimement ne rien retourner si seul le volet de
test a été utilisé. Elle compte des lignes d’événements, pas des conversations,
des personnes ou des exécutions corrigées de l’échantillonnage. Un `user_Id`
anonyme ne mesure pas fidèlement des personnes distinctes.

### Exercice 5 : Explorer le classeur facultatif

1. Dans Application Insights, ouvrez **Monitoring > Workbooks**.
2. Si la galerie le propose, ouvrez **Copilot Studio Dashboard**.
3. Sélectionnez la bonne ressource et la période. Déterminez si les données de
   test sont incluses avant d’interpréter les graphiques.
4. Examinez rubriques et outils, sans déduire la présence de durées de requêtes
   ou d’exceptions d’un onglet visible. Les requêtes `requests` et `exceptions`
   de la source exigent des événements et dimensions correspondants réels.
5. Enregistrez une copie seulement si vous y êtes autorisé. Ne créez pas d’action
   d’alerte et n’envoyez pas de courrier électronique.

![Schéma d’origine du flux de télémétrie](../assets/lab-03/image11.png)

*Capture de l’atelier d’origine, pas d’une nouvelle exécution. Original workshop
screenshot, not a new execution. Le schéma illustre le concept et ne prouve pas
qu’un flux a fonctionné dans le tenant examiné.*

### Plan de validation et résultats attendus précis

* `MON-01` : Déclenchez la rubrique une fois. Résultat attendu : message exact
  `Telemetry check requested.` et trace atteignant le nœud d’événement.
  Cela prouve le passage dans la branche, pas la réussite de l’ingestion.
* `MON-02` : Exécutez la découverte à la portée de la ressource. Résultat attendu :
  au moins un événement correspondant à l’heure et au marqueur après ingestion.
  Relevez enveloppe, dimensions et heure UTC. N’exigez pas une ligne unique :
  livraison et reprises peuvent modifier le nombre de lignes.
* `MON-03` : Développez l’événement. Résultat attendu : identifiant `MON-01` et
  rubrique `TelemetryCheck` dans les propriétés configurées. Notez les
  éventuels niveaux d’imbrication avant d’adapter la requête filtrée.
* `MON-04` : Appliquez le filtre des canaux publiés après une activité limitée
  au volet de test. Résultat attendu : exclusion des événements de test, pas
  présence nécessaire de trafic publié.
* `MON-05` : Examinez le contenu avec les options sensibles désactivées. Résultat
  attendu : aucun message ou identifiant personnel ajouté délibérément dans cet
  enregistrement personnalisé. Si des données sensibles apparaissent ailleurs,
  arrêtez l’export et signalez-les. Un réglage désactivé ne prouve pas que tous
  les champs de plateforme sont anonymes.

### Dépannage

* Si aucun événement n’apparaît, vérifiez portée, période, chaîne enregistrée,
  collecte activée, passage dans la rubrique, délai et plafonds d’ingestion.
* Si `customEvents` manque, vérifiez si la portée impose `AppEvents`, ou si vous
  examinez la télémétrie de l’environnement. N’interchangez pas les schémas
  d’événements et de dépendances.
* Si une propriété est vide, examinez l’objet dynamique brut avant conversion.
  Nom et casse comptent ; une chaîne vide peut masquer un chemin incorrect.
* En cas de refus d’accès, demandez les droits appropriés sur les journaux ou
  l’espace de travail. Le rôle créateur Copilot Studio ne les donne pas.
* Si Live Metrics ou Performance reste vide, utilisez Logs comme vérification
  principale. Des événements personnalisés standard n’impliquent ni diffusion
  Live Metrics ni instrumentation automatique des requêtes et exceptions.
* Si le classeur manque, consignez « préversion facultative indisponible » et
  continuez avec les requêtes.

### Retour arrière, nettoyage et preuves

1. Rétablissez la connexion et les options initiales de l’agent. Retirez la
   rubrique jetable ou restaurez la solution sauvegardée.
2. Supprimez uniquement les classeurs et autorisations d’atelier approuvés.
   Préservez toute ressource Application Insights ou tout espace partagé.
3. Faites autoriser la suppression des ressources dédiées. Retirer une connexion
   n’efface pas les événements déjà ingérés.
4. Appliquez les règles de conservation et d’incident aux données sensibles
   accidentelles. Ne promettez pas que supprimer l’agent efface Azure Monitor.
5. Conservez configuration expurgée, heure UTC, parcours, requêtes, structure
   observée et résultat du nettoyage. Les cas d’exécution restent **Non exécuté**
   tant qu’ils n’ont pas été réalisés.

La configuration et les schémas officiels ont été vérifiés sur documentation
uniquement. Enregistrement de connexion, disponibilité du nœud, livraison,
structure réelle des propriétés, classeur et retour arrière n’ont pas été testés.
Il faut une page de création d’agent fonctionnelle avec les droits de créateur,
une paire Application Insights/Log Analytics approuvée, une ingestion autorisée
et les droits de lecture pour lever le blocage. L’authentification n’est plus le
blocage observé.

### Références officielles vérifiées

Ces pages Microsoft Learn ont été consultées le 2026-10-19.

* [Configuration par agent et requêtes Application Insights][telemetry]
* [Portées de télémétrie et tables correspondantes][overview]
* [Créer Application Insights lié à un espace de travail][workspace]
* [Table AppEvents et colonnes][appevents]
* [Moteurs d’exécution de Copilot Studio][harness]
* [Accès aux agents standard][experience]

[telemetry]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/advanced-bot-framework-composer-capture-telemetry
[overview]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/telemetry-overview
[workspace]: https://learn.microsoft.com/en-us/azure/azure-monitor/app/create-workspace-resource
[appevents]: https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/appevents
[harness]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/harnesses-overview
[experience]: https://learn.microsoft.com/en-us/microsoft-copilot-studio/agents-experience/switch-experiences
