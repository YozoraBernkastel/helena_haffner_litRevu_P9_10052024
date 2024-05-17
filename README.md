# helena_haffner_litRevu_P9_10052024

## Description du programme

L'environnement virtuel utilisé pour ce projet est Poetry.

Ce projet s'inscrit dans le cadre d'une formation Python et vise un site destiné à apprendre la récupération d'informations sur internet.

## Environnement Virtuel
Environnement Virtuel utilisé : Poetry

Installation:
```shell
curl -sSL https://install.python-poetry.org | python3 - 
```

Activer l'environnement virtuel : 
```shell
poetry shell
```
Installer les dépendances (les fichiers pyproject.toml ou poetry.lock doivent être présents dans le dossier et qui sont l'équivalent de requirements.txt): 
```shell
poetry install 
```
Sortir de l'environnement virtuel : 
```shell
exit
```

## Lancer le programme depuis l'environnement virtuel
Dans le terminal, à la racine du projet :
```shell
python3 main.py
```

## Lancer le programme sans l'environnement virtuel
Dans le terminal, à la racine du projet :
```shell
poetry run python3 main.py
```




