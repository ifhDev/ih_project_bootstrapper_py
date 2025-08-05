import os

def create_structure(project_path, folders, files):
    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)
        print(f"Created folder: {os.path.join(project_path, folder)}")
    for file in files:
        file_path = os.path.join(project_path, file)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f'# {os.path.basename(file)}: Starter file\n')
            print(f"Created file: {file_path}")
