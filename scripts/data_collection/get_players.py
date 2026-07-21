"""
Download player data from the NBA Stats API.

This script retrieves player data for all NBA players - active or inactive.
Stores collected data in a data frame and saves to the data/raw directory.

Creates:
      data/raw/players.csv
"""


from nba_api.stats.static import players
import pandas as pd

# Download all NBA players
nba_players = players.get_players()

# Convert to a DataFrame
all_players = pd.DataFrame(nba_players)

# Display the first few rows
print(all_players.head())

# Save the data
from utils.paths import RAW_DATA

output_path = RAW_DATA / "players.csv"

all_players.to_csv(output_path, index=False)

print("\n======================================"
      f"\nSuccessfully downloaded {len(all_players)} players!"
      f"\nList of players saved to: {output_path}"
      "\n======================================")