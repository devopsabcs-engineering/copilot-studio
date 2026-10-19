---
title: Registre de réexécution réelle - 2026-10-19
description: Recherche PDF et livraison de courriel réellement testées, plan Terraform exécuté, échec SDK reproduit, restauration isolée et conditions cloud restantes.
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
La gestion d'un destinataire ambigu et la simulation d'une panne de connexion
n'ont **pas été exécutées** ; elles restent des cas complémentaires du
[guide du Lab 1](lab-01.md).
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
