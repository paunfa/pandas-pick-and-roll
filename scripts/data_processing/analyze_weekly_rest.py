"""
Analyzes weekly rest advantages for NBA teams.

Creates weekly rest summaries used for fantasy streaming analysis.
"""

import pandas as pd

from utils.paths import (
    PROCESSED_TEAM_GAME_LOGS_PATH,
    WEEKLY_REST_SUMMARY_PATH
)


def analyze_weekly_rest():

    print("Analyzing weekly rest data...")

    team_game_logs = pd.read_csv(
        PROCESSED_TEAM_GAME_LOGS_PATH
    )

    weekly_rest_summary = (
        team_game_logs
        .groupby(
            [
                "WEEK_START",
                "TEAM_ABBREVIATION"
            ]
        )
        .agg(
            BACK_TO_BACKS=("BACK_TO_BACK", "sum"),
            AVERAGE_REST=("REST_DAYS", "mean"),
            MIN_REST=("REST_DAYS", "min"),
            MAX_REST=("REST_DAYS", "max")
        )
        .reset_index()
    )

    weekly_rest_summary["AVERAGE_REST"] = (
        weekly_rest_summary["AVERAGE_REST"]
        .round(2)
    )

    weekly_rest_summary.to_csv(
        WEEKLY_REST_SUMMARY_PATH,
        index=False
    )

    print(
        f"\n========================================"
        f"\nSuccessfully created weekly rest summary.")
    print(
        f"Saved to: {WEEKLY_REST_SUMMARY_PATH}"
        f"\n========================================"
    )


def main():
    analyze_weekly_rest()


if __name__ == "__main__":
    main()