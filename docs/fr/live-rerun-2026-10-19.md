---
title: Registre de réexécution réelle - 2026-10-19
description: Initialisation, validation et plan Terraform exécutés, échec SDK reproduit, restauration isolée des dépendances et conditions restantes.
ms.date: 2026-10-19
---

## Périmètre et résultat actuel

[Tous les labs](index.md) | [English](../en/live-rerun-2026-10-19.md) | [Registre de validation](validation.md)

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

L'inventaire de cet abonnement ne retournait toujours aucun service Azure AI Search
ni composant Application Insights. Les applications existantes sans rapport avec
l'atelier n'ont pas été modifiées. L'inventaire réel des modèles dans eastus2 indiquait
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

L'agent de test a reçu la consigne d'actualiser cette nouvelle page directe et
d'utiliser les outils enregistrés plutôt que l'ancien accueil vide. Un nouveau
résultat réel sera consigné uniquement après l'exécution effective du test.

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

Les trois jeux de données intégrés ont aussi été évalués localement sans exécution
des cellules cloud. Ils contiennent chacun huit enregistrements, soit **24 au total**.
Chaque enregistrement possède des chaînes `id`, `title` et `content` non vides, avec
des identifiants uniques dans chaque jeu. Le contenu protégé lui-même n'est pas republié.

## Conditions d'exécution restantes

Aucune ressource facturable n'a été créée ou appliquée. Les demandes de budget
n'ont reçu aucune réponse humaine ; une réponse automatique d'indisponibilité
n'est pas interprétée comme une approbation. L'outil de prix n'a retourné aucun tarif
pour les requêtes de niveaux Search tentées. Aucun tarif ni plafond garanti n'est donc supposé.

La suite exige un périmètre dédié, un seuil de dépenses approuvé, une décision de
nettoyage et la confirmation des modèles et régions, puis les tests réels d'indexation,
recherche, télémétrie, prompt et agent connecté. Le lab 1 peut avancer indépendamment
avec l'agent et les connexions déjà enregistrés.

## Éléments restés intacts

Les documents Word, le notebook et les sources Terraform d'origine sont inchangés.
Les ressources de production ou d'autres usages n'ont pas été modifiées. Les preuves
initiales d'envoi et de réception du lab 1 restent des preuves historiques utilisateur,
distinctes de tout nouveau test exécuté par l'assistant.
