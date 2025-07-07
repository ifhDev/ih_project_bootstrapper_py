import os
import shutil
import sys
import json
import subprocess

# Universal variables
from project_data_templates import (
    DATA_SCIENCE_FOLDERS,
    DATA_SCIENCE_FILES,
    LIGHTWEIGHT_FOLDERS,
    LIGHTWEIGHT_FILES,
    GITIGNORE_ENTRIES,
)
CONFIG_FILE = "config.json"


# Functions
def dependency_check():
    if sys.version_info < (3, 8):
        print("This script requires Python 3.8 or higher.")
        exit(1)
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def choose_project_template():
    print("\nChoose project type:")
    print("1) Data Science (Cookiecutter style folders and .py starter files)")
    print("2) Lightweight Python (Kenneth Reitz style, only /sample, /docs, /tests)")
    choice = input("Enter 1 or 2: ").strip()
    if choice not in ("1", "2"):
        print("Invalid choice, defaulting to Data Science template.")
        choice = "1"
    return choice

def prompt_for_valid_directory(prompt_message):
    """
    Repeatedly prompt the user for a folder path until:
      - The folder exists
      - OR, the user chooses to create it (if missing)
    """
    while True:
        path = input(prompt_message).strip()
        if not path:
            print("Folder path can't be empty.")
            continue
        if os.path.isdir(path):
            return os.path.abspath(path)
        else:
            print(f"The folder '{path}' does not exist.")
            choice = input("Would you like to create it? (y/n): ").lower()
            if choice == 'y':
                try:
                    os.makedirs(path)
                    print(f"Created folder: {path}")
                    return os.path.abspath(path)
                except Exception as e:
                    print(f"Failed to create folder: {e}")
            else:
                print("Please enter a new folder path.")

def choose_project_template():
    print("\nChoose project type:")
    print("1) Data Science (Cookiecutter style folders and .py starter files)")
    print("2) Lightweight Python (Kenneth Reitz style, only /sample, /docs, /tests)")
    choice = input("Enter 1 or 2: ").strip()
    if choice not in ("1", "2"):
        print("Invalid choice, defaulting to Data Science template.")
        choice = "1"
    return choice


def load_config():
    """
    Loads config from file, or interactively creates a new one with safety checks.
    Config contents:
        default_project_dir: default folder for new data projects
        default_python_version: preferred Python version for new virtual environments
        standard_packages: standard Python packages that should be included in new projects
    """
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
        return config
    else:
        print("No config file found. Creating...")
        default_project_dir = prompt_for_valid_directory("Enter default folder for future data projects: ")
        default_python_version = input("Enter your preferred default Python version (e.g., 3.12): ").strip()
        standard_packages = input("Enter standard packages (comma-separated, e.g., pandas,numpy): ").split(",")
        standard_packages = [pkg.strip() for pkg in standard_packages if pkg.strip()]
        config = {
            "default_project_dir": default_project_dir,
            "default_python_version": default_python_version,
            "standard_packages": standard_packages
        }
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
        print("Config saved!")
        return config

# asks for new project name
def get_project_path(config):
    """
    Ask user for project name and location, combine, and return the intended path.
    Does not actually create any folders—just builds the path string.
    """
    print(f"\nDefault project location: {config['default_project_dir']}")
    project_name = input("Enter new project name: ").strip()
    while not project_name:
        print("Project name can't be empty.")
        project_name = input("Enter new project name: ").strip()
    custom_location = input("Press Enter to use the default folder, or specify a different location: ").strip()
    if custom_location:
        parent_dir = os.path.abspath(custom_location)
    else:
        parent_dir = os.path.abspath(config['default_project_dir'])
    project_path = os.path.join(parent_dir, project_name)
    return project_path

# creates new folder in specified location (with some safety-nets if you typo at the wrong moment)
def create_project_folder(config, project_path):
    """
    Try to create the project folder, handling missing parent directories and errors.
    """
    while True:
        parent_dir = os.path.dirname(project_path)
        if not os.path.isdir(parent_dir):
            print(f"Parent directory '{parent_dir}' does not exist.")
            choice = input("Would you like to create it? (y/n): ").lower()
            if choice == 'y':
                try:
                    os.makedirs(parent_dir)
                    print(f"Created parent directory: {parent_dir}")
                except Exception as e:
                    print(f"Failed to create parent directory: {e}")
                    print("Please enter a different path.")
                    project_path = get_project_path(config)
                    continue
            else:
                print("Please enter a different path.")
                project_path = get_project_path(config)
                continue

        # creates the actual project folder
        try:
            if os.path.exists(project_path):
                print(f"WARNING: Folder '{project_path}' already exists!")
                response = input("Continue anyway? (y/n): ").lower()
                if response != 'y':
                    raise Exception("User chose not to use existing folder.")
            else:
                os.makedirs(project_path)
                print(f"Created new project folder at: {project_path}")
            return project_path
        except Exception as e:
            print(f"\nError creating folder: {e}")
            print("Options:")
            print("1. Re-enter a new location")
            print("2. Use the default folder from config")
            print("3. Cancel project creation")
            choice = input("Choose [1/2/3]: ").strip()
            if choice == "1":
                project_path = get_project_path(config)
            elif choice == "2":
                default_dir = config["default_project_dir"]
                project_path = os.path.join(default_dir, os.path.basename(project_path))
                print(f"Using default folder: {default_dir}")
            else:
                print("Aborting project creation.")
                # cancel option
                return None

def init_project(config, project_path):
    # cd to project directory
    cwd = os.getcwd()
    try:
        os.chdir(project_path)

        # Step 1: uv init --python <version>
        python_version = config.get("default_python_version", "3.12")
        print(f"Running: uv init --python {python_version}")
        result = subprocess.run(["uv", "init", "--python", python_version], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("Error running 'uv init':", result.stderr)
            return False

        # Step 2: uv venv
        print("Running: uv venv")
        result = subprocess.run(["uv", "venv"], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("Error running 'uv venv':", result.stderr)
            return False

        # Step 3: Optionally add standard packages
        if config.get("standard_packages"):
            answer = input("Install standard packages in this project? (y/n): ").lower()
            if answer == "y":
                packages = config["standard_packages"]
                print(f"Adding standard packages: {', '.join(packages)}")
                result = subprocess.run(["uv", "add"] + packages, capture_output=True, text=True)
                print(result.stdout)
                if result.returncode != 0:
                    print("Error adding packages:", result.stderr)
            else:
                print("Skipping installation of standard packages.")

        print("Project initialized with uv!")
        return True

    finally:
        os.chdir(cwd)

def create_structure(project_path, folders, files):
    # folders
    for folder in folders:
        os.makedirs(os.path.join(project_path, folder), exist_ok=True)
        print(f"Created folder: {os.path.join(project_path, folder)}")
    # files
    for file in files:
        file_path = os.path.join(project_path, file)
        dir_name = os.path.dirname(file_path)
        os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, "w") as f:
                f.write(f'# {os.path.basename(file)}: Starter file\n')
            print(f"Created file: {file_path}")

def write_gitignore(project_path):
    """
    Add standard .gitignore entries from data template (as a list of lines).
    Appends to existing .gitignore if present, or creates a new one.
    """
    gitignore_entries = GITIGNORE_ENTRIES
    if gitignore_entries:
        gitignore_path = os.path.join(project_path, ".gitignore")
        mode = "a" if os.path.exists(gitignore_path) else "w"
        with open(gitignore_path, mode) as f:
            f.write('\n'.join(gitignore_entries) + "\n")
        print("Added standard entries to .gitignore")

def load_template(filename):
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    path = os.path.join(templates_dir, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def copy_project_setup_script(project_path, project_style):
    """
    Copies all template files from /templates to the correct destination in the new project.
    - For Data Science style: to src/tools/
    - For Lightweight Python: to sample/scripts/
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")

    # target decision
    if project_style == "1":  
        # Data Science
        target_dir = os.path.join(project_path, "src/tools/")
    else:
        # lightweight Python
        target_dir = os.path.join(project_path, "sample/scripts/")

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

# Main Function
def main():
    if not dependency_check():
        print("The 'uv' tool is not installed on this system.")
        print("Please install uv from https://github.com/astral-sh/uv and try again.")
        return
    # setup of names and locations
    config = load_config()
    
    # defining project template
    project_style = choose_project_template()
    if project_style == "1":
        folders = DATA_SCIENCE_FOLDERS
        files = DATA_SCIENCE_FILES
    else:
        folders = LIGHTWEIGHT_FOLDERS
        files = LIGHTWEIGHT_FILES

    project_path = get_project_path(config)
    final_path = create_project_folder(config, project_path)
    if not final_path:
        print("Project setup cancelled.")
        return
    print(f"Project folder ready at: {final_path}")

    # initialising project with uv
    success = init_project(config, final_path)
    if not success:
        print("Project setup failed during uv initialization.")
        return
    
    # creating folder structure
    create_structure(final_path, folders, files)

    # expand gitignore for data science
    if project_style == "1":
        write_gitignore(final_path)

    # copy setup scripts
    copy_project_setup_script(final_path, project_style)

    print("All done! Your new project is ready.")


# main-check
if __name__ == "__main__":
    main()