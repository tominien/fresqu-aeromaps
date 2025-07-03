# Fresqu'AéroMaps

Ce repository héberge un outil de simulation basé sur **AéroMAPS** ([Site Web](https://aeromaps.isae-supaero.fr/)).

Le projet contenu dans ce repository intervient dans le cadre de la **Fresqu'Aéro**, un atelier de sensibilisation à l'environnement dans le secteur aéronautique inspiré de la fresque du climat.

Ce projet implémente de manière interactive des simulations de l'évolution du transport Aérien jusqu'en 20250 au moyen de cartes solutions, choisies lors de la réalisation de l'activité. Ce projet permet de conclure l'atelier **Fresqu'Aéro**.

## Guide d'installation

Afin de pouvoir facilement installer, compiler, modifier et utiliser le Jupyter Notebook `main.ipynb` sur votre machine, il est fortement recommandé d'utiliser un environnement virtuel Python.

Vous trouverez ci-dessous une procédure d'installation simple, organisée par étapes :

1. Cloner ce dépôt GitHub :
    - `git clone https://github.com/tominien/Fresqu-aeromaps.git`
    - `cd Fresqu-aeromaps`
2. Installer les outils de compilation et les headers Python :
    - `sudo apt update`
    - `sudo apt install build-essential python3-dev`
3. Créer un environnement virtuel :
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
4. Installer les dépendances du projet :
    - `pip install --upgrade pip setuptools wheel`
    - `pip install -r requirements.txt`
5. Lancer le Jupyter Notebook :
    - `jupyter notebook` *Si vous utilisez Visual Studio Code, veillez bien à choisir le Kernel correspondant à l'environnement `.venv` en haut à droite du notebook.*

## Template du fichire d'environnement

Afin que Python "reconnaisse" bien le dossier `src/` du projet comme étant celui contenant tout le code source, il est fortement recommandé de créer un fichier `.env`, avec le contenu suivant à la racine du projet :
```
PYTHONPATH=./src
```
