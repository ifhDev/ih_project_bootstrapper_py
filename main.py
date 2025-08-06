
import os
from project_bootstrapper import *

def choose_project_template():
    print("\nChoose project type:")
    print("1) Data Science (Cookiecutter style folders and .py starter files)")
    print("2) Lightweight Python (Kenneth Reitz style, main package named by you)")
    choice = input("Enter 1 or 2: ").strip()
    return choice if choice in ("1", "2") else "1"

def get_project_path(config):
    print(f"\nDefault project location: {config['default_project_dir']}")
    project_name = input("Enter new project name: ").strip()
    while not project_name:
        print("Project name can't be empty.")
        project_name = input("Enter new project name: ").strip()
    custom_location = input("Press Enter to use the default folder, or specify a different location: ").strip()
    parent_dir = os.path.abspath(custom_location) if custom_location else os.path.abspath(config['default_project_dir'])
    return os.path.join(parent_dir, project_name)

def main():
    if not dependency_check():
        print("The 'uv' tool is not installed. Please install uv and try again.")
        return
    config = load_config()
    template_choice = choose_project_template()
    main_pkg_name = None

    if template_choice == "1":
        folders = DATA_SCIENCE_FOLDERS
        files = DATA_SCIENCE_FILES
    else:
        main_pkg_name = input("Name your main package (instead of 'sample'): ").strip()
        while not main_pkg_name.isidentifier():
            print("Please use a valid Python package name (letters, numbers, underscore, not starting with number).")
            main_pkg_name = input("Name your main package: ").strip()
        folders = get_lightweight_folders(main_pkg_name)
        files = get_lightweight_files(main_pkg_name)

    project_path = get_project_path(config)
    os.makedirs(project_path, exist_ok=True)
    create_structure(project_path, folders, files)
    init_project(config, project_path)
    copy_project_setup_script(project_path)
    print("All done! Your new project is ready.")

if __name__ == "__main__":
    main()