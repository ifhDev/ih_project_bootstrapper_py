import os
import subprocess
import sys

def main():
    print("Setting up environment for cloned project...")
    
    # ensuring correct location
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)

    # creating venv (if necessary)    
    if not os.path.isdir(".venv"):
        print("Creating virtual environment with uv...")
        result = subprocess.run(["uv", "venv"], capture_output=True, text=True)
        print(result.stdout)
        if result.returncode != 0:
            print("Error: Failed to create virtual environment:", result.stderr)
            sys.exit(1)
    else:
        print("Virtual environment already exists.")

    # install dependencies
    print("Installing dependencies from pyproject.toml/uv.lock...")
    result = subprocess.run(["uv", "pip", "sync", "uv.lock"], capture_output=True, text=True)
    print(result.stdout)
    if result.returncode != 0:
        print("Error: Failed to install dependencies:", result.stderr)
        sys.exit(1)
    print("All dependencies installed!")

    print("Project setup complete!")

if __name__ == "__main__":
    main()