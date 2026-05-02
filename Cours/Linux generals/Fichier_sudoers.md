# Fichier sudoers

Le fichier /etc/sudoers gère l'attribution des privilèges au sein du système.

## Syntaxe typique :

```bash
%wheel        ALL=(ALL:ALL)       ALL
```

## Explication :

La chaîne %wheel est l’utilisateur ou le groupe auquel la règle s’applique. Le signe de pourcentage (%) avant le mot wheel spécifie un groupe.

La commande ALL=(ALL:ALL)le premier ALL indique sur quel hôte (machines) la règle s'applique, les utilisateurs du groupe wheel peuvent exécuter des commandes en tant que n’importe quel autre utilisateur (le deuxième ALL) et n’importe quel autre groupe (le troisième ALL) sur le système.

La commande ALL finale spécifie que les utilisateurs du groupe wheel peuvent exécuter n’importe quelle commande.


## Cas où l'on doit spécifier la commande à attribuer :

```bash
bob          ALL=(ALL:ALL)       chemin/de/la/commande *
```

Exemple avec plusieurs commandes :

```bash
bob ALL=(root) /usr/bin/apt install *, /usr/bin/systemctl *, /usr/sbin/ip link set *
```