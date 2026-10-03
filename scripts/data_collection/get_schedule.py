"""
Download team game logs from the NBA Stats API.

This script retrieves all regular season team game logs for a specified season,
engineers basic schedule features, and saves the raw dataset to the data/raw
directory.

Creates:
    data/raw/team_game_logs_raw.csv
"""


import pandas as pd
from nba_api.stats.endpoints import LeagueGameLog
from utils.paths import RAW_DATA
from utils.nba_season import determine_target_season

def get_schedule(season):
    print(f"Downloading {season} team game logs...")

    game_logs = LeagueGameLog(
        season=season,
        season_type_all_star='Regular Season',
        player_or_team_abbreviation='T'
    )

    game_data = game_logs.get_data_frames()[0]

    # Create a Home/Away column
    def get_home_away(matchup:str) -> str:
        """
        Determine whether a game was played at home or away.

        Args:
            matchup: Matchup string from the NBA API
                (e.g. "GSW vs. LAL" or "LAL @ GSW").

        Returns:
            "Home" if the team played at home, otherwise "Away".
        """
        if "vs." in matchup:
            return "Home"
        else:
            return "Away"

    game_data["HOME_AWAY"] = game_data["MATCHUP"].apply(get_home_away)

    # Create an Opponent column
    def get_opponent(matchup:str) -> str:
        """
        Extract the opponent's team abbreviation from a matchup string.

        Args:
            matchup: Matchup string from the NBA API
                (e.g. "GSW vs. LAL").

        Returns:
            The opponent's team abbreviation.
        """
        return matchup.split()[-1]

    game_data["OPPONENT"] = game_data["MATCHUP"].apply(get_opponent)



    output_path = RAW_DATA / "team_game_logs_raw.csv"

    game_data.to_csv(output_path, index=False)

    print("\n===================================")
    print("Team game logs downloaded successfully!")
    print(f"Rows: {len(game_data)}")
    print(f"Saved to: {output_path}")
    print("===================================")

def main():
    target_season = determine_target_season()

    print(f"Collecting NBA season: {target_season}")

    get_schedule(target_season)

if __name__ == "__main__":
    main()
