Installer Python 3 sur Mac et Ubuntu
===

Nous utiserons Python 3 dans notre cours. Les versions précédentes peuvent poser des problèmes.


## Installation

### OS X

**Nous vous conseillons d'installer la distribution Anaconda**. Elle contient tous les modules et packages nécessaires pour ce cours. Elle est disponible pour toutes les plateformes et possède une procédure d'installation assez simple. Vous pouvez la télécharger depuis http://continuum.io/downloads.  Des détails pour l'installation peuvent être trouvés ici : http://docs.continuum.io/anaconda/install.html

Utilisez bien la version 3.6 proposée. Une fois installée, tapez ensuite

```shell
conda create -n cours-python
```

suivi de

```shell
source activate cours-python
```

Cette dernière active un environnement de python qui nous permet de ne pas modifier l'environnement général de votre ordinateur.

Allez dans le repository git puis tapez dans le terminal de ce dossier

```shell
pip install -r requirements.txt
```

Tapez désormais

```shell
ipython notebook --matplotlib=inline
```

Si tout va bien, cela devrait ouvrir votre navigateur sur la page http://127.0.0.1:8888/ qui s'appelle IP[y]: Notebook.

### Linux (Ubuntu/Debian)

Vous aurez besoin des droits d'administrateurs pour faire ce qui suit.

Ouvrez un terminal et tapez :

```shell
sudo apt-get install python3 libfreetype6-dev python3-pip python3-virtualenv
```

Puis, une fois cela installé, faites :

```shell
virtualenv ~/.cours-python -p python3
```
Cela créera un environnement virtuel dans lequel nous pourrons installer l'ensemble des informations nécessaires. Allez, dans le terminal, dans le dossier git du cours que vous avez cloné localement et tapez :

```shell
source ~/.cours-python/bin/activate
```

Cette commande sera obligatoire à chaque fois que vous voudrez travailler avec le cours. Dans le même terminal, tapez maintenant

```shell
pip install -r requirements.txt
```

Cela installera les packages nécessaires pour le cours. Une fois ces packages installés, il suffira de taper

```shell
ipython3 notebook
```

Si tout va bien, cela devrait ouvrir votre navigateur sur la page http://127.0.0.1:8888/ qui s'appelle IP[y]: Notebook.

## Contributeurs

- Mike Kestemont
- Folgert Karsdorp
- Maarten van Gompel
- Matt Munson
- Thibault Clérice