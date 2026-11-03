
from datetime import datetime

import pandas as pd
from nbainjuries import injury


EXPECTED_COLUMNS = [
    "Game Date",
    "Game Time",
    "Matchup",
    "Team",
    "Player Name",
    "Current Status",
    "Reason",
]


def load_injury_report(report_time: datetime) -> pd.DataFrame:
    """
    Load and validate an official NBA injury report.

    Args:
        report_time: Date and time associated with the NBA report.

    Returns:
        A DataFrame containing actual player records, excluding
        placeholder rows for teams that have not submitted reports.

    Raises:
        ValueError: If the report is invalid or has an unexpected structure.
    """
    if not injury.check_reportvalid(report_time):
        raise ValueError(
            f"No valid NBA injury report found for {report_time}."
        )

    report = injury.get_reportdata(
        timestamp=report_time,
        return_df=True,
    )

    if not isinstance(report, pd.DataFrame):
        raise ValueError("The injury report did not return a DataFrame.")

    missing_columns = [
        column for column in EXPECTED_COLUMNS
        if column not in report.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Injury report is missing expected columns: {missing_columns}"
        )

    # Remove placeholders for teams that have not submitted reports.
    player_report = report.dropna(
        subset=["Player Name", "Current Status"]
    ).copy()

    # Exclude any remaining unsubmitted-report placeholders.
    player_report = player_report[
        player_report["Reason"].ne("NOT YET SUBMITTED")
    ].copy()

    return player_report.reset_index(drop=True)
