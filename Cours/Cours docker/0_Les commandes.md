# Cours docker : Les commandes

Source :
https://blog.stephane-robert.info/docs/conteneurs/moteurs-conteneurs/docker/cli/#tirer-g%C3%A9rer-et-pousser-des-images-docker


## Images Docker

```bash
docker pull nginx # Télécharge la dernière image nginx
docker pull nginx:1.21.0 # Télécharge une version précise
docker build -t mon_app . # Construit une image à partir du Dockerfile courant
docker images # Liste les images locales
docker image ls # Variante plus explicite de docker images
docker rmi mon_app # Supprime une image locale
docker tag mon_app mon_compte/mon_app:latest # Ajoute un tag avant envoi vers un registre
docker push mon_compte/mon_app:latest # Envoie l'image vers Docker Hub ou un registre privé
```

## Conteneurs Docker

```bash
docker run nginx # Lance un conteneur au premier plan
docker run -d nginx # Lance un conteneur en arrière-plan
docker run -d --name mon_nginx nginx # Lance un conteneur nommé
docker run --name test-ubuntu ubuntu:24.04 bash -lc 'echo "Docker OK"' # Lance un test simple
docker ps # Liste les conteneurs en cours d'exécution
docker ps -a # Liste tous les conteneurs, même arrêtés
docker container ls -a # Variante plus explicite de docker ps -a
docker logs test-ubuntu # Affiche les logs d'un conteneur
docker exec -it mon_nginx /bin/bash # Ouvre un shell dans un conteneur actif
docker stop mon_nginx # Arrête un conteneur
docker restart mon_nginx # Redémarre un conteneur
docker rm test-ubuntu # Supprime un conteneur arrêté
```

## Volumes Docker

```bash
docker volume create mon_volume # Crée un volume persistant
docker volume ls # Liste les volumes disponibles
docker run -d --name nginx_volume -v mon_volume:/usr/share/nginx/html nginx # Monte un volume dans un conteneur
docker run -d --name nginx_mount --mount type=volume,source=mon_volume,target=/usr/share/nginx/html nginx # Syntaxe complète avec --mount
docker volume rm mon_volume # Supprime un volume inutilisé
```

## Réseaux Docker

```bash
docker network create mon_reseau # Crée un réseau personnalisé
docker network ls # Liste les réseaux disponibles
docker run -d --name web --network mon_reseau nginx # Lance un conteneur sur un réseau précis
docker network inspect mon_reseau # Affiche le détail d'un réseau
docker network rm mon_reseau # Supprime un réseau inutilisé
```

## Nettoyage

```bash
docker system prune # Supprime les ressources inutilisées
docker system prune -a # Nettoyage plus agressif, y compris les images non utilisées
docker image prune # Supprime les images dangling
docker volume prune # Supprime les volumes non utilisés
docker network prune # Supprime les réseaux non utilisés
```

## Surveillance et diagnostic

```bash
docker events # Affiche les événements Docker en temps réel
docker events --filter "type=container" # Filtre sur les événements liés aux conteneurs
docker events --filter "event=start" # Filtre sur un type d'action précis
docker events --filter "image=nginx" # Filtre sur une image précise
docker events --since '2024-10-10T12:00:00' --until '2024-10-10T13:00:00' # Filtre sur une période
```

## Raccourcis utiles

```bash
docker images # Images locales
docker ps -a # Tous les conteneurs
docker volume ls # Volumes existants
docker network ls # Réseaux existants
```
