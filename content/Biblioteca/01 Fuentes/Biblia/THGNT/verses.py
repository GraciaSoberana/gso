import os

def insertar_encabezados_en_md(ruta_base):
    for carpeta_actual, _, archivos in os.walk(ruta_base):
        nombre_carpeta = os.path.basename(carpeta_actual)
        for archivo in archivos:
            if archivo.endswith(".md"):
                ruta_completa = os.path.join(carpeta_actual, archivo)
                encabezado = f"## {nombre_carpeta}\n### {archivo}\n\n"
                with open(ruta_completa, "r", encoding="utf-8") as f:
                    contenido_original = f.read()
                with open(ruta_completa, "w", encoding="utf-8") as f:
                    f.write(encabezado + contenido_original)
                print(f"✅ Encabezado insertado: {ruta_completa}")

# Ejecutar en la carpeta actual
insertar_encabezados_en_md(".")