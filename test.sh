#! /bin/bash

docker build -t exolever/django-mentions:latest .

# Force clear all error images
docker images | grep 'django-mentions\|none' | awk '{print $3}' | xargs docker rmi --force
