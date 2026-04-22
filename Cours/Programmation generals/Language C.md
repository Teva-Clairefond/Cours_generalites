

# tableau pour comprendre les pointeurs

|  type  |  nom  |  adresse  |  contenu  |
------------------------------------------
|  int   |   i   |   0x123   |     5     |
|  int*  |   j   |   0x456   |   0x123   |
|  int** |   k   |   0x189   |   0x456   |

Ici la variable k contient l'adresse de j et donc pointe vers j.
j contient l'adresse de i et pointe vers i.
i contient la valeur 5.

