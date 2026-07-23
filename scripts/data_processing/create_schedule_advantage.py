"""
Creates a rudimentary weekly advantage score for each team by
factoring in their games per week and their weekly rest data.
"""
import pandas as pd
from utils.paths import (
    WEEKLY_SCHEDULE_PATH,
    WEEKLY_REST_SUMMARY_PATH,
    SCHEDULE_ADVANTAGE_PATH
)

# Score based on games played per week
GAME_SCORE_MAP = {
    1: 1,
    2: 2,
    3: 3,
    4: 4
}

# Bring multiple data points in to create ONE score for the week
def create_schedule_advantage():
    print("Creating schedule advantage scores...")

    # Read in weekly datasets
    weekly_schedule = pd.read_csv(
        WEEKLY_SCHEDULE_PATH
    )

    weekly_rest = pd.read_csv(
        WEEKLY_REST_SUMMARY_PATH
    )

    # Merge both data sets based on common columns
    schedule_advantage = weekly_schedule.merge(
        weekly_rest,
        on=[
            "WEEK_START",
            "TEAM_ABBREVIATION"
        ]
    )

    # Partial score based on amount of games for any given week
    schedule_advantage["GAME_SCORE"] = (
        schedule_advantage["GAMES_THIS_WEEK"]
        .map(GAME_SCORE_MAP)
    )

    # Partial score based on average rest days per week
    def calculate_rest_score(average_rest):
        if average_rest >= 2:
            return 2
        elif average_rest >= 1:
            return 1
        else:
            return 0

    # Partial score based on back-to-backs per week
    def calculate_b2b_penalty(back_to_backs):
        if back_to_backs >= 2:
            return -2
        elif back_to_backs == 1:
            return -1
        else:
            return 0

    # Update schedule_advantage dataframe with rest and B2B scores
    schedule_advantage["REST_SCORE"] = (
        schedule_advantage["AVERAGE_REST"]
        .apply(calculate_rest_score)
    )

    schedule_advantage["B2B_PENALTY"] = (
        schedule_advantage["BACK_TO_BACKS"]
        .apply(calculate_b2b_penalty)
    )

    # Calculate final weekly schedule advantage score
    schedule_advantage["SCHEDULE_ADVANTAGE"] = (
        schedule_advantage["GAME_SCORE"]
        + schedule_advantage["REST_SCORE"]
        + schedule_advantage["B2B_PENALTY"]
    )

    print(schedule_advantage.columns)
    print()
    print(schedule_advantage.head())

    # Save schedule_advantage to processed data folder
    output_path = SCHEDULE_ADVANTAGE_PATH

    schedule_advantage.to_csv(output_path, index=False)

    print(f"\n================================="
          f"\nSuccessfully saved weekly advantage scores."
          f"\nSaved to: {output_path}"
          f"\n=================================")

def main():
    create_schedule_advantage()

if __name__ == "__main__":
    main()