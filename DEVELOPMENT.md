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
Analytics
        ↓
Dashboard
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