Cours Active Directory


Annuaire LDAP

Domaine AD : Ensemble d'ordinateurs (windows pro) qui partagent la même sécurité

Sécurité (en informatique) = KKK (ki koi komment) = Identifier les utilisateurs, les ressources, et les droits d'accès

Kerberos : Méchanisme de validation d'ouverture de session 
    - Le client Kerberos (sur un ordi du réseau) envoie le login et mdp au serveur Kerberos (sur le DC) 
    - Le serveur valide le login et le mdp
    - Le serveur fournit au client le jeton Kerberos (validation d'ouverture de session). Le jeton contient les Access Control List (ACL) = les autorisations de l'user !
        - le rôle du jeton kerberos est l'optimisation : Quand l'user va effectuer des requêtes sur des machines du domaine, il va présenter son jeton pour montrer ses
        droits.
        - Il a une durée de vie de 10h.

AD NE PEUT PAS FONCTIONER SANS SERVEUR DNS !!! Il est pratique de l'installer sur le DC.
    