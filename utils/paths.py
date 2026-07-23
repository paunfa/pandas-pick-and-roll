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

# Data files that multiple scripts might use
RAW_TEAM_GAME_LOGS_PATH = RAW_DATA / "team_game_logs_raw.csv"
PROCESSED_TEAM_GAME_LOGS_PATH = PROCESSED_DATA / "team_game_logs_pro.csv"
WEEKLY_SCHEDULE_PATH = PROCESSED_DATA / "weekly_schedule.csv"
TEAM_REST_SUMMARY_PATH = PROCESSED_DATA / "team_rest_summary.csv"