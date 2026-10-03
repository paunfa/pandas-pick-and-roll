from datetime import date

from config.settings import (
    NBA_SEASON_OVERRIDE,
    NBA_REGULAR_SEASON_START_MONTH,
    NBA_REGULAR_SEASON_START_DAY
)


def determine_target_season(current_date=None):
    """
    Determine the NBA regular season to use for data collection.

    A manual season override takes precedence over automatic
    season selection.

    Args:
        current_date: Date used to determine the target season.
            Defaults to today's date.

    Returns:
        NBA season string in YYYY-YY format.
    """

    if NBA_SEASON_OVERRIDE is not None:
        return NBA_SEASON_OVERRIDE

    if current_date is None:
        current_date = date.today()

    season_start = date(
        current_date.year,
        NBA_REGULAR_SEASON_START_MONTH,
        NBA_REGULAR_SEASON_START_DAY
    )

    if current_date >= season_start:
        season_start_year = current_date.year
    else:
        season_start_year = current_date.year - 1

    return (
        f"{season_start_year}-"
        f"{str(season_start_year + 1)[-2:]}"
    )

