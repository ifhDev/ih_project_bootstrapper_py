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

def copy_project_setup_script(project_path):
    """
    Copies all template files from /templates to the root folder of new project.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    # target decision
    target_dir = os.path.join(project_path)

    os.makedirs(target_dir, exist_ok=True)

    for fname in os.listdir(templates_dir):
        source_path = os.path.join(templates_dir, fname)
        dest_path = os.path.join(target_dir, fname)
        # text files
        if fname.endswith(('.py', '.sh', '.bat', '.txt', '.md', '.rst')):
            with open(source_path, "r", encoding="utf-8") as fsrc:
                content = fsrc.read()
            with open(dest_path, "w", encoding="utf-8") as fdst:
                fdst.write(content)
        else:

            shutil.copy2(source_path, dest_path)
        print(f"Copied {fname} to {dest_path}")