#!/usr/bin/env python3
"""
Script para generar un índice de todos los pasajes bíblicos
en una estructura de carpetas organizadas por libros.
"""

import os
import re
from pathlib import Path
from collections import defaultdict

def extraer_info_capitulo(nombre_archivo):
    """
    Extrae el libro y número de capítulo del nombre del archivo.
    Ejemplos: "Gen 1.md" -> ("Gen", 1)
              "1 Sam 5.md" -> ("1 Sam", 5)
    """
    # Remover la extensión .md
    nombre = nombre_archivo.replace('.md', '')
    
    # Intentar extraer libro y capítulo
    # Patrón para capturar libros con números (ej: "1 Sam") y sin números
    patron = r'^(.+?)\s+(\d+)$'
    match = re.match(patron, nombre)
    
    if match:
        libro = match.group(1).strip()
        capitulo = int(match.group(2))
        return libro, capitulo
    
    return None, None

def generar_indice(ruta_biblia, archivo_salida="indice_biblia.md"):
    """
    Genera un índice completo de todos los pasajes bíblicos.
    
    Args:
        ruta_biblia: Ruta a la carpeta "biblia"
        archivo_salida: Nombre del archivo de índice a generar
    """
    ruta = Path(ruta_biblia)
    
    if not ruta.exists():
        print(f"Error: La ruta {ruta_biblia} no existe")
        return
    
    # Diccionario para organizar: {libro: {carpeta: [capitulos]}}
    libros = defaultdict(lambda: defaultdict(list))
    
    # Recorrer todas las subcarpetas
    for subcarpeta in sorted(ruta.iterdir()):
        if not subcarpeta.is_dir():
            continue
        
        nombre_carpeta = subcarpeta.name
        
        # Buscar archivos .md en la subcarpeta
        for archivo in sorted(subcarpeta.glob("*.md")):
            libro, capitulo = extraer_info_capitulo(archivo.name)
            
            if libro and capitulo:
                libros[libro][nombre_carpeta].append({
                    'capitulo': capitulo,
                    'ruta': str(archivo.relative_to(ruta))
                })
    
    # Generar el archivo de índice en Markdown
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("# Índice de Pasajes Bíblicos\n\n")
        f.write(f"Generado automáticamente desde: `{ruta_biblia}`\n\n")
        f.write("---\n\n")
        
        # Organizar por libro
        for libro in sorted(libros.keys()):
            f.write(f"## {libro}\n\n")
            
            # Para cada carpeta que contiene este libro
            for carpeta in sorted(libros[libro].keys()):
                capitulos_data = sorted(libros[libro][carpeta], 
                                       key=lambda x: x['capitulo'])
                
                # Si solo hay una carpeta por libro, no mostrar el nombre de carpeta
                if len(libros[libro]) == 1:
                    encabezado = ""
                else:
                    encabezado = f"**Carpeta: {carpeta}**\n\n"
                    f.write(encabezado)
                
                # Listar capítulos con enlaces en formato Obsidian wikilink
                for cap_data in capitulos_data:
                    cap = cap_data['capitulo']
                    # Extraer solo el nombre del archivo sin extensión ni ruta
                    nombre_archivo = Path(cap_data['ruta']).stem
                    f.write(f"- [[{nombre_archivo}]]\n")
                
                f.write("\n")
            
            f.write("\n")
        
        # Estadísticas al final
        total_capitulos = sum(
            len(caps) 
            for libro_data in libros.values() 
            for caps in libro_data.values()
        )
        f.write("---\n\n")
        f.write(f"**Total de libros:** {len(libros)}\n\n")
        f.write(f"**Total de capítulos:** {total_capitulos}\n")
    
    print(f"✓ Índice generado exitosamente: {archivo_salida}")
    print(f"  - {len(libros)} libros encontrados")
    print(f"  - {total_capitulos} capítulos totales")
    
    return archivo_salida

def generar_resumen_estadisticas(ruta_biblia):
    """Genera un resumen de estadísticas de la biblioteca bíblica."""
    ruta = Path(ruta_biblia)
    
    if not ruta.exists():
        print(f"Error: La ruta {ruta_biblia} no existe")
        return
    
    print("\n=== Estadísticas de la Biblioteca Bíblica ===\n")
    
    libros_stats = defaultdict(int)
    
    for subcarpeta in ruta.iterdir():
        if not subcarpeta.is_dir():
            continue
        
        for archivo in subcarpeta.glob("*.md"):
            libro, capitulo = extraer_info_capitulo(archivo.name)
            if libro:
                libros_stats[libro] += 1
    
    for libro in sorted(libros_stats.keys()):
        print(f"{libro:20} {libros_stats[libro]:3} capítulos")
    
    print(f"\nTotal: {len(libros_stats)} libros, {sum(libros_stats.values())} capítulos")

if __name__ == "__main__":
    import sys
    
    # Usar argumento de línea de comandos o valor por defecto
    if len(sys.argv) > 1:
        ruta_biblia = sys.argv[1]
    else:
        ruta_biblia = "./biblia"
    
    # Generar el índice
    generar_indice(ruta_biblia)
    
    # Mostrar estadísticas
    generar_resumen_estadisticas(ruta_biblia)