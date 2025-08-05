import subprocess
import os

def dependency_check():
    try:
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def init_project(config, project_path):
    cwd = os.getcwd()
    try:
        os.chdir(project_path)
        python_version = config.get("default_python_version", "3.12")
        subprocess.run(["uv", "init", "--python", python_version])
        subprocess.run(["uv", "venv"])
        if config.get("standard_packages"):
            answer = input("Install standard packages? (y/n): ").lower()
            if answer == "y":
                subprocess.run(["uv", "add"] + config["standard_packages"])
        print("Project initialized with uv!")
    finally:
        os.chdir(cwd)
