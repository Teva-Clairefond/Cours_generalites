Installation d'un serveur DHCP 

Explications :

    Mode de fonctionnement du DHCP (Dynamic Host Configuration Protocol) :
        1 - Client -> Serveur : DHCP discover
            # Recherche d'un serveur DHCP par le client
        2 - Serveur -> CLient : DHCP offer
            # Le serveur DHCP fait une proposition avec une adresse IP possible pour le client
        3 - Client -> Serveur : DHCP request
            # Demande effective de cette adress IP
        4 - Serveur -> CLient : DHCP ACK
            # Acceptation de la demande et attribution de l'adresse IP au client




1) Installation et association du serveur DHCP à la carte réseau à laquelle on attribue une IP statique :

    
    sudo apt install isc-dhcp-server -y
	
    sudo nano /etc/default/isc-dhcp-server
        INTERFACESv4="nom_de_l'interface_réseau_qui_va_agir_en_tant_que_serveur_DHCP"
        INTERFACESv6=""

    sudo nano /etc/network/interfaces
        auto enp0s8
            # auto : toujours au démarrage, même si l’interface est absente ou non branchée.
            # allow-hotplug : seulement quand l’interface est détectée (branchée / ajoutée). Voir fichier explicatif sur la différence entre auto et allow-hotplug
        iface enp0s8 inet static
        address 192.168.1.1       
            # Attribue une adresse IP locale statique à la carte LAN qui héberge le serveur DHCP
            # Ne dois pas être l'adresse du sous-réseau, donc ne dois pas terminer par .0 puisque c'est le sous-réseau qui termine de cette manière
        netmask 255.255.255.0
        gateway 192.168.1.2
            # Souvent dans un réseau NAT lié à des machines virtuelles, il y a la machine hôte sur X.X.X.1 et la gateway sur X.X.X.2.

2) Configuration du serveur DHCP :

        
    sudo nano /etc/dhcp/dhcpd.conf

        option domain-name "exemple.local";
            # Nom du domaine (optionnel), correspond au nom complet des appareils du réseau (du domaine) exemple : imprimante.exemple.local  

        option domain-name-servers 192.168.1.1;
            # Adresse de la machine qui fait office de serveur DNS (ici la carte LAN locale)

        default-lease-time 600;
        max-lease-time 7200;
            # Durée du bail (lease) pour une IP

        subnet 192.168.1.0 netmask 255.255.255.0 {
            range 192.168.1.100 192.168.1.200;
                # La range ne doit pas couvrir l'adresse IP fixe du serveur DHCP pour qu'il n'y ait pas de conflits
            option routers ip_de_la_gateway;
            option broadcast-address 192.168.1.255;
        }
        # Définition du réseau à distribuer, c'est l'interface LAN qui représente le routeur côté réseau local
        
        host imprimante {
            # "imprimante" est juste un nom au sein du fichier DHCP ce n'est pas forcément le nom d'hôte de la machine sur le réseau. 
            # Puisque cela nécessite une résolution DNS
        hardware ethernet 00:AA:BB:CC:DD:EE;
            # Adresse MAC de la machine pour l'identification
        fixed-address 192.168.1.10;
            # Cette ligne sert à attribuer une adresse IP fixe à la machine
        }

    sudo systemctl restart isc-dhcp-server



3) Démarrer et activer le service :

    sudo systemctl restart isc-dhcp-server
    sudo systemctl enable isc-dhcp-server
    sudo systemctl status isc-dhcp-server
    sudo systemctl restart networking   OU   sudo systemctl ifdown enp0s8 ; sudo systemctl ifup enp0s8


4) Vérifier le fonctionnement :

    ip addr
        # On vérifie l'attribution de l'IP à la carte réseau local

    journalctl -f
        # journalctl : lit le journal systemd (journald).
        # Ce journal est stocké dans un format binaire et contient non seulement le message de log,
        # mais aussi des métadonnées structurées (nom de l’unité systemd, PID, identifiant syslog, priorité, exécutable, boot id, etc.).    
        # -f : (follow) ouvre le journal et stream les nouvelles entrées au fur et à mesure qu’elles arrivent

    # Les requêtes DHCP doivent y apparaître

