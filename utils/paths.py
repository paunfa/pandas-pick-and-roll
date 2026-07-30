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

# Team game log data files
RAW_TEAM_GAME_LOGS_PATH = RAW_DATA / "team_game_logs_raw.csv"
PROCESSED_TEAM_GAME_LOGS_PATH = PROCESSED_DATA / "team_game_logs_pro.csv"

# Schedule analysis data files
WEEKLY_SCHEDULE_PATH = PROCESSED_DATA / "weekly_schedule.csv"
TEAM_REST_SUMMARY_PATH = PROCESSED_DATA / "team_rest_summary.csv"
WEEKLY_REST_SUMMARY_PATH = PROCESSED_DATA / "weekly_rest_summary.csv"
SCHEDULE_ADVANTAGE_PATH = PROCESSED_DATA / "schedule_advantage.csv"

# Player game log data files
RAW_PLAYER_GAME_LOGS_PATH = RAW_DATA / "player_game_logs_raw.csv"
PROCESSED_PLAYER_GAME_LOGS_PATH = PROCESSED_DATA / "player_game_logs_pro.csv"
RECENT_PLAYER_PRODUCTION_PATH = PROCESSED_DATA / "player_recent_production.csv"