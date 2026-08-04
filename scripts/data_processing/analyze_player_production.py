"""
Analyze recent player production from processed NBA player game logs.

This module calculates recent player performance metrics using processed
player game log data. For each player, it identifies the five AND ten most recent
games and computes average production statistics, including points,
rebounds, assists, and minutes played.

The resulting dataset is saved as `player_recent_production.csv` and serves
as the foundation for the Recent Fantasy Production component of the
Streaming Score model.

Pipeline:
    player_game_logs_pro.csv
            ↓
    analyze_player_production.py
            ↓
    player_recent_production.csv
"""

import pandas as pd
from utils.paths import PROCESSED_PLAYER_GAME_LOGS_PATH, RECENT_PLAYER_PRODUCTION_PATH

# Calculate average production statistics for a set of recent games.
def calculate_recent_production(
    player_logs: pd.DataFrame,
    prefix: str
) -> pd.DataFrame:
    """
        Calculate average production statistics for a player's recent games.

        Args:
            player_logs: DataFrame containing recent player game logs.
            prefix: Prefix used when naming output columns.

        Returns:
            DataFrame containing games played, average points, rebounds, assists,
            and minutes for each player.
        """


    recent_summary = (
        player_logs
        .groupby(
            [
                "Player_ID",
                "PLAYER_NAME"
            ]
        )
        .agg(
            **{
                f"{prefix}_GAMES": ("Game_ID", "count"),
                f"{prefix}_AVG_PPG": ("PTS", "mean"),
                f"{prefix}_AVG_RPG": ("REB", "mean"),
                f"{prefix}_AVG_APG": ("AST", "mean"),
                f"{prefix}_AVG_MPG": ("MIN", "mean"),
            }
        )
        .round(1)
        .reset_index()
    )

    return recent_summary

def analyze_player_production():

    # Reads in processed player game logs
    player_game_logs = pd.read_csv(
        PROCESSED_PLAYER_GAME_LOGS_PATH
    )

    # Groups data by player and filters last 5 games. player_game_logs is
    # pre-sorted by Player_ID and GAME_DATE in process_player_game_logs.py,
    # so tail(5) returns each player's five most recent games.
    last_five_games = (
        player_game_logs
        .groupby(
            [
                "Player_ID",
                "PLAYER_NAME"
            ]
        )
        .tail(5)
    )

    # Calculate last 5 game average PPG, RPG, AST, MIN
    last_five_production = calculate_recent_production(
        last_five_games,
        "LAST_FIVE"
    )

    # Same as above, but with last 10 games instead of 5
    last_ten_games = (
        player_game_logs
        .groupby(
            [
                "Player_ID",
                "PLAYER_NAME"
            ]
        )
        .tail(10)
    )

    last_ten_production = calculate_recent_production(
        last_ten_games,
        "LAST_TEN"
    )

    # Merge last 5 and last 10 production data
    player_recent_production = pd.merge(
        last_five_production,
        last_ten_production,
        on=[
            "Player_ID",
            "PLAYER_NAME"
        ]
    )

    # Saves to recent_player_production.csv
    output_path = RECENT_PLAYER_PRODUCTION_PATH
    player_recent_production.to_csv(
        output_path,
        index=False
    )

    print(f"\n===================================="
          f"\nSuccessfully logged recent player production."
          f"\nSaved to: {output_path}"
          f"\n====================================")


def main():
    analyze_player_production()

if __name__ == "__main__":
    main()