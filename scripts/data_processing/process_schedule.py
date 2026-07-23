"""
Reads raw NBA schedule data
Creates schedule context
Calculates:
    DAYS_BETWEEN_GAMES
    REST_DAYS
    BACK_TO_BACK
    WEEK_START
Saves the processed game-level schedule dataset
Creates the team rest summary

Takes game data from team_game_logs and calculates rest days for each team.
Determines amount of back-to-backs as well as average, min, and max rest
days for each team.

Creates:
    data/processed/team_game_logs_pro.csv
    data/processed/team_rest_summary.csv
"""

import pandas as pd

from utils.paths import (
    RAW_TEAM_GAME_LOGS_PATH,
    PROCESSED_TEAM_GAME_LOGS_PATH,
    TEAM_REST_SUMMARY_PATH
)


def analyze_rest():

    print("Analyzing rest day data...")

    # Retrieve already collected game data
    team_game_logs = pd.read_csv(RAW_TEAM_GAME_LOGS_PATH)

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

    # Find the start date of each week for any given game
    team_game_logs["WEEK_START"] = (
        team_game_logs["GAME_DATE"]
        - pd.to_timedelta(team_game_logs["GAME_DATE"].dt.weekday, unit="D")
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

    output_path = PROCESSED_TEAM_GAME_LOGS_PATH

    team_game_logs.to_csv(
        output_path,
        index=False
    )

    print(f"\n========================================="
          f"\nSuccessfully updated team game logs with rest day data."
          f"\nSaved to: {output_path}"
          f"\n=========================================")

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
    output_path = TEAM_REST_SUMMARY_PATH

    team_rest_summary.to_csv(output_path, index=False)

    print(f"\n====================================="
          f"\nSuccessfully saved rest day summaries for every team."
          f"\n Saved to: {output_path}"
          f"\n=====================================")


def main():
    analyze_rest()

if __name__ == "__main__":
    main()