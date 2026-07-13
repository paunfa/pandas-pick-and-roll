from nba_api.stats.static import players
import pandas as pd

# Download all NBA players
nba_players = players.get_players()

# Convert to a DataFrame
df = pd.DataFrame(nba_players)

# Display the first few rows
print(df.head())

# Save the data
df.to_csv("../data/players.csv", index=False)

print(f"\nSuccessfully downloaded {len(df)} players!")