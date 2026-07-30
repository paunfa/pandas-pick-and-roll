"""
    Process raw NBA player game logs into a clean dataset for analysis.

    Steps:
        1. Read raw player game logs.
        2. Convert GAME_DATE to datetime.
        3. Sort games by player and game date.
        4. Remove duplicate rows.
        5. Save the processed dataset.

    Returns:
        None

    Creates:
        data/processed/player_game_logs_pro.csv
"""

import pandas as pd
from utils.paths import RAW_PLAYER_GAME_LOGS_PATH, PROCESSED_PLAYER_GAME_LOGS_PATH

def process_player_game_logs():

    # Read in raw player logs
    player_game_logs = pd.read_csv(
        RAW_PLAYER_GAME_LOGS_PATH
    )

    # Convert GAME_DATE column to datetime data type
    player_game_logs["GAME_DATE"] = pd.to_datetime(
        player_game_logs["GAME_DATE"]
    )

    # Sort by alphabetical player name and ascending game date
    player_game_logs = player_game_logs.sort_values(
        by=[
            "Player_ID",
            "GAME_DATE"
        ]
    )

    # Remove duplicate rows in the dataframe (if any)
    player_game_logs = player_game_logs.drop_duplicates()

    # Save to processed data folder
    output_path = PROCESSED_PLAYER_GAME_LOGS_PATH

    player_game_logs.to_csv(
        output_path,
        index=False
    )

    print(f"\n========================================="
          f"\nSuccessfully processed player game logs."
          f"\nRows: {len(player_game_logs):,}"
          f"\nColumns: {len(player_game_logs.columns)}"
          f"\nSaved to: {output_path}"
          f"\n=========================================")

def main():
    process_player_game_logs()

if __name__ == "__main__":
    main()