#!/bin/bash
set -e

source /home/donquique/.bashrc

echo "Sincronizando contenido..."
cp -r --no-preserve=mode /home/donquique/Obsidian ./content_tmp
[ -d content/ ] && chmod -R u+w content/
rm -rf content/
mv content_tmp content

echo "Subiendo a GitHub..."
git add content/
git commit -m "actualización $(date '+%Y-%m-%d %H:%M')" || echo "Nada que commitear."
git push https://$GITHUB_TOKEN@github.com/GraciaSoberana/gso.git main

echo "¡Listo! El sitio se actualizará en unos minutos."
