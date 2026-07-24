"""
Reads players from active_players list; extracts data from playergamelog to create
a dataframe containing stats for every game.

Currently running in test mode to reduce processing time because dataset is large.

Creates:
    data/raw/player_game_logs_raw.csv
"""

import pandas as pd
from nba_api.stats.endpoints import playergamelog
from utils.paths import RAW_DATA


def get_player_logs(player_id, player_name):

    print(f"Collecting {player_name}")

    logs = playergamelog.PlayerGameLog(
        player_id=player_id
    )

    game_log = logs.get_data_frames()[0]

    game_log["PLAYER_NAME"] = player_name

    return game_log


def main():

    players = pd.read_csv(
        RAW_DATA / "active_players.csv"
    )

    # Limit the number of players during development to speed up testing.
    TEST_MODE = True

    if TEST_MODE:
        players = players.head(10)

    all_logs = []

    for _, player in players.iterrows():

        player_logs = get_player_logs(
            player["id"],
            player["full_name"]
        )

        all_logs.append(player_logs)

    player_game_logs = pd.concat(
        all_logs,
        ignore_index=True
    )

    output_path = RAW_DATA / "player_game_logs_raw.csv"

    player_game_logs.to_csv(
        output_path,
        index=False
    )

    print(f"\n======================================="
          f"\nSuccessfully saved player game logs."
          f"\nSaved to: {output_path}"
          f"\n=======================================")


if __name__ == "__main__":
    main()