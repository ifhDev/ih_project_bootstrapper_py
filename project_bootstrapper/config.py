import os
import json

CONFIG_FILE = "config.json"

def prompt_for_valid_directory(prompt_message):
    while True:
        path = input(prompt_message).strip()
        if not path:
            print("Folder path can't be empty.")
            continue
        if os.path.isdir(path):
            return os.path.abspath(path)
        else:
            choice = input(f"Folder '{path}' does not exist. Create it? (y/n): ").lower()
            if choice == 'y':
                os.makedirs(path)
                return os.path.abspath(path)
            else:
                print("Please enter a new folder path.")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    print("No config file found. Creating...")
    default_project_dir = prompt_for_valid_directory("Enter default folder for future data projects: ")
    default_python_version = input("Enter preferred default Python version (e.g., 3.12): ").strip()
    standard_packages = input("Enter standard packages (comma-separated): ").split(",")
    config = {
        "default_project_dir": default_project_dir,
        "default_python_version": default_python_version,
        "standard_packages": [pkg.strip() for pkg in standard_packages if pkg.strip()]
    }
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)
    print("Config saved!")
    return config