from pathlib import Path

# Root of the project (the folder containing pyproject.toml or .git)
PROJECT_ROOT_DIR = Path(__file__).resolve().parent.parent.parent
SRC_DIR = PROJECT_ROOT_DIR / "src"
TEMP_DIR = SRC_DIR / "temp"
TEMPLATES_DIR = SRC_DIR / "templates"


TEMP_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)
