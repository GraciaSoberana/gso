import os

# Define the text to search and replace
search_text = "Biblioteca/Notas/Biblia"
replace_text = "NotaDevocional"

# Get the current directory
directory = os.getcwd()

# Iterate through all files in the directory
for filename in os.listdir(directory):
    # Check if the file is a text file
    if filename.endswith(".md"):
        # Read the contents of the file
        with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
            file_contents = file.read()
        
        # Replace the target string
        new_contents = file_contents.replace(search_text, replace_text)
        
        # Write the new contents back to the file
        with open(os.path.join(directory, filename), 'w', encoding='utf-8') as file:
            file.write(new_contents)

print("Reemplazo completado.")
