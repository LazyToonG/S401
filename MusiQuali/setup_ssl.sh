#!/bin/bash

CERT="nginx/cert.pem"
KEY="nginx/key.pem"

mkdir -p nginx

if [ -f "$CERT" ] && [ -f "$KEY" ]; then
    echo "✔ Certificat déjà existant, rien à faire"
    exit 0
fi

echo ">> Génération certificat SSL..."

openssl req -x509 -newkey rsa:2048 \
  -keyout "$KEY" \
  -out "$CERT" \
  -days 365 \
  -nodes \
  -subj "/C=FR/ST=Dev/L=Local/O=MusiQuali/CN=localhost"

echo "✔ SSL créé"
