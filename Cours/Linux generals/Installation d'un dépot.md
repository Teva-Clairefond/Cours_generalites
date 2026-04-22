# Installation d'un dépot :

sudo apt update
sudo apt upgrade

sudo apt install apt-transport-https curl gnupg2 lsb-release
    # Avec apt-transport-https pour télécharger depuis un lien https
    # Curl pour télécharger depuis le net
    # gnupg2 pour manipuler les clés GPG
    # lsb-release pour avoir automatiquement le nom de ma version du système et installer un paquet compatible

curl -L https://example.com/key.gpg | sudo gpg --dearmor -o /usr/share/keyrings/mondepot.gpg
    # -L suit automatiquement les redirections HTTP (utile si l’URL redirige vers un autre serveur)
    # https://example.com/key.gpg lien URL de la clé GPG
    # | redirige le flux de sortie standard (stdout) vers l'entrée de la prochaine commande (stdin)
    # --dearmor Convertie la clé GPG ACII en binaire
    # -o écrit cette clé binaire dans le fichier /usr/share/keyrings/mondepot.gpg

echo "deb [signed-by=/usr/share/keyrings/mariadb.gpg] https://deb.mariadb.org/10.11/debian $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/mariadb.list
    # echo "..." : affiche "..." dans le terminal
    # deb : indique que c'est un dépot de paquet en binaire
    # [signed-by=/usr/share/keyrings/mariadb.gpg] : Vérifie que les paquets téléchargés depuis ce dépôt sont signés avec la clé GPG stockée dans /usr/share/keyrings/mariadb.gpg.
    # https://deb.mariadb.org/10.11/debian : URL de dépôt où sont les paquets binaires
    # $(lsb_release -cs) : Renvoie nom de la version débian de mon système
    # main : paquet principal du dépot
    # tee : tee écrit ce qu’il reçoit dans le fichier /etc/apt/sources.list.d/mariadb.list
    #       Par défaut, tee écrit aussi sur la sortie standard (donc ça s’affiche à l’écran).

sudo apt update

sudo apt install mariadb