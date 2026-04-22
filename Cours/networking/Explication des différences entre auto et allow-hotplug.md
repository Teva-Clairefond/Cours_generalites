Explication des différences entre auto {} et allow-hotplug {} dans le fichier /etc/network/interfaces



Explication générale :

    auto → configure l’interface au boot, quoi qu’il arrive.
    allow-hotplug → configure l’interface uniquement si le noyau/udev la voit comme présente.

I] Fonctionnement :

    1) La carte réseau (le matériel)

        C’est ton périphérique physique : carte Ethernet, carte Wi-Fi, adaptateur USB, etc.
        Tant qu’elle n’est pas présente (branchée ou intégrée à la machine), il n’y a rien à configurer.

    2) Le noyau (le pilote)

        Le noyau détecte le matériel via un pilote (e1000, rtl8169, iwlwifi, etc.).
        Quand le pilote charge correctement, il crée une interface logique (par ex. eth0, wlan0, enp3s0).
        C’est à ce moment-là que udev émet un événement → et que allow-hotplug peut réagir.
        Donc : interface “détectée” = le noyau a reconnu le périphérique et a créé l’interface réseau associée.

    3) L’interface réseau (niveau logiciel)

        Une fois l’interface créée, elle peut être activée (ifup) ou laissée en attente.


II] Exemples avec 2 cas :

    Cas A) : Carte intégrée (Ethernet)

        - avec auto : L’interface est montée au boot, même si aucun câble n’est branché.

        - avec allow-hotplug : L’interface est aussi montée au boot, car le noyau détecte la carte dès le départ.

    
    Cas B) : Carte amovible (USB Wi-Fi / USB Ethernet)

        - avec auto : Si la carte n’est pas branchée au boot → non configurée. Si on la branche après → il faut la monter manuellement avec ifup.

        - avec allow-hotplug : Si la carte n’est pas branchée au boot → rien ne se passe. Si on la branche après → udev déclenche automatiquement la configuration.


