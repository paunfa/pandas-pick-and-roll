# Development Guide

## Project Overview

Pandas Pick & Roll is an NBA fantasy basketball analytics dashboard designed to help fantasy managers identify waiver wire pickups and streaming opportunities.

The project uses NBA data to calculate fantasy-relevant insights including:
- Schedule advantages
- Player trends
- Minutes opportunities
- Streaming scores

---

# Project Structure
```
fantasy-streaming-assistant/
├── data/
│ ├── raw/
│ └── processed/
│
├── scripts/
│ ├── data_collection/
│ └── data_processing/
│
├── dashboard/
├── sql/
├── utils/
|
├── README.md
├── DEVELOPMENT.md
└── requirements.txt
```

---

# Coding Standards

## Python Style

Follow these conventions:

- Use descriptive variable names.
- Avoid generic names like `df` outside of quick exploration.
- Use type hints for functions.
- Add docstrings to functions.
- Keep scripts focused on one responsibility.

## Data Modeling Principles

The project separates:

- Human-readable classifications (e.g., `SCHEDULE_RATING`)
- Numeric scores (future `SCHEDULE_SCORE`)
- Composite analytics (future `STREAMING_SCORE`)

## Development Workflow

For each new feature:

1. Write the transformation.
2. Verify with temporary print statements.
3. Validate the output.
4. Remove temporary debugging output.
5. Save the processed dataset.
---

# Data Processing Standards

- Convert date columns to `datetime64` before performing any date calculations.
- Assign each game to a fantasy week using the Monday of that week (`WEEK_START`).
- Validate each transformation with temporary print statements, then remove them once verified.

---

# DataFrame Naming

DataFrames should describe the data they contain.

## Examples:

### Good:

```
players
team_game_logs
weekly_schedule
streaming_scores
```
### AVOID:
```
df
data
temp
```
---

# Functions

Functions should include:

* A descriptive name
* Type hints
* A docstring

Example:

```python
def get_opponent(matchup: str) -> str:
    """
    Extract opponent team abbreviation.

    Args:
        matchup: NBA matchup string.

    Returns:
        Opponent team abbreviation.
    """
```
--- 
# Data Pipeline Philosophy

 The project follows this structure:

```
Data Collection
        ↓
Raw Data
        ↓
Data Processing
        ↓
Feature Engineering
        ↓
Analytics Models
        ↓
Streaming Score  
        ↓
Power BI Dashboard
```

---

# Git Workflow

Commits should describe meaningful changes.

### Examples:

Good:

```
Add NBA schedule data collection

Create Weekly schedule analysis

Refactor file paths using pathlib
```

Avoid:
```
Update stuff

Fix code

Changes
```

---

# Current Development Goals

### Completed
* NBA player data collection
* Active player dataset
* Team game log collection

### In Progress
* Weekly schedule advantage tracker

### Future
* Fantasy production model
* Minutes trend analysis
* Injury opportunity scoring
* Streaming Score engine
* Power BI dashboard

---
# DEV DIARY

## Day 2: Weekly Schedule Analytics Pipeline

Completed:
- Built NBA schedule data collection pipeline
- Created raw and processed data structure
- Added weekly schedule calculations
- Added schedule strength ratings
- Improved script organization
- Connected project to GitHub
- Established main branch workflow

Git concepts learned:
- Feature branches
- Remote repositories
- Push/pull workflow
- Branch merging
- Default branch management

## Day 3: Per-Team Rest Day Analysis

### Completed

- Added shared path utilities
- Built rest analysis pipeline
- Calculated days between games
- Calculated actual rest days
- Detected back-to-back games
- Created team rest summary dataset

### Design Decisions

- Kept raw game logs separate from processed analytics outputs
- FINALLY stopped saving intermediate outputs to be more efficient with our space
  - Saved team-level summaries instead of duplicate game-level datasets
- Distinguished calendar gaps from actual rest days

## Day 4: Code Quality Refactoring and Weekly Schedule Advantage Score

- Added main() functions to all project scripts.
- Removed unnecessary debug print statements.
- Standardized script structure across the project.
- Removed `games_by_team.csv` because it duplicated information already available in the processed schedule pipeline.

  - The project now prioritizes analytical outputs over intermediate aggregations that do not create additional decision-making value.
- Renamed schedule datasets for clearer raw/processed separation:
  - team_game_logs_raw.csv
  - team_game_logs_pro.csv
- Updated utils/paths.py with centralized file path constants.
  
### Data Pipeline

Current schedule pipeline:
```
NBA API
    ↓
get_schedule.py
    ↓
team_game_logs_raw.csv
    ↓
process_schedule.py
    ↓
team_game_logs_pro.csv
    ├── weekly_schedule.csv
    ├── team_rest_summary.csv
    ├── weekly_rest_summary.csv
    └── schedule_advantage.csv
```

### Schedule Advantage Model (Version 1)

- Inputs:

  - weekly_schedule.csv
  - weekly_rest_summary.csv

- Scoring Components:

  - Game Score
  - Rest Score
  - Back-to-Back Penalty

- Output:

  - schedule_advantage.csv

* Version 1 intentionally uses transparent scoring rules to support debugging, explainability, and future model tuning.