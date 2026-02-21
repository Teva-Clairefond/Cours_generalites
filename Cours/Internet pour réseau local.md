Internet pour réseau local :

Contexte :

    Un réseau local est connecté à un routeur doté d'une carte LAN et d'une carte NAT.
    La carte LAN reçoit les paquets du réseau, la transmet à la carte NAT, qui les envoient vers internet.
    Lorsque les paquets sortent de la carte NAT, ils prennent pour IP source celle de la carte NAT, c'est le MASQUERADE.

OPTION A] Commandes avec iptables :

    sudo sysctl -w net.ipv4.ip_forward=1
        # sysctl : Sert à lire ou modifier les paramètres du noyau Linux
        # -w : "write" modification des paramètres
        # net.ipv4.ip_forward : Paramètre qui indique la politique de gestion des paquets destinés à un autre réseau (Agir en tant que routeur ou non)
        # Ce paramètre peut prendre la valeur de =1 : le noyau accepte de faire suivre les paquets d’une interface à l’autre → la machine devient un routeur IP
        #                                        =0 : comportement par défaut sur une machine classique → elle n’agit pas comme un routeur

    sudo iptables -A FORWARD -i eth1 -o eth0_NAT -j ACCEPT 
        # -A FORWARD : Gère le passage de paquets entre différentes interfaces réseaux
        # Autorise les paquets entrant sur eth1 et sortant par eth0

    sudo iptables -t nat -A POSTROUTING -o eth0_NAT -j MASQUERADE
        # -t nat : La règle concerne la table NAT (Network Address Translation)
        # -A POSTROUTING : La règle s'applique après le traitement du paquet par le routage
        # -o eth0 : "out" La règle s'applique aux paquets sortant de la carte eth0 NAT
        # -j MASQUERADE : La règle consiste à remplacer l'IP source du paquet par l'IP de la carte eth0 NAT
        # Donc cette règle consiste à remplacer l'IP source en sortie de la carte eth0 NAT

    sudo iptables -A FORWARD -i eth0 -o eth1_LAN -m state --state ESTABLISHED,RELATED -j ACCEPT
        # Autorise les paquets entrant par la NAT et sortant par la LAN si la connexion a déjà été établie et liée.



OPTION B] Commandes avec ufw :

1)
    sudo ufw enable
    sudo ufw default allow routed                       # Active la politique par défaut immédiatement mais pas de façon permanente au démarrage
    
    sudo sysctl -w net.ipv4.ip_forward=1

    sudo nano /etc/ufw/sysctl.conf
        net/ipv4/ip_forward=1                           # Cette ligne doit être décommentée

2) Autoriser le routage entre LAN et NAT
    sudo nano /etc/ufw/before.rules
        *nat                                            # Ajouter ce bloc avant la ligne *filter
        :POSTROUTING ACCEPT [0:0]                 
        -A POSTROUTING -o eth0_NAT -j MASQUERADE
        COMMIT
                                                        
        -A FORWARD -i eth1 -o eth0_NAT -j ACCEPT                                            # Autoriser le forwarding dans ufw
        -A FORWARD -i eth0_NAT -o eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT

3)
    sudo nano /etc/default/ufw  
        DEFAULT_FORWARD_POLICY="ACCEPT"                 # Active la politique par défaut au démarrage


4)
    sudo ufw disable
    sudo ufw enable                                     # ATTENTION : Cette commande fait foirer les connexions SSH, il faut redémarrer les VM
