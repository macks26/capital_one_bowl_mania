# Capital One Bowl Mania

Predicting NCAA Bowl Game cover probabilities using data from the CollegeFootballData (CFBD) API.

## Overview

This project fetches comprehensive college football bowl game data from the CFBD API, including:

- **Bowl Games**: Game schedules, matchups, and results
- **Team Season Statistics**: Advanced metrics adjusted for strength of schedule
- **SP+ Ratings**: Tempo and opponent-adjusted efficiency ratings
- **FPI Ratings**: Football Power Index with strength of schedule metrics
- **Betting Lines**: Game spreads and over/under lines (including closing lines)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/macks26/capital_one_bowl_mania.git
cd capital_one_bowl_mania
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up your CFBD API key:
   - Get a free API key at https://collegefootballdata.com/key
   - Copy `.env.example` to `.env`
   - Add your API key to the `.env` file

```bash
cp .env.example .env
# Edit .env and add your API key
```

**Note**: An API key is optional but recommended for higher rate limits.

## Usage

### Running the Example Script

The example script demonstrates all available API functions:

```bash
python example.py
```

This will fetch and display:
- Bowl games for the 2023 season
- Team season statistics
- SP+ ratings (strength of schedule adjusted)
- FPI ratings
- Betting lines for bowl games
- Complete dataset saved to JSON file

### Using the API Client in Your Code

Import and use the CFBD API client functions:

```python
from cfbd_api import (
    get_bowl_games,
    get_team_season_stats,
    get_sp_plus_ratings,
    get_fpi_ratings,
    get_betting_lines,
    get_bowl_game_complete_data
)

# Get all bowl games for 2023
bowl_games = get_bowl_games(2023)

# Get team stats for a specific team
alabama_stats = get_team_season_stats(2023, team="Alabama")

# Get SP+ ratings (includes strength of schedule)
sp_ratings = get_sp_plus_ratings(2023)

# Get betting lines for bowl games
betting_lines = get_betting_lines(2023, season_type="postseason")

# Get all data in one call
complete_data = get_bowl_game_complete_data(2023)
```

## API Functions

### `get_bowl_games(year, season_type="postseason")`
Fetches bowl games for a specific year.

**Parameters:**
- `year` (int): Year to fetch games for
- `season_type` (str): "postseason" for bowl games

**Returns:** List of game dictionaries

### `get_team_season_stats(year, team=None, conference=None)`
Fetches advanced team statistics including strength metrics.

**Parameters:**
- `year` (int): Year to fetch stats for
- `team` (str, optional): Specific team name
- `conference` (str, optional): Conference name

**Returns:** List of team statistics

### `get_sp_plus_ratings(year, team=None)`
Fetches SP+ ratings (tempo and opponent-adjusted efficiency).

**Parameters:**
- `year` (int): Year to fetch ratings for
- `team` (str, optional): Specific team name

**Returns:** List of SP+ ratings

### `get_fpi_ratings(year, team=None)`
Fetches FPI (Football Power Index) ratings including strength of schedule.

**Parameters:**
- `year` (int): Year to fetch ratings for
- `team` (str, optional): Specific team name

**Returns:** List of FPI ratings

### `get_betting_lines(year, week=None, season_type="postseason", team=None, home=None, away=None)`
Fetches betting lines including spreads and over/under.

**Parameters:**
- `year` (int): Year to fetch lines for
- `week` (int, optional): Week number
- `season_type` (str): "postseason" for bowl games
- `team` (str, optional): Specific team name
- `home` (str, optional): Home team name
- `away` (str, optional): Away team name

**Returns:** List of games with betting line information

### `get_bowl_game_complete_data(year)`
Convenience function that fetches all relevant data in a single call.

**Parameters:**
- `year` (int): Year to fetch data for

**Returns:** Dictionary containing all data types

## Data Sources

All data is sourced from the [CollegeFootballData API](https://collegefootballdata.com/), which aggregates:
- Game schedules and results
- Advanced team statistics
- SP+ ratings from ESPN
- FPI ratings from ESPN  
- Betting lines from various sportsbooks

## Requirements

- Python 3.7+
- requests >= 2.31.0
- python-dotenv >= 1.0.0

## License

This project uses data from the CollegeFootballData API. Please review their [terms of service](https://collegefootballdata.com/terms-of-service).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
