import os

folder_path = '.'  # Esto indica que la carpeta es la actual

# Recorre todos los archivos en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith('.md'):
        file_path = os.path.join(folder_path, filename)
        
        # Lee el contenido del archivo
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        # Encuentra la segunda aparición de '---\n'
        yaml_end_index = lines.index('---\n', 1)  # Encuentra la segunda aparición de '---\n'
        
        # Mantén solo el YAML front matter
        new_lines = lines[:yaml_end_index + 1]  # Incluye el YAML hasta el segundo '---\n'
        
        # Agrega ":" al final de la última línea del YAML
        if new_lines[-1].strip() == "---":
            new_lines[-2] = new_lines[-2].strip() + ":\n"
        
        # Escribe de nuevo el contenido en el archivo
        with open(file_path, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)
