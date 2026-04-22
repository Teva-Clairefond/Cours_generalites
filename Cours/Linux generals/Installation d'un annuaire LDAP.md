Installation d'un annuaire LDAP

Explications :

    Définition :

    Un annuaire LDAP est une base de données spécialisée conçue pour stocker et organiser des informations sur des objets (utilisateurs, groupes, périphériques, services, etc.) dans un réseau. On l’appelle « annuaire » car sa structure est hiérarchique et souvent utilisée comme un répertoire téléphonique numérique : vous pouvez chercher des objets en fonction de différents attributs, comme le nom, l’adresse e-mail, le rôle, etc.

    Exemples d’utilisations typiques :
        Authentification centralisée des utilisateurs dans une entreprise.
        Gestion des droits d’accès à des ressources réseau (fichiers, applications).
        Répertoire des contacts et des services disponibles sur un réseau.


    Structure hiérarchique (arborescence) :

    L’annuaire LDAP est organisé comme un arbre, appelé DIT (Directory Information Tree).
        - la racine hierarchique correspond aux Domains Components (dc)
        - Ensuite il y a les Organisationnal Units (ou) qui sont les branches
        - Enfin il y a les Common Names (cn) qui sont les feuilles de l'arbre, les éléments des ou

        dc=tesla,dc=com         ← Racine du domaine LDAP
        ├─ ou=utilisateurs       ← Conteneur logique
        │   ├─ cn=John           ← Objet utilisateur
        │   └─ cn=Alice
        └─ ou=groupes
            └─ cn=Admins         ← Objet groupe



Installation :

https://www.digitalocean.com/community/tutorials/how-to-install-and-configure-openldap-and-phpldapadmin-on-ubuntu-16-04


Attention : Avec nginx il faut que dans /etc/sites-available le fichier de config du site pointe vers /usr/share/phpldapadmin/htdocs :

        root /usr/share/phpldapadmin/htdocs;