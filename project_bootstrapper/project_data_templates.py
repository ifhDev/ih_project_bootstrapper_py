# data science setup
DATA_SCIENCE_FOLDERS = [
    "dev_notes",
    "data",
    "data/external",
    "data/interim",
    "data/processed",
    "data/raw",
    "notebooks",
    "reports",
    "reports/figures",
    "src",
    "src/modeling",
    "src/tools"
]

DATA_SCIENCE_FILES = [
    "src/__init__.py",
    "src/config.py",
    "src/dataset.py",
    "src/features.py",
    "src/modeling/__init__.py",
    "src/modeling/train.py",
    "src/modeling/predict.py",
    "src/plots.py"
]

# lightweight setup
def get_lightweight_folders(pkg_name):
    return [
        pkg_name,
        "scripts",
        "docs",
        "tests"
    ]

def get_lightweight_files(pkg_name):
    return [
        f"{pkg_name}/__init__.py",
        f"{pkg_name}/core.py",
        f"{pkg_name}/helpers.py",
        "docs/conf.py",
        "docs/index.rst",
        "tests/test_basic.py",
        "tests/test_advanced.py"
    ]

# .gitignore entries for Data Science template
GITIGNORE_ENTRIES = [
    "",
    "",
    "# data folder",
    "data/external/*",
    "data/interim/*",
    "data/processed/*",
    "data/raw/*",
    "",
    "# dev notes",
    "dev_notes/"
]