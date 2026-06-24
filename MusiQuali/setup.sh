#!/bin/bash

echo ">>Setup MusiQuali<<"

# venv
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi

source venv/bin/activate

# dépendances


# SSL directement ici (PLUS de fichier externe)
if [ ! -d "nginx" ]; then
  mkdir nginx
fi

bash setup_ssl.sh

echo "✔ Setup terminé"
