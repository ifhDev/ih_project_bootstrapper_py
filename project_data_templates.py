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
LIGHTWEIGHT_FOLDERS = [
    "sample",
    "sample/scripts",
    "docs",
    "tests"
]

LIGHTWEIGHT_FILES = [
    "sample/__init__.py",
    "sample/core.py",
    "sample/helpers.py",
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
    "data/*",
    "",
    "# dev notes",
    "dev_notes/"
]