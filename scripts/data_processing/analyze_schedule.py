"""
Determines and ranks the weekly schedule of any given team.

Retrieves game data and converts game dates to datetime data type.
Using datetime, determines the start date of any given fantasy week.
Assigns a strength rating for each team during the week based on
the amount of games played that week.
"""

import pandas as pd
from pathlib import Path


project_root = Path(__file__).resolve().parents[2]

input_path = project_root / "data" / "raw" / "team_game_logs.csv"

# Convert game dates to datetime data type
team_game_logs = pd.read_csv(input_path)
team_game_logs["GAME_DATE"] = pd.to_datetime(
    team_game_logs["GAME_DATE"]
)

# Find the start date of each week for any given game
team_game_logs["WEEK_START"] = (
    team_game_logs["GAME_DATE"]
    - pd.to_timedelta(team_game_logs["GAME_DATE"].dt.weekday, unit="D")
)

print()
print(
    team_game_logs[
        [
            "GAME_DATE",
            "TEAM_ABBREVIATION",
            "WEEK_START"
        ]
    ].head(10)
)

# Find total games played for each team
games_by_team = (
    team_game_logs
    .groupby("TEAM_ABBREVIATION")
    .size()
    .reset_index(name="TOTAL_GAMES")
)

output_path = project_root / "data" / "processed" / "games_by_team.csv"

games_by_team.to_csv(output_path, index=False)

print(f"\n====================================="
      f"\nSuccessfully verified amount of games played per team."
      f"\nSaved to:  {output_path}"
      f"\n====================================\n")

# Find amount of games played during any given fantasy week
weekly_schedule = (
    team_game_logs
    .groupby(
        [
            "WEEK_START",
            "TEAM_ABBREVIATION"
        ]
    )
    .size()
    .reset_index(name="GAMES_THIS_WEEK")
)

# Rudimentary weekly schedule rating
def get_schedule_rating(games_this_week: int) -> str:
    """
    Assign a qualitative schedule rating based on the number of games
    a team plays during a fantasy week.

    Args:
        games_this_week: Number of scheduled games.

    Returns:
        A schedule strength rating.
    """

    if games_this_week >= 4:
        return "Very Strong"

    if games_this_week == 3:
        return "Strong"

    if games_this_week == 2:
        return "Weak"

    else:
        return "Very Weak"

weekly_schedule["SCHEDULE_RATING"] = (
    weekly_schedule["GAMES_THIS_WEEK"]
    .apply(get_schedule_rating)
)


print(weekly_schedule.head(30))


output_path = project_root / "data" / "processed" / "weekly_schedule.csv"

weekly_schedule.to_csv(output_path, index=False)

print(f"\n================================"
      f"\nSuccessfully ranked weekly schedules for each team!"
      f"\nSaved weekly schedule to: {output_path}"
      f"\n================================")


