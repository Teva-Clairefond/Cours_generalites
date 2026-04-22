# Le masque de sous-réseau


## Définition

Le masque de sous réseau permet de définir pour une adresse IPv4 les adresses disponibles pour le sous réseau.

Il peut être exprimé de deux manières communes :
    - Par une addresse IPv4 en octet : Exemple : 255.255.255.0
    - Par un nombre de bit : /24


## Cas général :

Une adresse IPv4 est constituée de 32 bits soit 4 octets, lorsque l'on marque /24 cela signifie que 24 bits sur les 32 seront communs aux machines du sous réseau, soit : 
    => bits d'adresses disponibles pour le sous-réseau = 32 - 24 = 8 bits
    => Nombre d'adresses disponibles pour le sous-réseau = 2^8 = 256

### Composition du sous-réseau (exemple avec /24):
    - Adresse du sous-réseau :  xxx.xxx.xxx.0
    - Les adresses possibles du sous-réseau : xxx.xxx.xxx.1 -> xxx.xxx.xxx.254
    - Adresse de broadcast : xxx.xxx.xxx.255


## Cas de masque non-standard (/25 /26 ...)

Parfois le nombre de bits ne correspond pas à un nombre rond d'octets (8, 16, 24), par exemple /25. Cependant cela fonctionne exactement de la même manière.

Dans ce cas il y a 32 - 25 = 7 bits pour les adresses du sous-réseau 
    => 2^7 = 128 adresses possibles 

### Composition du sous-réseau (Exemple avec /25):
    - Adresse du sous-réseau :  xxx.xxx.xxx.0
    - Les adresses possibles du sous-réseau : xxx.xxx.xxx.1 -> xxx.xxx.xxx.126
    - Adresse de broadcast : xxx.xxx.xxx.127


## Découpage d'un réseau déjà existant :

Imaginons que nous ayons une entreprise avec différents services. Nous avons un sous-réseau /24 commun à toute l'entreprise, mais nous aimerions avoir des sous-réseaux pour chacun des 4 service de l'entreprise.

Ainsi nous allons découper notre /24 en 4, c'est à dire que chaque sous-sous-réseaux comportera un masque de /26, avec 2 bits pour définir le sous-sous-réseau. Ces 2 bits sont dis "empruntés".

![https://medium.com/%40TheClueMatrix/the-great-ip-addressing-subnetting-unblock-from-confusion-to-clarity-66035a83592a](/Images/sous-sous-reseaux.jpg)

![https://www.gatevidyalay.com/subnetting-in-networking-routing-table/?utm_source=chatgpt.com](/Images/sous-sous-reseaux2.jpg)

Ici le premier sous-sous-réseau :
    - Adresse du sous-sous-réseau :  xxx.xxx.xxx.0
    - Les adresses possibles du sous-sous-réseau : xxx.xxx.xxx.1 -> xxx.xxx.xxx.62
    - Adresse de broadcast : xxx.xxx.xxx.63

Le deuxième sous-sous-réseau :
    - Adresse du sous-sous-réseau :  xxx.xxx.xxx.64
    - Les adresses possibles du sous-sous-réseau : xxx.xxx.xxx.65 -> xxx.xxx.xxx.126
    - Adresse de broadcast : xxx.xxx.xxx.127

Le troisième sous-sous-réseau :
    - Adresse du sous-sous-réseau :  xxx.xxx.xxx.128
    - Les adresses possibles du sous-sous-réseau : xxx.xxx.xxx.129 -> xxx.xxx.xxx.190
    - Adresse de broadcast : xxx.xxx.xxx.191

Le quatrième sous-sous-réseau :
    - Adresse du sous-sous-réseau :  xxx.xxx.xxx.192
    - Les adresses possibles du sous-sous-réseau : xxx.xxx.xxx.193 -> xxx.xxx.xxx.254
    - Adresse de broadcast : xxx.xxx.xxx.255