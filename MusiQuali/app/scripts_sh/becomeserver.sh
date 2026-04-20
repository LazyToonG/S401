#!/bin/bash

SSH_CONFIG="/etc/ssh/sshd_config"
if ! grep -q "^GatewayPorts yes" $SSH_CONFIG; then
  echo "Activation de GatewayPorts..."
  echo "GatewayPorts yes" >> $SSH_CONFIG
fi

echo "Redémarrage du service SSH..."
systemctl restart ssh

#permet aux machines qui ont nom@ip et le mdp d'ouvrir un port de leur choix
