# Utilitaire Corpus

Utilitaires pour gérer les corpus CollabScore.

## Le script corpus_utils

Le script permet de produire un un fichier descriptif JSON à partir de méta-données
contenues dans un fichier MEI.


### Installation

Recommandé: installer un environnement virtuel au moins 
Python 3.7 et installer les dépendances:

```
pip3 install -r requirements.txt
```

Tester l'exécution de base:

```
python3 corpus_utils.py -h
```

On obtient la liste des options.

### Le dossier ``mei`` 

Contient les fichiers MEI à traiter. Il y aau moins un exemple: ``Brahms.mei``.

## Le dossier  ``json`` 

Les fichiers json y  sont placés après extraction.

### Extraire des métadonnées d'un fichier MEI

On donne le nom du fichier MEI (qui doit être dans le dossier ``mei``) 
et on obtient si tout se passe bien un fichier de même nom mais
avec l'extension ``json``  dans le dossier ``json``. 

La commande suivante devrait produire un fichier ``Brahms.json`` dans ``json``. 
```
python3 corpus_utils.py -f Brahms.mei -a extract
```

