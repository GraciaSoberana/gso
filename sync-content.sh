#!/bin/bash

VAULT="/home/donquique/Obsidian"
DEST="./content"

echo "Limpiando contenido anterior..."
chmod -R u+w "$DEST" 2>/dev/null
rm -rf "$DEST"
mkdir -p "$DEST"

echo "Sincronizando notas publicables..."
count=0

find "$VAULT" -name "*.md" | while read file; do
  if head -20 "$file" | grep -q "^publish: true"; then
    rel="${file#$VAULT/}"
    dest_file="$DEST/$rel"
    mkdir -p "$(dirname "$dest_file")"
    cp "$file" "$dest_file"
    count=$((count + 1))
  fi
done

# Copiar solo imágenes y PDFs
find "$VAULT" -type f \( -name "*.png" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.gif" -o -name "*.svg" -o -name "*.pdf" \) | while read file; do
  rel="${file#$VAULT/}"
  dest_file="$DEST/$rel"
  mkdir -p "$(dirname "$dest_file")"
  cp "$file" "$dest_file"
done

echo "Listo!"
