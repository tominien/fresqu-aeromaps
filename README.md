# Fresqu'AéroMaps

Ce repository est celui d'une extension de la Fresqu'aéro, atelier de sensibilisation à l'environnement dans le secteur aéronautique. Ce repo héberge un outil de simulation basé sur AeroMAPS, et est activé au moyen d'un Binder.

## Guide d'installation

Afin de pouvoir facilement installer, compiler, modifier et utiliser le Jupyter Notebook `Fresqu'aeromaps v1.2.ipynb` sur votre machine, il est fortement recommandé d'utiliser un environnement virtuel Python.

Vous trouverez ci-dessous une procédure d'installation simple, organisée par étapes :

1. Cloner ce dépôt GitHub :
    - `git clone https://github.com/tominien/Fresqu-aeromaps.git`
    - `cd Fresqu-aeromaps`
2. Créer un environnement virtuel :
    - `python3 -m venv .venv`
    - `source .venv/bin/activate`
3. Installer les dépendances du projet :
    - `pip install -r requirements.txt`
4. Lancer le Jupyter Notebook :
    - `jupyter notebook` *Si vous utilisez Visual Studio Code, veillez bien à choisir le Kernel correspondant à l'environnement `.venv` en haut à droit du notebook.*
