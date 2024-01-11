# Python Wrapper for CTFd's API

&rarr; *En attendant un `README.md` correct, des exemples illustrant les principales fonctionnalités sont disponibles 
dans [examples](./examples)*.


## Installation
Mise en place de l'environnement de travail :
```shell
python3 -m venv venv 
api venv/bin/activate
pip install -r requirements.txt
```

## Configuration
### Token
Le token CTFd est à mettre dans le fichier `.env` situé à la racine du projet : 
``` 
TOKEN=votre-magnifique-token
```
### Verbose
Dans la configuration : `.config`, mettre la valeur à `Nothing`, `Simple` ou `Full`:
``` 
VERBOSE=Full
```

## Installation de Black 
### En utilisant le Makefile de Sckathach
Il suffit de taper : `make install_black`

### À la main
Black est un outil de formatage de code python. Pour le lancer il suffit de l'installer et de lancer la commande à la
racine : 
```shell
pip install black 
black . 
```

Pour activer Black à chaque commit, il est possible de créer un hook git : 
```shell
echo -e '#!/bin/bash\nmake pre-commit' > .git/hooks/pre-commit
```

