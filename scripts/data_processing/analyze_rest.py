"""
Analyze team rest and back-to-back schedules.

Takes game data from team_game_logs and calculates rest days for each team.
Determines amount of back-to-backs as well as average, min, and max rest
days for each team.

Creates:
    data/processed/team_rest_summary.csv
"""

import pandas as pd

from utils.paths import RAW_DATA, PROCESSED_DATA


def analyze_rest():

    print("Analyzing rest day data...")

    # Retrieve already collected game data
    team_game_logs = pd.read_csv(
        RAW_DATA / "team_game_logs.csv"
    )

    # Convert game date data type from str to datetime to enable calculation
    team_game_logs["GAME_DATE"] = pd.to_datetime(
        team_game_logs["GAME_DATE"]
    )

    # Sort games alphabetically by team, and within that sort, sort chronologically
    team_game_logs = team_game_logs.sort_values(
        by=[
            "TEAM_ABBREVIATION",
            "GAME_DATE"
        ]
    )

    # Find the amount of days between any given team's current game and their last game
    team_game_logs["DAYS_BETWEEN_GAMES"] = (
        team_game_logs
            .groupby("TEAM_ABBREVIATION")["GAME_DATE"]
            .diff()
            .dt.days
    )

    # Differentiate between calendar date differences and actual rest days (e.g. back-to-backs have a 1-day difference but are considered to have 0 rest days)
    team_game_logs["REST_DAYS"] = (
        team_game_logs["DAYS_BETWEEN_GAMES"] - 1
    )

    # Determine whether any given game is the 2nd half of a back-to-back
    team_game_logs["BACK_TO_BACK"] = (
        team_game_logs["REST_DAYS"] == 0
    )

    # Create a table containing the amount of back-to-backs, average rest days, and min/max rest day amounts for each team
    team_rest_summary = (
        team_game_logs
        .groupby("TEAM_ABBREVIATION")
        .agg(
            GAMES=("GAME_ID", "count"),
            BACK_TO_BACKS=("BACK_TO_BACK", "sum"),
            AVERAGE_REST=("REST_DAYS", "mean"),
            MIN_REST=("REST_DAYS", "min"),
            MAX_REST=("REST_DAYS", "max"),
        )
        .reset_index()
    )

    team_rest_summary["AVERAGE_REST"] = (
        team_rest_summary["AVERAGE_REST"].round(2)
    )

    # Save summary
    output_path = PROCESSED_DATA / "team_rest_summary.csv"

    team_rest_summary.to_csv(output_path, index=False)

    print(f"\n====================================="
          f"\nSuccessfully saved rest day summaries for every team."
          f"\n Saved to: {output_path}"
          f"\n=====================================")


def main():
    analyze_rest()

if __name__ == "__main__":
    main()