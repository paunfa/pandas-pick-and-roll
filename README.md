# Pandas Pick & Roll
### An NBA Fantasy Streaming Assistant

Pandas Pick & Roll is a fantasy basketball analytics project built with **Python, pandas, and Power BI**.

The project analyzes NBA schedule data and recent player performance to help fantasy basketball managers identify potential **waiver-wire pickups and streaming opportunities**.

## Goal

Build a data-driven fantasy basketball decision system that combines:

- NBA schedule analysis
- Recent player performance
- Fantasy production
- Minutes trends
- Injury-related opportunity

The long-term goal is to combine these factors into a **Streaming Score** that can be used to identify and compare potential fantasy streaming options.

## Technology

- **Python** — Data collection, processing, and analytics
- **pandas** — Data manipulation and feature engineering
- **nba_api** — NBA data collection
- **Power BI** — Planned visualization and dashboard
- **Git / GitHub** — Version control and project management

## Project Architecture

The project is organized into several stages:

**Data Collection → Raw Data → Data Processing → Feature Engineering → Fantasy Analytics → Streaming Score → Power BI Dashboard**

This separation allows raw NBA data to be collected independently from the analytics and scoring logic built on top of it.

## Current Features

### NBA Schedule Analytics

The schedule analytics pipeline currently supports:

- NBA team game-log collection
- Fantasy-week organization
- Games played per team
- Team rest-day analysis
- Back-to-back detection
- Weekly rest summaries
- Schedule advantage scoring

The Schedule Advantage model currently considers:

- **Game volume**
- **Rest advantage**
- **Back-to-back penalties**

The resulting schedule analytics are stored in processed datasets for use by downstream fantasy analysis.

### Recent Player Production

The player production pipeline collects and processes NBA player game logs and calculates recent performance metrics.

Current metrics include:

- Points per game (PPG)
- Rebounds per game (RPG)
- Assists per game (APG)
- Minutes per game (MPG)
- Fantasy points per game

Performance is analyzed across:

- **Last 5 games**
- **Last 10 games**

The pipeline also records the number of games included in each sample.

### Configurable Fantasy Scoring

Fantasy scoring is separated from the analytics logic through a configurable scoring system.

The current configuration supports **Yahoo Fantasy scoring**, including per-game fantasy point calculations.

The architecture is designed to support additional scoring systems, such as:

- ESPN
- Custom league scoring
- Other fantasy formats

### Minutes Trend

The player production pipeline also calculates a short-term **Minutes Trend**:

`Last 5 Games Average MPG − Last 10 Games Average MPG`

A positive value indicates that a player's recent average minutes are higher than their longer-term average, while a negative value indicates a decrease.

A complete 10-game sample is required for the trend to be considered valid.

## Data Outputs

Key processed datasets currently include:

- `weekly_schedule.csv`
- `weekly_rest_summary.csv`
- `schedule_advantage.csv`
- `player_recent_production.csv`

These datasets form the foundation for the project's downstream fantasy decision models.

## Project Status

### Completed

- ✅ NBA player data pipeline
- ✅ Historical NBA schedule pipeline
- ✅ Weekly schedule analysis
- ✅ Team rest and back-to-back analysis
- ✅ Schedule Advantage scoring model
- ✅ Recent player production analysis
- ✅ Last 5 / Last 10 performance analysis
- ✅ Configurable fantasy scoring framework
- ✅ Yahoo fantasy scoring
- ✅ Recent fantasy production
- ✅ Minutes Trend feature

### In Progress

- 🚧 Streaming Score model

### Planned

- ⏳ Injury Opportunity analysis
- ⏳ Additional fantasy scoring configurations
- ⏳ Power BI dashboard
- ⏳ Integration of schedule, production, minutes, and injury factors into the final Streaming Score

## Development

Development practices, project architecture details, technical debt, and the current development roadmap are documented in [`DEVELOPMENT.md`](DEVELOPMENT.md).

GitHub branches and pull requests are used to develop and review individual features before they are merged into `main`.