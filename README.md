# CTFd Blabla - Blabla

## Préparation de l'étude

### **éléments à surveiller** :

*Entre 2 utilisateurs*
- Adresses IP en commun
- Timing des flags
- Distance de Jaccard
- Comparaison des solves
- comparaison des scores

*Pour un utilisateur*
- Comparer à la moyenne des utilisateurs, à l'écart type : vitesse de progression
- Temps entre le téléchargement d'un fichier et le flag
- Temps entre deux flag : pas possible de flag 1/2/3 en 2 secondes
- verification lors de connection en netcat,...
- connexion en netcat authentifiée
- writeups des challs difficiles

Prevention/detection/dissuasion

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

