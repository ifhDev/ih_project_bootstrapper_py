import os
import sys
import json
import subprocess


# Universal variables
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

        # change standard folders here or later in config
        project_folders = [
        "dev_notes", 
        "implementations", 
        "implementations/scripts", 
        "notebooks", 
        "src", 
        "src/data", 
        "src/models", 
        "tests", 
        "visuals"
        ]

        # configured to work with standard folders
        gitignore_entries = [
            "",
            "",
            "# data folder",
            "src/data/*",
            "visuals/",
            "",
            "# dev notes",
            "dev_notes/"
        ]
        config = {
            "default_project_dir": default_project_dir,
            "default_python_version": default_python_version,
            "standard_packages": standard_packages,
            "project_folders": project_folders,
            "gitignore_entries": gitignore_entries
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

def create_standard_folders(config, project_path):
    folders = config.get("project_folders", [])
    for folder in folders:
        path = os.path.join(project_path, folder)
        os.makedirs(path, exist_ok=True)
        print(f"Created folder: {path}")

def write_gitignore(config, project_path):
    """
    Add standard .gitignore entries from config (as a list of lines).
    Appends to existing .gitignore if present, or creates a new one.
    """
    gitignore_entries = config.get("gitignore_entries", [])
    if gitignore_entries:
        gitignore_path = os.path.join(project_path, ".gitignore")
        mode = "a" if os.path.exists(gitignore_path) else "w"
        with open(gitignore_path, mode) as f:
            # Always end with a newline, so formatting stays clean
            f.write('\n'.join(gitignore_entries) + "\n")
        print("Added standard entries to .gitignore")


# Main Function
def main():
    if not dependency_check():
        print("The 'uv' tool is not installed on this system.")
        print("Please install uv from https://github.com/astral-sh/uv and try again.")
        return
    # setup of names and locations
    config = load_config()
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
    create_standard_folders(config, final_path)

    # expand gitignore
    write_gitignore(config, final_path)
    print("All done! Your new project is ready.")


# main-check
if __name__ == "__main__":
    main()