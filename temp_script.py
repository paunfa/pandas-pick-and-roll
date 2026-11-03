from datetime import datetime

from utils.nba_injuries import load_injury_report

report_time = datetime(2026, 10, 27, 19, 45)

report = load_injury_report(report_time)

print("Rows:", len(report))
print("Columns:", report.columns.tolist())
print("\nStatus counts:")
print(report["Current Status"].value_counts(dropna=False))
print("\nMissing player names:", report["Player Name"].isna().sum())
print("Missing statuses:", report["Current Status"].isna().sum())
print("\nFirst five records:")
print(report.head())

# Basic data-quality checks
assert not report.empty, "The report should contain player records."
assert report["Player Name"].notna().all(), "Missing player names found."
assert report["Current Status"].notna().all(), "Missing statuses found."
assert not report["Reason"].eq("NOT YET SUBMITTED").any(), (
    "Unsubmitted-report placeholder found."
)

print("\nAll injury-report validation checks passed.")
