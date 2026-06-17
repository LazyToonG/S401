#!/bin/bash

echo "Configration MusiQuali"

# 1. Setup
bash setup.sh

# 2. Activation venv
source venv/bin/activate

# 3. Lancement app
echo "Démarrage Flask..."
echo -e "\033[32mHTTPS : https://127.0.0.1\033[0m"
echo -e "\033[33mCtrl + clic pour ouvrir le lien\033[0m"
echo -e "\033[33mCtrl + C pour arrêter le script\033[0m"

python3 main.py
