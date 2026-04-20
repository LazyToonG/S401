#!/bin/bash

SSH_CONFIG="/etc/ssh/sshd_config"


if grep -q "^GatewayPorts yes" $SSH_CONFIG; then 
  echo "Désactivation de GatewayPorts..."
  
  # Supprime la ligne "GatewayPorts yes"
  sed -i '/^GatewayPorts yes/d' $SSH_CONFIG
fi


systemctl restart ssh



