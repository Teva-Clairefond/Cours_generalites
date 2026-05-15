# Utilisation d'un parefeu ufw


Ce cours est basé sur le cours officiel de ubuntu : https://doc.ubuntu-fr.org/ufw

## Explication :

ufw (Uncomplicated Firewall) est un outil de configuration qui utilise le parefeu iptables ou nftables en sous-jacent qui appliquent des règles bas-niveau.

ufw fonctionne sur un système de règles numérotées :

```bash
[ 1] 22/tcp ALLOW Anywhere
[ 2] Anywhere DENY 203.0.113.50
```

Cela signifie que lors de la gestion d'un nouveau paquet les règles vont être parcourues dans l'ordre croissant. Dans cet exemple cela signifie que si l’IP 203.0.113.50 essaie de se connecter en SSH sur le port 22 :

1 - UFW regarde la règle 1 : “port 22 autorisé”
2 - Ça correspond
3 - Le paquet est accepté
4 - UFW ne regarde même pas la règle 2

Donc la règle de blocage arrive trop tard.

Il faut plutôt avoir :

```bash
[ 1] Anywhere DENY 203.0.113.50
[ 2] 22/tcp ALLOW Anywhere
```

C’est pour ça qu’on utilise :

```bash
sudo ufw insert 1 deny from 203.0.113.50
```
insert 1 veut dire : “mets cette règle en position 1”, donc avant toutes les autres.


Il y a un système de conservation des connexions déjà établie :

| Situation                                                          | Résultat avec `ufw deny 22`                |
| ------------------------------------------------------------------ | ------------------------------------------ |
| Quelqu’un essaie de se connecter à votre SSH local sur le port 22  | Bloqué                                     |
| Vous vous connectez en SSH vers un serveur distant sur son port 22 | Autorisé si le trafic sortant est autorisé |
| Les réponses du serveur distant reviennent vers vous               | Autorisées, car connexion établie          |

Les connections qui ont été établies dans le passé puis refermées ne sont pas considérées comme conservées et sont donc soumises aux règles de connexion.



## Installation :

```bash
sudo apt install ufw -y
sudo ufw enable
```


## Status actuel et réinitialisation :


```bash
sudo ufw status verbose
    # verbose permet aussi d'afficher les règles
sudo ufw status numbered
    # numbered permet d'afficher l'ordre d'application des règles
sudo ufw reset #/reset --force
```



## logs du parefeu :


```bash
Journalisation : on (low)
```

Indique que la journalisation est activée, vous pouvez retrouver toutes les interactions du pare-feu dans le fichier /var/log/ufw.log .

Activer la journalisation :

```bash
sudo ufw logging on #/off
```

## Gestion des règles par défaut :


Autoriser le traffic **entrant** selon les règles par défaut :

```bash
sudo ufw default allow incoming
    # Remarque on peut aussi ne pas préciser "incoming"
```

Autoriser le traffic **sortant** selon les règles par défaut :

```bash
sudo ufw default allow outgoing 
```

On utilise **deny** pour refuser.


## Les commandes de base :

[règle] est à remplacer par le numéro du port ou le nom du service désiré.

```bash
sudo ufw allow #/deny [règle]
    # Sans précision c'est un connexion entrante qu'on autorise

sudo ufw insert 1 deny from [ip]
    # Si vous voulez bloquer une IP sur tous vos services, il faut le faire "avant" les autorisations existantes. D'où le "insert 1" qui met ce "deny" avant tous les "allow". Dans le cas d'une série d'IP à bloquer vous pouvez utiliser à chaque entrée le "insert 1", pas besoin de spécifier dans le cas présent une autre place 

sudo ufw deny out [règle]
    # Refuser une connexion sortante
```

Supprimer une règle : 

```bash
sudo ufw delete allow [règle]
sudo ufw delete deny [règle]

sudo ufw delete [numéro]
```

## Syntaxe des règles :

Ouverture du port 53 en TCP et UDP :
```bash
sudo ufw allow 53
```

Ouverture du port 25 en TCP uniquement :
```bash
sudo ufw allow 25/tcp
``` 

UFW regarde dans sa liste de services connus pour appliquer les règles standards associées à ces services (apache2, smtp, imaps, etc..). Ces règles sont automatiquement converties en ports. 

```bash
sudo ufw allow smtp
sudo ufw allow out 2628/tcp
sudo ufw allow out pop3s
```

## Règles complèxes :

Refuser le protocole (proto) TCP à (to) tout le monde (any) sur le port (port) 80 : 

```bash
sudo ufw deny proto tcp to any port 80
```
Refuser les données utilisant le protocole (proto) UDP provenant (from) de 1.2.3.4 sur le port (port) 514 : 

```bash
sudo ufw deny proto udp from 1.2.3.4 to any port 514
```

Refuser à l'adresse 192.168.0.5 de recevoir toutes données provenant du serveur web de la machine hébergeant le pare-feu : 

```bash
sudo ufw deny out from 192.168.0.5 to any port 80
```

Accepter pour une interface réseau spécifique :

```bash
ufw allow in on ens34 from 192.168.1.0/24 to any port 53 proto udp
```

### Insersion de règle :

Vous pouvez insérer une règle à une position précise en utilisant le numéro :
```bash
sudo ufw insert NUM RULE
```

