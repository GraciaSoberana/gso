import os

def truncate_decimals(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(file_path, 'w') as file:
        for line in lines:
            new_line = ''.join([char if char != '.' else char.split('.')[0] for char in line])
            file.write(new_line)

folder_path = '/'

for filename in os.listdir(folder_path):
    file_path = os.path.join(folder_path, filename)
    if os.path.isfile(file_path):
        truncate_decimals(file_path)
