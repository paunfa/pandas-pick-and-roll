"""
Download player data from the NBA Stats API.

This script retrieves player data for all NBA players - active or inactive.
Stores collected data in a data frame and saves to the data/raw directory.
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
from pathlib import Path

project_root = Path(__file__).resolve().parents[2]

output_path = project_root / "data" / "raw" / "players.csv"

all_players.to_csv(output_path, index=False)

print("\n======================================"
      f"\nSuccessfully downloaded {len(all_players)} players!"
      "\n======================================")