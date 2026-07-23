# Pandas Pick & Roll
### An NBA Fantasy Streaming Assistant

A fantasy basketball analytics project built with Python and Power BI.

## Goal

Help fantasy basketball managers identify the best waiver-wire pickups and streaming opportunities using NBA schedule and player performance data.

## Tools

- Python
- pandas
- nba_api
- Power BI
- GitHub




# Progress Log

## Current Progress

- ✅ Player data pipeline
- ✅ Historical schedule pipeline
- 🚧 Streaming Score model
- ⏳ Power BI dashboard

## Completed Analytics Features

- ✅ Weekly Schedule Advantage Analysis
- ✅ Team Rest & Back-to-Back Analysis
- ✅ Schedule Advantage Scoring Model (Version 1)
---
## Day 1 Completed Features
- Set up Python environment
- Created Git repository
- Built NBA player data pipeline
- Added initial data exploration scripts
---
## Day 2 Completed Features

### Weekly Schedule Advantage Tracker

The dashboard now includes a historical NBA schedule pipeline.

Current capabilities:
- Collect NBA team game logs
- Organize games by fantasy week
- Calculate games played per team
- Classify schedule strength

Schedule categories:
- 4+ games: Very Strong
- 3 games: Strong
- 2 games: Weak
- 1 game or less: Very Weak
---
## Day 3 Completed Features
### Per-Team Rest Day Analysis

Features added:
- Player data collection
- Weekly schedule analysis
- Team rest analysis
- Back-to-back detection
---
## Day 4 Completed Features
### Schedule Processing Pipeline
- Separated raw and processed schedule data.
- Introduced team_game_logs_raw.csv and team_game_logs_pro.csv.
- Standardized the schedule processing pipeline for downstream analytics.

### Weekly Rest Analysis
- Added weekly rest aggregation by fantasy week.
- Calculated:
  - Back-to-backs
  - Average rest days
  - Minimum rest
  - Maximum rest
  - Generated weekly_rest_summary.csv.
    
### Schedule Advantage Model (Version 1)

- Implemented the first fantasy decision model by combining:

  - Weekly game volume
  - Rest advantage
  - Back-to-back penalties

- Created schedule_advantage.csv containing:

  - GAME_SCORE
  - REST_SCORE
  - B2B_PENALTY
  - SCHEDULE_ADVANTAGE