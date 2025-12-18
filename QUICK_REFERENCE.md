# CFBD API Quick Reference

## Overview

This guide provides quick reference for using the CFBD API client to fetch bowl game data.

## Getting Started

```python
from cfbd_api import (
    get_bowl_games,
    get_team_season_stats,
    get_sp_plus_ratings,
    get_fpi_ratings,
    get_betting_lines,
    get_bowl_game_complete_data
)
```

## Common Use Cases

### 1. Get All Bowl Games for a Season

```python
# Get all bowl games for 2023
games = get_bowl_games(2023)

# Access game details
for game in games:
    home_team = game['home_team']
    away_team = game['away_team']
    venue = game['venue']
    start_date = game['start_date']
```

### 2. Get Team Stats with Strength of Schedule

```python
# Get all team stats
all_stats = get_team_season_stats(2023)

# Get stats for a specific team
alabama_stats = get_team_season_stats(2023, team="Alabama")

# Access offensive and defensive metrics
for stats in all_stats:
    team = stats['team']
    offense = stats['offense']
    defense = stats['defense']
    
    # Metrics include success rate, explosiveness, etc.
    off_success_rate = offense.get('successRate')
    def_success_rate = defense.get('successRate')
```

### 3. Get SP+ Ratings (Strength of Schedule Adjusted)

```python
# SP+ is a tempo- and opponent-adjusted measure
sp_ratings = get_sp_plus_ratings(2023)

# Get for specific team
georgia_sp = get_sp_plus_ratings(2023, team="Georgia")

# Access rating components
for rating in sp_ratings:
    team = rating['team']
    overall = rating['rating']
    offense = rating['offense']
    defense = rating['defense']
    special_teams = rating['specialTeams']
```

### 4. Get FPI Ratings with Strength of Schedule

```python
# FPI includes explicit SOS metric
fpi_ratings = get_fpi_ratings(2023)

for rating in fpi_ratings:
    team = rating['team']
    fpi = rating['fpi']
    sos = rating['sos']  # Strength of schedule
```

### 5. Get Betting Lines (Including Closing Spreads)

```python
# Get betting lines for bowl games
betting_lines = get_betting_lines(2023, season_type="postseason")

# Get lines for specific matchup
lines = get_betting_lines(
    2023,
    home="Alabama",
    away="Georgia",
    season_type="postseason"
)

# Access line data
for game in betting_lines:
    home = game['homeTeam']
    away = game['awayTeam']
    
    # Multiple providers may be available
    for line in game.get('lines', []):
        provider = line['provider']
        spread = line.get('spread')
        over_under = line.get('overUnder')
```

### 6. Get All Data at Once

```python
# Fetch everything in one call
data = get_bowl_game_complete_data(2023)

# Access different data types
bowl_games = data['bowl_games']
team_stats = data['team_stats']
sp_plus = data['sp_plus']
fpi = data['fpi']
betting_lines = data['betting_lines']

# Save to file
import json
with open('bowl_data_2023.json', 'w') as f:
    json.dump(data, f, indent=2)
```

## Strength of Schedule Metrics

### Where to Find SOS Data

1. **SP+ Ratings**: Inherently adjusted for opponent quality (tempo and opponent-adjusted)
   - Access via: `get_sp_plus_ratings(year)`
   - Rating is already SOS-adjusted

2. **FPI Ratings**: Explicit SOS metric
   - Access via: `get_fpi_ratings(year)`
   - Check: `rating['sos']`

3. **Advanced Team Stats**: Contains opponent-adjusted metrics
   - Access via: `get_team_season_stats(year)`
   - Includes success rates and explosiveness metrics

## Example: Analyzing a Bowl Game Matchup

```python
year = 2023
team1 = "Alabama"
team2 = "Georgia"

# Get both teams' stats
team1_stats = get_team_season_stats(year, team=team1)
team2_stats = get_team_season_stats(year, team=team2)

# Get SP+ ratings (SOS-adjusted)
team1_sp = get_sp_plus_ratings(year, team=team1)
team2_sp = get_sp_plus_ratings(year, team=team2)

# Get FPI with explicit SOS
team1_fpi = get_fpi_ratings(year, team=team1)
team2_fpi = get_fpi_ratings(year, team=team2)

# Get betting lines
lines = get_betting_lines(year, home=team1, away=team2, season_type="postseason")

# Now you have comprehensive data for analysis:
# - Advanced stats
# - Strength-adjusted ratings
# - Market expectations (betting lines)
```

## API Rate Limits

- **Without API Key**: Limited requests per hour
- **With Free API Key**: Higher rate limits
- **Get a key**: https://collegefootballdata.com/key

To use your API key:
1. Copy `.env.example` to `.env`
2. Add your key: `CFBD_API_KEY=your_key_here`

## Data Freshness

- Historical data is stable
- Current season data updates regularly
- Betting lines update as games approach
- Closing lines available after games complete

## Error Handling

```python
try:
    games = get_bowl_games(2023)
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")
```

## Additional Resources

- CFBD API Documentation: https://api.collegefootballdata.com/api/docs
- Get API Key: https://collegefootballdata.com/key
- SP+ Explanation: https://www.espn.com/college-football/story/_/id/17207291
- FPI Explanation: https://www.espn.com/blog/statsinfo/post/_/id/122612

## Common Gotchas

1. **Team Names**: Use exact names as they appear in CFBD (e.g., "Ohio State", not "OSU")
2. **Season Types**: Use "postseason" for bowl games, "regular" for regular season
3. **Year**: Refers to the season year (2023 bowl games are part of 2023 season)
4. **Betting Lines**: May have multiple providers; look for "consensus" or your preferred source
5. **Missing Data**: Not all metrics available for all years; check for None/null values
