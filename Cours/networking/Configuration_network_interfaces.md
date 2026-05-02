# Configuration du fichier network interfaces

Ce fichier permet de configurer les interfaces réseaux.

## Structure de base : 

```bash
# Interface loopback (toujours présente)
auto lo
iface lo inet loopback

# Interface réseau classique
auto eth0
iface eth0 inet dhcp
```

## Explication des directives :

auto <interface>
→ Active automatiquement l’interface au démarrage
iface <interface> <famille> <méthode>
→ Définit la configuration :
    <famille> : inet (IPv4) ou inet6 (IPv6)
    <méthode> :
        dhcp → IP automatique
        static → IP fixe
        manual → pas de configuration automatique

## Exemple de syntaxe avec une interface réseau avec une ip statique :

```bash
auto eth0
    # auto : toujours au démarrage, même si l’interface est absente ou non branchée.
    # allow-hotplug : seulement quand l’interface est détectée (branchée / ajoutée). Voir fichier explicatif sur la différence entre auto et allow-hotplug
iface eth0 inet static
    address 192.168.1.100
        # Attribue une adresse IP locale statique à la carte LAN qui héberge le serveur DHCP
        # Ne dois pas être l'adresse du sous-réseau, donc ne dois pas terminer par .0 puisque c'est le sous-réseau qui termine de cette manière
    netmask 255.255.255.0
        # Masque de sous-réseau
    gateway 192.168.1.2
        # Souvent dans un réseau NAT lié à des machines virtuelles, il y a la machine hôte sur X.X.X.1 et la gateway sur X.X.X.2.
    dns-nameservers 8.8.8.8 8.8.4.4
        # Serveur DNS qui doit être contacté pour la résolution de nom de domaine. S'il y a un serveur DNS local mettre son adresse.
```

**IMPORTANT : Je le rappelle mais souvent dans VMware en NAT l'ip xxx.xxx.xxx.1 est utilisée par la machine hôte donc la gateway deviens xxx.xxx.xxx.2 !**



## Exemple de syntaxe avec DHCP :

```bash
auto eth0
iface eth0 inet dhcp
```

## Exemple avec une interface WI-Fi :

```bash
auto wlan0
iface wlan0 inet dhcp
    wpa-ssid "NomDuWifi"
    wpa-psk "MotDePasse"
```