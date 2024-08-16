# helena_haffner_litRevu_P9_10052024

## Description du programme
Ce projet s'inscrit dans le cadre d'une formation Python et vise un site destiné à apprendre la récupération d'informations sur internet.

Ce projet est un site web Django. Sur ce site, un utilisateur peut créer son compte, se connecter et se déconnecter, 
faire des demandes de critiques de livres ou articles précis et 
écrire une critique. Un utilisateur peut également s'abonner à un autre utilisateur. Dans ce cas, le contenu de ce dernier sera ajouté à son flux.

La base de données db.sqlite3 est présente dans le répertoire, tout comme les images utilisées pour les quelques tickets qui alimentent déjà celle-ci.

Pour lancer le site, il faut d'abord installer l'environnement virtuel.

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


## Installer la base de données
Une fois l'environnement virtuel lancé, utilisez dans le terminal la commande:
```shell
python manage.py migrate
```
## Lancer le serveur en local

Toujours dans l'environnement virtuel, et une fois la base de données configurée, dans le terminal, entrez la commande:
```shell
python manage.py runserver
```

## Se connecter au site 

Une fois le serveur lancé en local, vous pouvez vous consulter le site depuis le navigateur en allant à l'adresse suivante:
[http://localhost:8000/](http://localhost:8000/)

Vous pourrez alors soit créer un nouveau compte, soit utiliser l'un des trois déjà existants:

- _Compte Super Utilisateur:_ 


        login: admin 
        mot de passe: admin

- _Premier Compte Utilisateur:_


        login: shikabane
        mot de passe: shi12345

- _Second Compte Utilisateur:_


        login: Lain
        mot de passe: iwa12345

- _Troisième Compte Utilisateur (aucun contenu créé et aucun abonnement):_


        login: Sunako
        mot de passe: suna12345
