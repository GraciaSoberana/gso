import re

def eliminar_notas_al_pie(texto):
    # Elimina cualquier nota al pie en formato ^[ ... ]
    texto_sin_notas = re.sub(r'\^

\[.*?\]

', '', texto)
    return texto_sin_notas

# Archivos específicos que usarás
archivo_entrada = '30. El modo optativo (slides).md'
archivo_salida = '30. El modo optativo (slides) [limpio].md'

# Cargar contenido, eliminar notas y guardar resultado
with open(archivo_entrada, 'r', encoding='utf-8') as f:
    contenido = f.read()

contenido_limpio = eliminar_notas_al_pie(contenido)

with open(archivo_salida, 'w', encoding='utf-8') as f:
    f.write(contenido_limpio)

print('✅ Archivo procesado y guardado como:', archivo_salida)
