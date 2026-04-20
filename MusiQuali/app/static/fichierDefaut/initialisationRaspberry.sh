#!/bin/bash

# Vérifie que le script est exécuté en root
if [ "$EUID" -ne 0 ]; then #EUID = Effective User ID,  -ne = not equal, 0 = l’ID de l’utilisateur root
  echo "Veuillez exécuter ce script en tant que root (sudo)."
  exit 1
fi

echo "Vérification de SSH..."

# 1. Vérifier si openssh-server est installé
if ! dpkg -l | grep -q openssh-server; then
  echo "openssh-server n'est pas installé."
  echo "Installation de openssh-server..."
  apt update
  apt install -y openssh-server
else
  echo "openssh-server est déjà installé."
fi

# 2. Vérifier si le service SSH est actif
if systemctl is-active --quiet ssh; then
  echo "Le service SSH est déjà actif."
else
  echo "Le service SSH n'est pas actif."
  echo "Activation et démarrage du service SSH..."
  systemctl enable ssh
  systemctl start ssh
fi

# 3. Vérification finale
if systemctl is-active --quiet ssh; then
  echo "SSH est maintenant activé et fonctionnel."
else
  echo "Une erreur est survenue lors de l'activation de SSH."
fi
