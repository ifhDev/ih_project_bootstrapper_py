# Data Project Bootstrapper

Cross-platform setup for my projects. Made with data science in mind but might be useful for other kinds of Python, too.

## Features

- Prompts for project name and location, with config file support for defaults.
- Safely creates project folder structures (with typo/error protection).
- Initialises Python environment with [`uv`](https://github.com/astral-sh/uv) for fast, reproducible setup.
- Optionally installs your standard packages (`pandas`, `numpy`, etc.) with a single prompt.
- Auto-creates your preferred folder structure (customisable via `config.json`).
- Appends standard ignore patterns to `.gitignore`.
- Fully cross-platform: works on Windows, Mac, and Linux.

## Dependencies

- **Python** 3.8 or higher (made with 3.12, recommended 3.12+)
- This project uses [`uv`](https://github.com/astral-sh/uv) (install with `pip install uv`) for dependency management; dependencies are in `pyproject.toml`

## Quickstart

1. Clone/download this repository.
2. Make sure Python and `uv` are installed and available in your system path.
3. Run the script:

   ```
   python main.py
   ```

4. Follow the prompts to configure your defaults (first run only), and create your first project!

## Customisation

- Edit `config.json` to change your standard folder structure, default Python version, or your preferred starter packages.
- Update the `gitignore_entries` list in `project_data_templates.py` to change what is ignored by default.
