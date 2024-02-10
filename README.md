# Installation

Mise en place de l'environnement de travail :

```console
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

# Initialisation du CTFd

Pour faire des tests, il est possible d'installer une version dockerisée du CTFd :

1. Télécharger le projet depuis GitHub : <https://github.com/CTFd/CTFd>
2. Lancer le docker : `docker run -p 8000:8000 -it ctfd/ctfd`

Durant la configuration de départ, selectionner `User Mode` dans l'onglet `Mode`. Une fois le CTFd initialisé, il faut,
avec un compte administrateur (compte créé de base), dans `Settings`, puis `Access Tokens`. Il faut ensuite générer un
token et le mettre dans les variables d'environnement :

1. Créer un fichier `.env` à la racine du projet
2. Ajouter la ligne : `TOKEN=ctfd-votre-token`

# Utilisation

Une fois l'installation faite, il est possible de la tester en lançant la commande `pytest`. Si aucun test ne passe,
peut-être que le wrapper n'arrive pas à se connecter à l'instance de CTFd, vérifiez alors l'URL et le TOKEN.

Des \[exemples\](./examples) sont disponibles dans le code. Des \[tests\](./tests) sont aussi disponibles.

# Debug

Les requêtes peuvent être essayées sans le wrapper, la documentation est disponible sur
\[docs.ctfd.io\](<https://docs.ctfd.io/docs/api/redoc/>).

La structure des objets est celle du CTFd, les requêtes sont toutes lancées depuis `client.py`.

# Installation de Black

## Avec le Makefile de Sckathach

Il suffit de taper : `make install_black`

## À la main

Black est un outil de formatage de code python. Pour le lancer il suffit de l'installer et de lancer la commande à la
racine :

```console
pip install black
black .
```

Pour activer Black à chaque commit, il est possible de créer un hook git :

```console
echo -e '#!/bin/bash\nmake pre-commit' > .git/hooks/pre-commit
```
