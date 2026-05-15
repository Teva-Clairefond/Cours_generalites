# Changer le nom de la machine :


## Commande :

```bash
sudo hostnamectl set-hostname {nouveau nom de la machine}
```

## Configuration réseau :

```bash
sudo nano /etc/hosts
    # remplacer 127.0.1.1 {ancien nom} par :
    127.0.1.1 {nouveau nom}
```

## Application immédiate :

```bash
sudo reboot
```