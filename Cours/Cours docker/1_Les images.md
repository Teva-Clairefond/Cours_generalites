# Cours docker : Les images

Ce cours est basé sur ces ressources. Certains paragraphes et images sont copiés, tous droits appartenant à leur auteur.

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


### Pourquoi COPY . . correspond à une couche qui change souvent ?


Pour `COPY . .`, l’idée “couche qui bouge souvent” vient de **ce que représente le `.`**.

#### Ce que `COPY . .` copie exactement

* Le premier `.` = **le contexte de build** (le dossier que vous donnez à `docker build`, typiquement votre dossier projet).
* Le second `.` = **le répertoire de travail dans l’image** (souvent `WORKDIR /app`, donc ça copie tout dans `/app`).

Donc `COPY . .` = “copie *tout mon projet* dans l’image”.

#### Pourquoi cette couche change souvent ?

Docker calcule si la couche peut être réutilisée via le cache en regardant (en gros) **le contenu des fichiers copiés**. Résultat :

* On modifie **un seul fichier** (ex: `app.js`, `main.py`, `README.md`) → l’entrée `COPY . .` n’est plus identique → **cette couche est invalidée**.
* Et comme Docker construit **ligne par ligne**, toutes les lignes **après** doivent être reconstruites.

C’est pour ça que `COPY . .` est souvent considéré comme “instable” : le code change très fréquemment.

#### Ce qui empire le problème

Sans `​.dockerignore`, `COPY . .` peut embarquer des dossiers/fichiers qui changent encore plus souvent que votre code :

* `node_modules/`, `venv/`, `.pytest_cache/`, `.mypy_cache/`
* `dist/`, `build/`, `.next/`
* `.git/` (ça change à chaque commit)
* logs, fichiers temporaires, etc.

Et là, la couche devient “bruyante” : elle change même quand le code applicatif change peu.


### Où mettre le Dockerfile ?

Le Dockerfile doit être **dans le dossier l'on utilise comme contexte de build**, **là où on lance `docker build`**.

Exemple :
   * Si Docker tourne sur la **machine hôte** → Dockerfile sur l’hôte (dans le dossier projet).
   * Si Docker tourne **dans la VM** → Dockerfile dans la VM (ou accessible dans la VM) et on lance `docker build` depuis la VM.


## Union Filesystem et Copy-on-Write


"Pour assembler les couches en un système de fichiers cohérent, Docker utilise un Union Filesystem (généralement OverlayFS via le driver overlay2). Ce système :

    Superpose les couches read-only les unes sur les autres
    Présente une vue unifiée au conteneur (comme un seul système de fichiers)
    Utilise le mécanisme Copy-on-Write (CoW) pour les modifications

Quand un conteneur modifie un fichier existant dans une couche read-only :

    Le fichier est copié dans la couche d’écriture du conteneur
    La modification s’applique sur cette copie
    La couche originale reste intacte"


Une question légitime est donc : "COPY . . copie l'environnement du dossier où se trouve notre dockerfile et donc notre projet. Mais quelle est la différence avec ce que docker copie dans son writeable/upperdir ?"

`COPY . .` : ça copie (presque) tout le dossier projet **dans l’image** pendant le **build**.

La différence avec le **writable/upperdir** (la couche du conteneur) tient surtout à **quand** et **pourquoi** ça arrive.

### 1) `COPY . .` = au moment du *build*, dans l’image (read-only)

* Ça se passe quand on fait `docker build`.
* Les fichiers sont ajoutés dans une **couche d’image** (une layer).
* Cette couche devient **read-only** une fois l’image construite.
* Elle sera partagée par tous les conteneurs lancés depuis cette image.

👉 En bref : `COPY` sert à “emballer” le code **dans l’image**.

### 2) `upperdir` = au moment de l’exécution, spécifique à *un conteneur*

* Ça se passe quand le conteneur tourne (`docker run`, puis actions dedans).
* Dès que le conteneur écrit/modifie/supprime un fichier, ça va dans **sa couche writable**.
* Cette couche est **unique** à ce conteneur et disparaît si on le supprime.

👉 En bref : `upperdir` sert à stocker les **changements runtime**.

### Mini-exemple concret

* Vous faites `COPY app.py /app/app.py` dans le Dockerfile → `app.py` fait partie de l’image (read-only).
* Vous lancez le conteneur, puis vous éditez `/app/app.py` dans le conteneur → la version modifiée est dans `upperdir` (et masque celle de l’image).

### Le piège courant : “mais Docker copie déjà tout dans upperdir ?”

Non : Docker ne “copie pas votre projet” automatiquement dans `upperdir`.
`upperdir` ne reçoit que **les différences** créées *pendant l’exécution* (ou des fichiers créés/modifiés par votre application).

**C’est pourquoi les modifications dans un conteneur ne persistent pas après sa suppression, sauf si vous utilisez des **volumes**.**


## Comment une image est-elle structurée ?


Si l'on extrait une image docker et qu'on l'a décompresse de cette manière : 

`docker save nginx:alpine -o nginx-alpine.tar`
`mkdir nginx-image && tar -xf nginx-alpine.tar -C nginx-image`

On va avoir quelque chose comme :

![Structure d'une image](/Images/docker-image-structure.png)

Ainsi on peut voir un répertoire 'blob' (Binary Large OBject) contenant une série de fichiers dont les titres sont des hash.

Les fichiers qui sont dans blobs/sha256/, sont des blobs binaires compressés représentant soit :
    des couches de fichiers (layer.tar.gz)
    des manifests JSON
    des configurations de conteneur

``manifest.json`` : décrit les couches et la configuration.

``repositories`` : indique le nom de l’image et son tag.


### A quoi sert le fichier OCI-layout ?

Le fichier **`oci-layout`** sert à dire : *“ce dossier respecte la structure standard OCI Image Layout”* et **quelle version** de ce format il utilise.

Concrètement :

* c’est un petit fichier JSON,
* il contient typiquement un champ `imageLayoutVersion` (ex: `"1.0.0"`),
* il permet à un outil compatible OCI (Docker/containerd/skopeo, etc.) de reconnaître qu’il peut lire ce répertoire comme un **layout OCI**.

Dans ce layout :

* les objets (couches, config, manifests) sont dans `blobs/<algo>/<digest>`
* l’entrée principale est dans `index.json` (qui pointe vers un/des manifests).


### Description du fichier manifest.json

"Ce fichier manifest.json est un élément clé d’une image Docker exportée au format OCI. Il décrit la composition complète de l’image, notamment :
- le fichier de configuration (Config)
- les couches de fichiers (Layers)
- les informations sur chaque blob (LayerSources)
- les tags associés à l’image (RepoTags)

Notre exemple de manifest.json :

```[
  {
    "Config": "blobs/sha256/1ff4bb4faebcfb1f7e01144fa9904a570ab9bab88694457855feb6c6bba3fa07",
    "RepoTags": [
      "nginx:alpine"
    ],
    "Layers": [
      "blobs/sha256/08000c18d16dadf9553d747a58cf44023423a9ab010aab96cf263d2216b8b350",
      "blobs/sha256/c1761f3c364a963ec0ebd4d728cb6dd5aa24273f7dba0c3dd2fdb8411682ef0a",
      "blobs/sha256/8f3c313eb1240a3b86e0c76d0abda7a6fa7df30ad3151e98c4e3725a3fb710dc",
      "blobs/sha256/c9ce8cb4e76a801ef89c226cb8657556e62e3bb962b3641b051bb25f13dd1a26",
      "blobs/sha256/252b6db79fae151ab547c0f86a873dc97274d8b61f3921158d480b4242fef957",
      "blobs/sha256/f1f70b13aacc43849d4f4ab87a889304a4300210ecd32be5a55305486af5f1ea",
      "blobs/sha256/9af9e76ea07fe05a1f7660b80ec2417bc3fe500991df4995b0adfa13aade20b6",
      "blobs/sha256/c18897d5e3dd125d3d9f2ca7f361cb6b05cf7fad8ef9bc00548f3eb6f3def644"
    ],
    "LayerSources": {
      "sha256:08000c18d16dadf9553d747a58cf44023423a9ab010aab96cf263d2216b8b350": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 8120832,
        "digest": "sha256:08000c18d16dadf9553d747a58cf44023423a9ab010aab96cf263d2216b8b350"
      },
      "sha256:252b6db79fae151ab547c0f86a873dc97274d8b61f3921158d480b4242fef957": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 2560,
        "digest": "sha256:252b6db79fae151ab547c0f86a873dc97274d8b61f3921158d480b4242fef957"
      },
      "sha256:8f3c313eb1240a3b86e0c76d0abda7a6fa7df30ad3151e98c4e3725a3fb710dc": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 3584,
        "digest": "sha256:8f3c313eb1240a3b86e0c76d0abda7a6fa7df30ad3151e98c4e3725a3fb710dc"
      },
      "sha256:9af9e76ea07fe05a1f7660b80ec2417bc3fe500991df4995b0adfa13aade20b6": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 7168,
        "digest": "sha256:9af9e76ea07fe05a1f7660b80ec2417bc3fe500991df4995b0adfa13aade20b6"
      },
      "sha256:c1761f3c364a963ec0ebd4d728cb6dd5aa24273f7dba0c3dd2fdb8411682ef0a": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 4504064,
        "digest": "sha256:c1761f3c364a963ec0ebd4d728cb6dd5aa24273f7dba0c3dd2fdb8411682ef0a"
      },
      "sha256:c18897d5e3dd125d3d9f2ca7f361cb6b05cf7fad8ef9bc00548f3eb6f3def644": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 36649472,
        "digest": "sha256:c18897d5e3dd125d3d9f2ca7f361cb6b05cf7fad8ef9bc00548f3eb6f3def644"
      },
      "sha256:c9ce8cb4e76a801ef89c226cb8657556e62e3bb962b3641b051bb25f13dd1a26": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 4608,
        "digest": "sha256:c9ce8cb4e76a801ef89c226cb8657556e62e3bb962b3641b051bb25f13dd1a26"
      },
      "sha256:f1f70b13aacc43849d4f4ab87a889304a4300210ecd32be5a55305486af5f1ea": {
        "mediaType": "application/vnd.oci.image.layer.v1.tar",
        "size": 5120,
        "digest": "sha256:f1f70b13aacc43849d4f4ab87a889304a4300210ecd32be5a55305486af5f1ea"
      }
    }
  }
]```

Voici une explication détaillée de chacune des parties de ce fichier `manifest.json` :

### `"Config"` : métadonnées de l’image

```json
"Config": "blobs/sha256/1ff4bb4faebcfb1f7e01144fa9904a570ab9bab88694457855feb6c6bba3fa07"
```

Ce fichier (un blob JSON) contient toutes les instructions du Dockerfile compilées : la commande par défaut (CMD), les variables d’environnement, les volumes, les labels, etc. C’est le cerveau du conteneur."


#### "RepoTags" : nom et version de l’image

"RepoTags": ["nginx:alpine"]

#### "Layers" : couches empilées de l’image

```"Layers": [
  "blobs/sha256/08000c18d16da...",
  "blobs/sha256/c1761f3c364a...",
  ...
]
```

"Chaque fichier listé ici correspond à une couche de fichiers (layer.tar) ajoutée lors du docker build. Elles sont appliquées dans l’ordre, de la base vers le haut. Le contenu de ces archives représente les ajouts ou suppressions de fichiers à chaque étape du build."

#### "LayerSources" : métadonnées des couches
