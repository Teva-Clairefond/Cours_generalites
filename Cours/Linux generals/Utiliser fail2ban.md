# Installation et utilisation de fail2ban


## Généralités :

```
Jail A = Backend_A + Filter_A + Compteur_A + Actions_A
Jail B = Backend_B + Filter_B + Compteur_B + Actions_B
Jail C = Backend_C + Filter_C + Compteur_C + Actions_C
```

Backend lit les logs (par exemple systemd mais pas seulement)
Filter détecte une attaque
Compteur regarde si le seuil a été franchi
Action applique le ban en envoyant une commande au firewall


Les fichiers de configuration de fail2ban se trouvent dans /etc/fail2ban :

fail2ban.conf        → config globale (à ne pas modifier)
jail.conf            → jails par défaut (à ne pas modifier)
jail.local           → notre config principale (remplace jail.conf)
filter.d/            → filtres (regex)
action.d/            → actions (firewall, mail…)


Chaque 


## Installation et configuration :

```bash
sudo apt install fail2ban -y
```


