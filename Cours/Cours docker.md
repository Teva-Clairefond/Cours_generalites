# Cours docker

Les bases de docker : https://www.docker.com/101-tutorial/sudo
Comprendre les images docker : https://blog.stephane-robert.info/docs/conteneurs/images-conteneurs/
Ecrire le dockerfile : https://blog.stephane-robert.info/docs/conteneurs/images-conteneurs/ecrire-dockerfile/


## Qu'est-ce que docker ?

Docker est un logiciel qui permet de créer des "conteneurs" à partir d'"images".
Les conteneurs permettent d'émuler un environnement virtuel à la manière d'une VM migrée. Cependant, les conteneurs n'émulent pas l'ensemble du système comme sur une VM classique, mais ils partagent leur noyau avec l'hôte. Ainsi, leur isolation est moindre que sur une VM classique, et ils sont donc moins sécurisés.

## Qu'est-ce qu'une image docker ?

Une image docker est dite "build" à partir d'une image de base. Cette image de base peut-être déjà très complète, avec l'app, les dépendances, les librairies etc. Mais elle peut être aussi basique avec seulement la base d'un OS.

"L’image de base, c’est le point de départ. Elle peut être :

    Une distribution minimaliste comme alpine
    Une image préconfigurée comme python:3.11-slim ou nginx
    Ou même scratch, qui signifie… aucune base du tout"

Il existe plusieurs types d'images de base :

| Type d'image | Exemple | Taille typique | Shell inclus | Cas d'usage |
|---|---|---|---|---|
| Standard | `python:3.12` | 900+ Mo | Oui | Dev, debug |
| Slim | `python:3.12-slim` | ~150 Mo | Oui | Production generale |
| Alpine | `python:3.12-alpine` | ~50 Mo | Oui (busybox) | Contraintes de taille |
| Distroless | `gcr.io/distroless/python3` | ~20 Mo | Non | Securite maximale |
| Chainguard | `cgr.dev/chainguard/python` | ~30 Mo | Non | Securite + zero CVE |


On construit une nouvelle image à partir de cette base.

Pour construire une image, on va ajouter des couches à cette image de base. Chaque couche est le résultat d’une instruction dans le Dockerfile. Ces instructions sont exécutées dans l’ordre, mais toutes les instructions ne créent pas de couche !


## Qu'est-ce que le Dockerfile ?

"Un Dockerfile est un fichier texte qui définit une suite d’instructions qui vont permettre d’installer tous les éléments nécessaires à l’exécution de notre application."

![Schema des couches Dockerfile](/Images/docker-image-layers.CYawgeO-_Z2r6UGt.svg)


### Content-Addressable Storage : la déduplication intelligente

Docker utilise un stockage adressable par contenu (Content-Addressable Storage). Chaque couche est identifiée par le hash SHA256 de son contenu, pas par son nom ou sa position.

### Deux caches différents :

* **Cache de téléchargement (pull)** : évite de retélécharger des couches déjà stockées localement.
* **Cache de build** : évite de **ré-exécuter** des étapes du Dockerfile (ex : `apt-get`, `pip install`, `npm install`) en réutilisant une couche déjà construite.

Autrement dit : Lors du build d'une nouvelle image, Docker 'pioche' dans les couches qu'il a en stock en suivant l'ordre du dockerfile, et il build à partir de ce qui est déjà construit.

Donc l'image alpine du build A peut aussi être en même temps l'image alpine du build B. De ce fait chaque layer n'est stoqué qu'une seule fois...

### Pourquoi l’ordre des lignes change tout

Docker lit le Dockerfile ligne par ligne. Si une ligne change, **toutes celles d’après sont invalidées** (il doit reconstruire les couches suivantes).

Ainsi, s'il y a une couche qui "change" souvent en dessous d'une couche qui est plus "stable" alors il y a une perte d'efficacité car on va reconstruire aussi la couche stable alors que ça aurait pu être évité.

Exemple typique :

**Mauvais pour le cache :**

```dockerfile
COPY . .
RUN npm install
```

➡️ Si vous modifiez un seul fichier de votre code, `COPY . .` change → Docker doit refaire `npm install` (long).

**Meilleur :**

```dockerfile
COPY package*.json ./
RUN npm install
COPY . .
```

➡️ Tant que `package*.json` ne change pas, Docker réutilise la couche “npm install”, même si votre code change tous les jours.


### Où mettre le Dockerfile ?

Le Dockerfile doit être **dans le dossier l'on utilise comme contexte de build**, **là où on lance `docker build`**.

Exemple :
   * Si Docker tourne sur la **machine hôte** → Dockerfile sur l’hôte (dans le dossier projet).
   * Si Docker tourne **dans la VM** → Dockerfile dans la VM (ou accessible dans la VM) et on lance `docker build` depuis la VM.