#! /bin/bash

docker build -t exolever/django-exo-mentions:latest .

# Force clear all error images
docker images | grep 'django-exo-mentions\|none' | awk '{print $3}' | xargs docker rmi --force
