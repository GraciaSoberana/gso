import os

# El texto a buscar y su reemplazo
old_text = "book: Teología Sistemática de Grudem"
new_text = 'book: "[[Teología Sistemática de Grudem]]"'

# Obtén el nombre del archivo del script
script_name = os.path.basename(__file__)

# Recorre todos los archivos en la carpeta actual
for filename in os.listdir('.'):
    # Evita procesar el propio script y asegura trabajar sólo con archivos .md
    if os.path.isfile(filename) and filename != script_name and filename.endswith('.md'):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Reemplaza el texto
        new_content = content.replace(old_text, new_text)
        
        # Escribe los cambios de vuelta al archivo
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(new_content)

print("¡Reemplazo completo!")
