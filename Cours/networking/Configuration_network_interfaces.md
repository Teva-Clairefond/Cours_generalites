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
iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.1
    dns-nameservers 8.8.8.8 8.8.4.4
```

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

