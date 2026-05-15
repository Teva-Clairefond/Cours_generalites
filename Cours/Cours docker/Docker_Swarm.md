# Docker_Swarm


## Explication :

Pour pouvoir prendre des décisions, le cluster nécessite un vote de majorité par les managers. Il faut donc le nombre de managers en activité soit toujours strictement supérieur au nombre de managers total. Ce nombre minimum de manager, qui dépend du nombre total, est appelé quorum.

Le nombre de pannes correspond au nombre de managers qui peuvent tomber en panne sans que le cluster ne puisse plus prendre de décision.

quorum : (Nombre de panne / 2) + 1

https://blog.stephane-robert.info/docs/conteneurs/orchestrateurs/docker-swarm/

