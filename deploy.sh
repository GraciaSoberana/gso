#!/bin/bash

source /home/donquique/.bashrc

echo "Sincronizando contenido..."
rm -rf content/
cp -r /home/donquique/Obsidian ./content

echo "Subiendo a GitHub..."
git add .
git commit -m "actualización $(date '+%Y-%m-%d %H:%M')"
git push https://$GITHUB_TOKEN@github.com/GraciaSoberana/gso.git main

echo "¡Listo! El sitio se actualizará en unos minutos."
