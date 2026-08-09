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

# Fantasy Scoring Design Decisions

Fantasy points are calculated at the individual game level before recent
production averages are calculated.

Per-game fantasy points are calculated using vectorized pandas operations
rather than row-wise `DataFrame.apply()`.

The reusable `calculate_fantasy_points()` utility remains available for
individual stat-line calculations, testing, and validation, while the
production pipeline uses vectorized calculations for efficiency.

---

# Current Development Goals

### Completed

#### Data Collection

* NBA player data collection
* Active player dataset
* Team game log collection
* Player game log collection

#### Data Processing

* Team game log processing
* Player game log processing
* Player game log deduplication and chronological sorting

#### Schedule Analytics

* Weekly schedule analytics
* Team rest analysis
* Schedule Advantage model

#### Player Analytics

* Recent Player Production v1
* Recent Player Production v2
* Last 5-game production averages
* Last 10-game production averages
* Games played within each rolling window

#### Fantasy Production

* Configurable fantasy scoring architecture
* Initial Yahoo Fantasy scoring configuration
* Reusable fantasy point calculation utility
* Per-game fantasy point calculation
* Last 5-game average fantasy points
* Last 10-game average fantasy points

### In Progress

#### Per-Game Fantasy Tracking

* Continue expanding the fantasy production foundation
* Develop additional fantasy-relevant player production metrics
* Prepare fantasy production features for integration into the Streaming Score

### Technical Debt

#### Data Collection

* Add retry logic for `nba_api` requests
* Add request throttling (`time.sleep`)
* Continue collection after individual player failures
* Log failed player IDs

#### Testing

* Add automated tests for fantasy scoring calculations
* Add validation for scoring configurations
* Expand test coverage for player production calculations

#### Configuration

* Complete ESPN scoring configuration
* Implement custom league scoring configuration
* Add validation for configurable scoring dictionaries

### Future Feature Engineering

The immediate goal is to complete the points-based, per-game fantasy tracking system before expanding into additional fantasy formats.

Planned features include:

* Fantasy Production Score
* Minutes Trend Score
* Injury Opportunity Score
* Streaming Score

### Long-Term Fantasy Goals

After the initial Pick & Roll project is fully developed, prioritize long-term support for 9-category (9-cat) fantasy basketball analysis.

Potential future expansion includes:

* 9-cat category analysis
* Category-specific player strengths and weaknesses
* Z-score based player evaluation
* Punt-category analysis
* 9-cat waiver and streaming recommendations


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

## Day 5: Recent Player Production

### Recent Player Production (v1)

Created a complete player analytics pipeline.

Data Collection:
- get_player_game_logs.py

Processing:
- process_player_game_logs.py

Feature Engineering:
- analyze_player_production.py

Outputs:
- player_game_logs_raw.csv
- player_game_logs_pro.csv
- player_recent_production.csv

### Lessons Learned

- Use `groupby().tail(n)` to isolate each player's most recent games.
- Separate data processing from feature engineering.
- Validate intermediate datasets before creating downstream features.
- Maintain descriptive variable names and consistent project structure.

## Day 6: Recent Player Production v2

- Refactored production aggregation into reusable helper function:
    calculate_recent_production()

- Added rolling 10-game production analysis

- Added games played counts for each rolling window

- Merged 5-game and 10-game summaries into a unified
  player_recent_production.csv dataset

- Improved variable naming consistency

- Added function type hints and documentation

## Day 7: Fantasy Production Foundation
- Created config/fantasy_scoring.py to centralize fantasy scoring configurations.
- Chose a dictionary-based configuration approach to allow scoring systems to be passed into reusable calculation functions.
- Planned a reusable fantasy point utility that will consume scoring dictionaries and produce fantasy point totals independent of league format.



The project currently supports configurable points-based fantasy scoring.

The fantasy production pipeline follows this structure:

```
Player Game Logs
        ↓
Processed Player Game Logs
        ↓
Fantasy Scoring Configuration
        ↓
Per-Game Fantasy Points
        ↓
Recent Player Production
        ↓
Last 5 / Last 10 Fantasy Averages
```

The initial scoring configuration is based on Yahoo Fantasy points scoring.

Fantasy scoring is separated from the calculation logic through configurable
scoring dictionaries, allowing future support for ESPN and custom league
formats without changing the underlying fantasy point calculation logic.

Current fantasy production features include:

- `FANTASY_POINTS`
- `LAST_FIVE_AVG_FANTASY_PTS`
- `LAST_TEN_AVG_FANTASY_PTS`