import pandas as pd

# Load the CSV we created
df = pd.read_csv("../data/players.csv")

print("=== Dataset Info ===")
print(df.info())

print("\n=== First 5 Players ===")
print(df.head())

print("\n=== Number of Players ===")
print(len(df))

print("\n=== Active Players ===")
print(df["is_active"].sum())

print("\n=== Inactive Players ===")
print(len(df) - df["is_active"].sum())