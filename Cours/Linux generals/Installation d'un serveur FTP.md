Installation d'un serveur FTP


Explications :

    Le serveur FTP est une sorte d'interface entre un client distant et le systeme de fichier de la machine où le serveur est installé
    Il controle :
        Qui peut accéder (utilisateurs locaux ou anonymes).
        Quels fichiers ou répertoires ils peuvent voir et modifier.
        Quelles actions sont permises : lecture, écriture, suppression, création de dossiers.
    Les opérations sur le système de fichier se font via les commandes FTP


    Types d'utilisateurs :
        Utilisateurs locaux : Ils ont un compte utilisateur sur l'OS de la machine où le serveur ftp est installé. Leur droit d'accès ftp est lié à ce compte.
        Utilisateurs virtuels : Leur compte d'utilisateur du serveur ftp n'est pas adossé à un compte utilisateur d'OS
        Utilisateurs anonymes : N'importe qui peut s'y connecter, mais les permissions sont strictes. Ce compte sert à partager des données publiques.

    
    Le serveur SFTP :

        C'est un serveur FTP utilisant le protocole SSH pour sécuriser la connexion. Contrairement au FTPS, le SFTP n'est pas un serveur FTP modifié pour accueillir le
        SSH. C'est un service séparé et préinstallé qui fait partie d'OpenSSH, et c'est pourquoi il n'apparaît pas dans se cours.


    Le chiffrement et la sécurisation TLS :
        TLS (Transport Layer Security) : Protocole d'établissement d'une session sécurisée
            1 - Le serveur possède sa clé privée et envoie sa clé publique au client via le certificat.
            2 - Le client génère une clé de session temporaire (symétrique, ex. AES-256) pour chiffrer les données.
            3 - Le client chiffre cette clé symétrique avec la clé publique du serveur et l’envoie au serveur.
            4 - Le serveur déchiffre avec sa clé privée et obtient la même clé symétrique. Cette clé symétrique permettra l'échange pour la session.
        RSA (Rivest–Shamir–Adleman) : Algorithme de cryptographie asymétrique (clé publique / clé privée).
            Chaque certificat utilise une clé privée (à garder secrète sur le serveur) et une clé publique (que le client connaît via le certificat).
        Certificat
            Public_Key : Donnée au client par le serveur, sert a chiffrer
            CN (Common Name) : CN est un champ dans le certificat X.509.
                # Il représente le nom principal du serveur que le certificat valide.
                # Pour un serveur FTP, c’est généralement : le nom DNS complet : ftp.exemple.com , ou pour usage interne : ftp.exemple.local
            SAN (Subject Alternative Name) : SAN est aussi un champ dans le certificat X.509
                # Il liste des noms/IP supplémentaires côté serveur
                # CN et SAN dans le certificat sont une preuve de l'identité du serveur afin que par la suite le client puisse vérifier
                # qu'il tente de se connecter au bon serveur

    Etapes de FTPS (FTP + TLS):
        I - Connexion initiale
            1 - Le client tente de se connecter au serveur FTP sur le port 21.
            2 - Le client demande AUTH TLS (mode explicit FTPS) pour initier la sécurisation de la session.

        II - Réception du certificat
            1 - Le serveur envoie son certificat X.509 (qui contient la clé publique, le CN et le SAN).
            2 - Le client lit le certificat.

        III - Vérification de l’identité
            1 - Le client compare le nom ou l’IP auquel il se connecte avec :
                le CN (nom principal)
                et tous les SAN (DNS et IP supplémentaires)
            2 - Si le nom/IP correspond à au moins un SAN ou le CN, le client peut continuer le handshake TLS.
            3 - Si aucun ne correspond → avertissement ou refus de connexion, selon le client.

        IV - Echange de clés (handshake TLS):
            1 - Le client génère une clé symétrique temporaire pour la session.
            2 - Cette clé est chiffrée avec la clé publique RSA du serveur et envoyée.
            3 - Le serveur déchiffre avec sa clé privée.

        V - Session sécurisée FTPS 





I] Installation du serveur FTP :

    1) Installation des paquets :

        sudo apt update
        sudo apt upgrade -y
        sudo apt install vsftpd -y


    2) Configuration du serveur ftp :
        
        sudo nano /etc/vsftpd.conf
            listen=YES
                # Le serveur écoute les IPv4 
            anonymous_enable=NO
                # Ne permet pas aux utilisateurs anonymes de se connecter au serveur
            local_enable=YES
                # Autoriser les utilisateurs locaux à accéder au serveur ftp avec leur compte d'OS, sans compte virtuel
            write_enable=YES
                # Autoriser les opérations d’écriture (upload, création de dossier, suppression)
            chroot_local_user=YES
                # chroot (Change Root) = Quand un utilisateur est “chrooté” dans un répertoire, ce répertoire devient la nouvelle racine (/) pour cet utilisateur.
                # L’utilisateur ne peut pas remonter plus haut que ce répertoire. Il ne voit pas le reste du système de fichiers.
            allow_writeable_chroot=YES
                # Permet aux utilisateurs d'uploader et gérer leurs fichiers dans leur home directory, mais peut présenter des failles de sécurité.


    3) Ouverture des ports du pare-feu:

        sudo apt install ufw

        # Si ufw n'est pas de le path de l'utilisateur :
            nano /home/{utilisateur}/.bashrc
                export PATH=$PATH:/usr/sbin
            # Recharger les paramètre du path
            source ~/.bashrc

        sudo ufw allow 20
        sudo ufw allow 21
        
        ou

        sudo apt install iptables
        sudo iptables -A INPUT -p tcp --dport 20 -j ACCEPT
        sudo iptables -A INPUT -p tcp --dport 21 -j ACCEPT


    4) Redemmarer le service :

        sudo systemctl restart vsftpd
        systemctl status vsftpd


II] Passage en FTPS :


    1) Ajout de SAN (Subject Alternative Names) et fichier de configuration du certificat

        nano /tmp/vsftpd_openssl.cnf
            # C'est un fichier temporaire qui fichier ne sert qu'une fois : Au moment de générer le certificat
            # Une fois le certificat (.crt) et la clé privée (.key) générés, il n’y a plus besoin du fichier de config
            # Si on veut générer plusieurs certificats identiques, il faut le mettre dans /etc/ssl par exemple

            [ req ]
                # Section principale qui dit à OpenSSL comment générer la requête de certificat (CSR) ou un certificat auto-signé
                # Si on fait appel à une certification extérieur, dans ce cas on génèrera une CSR, dans l'autre cas ça sera un certif auto-signé
            distinguished_name = req_distinguished_name
                # distinguished_name = req_distinguished_name → indique la section où sont définis les champs d’identité du certificat (DN)
            req_extensions = v3_req
                # req_extensions = v3_req → précise quelle section contient les extensions X.509 à ajouter (dans la section on ajoutera le SAN)
            prompt = no
                # OpenSSL n’affiche pas le questionnaire sur les infos du DN et prend directement les valeurs écrites dans la section [ req_distinguished_name ]

            [ req_distinguished_name ]
            C = FR
            ST = Île-de-France
            L = Paris
            O = MaSociete
            CN = ftp.exemple.local
                # CN = Common Name (doit correspondre au nom DNS que les clients utiliseront, ex. ftp.exemple.local)
                # L'ensemble de ces infos (Pays, département, ville...) constituent ce que l'on appelle le Distinguished Name (DN)

            [ v3_req ]
                # Définit les extensions X.509 de la requête
            subjectAltName = @alt_names
                # La liste SAN (noms alternatifs du serveur) sera définie dans la section [ alt_names ]

            [ alt_names ]
            DNS.1 = ftp.exemple.local
            DNS.2 = serveur.exemple.local
            IP.1 = 192.0.2.10
                # définis tous les noms/IP pour lesquels le certificat est valide
                    # DNS.1 = ftp.exemple.local → le certificat est valide si le client se connecte à ftp.exemple.local
                    # DNS.2 = serveur.exemple.local → valide aussi pour ce deuxième nom DNS
                    # IP.1 = 192.0.2.10 → valide aussi si le client se connecte directement via cette IP


        VERSION COPIABLE :

            [ req ]
            distinguished_name = req_distinguished_name
            req_extensions = v3_req
            prompt = no

            [ req_distinguished_name ]
            C = FR
            ST = Île-de-France
            L = Paris
            O = MaSociete
            CN = ftp.exemple.local

            [ v3_req ]
            subjectAltName = @alt_names

            [ alt_names ]
            DNS.1 = ftp.exemple.local
            DNS.2 = serveur.exemple.local
            IP.1 = 192.0.2.10


    2) Génération d'une clé privée + certificat auto-signé :

        sudo openssl req -x509 -nodes -newkey rsa:4096 \
            # openssl req : lance la génération d’une requête de signature (CSR) — ici utilisé pour créer le certificat auto-signé
            # -x509 : demande la génération directe d’un certificat auto-signé au lieu d’une CSR uniquement
            # -nodes : ne chiffrera pas la clé privée (no DES) → la clé privée n’a pas de passphrase. 
                # Important : vsftpd ne peut pas demander une passphrase au démarrage, donc la clé doit être sans passphrase. La passphrase est un mdp qui permet
                # d'acceder au fichier au se trouve la clé privée
            # -newkey rsa:4096 : crée une nouvelle paire clé RSA de 4096 bits (taille recommandée pour sécurité).

            -keyout /etc/ssl/private/vsftpd.key \
                # -keyout /etc/ssl/private/vsftpd.key : chemin où sera écrit la clé privée. Par convention les clés privées vont dans /etc/ssl/private

            -out /etc/ssl/certs/vsftpd.crt \
                # -out /etc/ssl/certs/vsftpd.crt : chemin du certificat X.509 auto-signé généré

            -days 3650 \
                # -days 3650 : durée de validité du certificat en jours (ici 10 ans). Pour tests/intranet, ok ; pour production pense à renouveler régulièrement

            -config /tmp/vsftpd_openssl.cnf \
                # Indique le fichier de configuration du certificat

            -extensions v3_req
                # indique d’appliquer la section v3_req (où subjectAltName pointe vers alt_names)

    
    VERSION COPIABLE :

        sudo openssl req -x509 -nodes -newkey rsa:4096 \
            -keyout /etc/ssl/private/vsftpd.key \
            -out /etc/ssl/certs/vsftpd.crt \
            -days 3650 \
            -config /tmp/vsftpd_openssl.cnf \
            -extensions v3_req


    3) Vérifications 1 :

        openssl x509 -in /etc/ssl/certs/vsftpd.crt -noout -text | grep -A2 "Subject Alternative Name"
            # Cette ligne vérifie que SAN est bien inclu
            # openssl x509 Utilise la sous-commande x509 d’OpenSSL : permet de lire, afficher ou convertir un certificat X.509
            # -in /etc/ssl/certs/vsftpd.crt : Chemin du certificat à analyser
            # -noout : Demande à OpenSSL de ne pas afficher le certificat encodé en Base64 (PEM).
                # Sans cette option, tu aurais aussi tout le bloc -----BEGIN CERTIFICATE----- ... -----END CERTIFICATE----- affiché → pas utile pour la lecture.
            # -text : Demande à OpenSSL d’afficher les informations du certificat en clair (lisibles par un humain) → DN, validité, extensions, SAN, etc
            # | grep -A2 "Subject Alternative Name" :
                # | : envoie la sortie de la commande précédente vers grep.
                # grep "Subject Alternative Name" : cherche la ligne contenant l’extension Subject Alternative Name (SAN).
                # -A2 : affiche aussi les 2 lignes suivantes (After = 2).
                # Utile car la liste des SAN (DNS, IP, etc.) est imprimée sur les lignes juste après.

    
    4) Permissions :

        sudo chown root:root /etc/ssl/private/vsftpd.key
        sudo chmod 600 /etc/ssl/private/vsftpd.key
        sudo chmod 644 /etc/ssl/certs/vsftpd.crt


    5) Activer le FTPS dans le fichier de config FTP :

        nano /etc/vsftpd.conf
            # A ajouter à la suite du fichier
            rsa_cert_file=/etc/ssl/certs/vsftpd.crt
                # Chemin vers le certificat X.509 du serveur
            rsa_private_key_file=/etc/ssl/private/vsftpd.key
                # Chemin vers la clé privée RSA du serveur
            ssl_enable=YES
                # Active TLS

    6) Vérifications 2 :

        systemctl status vsftpd

        sudo ss -tuln | grep :21
            # Vérifie que le service écoute bien sur le port 21
        openssl s_client -connect 172.16.0.1:21 -starttls ftp
            # Test la connexion 