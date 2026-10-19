---
title: Publication and maintenance / Publication et maintenance
description: Validate canonical bilingual documentation and synchronize the same content to GitHub wiki.
ms.date: 2026-10-19
---

## English publication procedure

[English guide](en/index.md) | [Guide français](fr/index.md) | [Repository home](../README.md)

The canonical pages live in the repository. The wiki is a generated mirror with flat
page names, shared assets, a sidebar, and a footer. Edit the canonical guides, not the
generated wiki pages, to keep the two languages and publication surfaces consistent.

Destinations:

* [Repository](https://github.com/devopsabcs-engineering/copilot-studio)
* [GitHub wiki](https://github.com/devopsabcs-engineering/copilot-studio/wiki)

The repository was created private. GitHub CLI authentication can publish repository
and wiki commits, but the wiki must first be initialized with a page in the browser.
The owner initialized Home while signed in; that enabled its separate Git endpoint.
Do not change visibility or put an access token into a command, document, or remote URL.

### Validate the source documentation

From the repository root in PowerShell:

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts\validate_docs.py
```

The checks cover English/French page coverage, required metadata, local links,
image links, screenshot parity, provenance, and a translation-length smoke check.
They do not certify translation quality, cloud behavior, licensing compliance,
or the contents of every external reference.

The repository started empty: no existing Markdown linter, package build, or CI suite
was available. The export and checks use Python's standard library and do not require
installing the workshop notebook's dependencies.

### Export and check wiki pages

```powershell
python scripts\build_wiki.py --output .wiki-build
python scripts\validate_docs.py --wiki .wiki-build
```

The [export script](../scripts/build_wiki.py) converts local guide links into wiki page
links and copies shared assets. For example, the English Lab 1 guide becomes
`EN-lab-01`, the French guide becomes `FR-lab-01`, and the repository README becomes
`Home`. Wiki links deliberately omit the Markdown extension.

Canonical Markdown retains the required YAML metadata. GitHub wiki does not render
that frontmatter as repository Markdown does: it displays it as page content.
The generated wiki-only files therefore convert the metadata title to a visible
heading and omit the remaining frontmatter. This compatibility exception also applies
to the generated sidebar and footer; the canonical source metadata remains intact.

### Publish the same content to the wiki

Before publishing, review the destination, current remote branch, and any human edits.
For a new local wiki checkout:

```powershell
git clone https://github.com/devopsabcs-engineering/copilot-studio.wiki.git .wiki-publish
git -C .wiki-publish status --short
python scripts\build_wiki.py --output .wiki-publish
python scripts\validate_docs.py --wiki .wiki-publish
git -C .wiki-publish diff --stat
```

If the wiki checkout already exists, fetch and reconcile its current branch before
exporting. Do not overwrite unrelated human changes or use a force push. The exporter
does not delete stale or human-authored pages; review intentional removals separately.
After reviewing the generated content, stage only the intended wiki pages and assets,
create a Conventional Commit with the required attribution, and push the actual wiki
branch shown by `git branch --show-current`.

The repository and wiki have independent commit histories. Verify both remote commit
IDs after publication and open the English and French pages in the browser.
If a later wiki publication fails, the repository guides remain available.

### Maintain evidence and translations

When adding a live result, update both language guides, the evidence manifest,
and both validation ledgers. Identify the precise test, not an entire lab by implication.
Keep original screenshots outside the repository, publish only reviewed derivatives,
and distinguish historical figures from newly observed execution.

## Procédure de publication en français

Les pages de référence résident dans le dépôt. Le wiki est un miroir généré avec des
noms de pages à plat, des images partagées, une barre latérale et un pied de page.
Modifiez les guides de référence plutôt que les pages générées pour conserver la
cohérence entre langues et supports.

Destinations :

* [Dépôt](https://github.com/devopsabcs-engineering/copilot-studio)
* [Wiki GitHub](https://github.com/devopsabcs-engineering/copilot-studio/wiki)

Le dépôt a été créé privé. L'authentification GitHub CLI permet de publier les commits
du dépôt et du wiki, mais une première page doit être créée dans le navigateur pour
initialiser le wiki. Le propriétaire a initialisé Home après connexion, ce qui a rendu
son point d'accès Git distinct disponible. Ne changez pas la visibilité et ne placez
jamais de jeton dans une commande, un document ou l'URL d'un dépôt distant.

### Vérifier la documentation de référence

Depuis la racine du dépôt dans PowerShell :

```powershell
python -m unittest discover -s scripts -p "test_*.py" -v
python scripts\validate_docs.py
```

Les contrôles vérifient la couverture français/anglais, les métadonnées requises,
les liens locaux, les images, la parité des captures, la provenance et la longueur
relative des traductions. Ils ne certifient ni la qualité linguistique, ni l'exécution
cloud, ni la conformité des licences, ni chaque référence externe.

Le dépôt était vide : aucun linter Markdown, build de paquet ou suite CI préexistante
n'était disponible. L'export et les vérifications emploient la bibliothèque standard
de Python et n'exigent pas l'installation des dépendances du notebook d'atelier.

### Exporter et vérifier les pages du wiki

```powershell
python scripts\build_wiki.py --output .wiki-build
python scripts\validate_docs.py --wiki .wiki-build
```

Le [script d'export](../scripts/build_wiki.py) transforme les liens locaux en liens de
pages wiki et copie les images partagées. Le guide anglais du lab 1 devient
`EN-lab-01`, son équivalent français `FR-lab-01`, et l'accueil du dépôt devient `Home`.
Les liens wiki omettent volontairement l'extension Markdown.

Les sources Markdown conservent les métadonnées YAML requises. Le wiki GitHub ne les
interprète pas comme le dépôt : il les affiche dans le contenu. Les fichiers générés
pour le wiki convertissent donc le titre en en-tête visible et omettent les autres
métadonnées. Cette exception de compatibilité concerne aussi la barre latérale et
le pied de page générés ; les sources de référence restent intactes.

### Publier le même contenu sur le wiki

Avant publication, vérifiez la destination, la branche distante et les modifications
humaines éventuelles. Pour un nouveau clone local du wiki :

```powershell
git clone https://github.com/devopsabcs-engineering/copilot-studio.wiki.git .wiki-publish
git -C .wiki-publish status --short
python scripts\build_wiki.py --output .wiki-publish
python scripts\validate_docs.py --wiki .wiki-publish
git -C .wiki-publish diff --stat
```

Si le clone existe déjà, récupérez et réconciliez sa branche avant l'export.
N'écrasez pas les modifications humaines sans rapport et ne forcez pas l'envoi.
L'exporteur ne supprime pas les anciennes pages ou celles ajoutées manuellement ;
examinez séparément toute suppression voulue. Après revue, indexez uniquement les
pages et images prévues, créez un commit conventionnel avec l'attribution requise,
puis publiez la branche réelle affichée par `git branch --show-current`.

Le dépôt et le wiki ont des historiques indépendants. Vérifiez leurs deux identifiants
de commits distants et ouvrez les pages françaises et anglaises dans le navigateur.
Si une publication ultérieure du wiki échoue, les guides du dépôt restent disponibles.

### Maintenir les preuves et les traductions

Pour chaque nouveau résultat réel, mettez à jour les deux guides, le manifeste
d'images et les deux registres de validation. Identifiez le test précis sans laisser
entendre que tout le lab est validé. Conservez les originaux hors du dépôt, publiez
uniquement des versions dérivées revues et distinguez les figures historiques des
exécutions nouvellement observées.
