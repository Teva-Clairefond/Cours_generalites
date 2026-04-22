Protocole SSH et Connexion en ssh machine hote vers VM :


Explications :

    Général :
        Tout comme le protocole TLS le protocole SSH fonctionne aussi sur un système de clés publiques et privées.
        Cependant celles-ci sont très différentes : Dans le protocole SSH elles sont comme des tampons qui attestent de l'identité du Client/Serveur,
        là où dans le protocole TLS ces clés servent à chiffrer et déchiffrer.

    Fabrication d'une clé symétrique (exemple Diffie-Hellman) :

        L’idée clé : les deux parties créent la même clé sans jamais l’envoyer sur le réseau.

        Exemple simplifié (DH classique) :
            Le client et le serveur choisissent un nombre public (p, g).
            Le client choisit un secret a, calcule A = g^a mod p, envoie A au serveur.
            Le serveur choisit un secret b, calcule B = g^b mod p, envoie B au client.
            Le client calcule K = B^a mod p.
            Le serveur calcule K = A^b mod p.
            → les deux trouvent la même valeur K, sans jamais échanger leurs secrets a et b.
            Cette valeur K devient la clé symétrique de la session.


    Etapes du protocole SSH :

    1 - Client → Serveur : Demande de connexion au Serveur sur le port 22
        Le Client envoie un paquet KEXINIT → il liste les algorithmes qu’il supporte :
            méthodes d’échange de clé (ex : diffie-hellman-group14-sha256, curve25519-sha256),
            algorithmes de chiffrement symétrique (AES, ChaCha20…),
            fonctions de hachage (SHA-256…), etc.

    2 - Serveur → Client : choix
        Le Serveur répond avec son propre KEXINIT → il choisit un algorithme parmi ceux proposés.

    3 - Client → Serveur : envoi de A
        Le client choisit un secret aléatoire a.
        Il calcule A = g^a mod p (ou l’équivalent elliptique pour Curve25519).
        Il envoie A au serveur.

    4 - Serveur → Client : envoi de B signé
        Le serveur choisit un secret aléatoire b.
        Il calcule B = g^b mod p.
        Il signe les données d’échange (A, B, paramètres, et un identifiant de session) avec sa clé privée de serveur.
        Il envoie au client :
            sa clé publique de serveur (si première connexion, sinon le client a déjà known_hosts),
            la valeur B,
            et la signature de tout ça.    

    5 - Client : Vérifie la signature avec la clé publique Serveur

    6 - Calcul de la clé symétrique
        Le client calcule K = B^a mod p.
        Le serveur calcule K = A^b mod p.
        Les deux obtiennent la même clé symétrique K, sans jamais l’avoir transmise.

    7 - Activation du chiffrement
        À partir de ce moment, tout le trafic (y compris l’authentification du client) est chiffré avec une clé dérivée de K.


    Cas A) Identification paire de clés client :

    8 - Client → Serveur : Envoie la clé publique Client

    9 - Serveur → Client : Envoie un défi au Client

    10 - Client → Serveur : Renvoie le défi signé avec la clé privée Client 

    11 - Serveur : Vérifie la signature avec la clé publique Client
 

    Cas B) Identification du client par mot de passe :

    8 - Client → Serveur : Indique qu'il souhaite s'authentifier par mdp

    9 - Serveur → Client : Demande le mdp

    10 - Client → Serveur : Envoi du mdp

    11 - Serveur : Compare le mdp avec celui stocké localement



Connexion en SSH :


    1 - Ouvrir les ports ssh de la VM

        sudo apt install ssh iptables iptables-persistent
        iptables -A INPUT -p tcp --dport 22 -j ACCEPT
        iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT (Dans le doute)
        iptables -A INPUT -m state --state RELATED,ESTABLISHED -j ACCEPT
        sudo netfilter-persistent save
        sudo netfilter-persistent reload    


    2 - Rediriger le port 2222 (ou autre) de l'hote vers le port 22 de la VM

        Eteindre la VM
        Configuration > Réseau > Rediriger les ports



Cas A] Connexion SSH via paire de clés client :

    3 - Générer une paire de clés SSH pour le client

        ssh-keygen -t ed25519 -C user@vm
            # -t ed25519 : L’option -t choisit le type d’algorithme pour la clé.
                # Ici ed25519 = algorithme moderne basé sur les courbes elliptiques (Curve25519).

    4 - Envoi de la clé publique vers le serveur

        ssh-copy-id -p 2222 user@localhost
            # Cela ajoute la clé publique dans ~/.ssh/authorized_keys sur la VM serveur
            # Ne fonctionne PAS sur Windows !!!

        ou :

        notepad C:\Users\<nom_utilisateur>/.ssh/id_ed25519.pub
            # Et copier manuellement la clé dans /home/<utilisateur>/.ssh/authorized_keys

    5 - Connexion SSH

        ssh -p 2222 user@localhost
            # Pas besoin de mdp



Cas B] Connexion SSH via mdp client :

    3 - Effectuer la connexion ssh depuis la machine hote

        ssh -p 2222 teva@127.0.0.1
            # Puis rentrer le mdp

        # IMPORTANT : L'adresse IP cible de connexion doit bien être 127.0.0.1 et non localhost. En effet VMware n'écoute que sur le port IPV4 et non sur le port IPV6...
        Ainsi quand on écrit 'localhost', c'est le port IPV6 auquel le paquet va être transmit en priorité.

        En marquant 127.0.0.1, on est sûr que c'est le port 2222 IPV4 qui va le recevoir.

        NB : 
            Si l'on veut écouter (ou émettre) à l'adresse IPV4 de toutes les interfaces réseau : '0.0.0.0'
            Si l'on veut écouter (ou émettre) au loopback IPV6 : '::1'
            Si l'on veut écouter (ou émettre) à l'adresse IPV6 de toutes les interfaces réseau : '::'