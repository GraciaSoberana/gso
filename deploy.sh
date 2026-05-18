#!/bin/bash
set -e                              # Si algo falla, detener todo

source /home/donquique/.bashrc      # Cargar tus variables de entorno (el GITHUB_TOKEN)

echo "Sincronizando contenido..."
cp -r --no-preserve=mode /home/donquique/Obsidian ./content_tmp   # Copia tu vault a una carpeta temporal
[ -d content/ ] && chmod -R u+w content/                          # Da permisos de escritura a content/ si existe
rm -rf content/                                                    # Borra el content/ viejo
mv content_tmp content                                             # Renombra la carpeta temporal a content/

echo "Subiendo a GitHub..."
git add content/
git commit -m "actualización $(date '+%Y-%m-%d %H:%M')" || echo "Nada que commitear."
git push  https://$GITHUB_TOKEN@github.com/GraciaSoberana/gso.git main

echo "¡Listo! El sitio se actualizará en unos minutos."
