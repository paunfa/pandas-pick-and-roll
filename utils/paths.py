"""
Stores folder paths to streamline usage in other scripts.
"""

from pathlib import Path

# Project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data folders
DATA = PROJECT_ROOT / "data"
RAW_DATA = DATA / "raw"
PROCESSED_DATA = DATA / "processed"

# Other project folders (for future use)
SCRIPTS = PROJECT_ROOT / "scripts"
DASHBOARD = PROJECT_ROOT / "dashboard"
SQL = PROJECT_ROOT / "sql"