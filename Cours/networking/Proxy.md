Un proxy ou Mandataire HTTP est un serveur qui sert d'intermédiaire entre un client et un serveur internet, surtout pour le trafic web (HTTP/HTTPS). Il agit donc à la couche 7 (Application) du model OSI.


ROLE DU PROXY :

    Son rôle, c’est d’ajouter des fonctions “en plus” par rapport à un simple routeur.

    Voici les rôles les plus fréquents :

        -> Contrôle d’accès / filtrage : autoriser ou bloquer certains sites, catégories, horaires, utilisateurs.
        -> Authentification : obliger les utilisateurs à s’identifier avant d’accéder au web.
        -> Journalisation (logs) : garder une trace de qui a accédé à quoi (utile en entreprise).
        -> Cache : conserver des copies de contenus pour accélérer et économiser la bande passante (utile pour mises à jour, téléchargements répétés).
        -> Sécurité : limiter l’exposition directe, appliquer des règles, parfois analyser le trafic (selon le type de proxy).

    👉 Le routeur décide “où ça va” (routage IP).
    👉 Le proxy décide “est-ce que j’autorise, je filtre, je mets en cache, je trace, etc.” au niveau applicatif.


PLACEMENT DU PROXY :

    Le trajet d’une requête HTTP avec proxy

    Sans proxy :
        Navigateur → routeur (passerelle) → Internet → serveur web

    Avec proxy :
        Navigateur → (routeur) → proxy → Internet → serveur web

    Le routeur reste là pour “acheminer” les paquets jusqu’au proxy.


    Pour “où il tourne physiquement”, il y a plusieurs scénarios (les plus courants) :

        1) Machine dédiée (le cas classique en entreprise)

            Le proxy tourne sur un serveur (machine supplémentaire) dans le réseau interne ou une DMZ.

            Votre PC → routeur/passerelle → serveur proxy → Internet
            C’est très fréquent (Squid, BlueCoat, etc.).

        2) Sur le pare-feu / routeur (possible, surtout sur du matériel pro)

            Certains équipements (pare-feu UTM, appliances) intègrent une fonction proxy :
                le proxy est un service qui tourne dans l’équipement (ou sur un module).
                on parle parfois de “proxy explicite” ou “filtrage web” intégré.

        3) Proxy local sur votre PC (surprise fréquente)

            Un logiciel peut installer un proxy local :
                votre navigateur parle à 127.0.0.1:xxxx
                et ce logiciel relaie ensuite vers Internet (pour filtrer, inspecter, etc.).

            À retenir
                Un proxy n’est pas “un endroit” fixe : c’est un service qui peut tourner :
                sur le routeur/pare-feu, ou sur un serveur à part, ou sur le poste client.

