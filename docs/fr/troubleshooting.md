---
title: Dépannage et reprise sûre
description: Diagnostiquer les problèmes d'environnement, connaissances, connecteurs, recherche, modèles et télémétrie sans contourner les protections.
ms.date: 2026-10-19
---

## Commencer par la frontière en échec

[Tous les labs](index.md) | [English](../en/troubleshooting.md)

Notez l'identifiant du lab et du test, l'erreur exacte, l'horodatage, l'environnement,
le moteur et la dernière étape réussie. Ne relancez pas tout le lab si un test direct
du composant permet d'isoler la panne. N'incluez ni identifiants secrets ni conversations
clients brutes dans une demande de support ou une capture.

## Environnement et licences

| Symptôme                                          | Vérification                                                      | Action sûre                                                                               |
| ------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| Agent absent de l'accueil                         | Environnement, compte, moteur et filtres                          | Ouvrir Agents ou l'expérience standard avant toute recréation                             |
| Absence de crédits Copilot                        | Affectation à l'environnement, droits et stratégie de facturation | Faire vérifier la capacité ; ne pas supposer un provisionnement encore en cours           |
| Prompt ou connecteur indisponible                 | Stratégies effectives, paramètres et moteur choisi                | Utiliser une configuration approuvée, sans changer de compte pour contourner la stratégie |
| Agent existant fonctionnel, nouvel agent en échec | Moteur, modèle, instructions ou identité de connexion différents  | Comparer la configuration consignée sans modifier des paramètres sans rapport             |
| Portail Azure accessible mais données refusées    | Rôle de gestion et rôle d'accès aux données                       | Faire attribuer uniquement le droit nécessaire par un administrateur habilité             |

Consultez le [lab 0](lab-00.md) et les [changements de plateforme](platform-changes.md).

## Connaissances et courriel

Si un fichier reste indisponible, vérifiez la recherche Dataverse, la capacité, le
format, la taille et le chiffrement. Un document Word protégé que vous pouvez ouvrir
n'est pas automatiquement une source de connaissances importable. Ne retirez jamais
sa protection pour réussir l'importation.

Si les réponses ne sont pas fondées, démarrez une nouvelle conversation, vérifiez
l'édition active, désactivez les sources sans rapport pour le test contrôlé et examinez
la recherche visible. Une réponse plausible ne prouve pas la consultation de la source.

Si un courriel manque :

1. Vérifiez la boîte d'envoi réelle de la connexion.
2. Examinez le résultat de l'outil, pas seulement le texte de l'agent.
3. Vérifiez les Éléments envoyés et le destinataire exact.
4. Contrôlez la boîte de réception, le courrier indésirable et, si autorisé, le suivi des messages.
5. Recherchez les doublons avant de recommencer. N'envoyez pas en boucle pour tester la réception.

## Search et vectorisation

Testez dans cet ordre : accès autorisé au blob, inférence du modèle, exécution de
l'indexeur, requête Search directe, puis Copilot Studio. En cas d'échec de l'indexeur,
consultez l'erreur par document et l'identité employée. Le fait qu'un créateur puisse
télécharger le blob ne prouve pas que le service Search peut le lire.

Si la recherche vectorielle est vide, comparez :

* Le modèle d'embedding et le nom de déploiement
* Les dimensions de l'index et celles de la sortie du modèle
* Les champs recherchables ou récupérables et ceux sélectionnés par le connecteur
* La configuration sémantique, le type de requête, le filtre et l'index choisi
* La disponibilité du modèle et du point de terminaison ainsi que la version d'API

Un connecteur qui attend `chunk` ne peut pas exploiter `content` sans correspondance
réelle. Inspectez la sortie avant de définir le schéma d'analyse. Conservez les titres
et métadonnées de citation ; ne concaténez pas silencieusement des résultats vides.

## Application Insights

Vérifiez la ressource cible, la configuration prise en charge de la chaîne de connexion,
les options de journalisation, la plage horaire UTC et le schéma réel des tables et
événements. Prévoyez le délai d'ingestion. Une vue Live Metrics vide ne prouve pas
l'échec d'ingestion des événements personnalisés. Interrogez les journaux et corrélez
le marqueur du lab.

Utilisez un événement émis volontairement pour le test. Une requête portant sur un
nom jamais émis ne démontre pas une panne. Laissez désactivée la journalisation des
activités sensibles sauf si un test approuvé l'exige.

## BYOM et Foundry IQ

Vérifiez directement le modèle ou l'agent Foundry avant l'intégration à Copilot.
Distinguez noms de déploiement et de modèle, identifiants classiques et noms/versions
des nouveaux agents. Vérifiez locataire, droits, format du point de terminaison,
prise en charge du connecteur, version d'API en préversion et versions réelles des dépendances.

Pour le lab 6, examinez les références aux données locales du notebook avant d'exécuter
les cellules cloud. S'il manque des données ou un fichier de configuration requis,
indiquez **bloqué** au lieu de remplacer le résultat par une réponse générique et
d'annoncer la réussite.

## Produire un rapport d'échec utile

```text
Identifiant du lab et du test :
Résultat attendu :
Erreur observée et horodatage UTC :
Dernier test direct de composant réussi :
Environnement/moteur/modèle/version d'API (registre privé) :
Capture masquée ou erreur structurée :
Impact et condition d'arrêt :
Prochaine action autorisée la plus ciblée :
```

## Nettoyer sans effet sur les autres usages

Déconnectez les connexions inutilisées, restaurez la configuration initiale de l'agent
si nécessaire et supprimez uniquement les objets dédiés que vous avez créés pour
l'atelier. Examinez le contenu et les dépendances d'un groupe de ressources avant
d'en approuver la suppression. Ne supprimez pas de ressources Foundry, Search,
Storage, Log Analytics ou réseau partagées. Conservez les preuves masquées et le
registre d'acceptation après le nettoyage.
