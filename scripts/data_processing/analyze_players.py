"""
Reads collected NBA player data and analyzes it.

This script takes data from our players.csv file (made from the NBA Stats API)
and executes basic search functions.  Saves a list of currently active players
to the data/raw directory.

Creates:
      data/raw/active_players.csv
"""

import pandas as pd
from utils.paths import RAW_DATA

# Load the CSV we created
player_data = pd.read_csv(
      RAW_DATA / "players.csv"
)

print("=== Dataset Info ===")
print(player_data.info())

print("\n=== First 5 Players ===")
print(player_data.head())

print("\n=== Number of Players ===")
print(len(player_data))

print("\n=== Active Players ===")
print(player_data["is_active"].sum())

print("\n=== Inactive Players ===")
print(len(player_data) - player_data["is_active"].sum())

print("\n=== Players whose first names start with J")
print(player_data["first_name"].str.startswith("J").sum())






# Keep only active players
active_players = player_data[player_data["is_active"]]

print("\n=== Active Player Sample ===")
print(active_players.head())

# Save active players
output_path = RAW_DATA / "active_players.csv"

active_players.to_csv(output_path, index=False)

print("\n==========================================="
      "\nSuccessfully saved log of active players!"
      f"\nSaved to: {output_path}"
      "\n===========================================")