#!/bin/bash

echo ">>Configuration MusiQuali<<"

# 1. Setup
bash setup.sh

# 2. Activation venv
source venv/bin/activate

# 3. Lancement app
echo ">>Démarrage Flask..."
# Modification ici : on ajoute le port 8000 dans l'affichage
# echo -e "\033[32mHTTPS : https://127.0.0.1:8000\033[0m"
# echo -e "\033[33mCtrl + clic pour ouvrir le lien\033[0m"
# echo -e "\033[33mCtrl + C pour arrêter le script\033[0m"

python3 main.py