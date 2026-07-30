"""
Analyze recent player production from processed NBA player game logs.

This module calculates recent player performance metrics using processed
player game log data. For each player, it identifies the five most recent
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
    player_recent_production = (
        last_five_games
        .groupby(
            [
                "Player_ID",
                "PLAYER_NAME"
            ]
        )
        .agg(
            LAST_FIVE_AVG_PPG=("PTS", "mean"),
            LAST_FIVE_AVG_RPG=("REB", "mean"),
            LAST_FIVE_AVG_APG=("AST", "mean"),
            LAST_FIVE_AVG_MPG=("MIN", "mean")
        )
        .round(1)
        .reset_index()
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