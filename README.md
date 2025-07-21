# Fresqu'AéroMaps

Ce repository héberge un outil de simulation basé sur **AéroMAPS** ([Site Web](https://aeromaps.isae-supaero.fr/)).

Le projet contenu dans ce repository intervient dans le cadre de la **Fresqu'Aéro**, un atelier de sensibilisation à l'environnement dans le secteur aéronautique inspiré de la fresque du climat.

Ce projet implémente de manière interactive des simulations de l'évolution du transport Aérien jusqu'en 20250 au moyen de cartes solutions, choisies lors de la réalisation de l'activité. Ce projet permet de conclure l'atelier **Fresqu'Aéro**.

## Guide d'installation

Afin de pouvoir facilement installer, modifier et utiliser l'application **Fresqu'AéroMAPS** sur votre machine, il est fortement recommandé d'utiliser un environnement virtuel Python.

Vous trouverez ci-dessous une procédure d'installation simple, organisée par étapes :

1. Cloner ce dépôt GitHub :
    - `git clone https://github.com/tominien/Fresqu-aeromaps.git`
    - `cd Fresqu-aeromaps`
2. Installer les outils de compilation et les headers Python :
    - `sudo apt update`
    - `sudo apt install build-essential python3.12-dev`
3. Créer un environnement virtuel :
    - `python3.12 -m venv .venv`
    - `source .venv/bin/activate`
4. Installer les dépendances du projet :
    - `pip install --upgrade pip setuptools wheel`
    - `pip install -r requirements.txt`
5. Créer le fichier d'environnement :
    - Créer le fichier `.env` à la racine du projet.
    - Copier le contenu du template de fichier d'environnement donné dans la section en bas de fichier.

## Guide de lancement EN LOCAL

L'application **Fresqu'AéroMAPS** possède deux interfaces, une version "web" et une version "Jupyter Notebook".
Vous trouverez ci-dessus un tutoriel de lancement en local pour chaque version.

Tutoriel de lancement de la version "web" :

- Via le `Dockerfile`, version utilisée par [Render](https://render.com) **[VERSION RECOMMANDÉE]** :
    - `docker build -t fresque-aeromaps .` *Cette commande est un peu longue à s'exécuter, il y en aura pour environ 15 minutes.*
    - `docker run --rm -p 8888:8888 fresque-aeromaps`
- Via le fichier racine `app.py` :
    - `panel serve app.py --address=0.0.0.0 --port=8888 --allow-websocket-origin="*" --prefix="" --index="app" --log-level='error'`
- L'application sera alors accessible à l'adresse http://localhost:8888 (et http://localhost:8888/app).

Tutoriel de lancement de la version "Jupyter Notebook" :

- Via le fichier racine `app.ipynb` :
    - `jupyter notebook app.ipynb` *Si vous utilisez Visual Studio Code, veillez bien à choisir le Kernel correspondant à l'environnement `.venv` en haut à droite du notebook.*

## Guide de lancement EN LIGNE

L'application **Fresqu'AéroMAPS** est hébergée en ligne sur 2 sites.

1. Sur [render.com](https://render.com), via l'adresse suivante : https://tominien.onrender.com.
    - Le temps de chargement initial et de mise à jour de l'application peut être un peu long.
2. Sur [binder.org](https://mybinder.org), en cliquant sur le bouton suivant : [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/tominien/Fresqu-aeromaps/HEAD?urlpath=%2Fdoc%2Ftree%2Fapp.ipynb)
    - Cette version est plus rapide que celle hébergée sur Render, mais elle est moins intuitive.

## Template du fichier d'environnement

Afin que Python "reconnaisse" bien le dossier `src/` du projet comme étant celui contenant tout le code source, il est fortement recommandé de créer un fichier `.env`, avec le contenu suivant à la racine du projet :
```
PYTHONPATH=./src
```
