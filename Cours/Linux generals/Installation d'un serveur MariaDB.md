Installation d'un serveur MariaDB (serveur SQL gestionnaire de base de données)




Explications : 

    Le code inséré dans /var/www/index.php (par exemple) fait appel à une bibliothèque (comme mysqli par exemple).
    Cette bibliothèque permet de communiquer avec le serveur MariaDB via le protocole MariaDB.
    
    Les données de la base de données étant amenées à changer, elles sont situées dans /var/lib/mysql

    Socket Unix : Fichier spécial qui permet à deux processus sur la même machine de communiquer, un peu comme un "port réseau interne" mais sans passer par TCP/IP.





Installation et configuration d'un serveur MariaDB :

    1) Installation des paquets :

        sudo apt update
        sudo apt upgrade -y
        sudo apt install mariadb-server -y
        sudo systemctl enable mariadb
        sudo systemctl status mariadb

    2) Connexion en tant que root MariaDB et configuration:

        sudo mysql
            # Ouvre l'invite de commande MariaDB
            # Connexion en tant que super utilisateur système au root MariaDB au travers de socket unix -> Pas besoin de mdp

        sudo mysql_secure_installation;
            # Script de sécurité pour modifier les options par défaut les moins sûres
                1 - Identification en tant qu'utilisateur root de la BdD avec son mdp actuel : Cliquer sur "ENTER" (aucun mdp)
                2 - Identification avec la socket UNIX, résultat : seul le compte root Linux peut admin la BdD.
                3 - Création de mdp pour l'user root de la BdD ? : "N"
                    # Pas besoin car root continuera de se connecter via le socket unix de la machine
                4 - Pour toutes les questions suivantes il faut garder les valeurs par défaut : "Y"
                    # Supprime les utilisateurs anonymes et la base de données de test, 
                    # désactive les connexions root distantes, mais pas les non-root
                    # chargera ces nouvelles règles afin que MariaDB implémente immédiatement les modifications que vous avez apportées.


Cas A] Les serveurs Web et MariaDB sont sur la même machine : 

    3) Vérifications et tests :

        sudo systemctl status mariadb

        sudo mysqladmin version
            # Le but est de voir si l'on peut se connecter à la BdD. Ici on utilise l'outil mysqladmin qui est un client permettant d'executer des commandes d'admin.
            # Ici la commande consiste à se connecter en tant que root de la BdD et à renvoyer la version


Cas B] Les serveurs Web et MariaDB sont sur des machines différentes et communiques via le réseau :

    3) Configuration de MariaDB pour définir la carte réseau à écouter :

        # On veut que le serveur web puisse acceder au serveur MariaDB
        # On veut pouvoir acceder depuis la VM hôté MariaDB au serveur MariaDB

        sudo nano /etc/mysql/mariadb.conf.d/50-server.cnf
            # Ce fichier correspond aux paramètres du serveur en lui-même
            # Tous les fichiers de mariadb.conf.d sont lus lors du démarrage du service mysqld

            bind-address = 0.0.0.0
                # A la place du localhost 127.0.0.1
                # IP ici coorespond à l'IP de la carte réseau de la machine hôte du serveur MariaDB sur laquelle MariaDB doit écouter
                # Ici vu que l'on veut pouvoir configurer MariaDB depuis la machine hote du serveur MariaDB et que l'on veut aussi que le serveur écoute
                # le serveur web distant, on doit ouvrir l'écoute à toutes les cartes réseaux (0.0.0.0) puis ensuite configurer le firewall.

        sudo systemctl restart mariadb

    
    4) Configuration du firewall :

        # On souhaite que le firewall permettent l'accès du client MariaDB côté serveur web vers le serveur MariaDB qui écoute sur le port 3306
        # On souhaite aussi que l'admin puisse se connecter depuis la machine hôte sur le serveur MariaDB en root
        # On souhaite que par défaut le firewall n'autorise pas les autres connexions (peut-être SSH mais nous allons sécuriser les connexions avec le TLS de MariaDB)

        sudo apt install ufw -y

        sudo ufw allow from IP_serv_web to any port 3306
            # from IP_serv_web : Permet l'accès depuis cette adresse IP
            # to any : Sur n'importe quelles carte réseau de la machine hôte du serveur MariaDB
            # port 3306 : sur le port MariaDB
        
        sudo ufw allow from 127.0.0.1 to any port 3306
    
        sudo ufw default deny incoming
            # Toutes les connexions entrantes sont bloquées par défaut

        sudo ufw status
    
    
    5) Création d'un utilisateur pour le serveur web :

        # Il faut créer un compte utilisateur pour l’accès par mot de passe du serveur web vers le serveur MariaDB

        sudo mysql -u root
            # Ouvre l'invite de commande MariaDB
            # Connexion en tant que super utilisateur système à l'utilisateur root MariaDB au travers de socket unix -> Pas besoin de mdp
            # l’utilisateur root MariaDB est configuré pour s’authentifier à l’aide du plugin unix_socket par défaut plutôt qu’avec un mot de passe. 


        CREATE USER 'webuser'@'192.168.1.10' IDENTIFIED BY 'MotDePasseTresFort';
            # Ici IP correspond bien à l'IP du serveur web sur le LAN

        CREATE DATABASE webdb;
        GRANT SELECT, INSERT, UPDATE, DELETE ON webdb.* TO 'webuser'@'192.168.1.10';
            # Donne des privilèges à l'utilisateur sur la BdD
        FLUSH PRIVILEGES;
            # Active les modifications immédiatement

        SHOW GRANTS FOR 'webuser'@'192.168.1.10';
            # Montre les permissions de l'utilisateur

    
    6) Configurer le serveur web pour se connecter à MariaDB :

        # Sera fait dans un autre cours

    
    7) Chiffrement des connexions avec le TLS natif MariaDB :

        # Sera fait dans un autre cours
    






    