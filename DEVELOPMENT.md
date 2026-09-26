# Development Guide

## 1. Project Overview

**Pandas Pick & Roll** is an NBA fantasy basketball analytics project designed to identify waiver-wire pickups and streaming opportunities.

The project analyzes NBA data to produce fantasy-relevant features including:

- Schedule advantage
- Recent player production
- Minutes trends
- Injury opportunity
- Fantasy production
- Streaming score

The long-term goal is to provide these insights through a Power BI dashboard.

---

## 2. Project Architecture

The project follows this general pipeline:

```text
NBA Data
   ↓
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

The project separates raw data, processed data, feature engineering, and analytical outputs so that each stage can be validated independently.

---

## 3. Project Structure

```text
fantasy-streaming-assistant/
├── data/
│   ├── raw/
│   └── processed/
│
├── scripts/
│   ├── data_collection/
│   └── data_processing/
│
├── dashboard/
├── sql/
├── utils/
├── config/
│
├── README.md
├── DEVELOPMENT.md
└── requirements.txt
```

---

## 4. Coding Standards

### Python

- Use descriptive variable and function names.
- Avoid generic names such as `df`, `data`, or `temp` outside of quick exploration.
- Use type hints for functions.
- Add docstrings to functions.
- Keep scripts focused on a single responsibility.
- Prefer reusable functions over duplicated logic.

### DataFrames

DataFrames should describe the data they contain.

Good:

```python
players
team_game_logs
weekly_schedule
player_recent_production
streaming_scores
```

Avoid:

```python
df
data
temp
```

### Data Processing

- Convert date columns to `datetime64` before performing date calculations.
- Assign games to fantasy weeks using the Monday of that week (`WEEK_START`).
- Keep raw datasets separate from processed analytical datasets.
- Validate transformations before creating downstream features.

---

## 5. Data Modeling Principles

The project distinguishes between:

1. **Human-readable classifications**
   - Example: `SCHEDULE_RATING`

2. **Numeric scores**
   - Example: future `SCHEDULE_SCORE`

3. **Composite analytics**
   - Example: future `STREAMING_SCORE`

This separation keeps individual analytical components understandable and makes the final Streaming Score easier to explain and tune.

---

## 6. Feature Development Workflow

For each new feature:

1. Define the purpose of the feature.
2. Identify the required input dataset(s).
3. Implement the transformation.
4. Validate the output.
5. Check edge cases and missing data.
6. Remove temporary debugging code.
7. Save the processed output.
8. Commit the completed feature to a dedicated Git branch.
9. Open a pull request.
10. Review the changes before merging into `main`.

Intermediate calculations should be preserved when they provide useful transparency or may be required by future features.

---

## 7. Git Workflow

Development should use feature branches rather than making feature changes directly on `main`.

### Standard workflow

```text
main
 ↓
Create feature branch
 ↓
Develop + test
 ↓
Commit
 ↓
Push branch
 ↓
Open Pull Request
 ↓
Review
 ↓
Merge into main
 ↓
Delete feature branch
```

### Branch naming

Use descriptive feature branches such as:

```text
feature/minutes-trend
feature/injury-opportunity
feature/streaming-score
```

### Commit messages

Commits should describe meaningful changes.

Good:

```text
Add NBA schedule data collection
Add minutes trend feature
Refactor file paths using pathlib
```

Avoid:

```text
Update stuff
Fix code
Changes
```

### Pull Requests

Pull requests should contain:

- A clear title
- A short description of the change
- Relevant validation or testing information
- The files/features affected

For completed features, prefer a **squash merge** when appropriate so the `main` branch maintains a clean feature-level history.

---

## 8. Current Analytical Pipeline

### Schedule Analytics

The schedule pipeline currently produces:

- Weekly schedule information
- Team rest analysis
- Back-to-back detection
- Schedule Advantage

The Version 1 Schedule Advantage model uses:

- Game Score
- Rest Score
- Back-to-Back Penalty

The model intentionally uses transparent scoring rules so that its behavior can be understood, debugged, and tuned later.

### Player Analytics

The player production pipeline currently produces:

- Last 5-game averages
- Last 10-game averages
- Games played within each rolling window
- Points, rebounds, assists, and minutes averages
- Fantasy-point averages
- Minutes Trend

Minutes Trend currently compares:

```text
Last 5-game average MPG
        -
Last 10-game average MPG
```

A complete 10-game window is required for a valid Minutes Trend value.

### Fantasy Production

The project currently supports configurable points-based fantasy scoring.

The pipeline follows:

```text
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

Fantasy scoring is separated from calculation logic through configurable scoring dictionaries so that additional scoring systems can be added without rewriting the underlying calculation logic.

Per-game fantasy points are calculated using vectorized pandas operations rather than row-wise `DataFrame.apply()`.

The reusable `calculate_fantasy_points()` utility remains available for individual stat-line calculations, testing, and validation.

---

## 9. Current Project Status

### Completed

#### Data Collection

- NBA player data collection
- Active player dataset
- Team game log collection
- Player game log collection

#### Data Processing

- Team game log processing
- Player game log processing
- Player game log deduplication
- Chronological sorting
- Centralized project paths

#### Schedule Analytics

- Weekly schedule analytics
- Team rest analysis
- Back-to-back detection
- Schedule Advantage model

#### Player Analytics

- Recent Player Production
- Last 5-game production averages
- Last 10-game production averages
- Games played within rolling windows
- Minutes Trend

#### Fantasy Production

- Configurable fantasy scoring architecture
- Yahoo Fantasy points configuration
- Reusable fantasy-point calculation utility
- Per-game fantasy-point calculation
- Last 5-game fantasy averages
- Last 10-game fantasy averages

---

## 10. Current Development Focus

The immediate goal is to complete the points-based, per-game fantasy tracking system before expanding into additional fantasy formats.

Current/future feature priorities include:

1. Fantasy Production Score
2. Minutes Trend Score
3. Injury Opportunity Score
4. Streaming Score
5. Power BI dashboard integration

---

## 11. Technical Debt

### Data Collection

- Add retry logic for `nba_api` requests.
- Add request throttling.
- Continue collection after individual player failures.
- Log failed player IDs.

### Testing

- Add automated tests for fantasy scoring calculations.
- Add validation for scoring configurations.
- Expand test coverage for player production calculations.

### Configuration

- Complete ESPN scoring configuration.
- Implement custom league scoring configuration.
- Add validation for configurable scoring dictionaries.

---

## 12. Long-Term Goals

After the initial Pick & Roll system is fully developed, the project will expand toward 9-category fantasy basketball analysis.

Potential future capabilities include:

- 9-cat category analysis
- Category-specific player strengths and weaknesses
- Z-score based player evaluation
- Punt-category analysis
- 9-cat waiver and streaming recommendations

---

## 13. Design Principles

The project prioritizes:

- **Transparency** — individual analytical components should be understandable.
- **Modularity** — features should be reusable and independently testable.
- **Separation of concerns** — collection, processing, feature engineering, and analytics remain distinct.
- **Explainability** — scoring models should be understandable before being made more sophisticated.
- **Validation** — new features should be validated before becoming inputs to downstream models.
- **Extensibility** — scoring systems and analytical features should be configurable where practical.