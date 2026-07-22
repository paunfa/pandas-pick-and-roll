"""
Determines and ranks the weekly schedule of any given team.

Retrieves game data and converts game dates to datetime data type.
Using datetime, determines the start date of any given fantasy week.
Assigns a strength rating for each team during the week based on
the amount of games played that week.

Creates:
    data/processed/weekly_schedule.csv
    data/processed/team_schedule_clean.csv
"""

import pandas as pd
from utils.paths import RAW_DATA, PROCESSED_DATA

team_game_logs = pd.read_csv(
        RAW_DATA / "team_game_logs.csv"
    )
team_game_logs["GAME_DATE"] = pd.to_datetime(
    team_game_logs["GAME_DATE"]
)

def team_schedule():

    print("Verifying games played per team...")

    # Find the start date of each week for any given game
    team_game_logs["WEEK_START"] = (
        team_game_logs["GAME_DATE"]
        - pd.to_timedelta(team_game_logs["GAME_DATE"].dt.weekday, unit="D")
    )


    # Find total games played for each team
    games_by_team = (
        team_game_logs
        .groupby("TEAM_ABBREVIATION")
        .size()
        .reset_index(name="TOTAL_GAMES")
    )

    output_path = PROCESSED_DATA / "team_schedule_clean.csv"

    games_by_team.to_csv(output_path, index=False)

    print(f"\n====================================="
          f"\nSuccessfully verified amount of games played per team."
          f"\nSaved to:  {output_path}"
          f"\n====================================\n")


def week_schedule():

    print("Rating schedules based on weekly schedule data...")

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



    output_path = PROCESSED_DATA / "weekly_schedule.csv"

    weekly_schedule.to_csv(output_path, index=False)

    print(f"\n================================"
          f"\nSuccessfully ranked weekly schedules for each team!"
          f"\nSaved weekly schedule to: {output_path}"
          f"\n================================")


def main():
    team_schedule()
    week_schedule()

if __name__ == "__main__":
    main()