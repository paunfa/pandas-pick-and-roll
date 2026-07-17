import pandas as pd

# Load the CSV we created
player_data = pd.read_csv("../../data/raw/players.csv")

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
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

output_path = project_root / "data" / "raw" / "active_players.csv"

active_players.to_csv(output_path, index=False)

print(f"\nSuccessfully saved log of active players to {output_path}!")