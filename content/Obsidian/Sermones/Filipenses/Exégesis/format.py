import re

# Función para formatear el texto
def format_text(text):
    # Reemplaza los números con la versión en negritas y un espacio después
    formatted_text = re.sub(r'(\d)', r'**\1** ', text)
    return formatted_text

# Lee el contenido del archivo
with open('fil.md', 'r', encoding='utf-8') as file:
    input_text = file.read()

# Formatea el texto
formatted_text = format_text(input_text)

# Guarda el texto formateado en el mismo archivo
with open('Fil.md', 'w', encoding='utf-8') as file:
    file.write(formatted_text)

print("El archivo ha sido actualizado correctamente.")
