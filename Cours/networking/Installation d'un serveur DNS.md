Installation d'un serveur DNS :


1) Installation des paquets :

    sudo apt install bind9 bind9utils
        # bind9 : Démon DNS
        # bind9utils
        # outils utiles (ex : named-checkconf, named-checkzone,...)

2) Déclaration de la zone DNS

    # Différence entre un domaine et une zone DNS :
        Le domaine est un nom, un territoire. La zone est un territoire mais administré, sous-contrôle d'un royaume.
        Les sous-zones sont les villes et les quartiers de ce royaume, les noms d'hote sont les maisons, et les bâtiments, et les enregistrements DNS
        sont des infos sur les maisons ou le quartier comme l'adresse exacte (enregistrement A ou AAAA), le surnom de la maison (CNAME), 
        la boite au lettre du quartier (MX), la mairie du quartier (NS)...
        Le nom d'hôte est le nom de la maison : maison1
        Le nom de domaine hierarchique correspond à l'addresse complète : maison1.quartier3.ville5
    
    # Différences maître - esclave :
        Le maître correspond au serveur DNS principal qui a autorité, l'esclave est un serveur secondaire qui peut résoudre les noms de domaines mais qui est
        une copie du serveur principal maître. L'esclave ne peut pas modifier les enregistrements.


    sudo nano /etc/bind/named.conf.local
        zone "exemple.local" {      
            # Déclaration d'une zone DNS nommée exemple.local
            type master;    
                # Ce serveur est le maître (source) pour cette zone ; c’est lui qui contient le fichier de zone d’origine. (Autre valeur : slave pour esclave)
            file "/etc/bind/db.exemple.local"; 
                # chemin du fichier de zone qui contient les enregistrements DNS (A, NS, MX, etc.) pour cette zone.
        };

3) Création du fichier de zone DNS

    # IL FAUT ENLEVER LES COMMENTAIRES POUR QUE LE FICHIER FONCTIONNE !!!

    sudo nano /etc/bind/db.exemple.local
        $TTL    604800
            # TimeTolive : Temps durant lequel le cache du client va conservé l'IP de sa machine cible, avant de redemander au resolveur DNS.
            # Un client demande à envoyer un paquet à pc1. Le serveur DNS local lui donne l'IP.
            # Puis le client va contacter pc1 avec son IP. Durant le TTL, le client n'a pas besoin de redemander l'ip au serveur DNS et 
            # peut directement envoyer au pc1.

        @       IN      SOA     dns.exemple.local. admin.exemple.local. (
            # SOA : Start Of Authority indique le serveur qui a l'autorité
            # dns.exemple.local. : Serveur maître, serveur DNS du réseau local, nom de domaine FQDN (Fully Qualified Domain Name) qui commence à la racine (.)
            # admin.exemple.local : Stockage du mail de l'admin sous forme de nom de domaine, inutilisable sans outils extérieurs.
                    2         ; Serial      # Num de version de la zone, dois être incrémenté à chaque modification
                604800         ; Refresh    # Si le numéro de série (serial) du maître est plus grand que celui que l’esclave connaît, 
                                            # ça veut dire que la zone a été modifiée.
                                            # L’esclave va alors télécharger la version mise à jour pour rester à jour
                                            # Ici, tous les 604800 secondes (7 jours), l'esclave check le serial du maître
                86400         ; Retry       # Si l'esclave (serveur secondaire) n'a pas pu contacter le maître (serveur DNS principal) 
                                            # alors il rééssayera dans 86400 secondes (1 jour).
                2419200         ; Expire    # Si l’esclave ne peut pas contacter le maître pendant la durée Expire, il considère sa copie obsolète
                                            # Dans ce cas : l’esclave arrête de répondre aux requêtes pour cette zone ou répond avec une erreur 
                                            # de serveur DNS (SERVFAIL)
                604800 )       ; Negative Cache TTL;    # Negative TTL : durée pendant laquelle une réponse négative (nom inexistant) peut être mise en cache.

        @       IN      NS      dns.exemple.local.  ;
            # Définition du serveur DNS, par son nom de domaine FQDN

        dns     IN      A       192.168.1.10    ;
            # Adresse IP locale du serveur DNS lui-même

        pc1     IN      A       192.168.1.20
        imprimante IN   A       192.168.1.30
            # Exemple d’hôtes dans le LAN
            # Tous les noms que l'on souhaite résoudre doivent se trouver dans le fichier

    sudo chown root:bind /etc/bind/db.exemple.local
        # Le fichier a pour propriétaire l'utilisateur root et le groupe bind (groupe qui peut gérer le serveur DNS)
    sudo chmod 640 /etc/bind/db.exemple.local
        # Défini les permissions du fichier : rw- pour l'utilisateur ; r-- pour le groupe ; --- pour les autres

4) Vérifier la configuration

    sudo named-checkconf
        # Vérifie la syntaxe des fichiers de configuration bind, si rien est affiché, pas d'erreur
    sudo named-checkzone exemple.local /etc/bind/db.exemple.local
        # named-checkzone <zonename> <fichier_de_zone> : vérifie la cohérence de la zone (format, SOA, enregistrements). 
        # Te retourne OK si tout va bien, sinon des erreurs indiquant la ligne fautive.

5) Redémarrer le service :

    sudo systemctl restart bind9
    sudo systemctl enable bind9
    sudo systemctl status bind9

6) Configuration du serveur DHCP :

    # Voir le fichier [Installation d'un serveur DHCP](/Cours/networking/Installation%20d'un%20serveur%20DHCP.md)

7) Tester la résolution DNS : 3 options

    Sur la machine cliente :
        Option 1) - nslookup pc1.exemple.local 192.168.1.10
            # nslookup : outil de diagnostique DNS
            # pc1.exemple.local : Le nom de domaine que l'on souhaite résoudre
            # 192.168.1.10 : Adresse IP du serveur DNS a interroger
            # La commande envoie une requête DNS au serveur et affiche la réponse
        Option 2) - dig @192.168.1.10 pc1.exemple.local
            # dig : outil moderne et verbeux pour interroger DNS (souvent fourni par dnsutils ou bind-utils)
            # @192.168.1.10 : indique explicitement le serveur à interroger (notation @serveur).
            # pc1.exemple.local : le nom de domaine à interroger.
            # La commande interroge 192.168.1.10 pour le nom demandé et affiche un rapport complet (header, question, réponse, autorité, supplémentaires, stats)
        Option 3) - host imprimante.exemple.local 192.168.1.10
            # host : outil simple pour résoudre un nom ou une IP (résumé, facile à lire).
            # imprimante.exemple.local : Nom de domaine à résoudre
            # 192.168.1.10 : serveur DNS à interroger 
            # La commande envoie une requête DNS au serveur indiqué (type par défaut A si c’est un nom ; si tu donnes une IP il fait une recherche inverse PTR)
            # PTR = Pointer Record, enregistrement inverse de A qui attribue un nom de domaine a une IP donnée.

8) Faire en sorte que le DNS local redirige les noms inconnus (forwarders) :

    nano /etc/bind/named.conf.options
        options {
            directory "/var/cache/bind";
                # Répertoire de travail de bind où sont stockées les données de cache et les fichiers temporaires
            recursion yes;
                # recursion yes; : permet au serveur de faire des requêtes récursives pour des noms qu’il ne connaît pas
            allow-query { any; };
                # Tous les clients peuvent formuler des requêtes DNS
            allow-recursion { localnets; localhost; };
                # allow-recursion { localnets; localhost; }; : ne permet la récursion qu’aux clients locaux (sécurité)

            forwarders {                # Partie intéressante : Elle fait la redirection vers les serveurs publiques pour CE serveur DNS,
                                        # mais de façon générale la redirection (par exemple pour une car NAT) se fait dans /etc/resolv.conf
                8.8.8.8;
                1.1.1.1;
            };
                # DNS publics vers lesquels BIND redirigera les requêtes inconnues
            
            dnssec-validation auto;
                # DNSSEC (Domain Name System Security Extensions) ajoute une signature cryptographique aux enregistrements DNS.
                # dnssec-validation auto; = “Active la vérification automatique de l’authenticité des réponses DNS signées par DNSSEC”.
                # Pourquoi ? : Si un client demande une résolution DNS au serveur (Nom -> IP) et qu'un attaqauant se place en tant que serveur DNS,
                # il peut rediriger vers une adresse ip frauduleuse et donc un sevreur frauduleux.

            listen-on { 127.0.0.1; 192.168.1.10; };
                # listen-on : définit les interfaces côté serveur qui peuvent écouter les requêtes
        };

9) Firewall : ouvrir le port DNS :

    iptables -A INPUT -p udp --dport 53 -j ACCEPT
    iptables -A INPUT -p tcp --dport 53 -j ACCEPT

10) Reverse DNS :

    nano /etc/bind/named.conf.local
        zone "1.168.192.in-addr.arpa" {
            # in-addr.arpa : Zone inverse pour associer l'IP au nom de domaine PTR
            # Le nom de zone 1.168.192.in-addr.arpa est la forme inversée des octets d’adresse : il couvre 192.168.1.0/24.
            # Avec une IP type B on aurait 168.192.in-addr.arpa
            # En reverse DNS on écrit les octets à l’envers
            type master;
            file "/etc/bind/db.192.168.1";
        };

    nano /etc/bind/db.192.168.1
        $TTL    604800
        @       IN      SOA     dns.exemple.local. admin.exemple.local. (
                                2025091401 ; Serial (à incrémenter à chaque modif)
                                604800     ; Refresh (7 jours)
                                86400      ; Retry (1 jour)
                                2419200    ; Expire (28 jours)
                                604800 )   ; Negative Cache TTL
        
        # Serveur DNS autoritaire de la zone
                IN      NS      dns.exemple.local.
        
        # Résolution inverse (IP → nom)
        1       IN      PTR     routeur.exemple.local.
        10      IN      PTR     pc1.exemple.local.
        20      IN      PTR     pc2.exemple.local.
            # Associe l’IP 192.168.1.20 à pc2.exemple.local. , adresse FQDN
        100     IN      PTR     imprimante.exemple.local.

11) Logs et diagnostic :

    sudo tail -f /var/log/syslog | grep named
        # tail -f : suit le fichier en temps réel (comme un flux continu).
        # grep named : filtre seulement les lignes contenant named (le démon BIND).
    dig pc1.exemple.local @192.168.1.10
    dig +trace example.com
        # Interroge le serveur racine (.)
        # Reçoit la liste des TLD (.com)
        # Interroge le serveur TLD .com
        # Reçoit le NS pour example.com
        # Interroge le serveur autoritatif de example.com
        # Reçoit l’IP finale

12) Restart et reload :

    sudo systemctl restart bind9
    sudo systemctl enable bind9
    sudo systemctl status bind9


REMARQUE : 

Si des modifications sont faites dans le fichier /etc/bind/db.exemple.local, alors il faut incrémenter le compteur qui se trouve dans le fichier puis relancer bind9