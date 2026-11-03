
from datetime import datetime
from pathlib import Path
import unicodedata

import pandas as pd
from nba_api.stats.endpoints import commonallplayers

from utils.nba_injuries import load_injury_report


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent

ACTIVE_PLAYERS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "active_players.csv"
)

ALL_PLAYERS_PATH = (
    PROJECT_ROOT / "data" / "raw" / "players.csv"
)

REPORT_TIME = datetime(2026, 10, 27, 19, 45)
NBA_SEASON = "2026-27"


# --------------------------------------------------
# NAME NORMALIZATION
# --------------------------------------------------

def normalize_name(name):
    """Standardize player names for reliable matching."""

    if pd.isna(name):
        return ""

    name = str(name).strip().casefold()
    name = name.replace(",", "")

    # Normalize accented and special characters.
    name = unicodedata.normalize("NFKD", name)
    name = "".join(
        char
        for char in name
        if not unicodedata.combining(char)
    )

    # Remove extra whitespace.
    return " ".join(name.split())


def normalize_injury_name(name):
    """
    Convert injury report names from Last, First format
    into First Last format before normalizing.
    """

    if pd.isna(name):
        return ""

    name = str(name).strip()
    parts = [part.strip() for part in name.split(",")]

    if len(parts) == 2:
        last_name, first_name = parts
        name = f"{first_name} {last_name}"

    elif len(parts) == 3:
        last_name, suffix, first_name = parts
        name = f"{first_name} {last_name} {suffix}"

    return normalize_name(name)


# --------------------------------------------------
# LOAD INJURY REPORT
# --------------------------------------------------

print("\nLoading NBA injury report...")

injuries = load_injury_report(REPORT_TIME)

print(f"Total injury records: {len(injuries)}")

print("\nInjury status counts:")
print(injuries["Current Status"].value_counts())


# --------------------------------------------------
# LOAD PLAYER REGISTRIES
# --------------------------------------------------

print("\nLoading player registries...")

active_players = pd.read_csv(ACTIVE_PLAYERS_PATH)
all_players = pd.read_csv(ALL_PLAYERS_PATH)

print(f"Active player records: {len(active_players)}")
print(f"Historical player records: {len(all_players)}")


# --------------------------------------------------
# NORMALIZE PLAYER NAMES
# --------------------------------------------------

injuries["MATCH_NAME"] = (
    injuries["Player Name"].apply(normalize_injury_name)
)

active_players["MATCH_NAME"] = (
    active_players["full_name"].apply(normalize_name)
)

all_players["MATCH_NAME"] = (
    all_players["full_name"].apply(normalize_name)
)


# --------------------------------------------------
# CHECK ACTIVE REGISTRY FOR DUPLICATES
# --------------------------------------------------

print("\nChecking active registry for duplicate names...")

duplicate_names = active_players[
    active_players["MATCH_NAME"].duplicated(keep=False)
].sort_values("MATCH_NAME")

if duplicate_names.empty:
    print("No duplicate normalized names found.")
else:
    print("Duplicate normalized names found:")
    print(duplicate_names[["full_name", "id", "MATCH_NAME"]])


# --------------------------------------------------
# MATCH INJURIES TO ACTIVE PLAYERS
# --------------------------------------------------

print("\nMatching injury records to active players...")

active_matches = injuries.merge(
    active_players[["id", "full_name", "MATCH_NAME"]],
    on="MATCH_NAME",
    how="left",
    validate="many_to_one",
    indicator=True
)

matched = active_matches[
    active_matches["_merge"] == "both"
].copy()

unmatched = active_matches[
    active_matches["_merge"] == "left_only"
].copy()

print(f"\nTotal injury records: {len(injuries)}")
print(f"Matched to active registry: {len(matched)}")
print(f"Unmatched to active registry: {len(unmatched)}")



# --------------------------------------------------
# CHECK UNMATCHED PLAYERS AGAINST HISTORICAL REGISTRY
# --------------------------------------------------

print("\nChecking unmatched players against historical registry...")

# Identify duplicate normalized names in the historical registry.
historical_duplicates = all_players[
    all_players["MATCH_NAME"].duplicated(keep=False)
].sort_values("MATCH_NAME")

print(
    f"Duplicate normalized names in historical registry: "
    f"{historical_duplicates['MATCH_NAME'].nunique()}"
)

if not historical_duplicates.empty:
    print("\nHistorical registry duplicates:")
    print(
        historical_duplicates[
            ["full_name", "id", "MATCH_NAME"]
        ].to_string(index=False)
    )

# Check whether unmatched injury names exist in the historical registry.
historical_names = set(all_players["MATCH_NAME"])

found_in_historical = unmatched[
    unmatched["MATCH_NAME"].isin(historical_names)
].copy()

missing_from_historical = unmatched[
    ~unmatched["MATCH_NAME"].isin(historical_names)
].copy()

print(
    f"\nFound in historical registry: "
    f"{len(found_in_historical)}"
)

print(
    f"Missing from historical registry: "
    f"{len(missing_from_historical)}"
)

# Show the historical player records for matching names.
if not found_in_historical.empty:
    historical_candidates = found_in_historical[
        ["Player Name", "MATCH_NAME"]
    ].merge(
        all_players[["id", "full_name", "MATCH_NAME"]],
        on="MATCH_NAME",
        how="left"
    )

    print("\nHistorical player matches:")
    print(
        historical_candidates[
            ["Player Name", "id", "full_name"]
        ].to_string(index=False)
    )


# --------------------------------------------------
# CHECK UNMATCHED PLAYERS AGAINST DYNAMIC NBA REGISTRY
# --------------------------------------------------

print("\nDownloading dynamic NBA player registry...")

dynamic_players = commonallplayers.CommonAllPlayers(
    is_only_current_season=0,
    league_id="00",
    season=NBA_SEASON,
).get_data_frames()[0]

dynamic_players["MATCH_NAME"] = (
    dynamic_players["DISPLAY_FIRST_LAST"].apply(normalize_name)
)

print(f"Dynamic registry records: {len(dynamic_players)}")


# Compare names that were not found in the active registry.
missing_from_dynamic = unmatched[
    ~unmatched["MATCH_NAME"].isin(dynamic_players["MATCH_NAME"])
].copy()

found_in_dynamic = unmatched[
    unmatched["MATCH_NAME"].isin(dynamic_players["MATCH_NAME"])
].copy()

print("\nDynamic registry matching results:")
print(f"Found in dynamic registry: {len(found_in_dynamic)}")
print(f"Still unmatched: {len(missing_from_dynamic)}")


# --------------------------------------------------
# FINAL UNMATCHED PLAYER REPORT
# --------------------------------------------------

if missing_from_dynamic.empty:
    print("\nAll injury report player names were found in the dynamic registry.")
else:
    print("\nPlayers still missing from the dynamic registry:")

    print(
        missing_from_dynamic[
            ["Player Name", "Current Status", "MATCH_NAME"]
        ].to_string(index=False)
    )


# --------------------------------------------------
# NAME NORMALIZATION SANITY CHECK
# --------------------------------------------------

print("\nErnest Udeh Jr. normalization check:")

print(
    normalize_injury_name("Udeh, Jr., Ernest")
)

print(
    normalize_name("Ernest Udeh, Jr.")
)

print("\nPlayer matching diagnostic complete.")
