# Erreur de dépot après installation via l'iso complète de debian


## Problème :

```bash
Error: The repository 'cdrom://[...] trixie Release' does not have a Release file.
```

Le système essaie d’utiliser le DVD d’installation comme dépôt APT, ce qui ne fonctionne pas pour les mises à jour.

## Solution :

Supprimer la source CD-ROM :

```bash
nano /etc/apt/sources.list
```

Puis commenter ou supprimer la ligne qui commence par :

```bash
deb cdrom:
```

Ensuite ajouter un vrai dépôt Debian (exemple pour Trixie) :
```bash
deb http://deb.debian.org/debian trixie main contrib non-free non-free-firmware
deb http://security.debian.org/debian-security trixie-security main
```

Puis :
```bash
apt update
```