"""
Stores fantasy basketball scoring configurations for supported league formats.

Scoring dictionaries can be passed into fantasy point calculation functions,
allowing the analytics pipeline to support Yahoo, ESPN, and custom leagues
without modifying calculation logic.
"""

# Dictionary for Yahoo Fantasy scoring
YAHOO_SCORING = {
    "PTS": 1.0,
    "REB": 1.2,
    "AST": 1.5,
    "STL": 3.0,
    "BLK": 3.0,
    "TOV": -1.0,
}

# TO-DO: Dictionary for ESPN Fantasy Scoring
ESPN_SCORING = {}

# TO-DO: Dictionary for custom leagues
CUSTOM_SCORING = {}