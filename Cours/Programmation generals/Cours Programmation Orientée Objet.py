# Cours explication sur les librairies Python

'''
Fonctionnement d'une bibliothèque :

    Bibliothèque / Package
    │
    ├── Module 1 (.py)
    │   ├── Classe A
    │   │   ├── Attributs (données de l’objet)
    │   │   └── Méthodes (fonctions qui agissent sur l’objet)
    │   └── Fonctions libres (pas liées à un objet)
    │
    ├── Module 2 (.py)
    │   └── Classe B
    │       ├── Attributs
    │       └── Méthodes
    │
    └── Module 3 ...

Les modules :
    Un module est un fichier Python (.py) qui contient du code (fonctions, classes, variables). 
    C'est comme une étagère où l'on range des livres spécifiques pour une thématique spécifique. Par exemple le module "magie" qui contient des fonctions 
    et classes liées à la magie.

Les classes :
    Une classe est un plan (blueprint) pour créer des objets. 
    Elle définit des attributs (données) et des méthodes (fonctions) qui agissent sur ces données.
    C'est un livre dans l'étagère qui explique comment créer et manipuler un type spécifique d'objet. Exemple : une classe "Summoning" qui créer des objets "Summon" 
    avec des attributs comme "name", "power", "element" et des méthodes comme "summon()", "dismiss()", "attack()".  

Les objets :
    Un objet est une réalisation concrète du plan défini par la classe. 
    Par exemple, si "Summoning" est une classe, alors "FireDragon" pourrait être un objet de cette classe avec des attributs spécifiques 
    (name="FireDragon", power=100, element="fire").   
    On peut créer des objets affectés à aucune variable en appelant directement la classe, par exemple :
        magie.Summoning()
        Ces objets peuvent être utilisés immédiatement, mais on ne peut pas y accéder plus tard car ils ne sont pas stockés dans une variable. Ils sont effémères.
    
Les attributs :
    Ils sont définis avec la méthode spéciale __init__() dans une classe.
        Par exemple :
        class Summoning:
            def __init__(self, name, power, element):
                self.name = name
                self.power = power
                self.element = element
    
        Ici name, power et element sont des paramètres, des variables locales n'existant que dans le cadre de __init__()
        et self.name, self.power et self.element sont des attributs de l'objet, des variables liées à l'objet qui prennent la valeur des paramètres.
        
    Pour créer un objet dragon par exemple :
        FireDragon = Summoning("FireDragon", 100, "fire") # On met les attributs entre les parenthèses de la classe. 

    Si on ne met rien entre les parenthèses, les attributs prennent des valeurs par défaut définies dans la méthode __init__(). 

Les méthodes :
    Les méthodes sont des fonctions définies à l'intérieur d'une classe. Et associées à un objet spécifique. 
    Elles peuvent accéder et modifier les attributs de l'objet.

Les fonctions :
    Elles ne sont associées à aucun objet et peuvent exister par elles-mêmes. Elles peuvent créer des objets tout comme les classes.
    

La syntaxe :
    En Python, la syntaxe X.Y signifie :
    "va chercher l’élément Y qui est défini dans l’espace de noms X".
    Exemple : magie.Summoning.summon() signifie "va chercher la méthode summon() qui est définie dans la classe Summoning de la librairie magie".

'''



# 1) Exemple de script python :

    #!/usr/bin/env python3
        # indique que le script doit ête executé par l'interpréteur python3 situé dans /usr/bin/env
    import paramiko     # bibliothèque pour les connexions SSH

    # --- Création d’un client SSH ---
    client = paramiko.SSHClient()       # Cree un objet client SSH à partir de la classe SSHClient de la librairie paramiko
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())        # Méthode pour accepter les clés inconnues

    # --- Connexion au serveur et authentification ---
    client.connect("192.168.1.10", username="user", password="mypassword")

    # --- Exécution d'une commande ---
    stdin, stdout, stderr = client.exec_command("ls -l /home/user")
    print(stdout.read().decode())

    # --- Transfert de fichier ---
    sftp = client.open_sftp()
    sftp.get("/remote/path/file.txt", "local_file.txt")  # Télécharger
    sftp.put("local_file.txt", "/remote/path/file.txt")  # Envoyer
    sftp.close()

    # --- Déconnexion ---
    client.close()

