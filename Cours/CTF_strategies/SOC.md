utiliser sort car les logs ne sont pas toujours dans l'ordre.

## Définitions :

lecture -> confidentialité compromise
écriture sur le serveur -> intégrité compromise
execution d'une backdoor -> Initialisatiion du reverse shell

Backdoor -> Commande persistante permettant un accès distant, typiquement via un reverse shell.
Reverse shell -> Technique informatique qui permet de rediriger sur un ordinateur local l'entrée et la sortie d'un shell vers un ordinateur distant, au travers d'un service capable d'interagir entre les deux ordinateurs. L'un des avantages de cette technique est de rendre un shell local accessible depuis ce serveur distant sans être bloqué par un pare-feu.



## Regex :
selectionner les adresses ip avec grep : grep -oE '\b([0-9]{1,3}\.){3}[0-9]{1,3}\b'
    -o : n’affiche que la partie qui matche
    -E : active les regex étendues
