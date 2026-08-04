"""
Utility functions for calculating fantasy basketball points.

Fantasy point calculations use configurable scoring dictionaries,
allowing support for Yahoo, ESPN, and custom league formats.
"""
import pandas as pd

def calculate_fantasy_points(
    player_stats: dict | pd.Series,
    scoring: dict
) -> float:
    """
    Calculates fantasy points for a player's stat line using the
    provided scoring configuration.

    Args:
        player_stats (pd.Series | dict):
            Player statistics for a single game.

        scoring (dict):
            Fantasy scoring configuration.

    Returns:
        float:
            Fantasy points for the player's stat line.
    """

    fantasy_points = 0.0

    for stat, weight in scoring.items():
        fantasy_points += player_stats.get(stat, 0) * weight

    return fantasy_points