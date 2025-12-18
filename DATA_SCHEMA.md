# CFBD API Data Schema Reference

This document describes the data structures returned by each API function.

## Bowl Games (`get_bowl_games`)

```python
{
    "id": int,                      # Unique game ID
    "season": int,                  # Season year
    "week": int,                    # Week number
    "season_type": str,             # "postseason" for bowl games
    "start_date": str,              # ISO 8601 datetime
    "start_time_tbd": bool,         # Whether time is TBD
    "completed": bool,              # Whether game has finished
    "neutral_site": bool,           # Whether neutral site
    "conference_game": bool,        # Whether conference game
    "attendance": int,              # Attendance number
    "venue_id": int,                # Venue ID
    "venue": str,                   # Venue name
    "home_id": int,                 # Home team ID
    "home_team": str,               # Home team name
    "home_conference": str,         # Home team conference
    "home_division": str,           # FBS/FCS
    "home_points": int,             # Home team score
    "home_line_scores": [int],      # Scores by quarter
    "home_post_win_prob": float,    # Post-game win probability
    "home_pregame_elo": int,        # Pre-game Elo rating
    "home_postgame_elo": int,       # Post-game Elo rating
    "away_id": int,                 # Away team ID
    "away_team": str,               # Away team name
    "away_conference": str,         # Away team conference
    "away_division": str,           # FBS/FCS
    "away_points": int,             # Away team score
    "away_line_scores": [int],      # Scores by quarter
    "away_post_win_prob": float,    # Post-game win probability
    "away_pregame_elo": int,        # Pre-game Elo rating
    "away_postgame_elo": int,       # Post-game Elo rating
    "excitement_index": float,      # Game excitement metric
    "highlights": str,              # Video highlights URL
    "notes": str                    # Additional notes
}
```

## Team Season Stats (`get_team_season_stats`)

```python
{
    "season": int,                  # Season year
    "team": str,                    # Team name
    "conference": str,              # Conference name
    "offense": {
        "plays": int,               # Total offensive plays
        "drives": int,              # Number of drives
        "ppa": float,               # Predicted Points Added per play
        "totalPPA": float,          # Total PPA
        "successRate": float,       # Success rate (0-1)
        "explosiveness": float,     # Explosiveness metric
        "powerSuccess": float,      # Power running success
        "stuffRate": float,         # Rate of stuffed runs
        "lineYards": float,         # O-line yards
        "lineYardsTotal": float,    # Total line yards
        "secondLevelYards": float,  # Second level yards
        "secondLevelYardsTotal": float,
        "openFieldYards": float,    # Open field yards
        "openFieldYardsTotal": float,
        "standardDowns": {          # Performance on standard downs
            "ppa": float,
            "successRate": float,
            "explosiveness": float
        },
        "passingDowns": {           # Performance on passing downs
            "ppa": float,
            "successRate": float,
            "explosiveness": float
        },
        "rushingPlays": {           # Rushing play stats
            "ppa": float,
            "successRate": float,
            "explosiveness": float
        },
        "passingPlays": {           # Passing play stats
            "ppa": float,
            "successRate": float,
            "explosiveness": float
        }
    },
    "defense": {
        # Same structure as offense
        # Represents defensive performance
    }
}
```

## SP+ Ratings (`get_sp_plus_ratings`)

```python
{
    "year": int,                    # Season year
    "team": str,                    # Team name
    "conference": str,              # Conference name
    "rating": float,                # Overall SP+ rating
    "ranking": int,                 # National ranking
    "secondOrderWins": float,       # Expected wins based on SP+
    "sos": float,                   # Strength of schedule (implicit in rating)
    "offense": {
        "ranking": int,             # Offensive ranking
        "rating": float             # Offensive SP+ rating
    },
    "defense": {
        "ranking": int,             # Defensive ranking
        "rating": float             # Defensive SP+ rating
    },
    "specialTeams": {
        "ranking": int,             # Special teams ranking
        "rating": float             # Special teams rating
    }
}
```

## FPI Ratings (`get_fpi_ratings`)

```python
{
    "year": int,                    # Season year
    "team": str,                    # Team name
    "conference": str,              # Conference name
    "fpi": float,                   # FPI rating
    "resumeRanks": {
        "strengthOfRecord": int,    # Strength of record rank
        "fpi": int,                 # FPI rank
        "averageWinProbability": int,
        "strengthOfSchedule": int,  # SOS rank
        "remainingStrengthOfSchedule": int,
        "gameControl": int
    },
    "efficiencies": {
        "overall": float,           # Overall efficiency
        "offense": float,           # Offensive efficiency
        "defense": float,           # Defensive efficiency
        "specialTeams": float       # Special teams efficiency
    },
    "strengthOfSchedule": float,    # Explicit SOS rating
    "sos": float                    # Alternative SOS field
}
```

## Betting Lines (`get_betting_lines`)

```python
{
    "id": int,                      # Game ID
    "season": int,                  # Season year
    "week": int,                    # Week number
    "seasonType": str,              # "postseason" for bowls
    "startDate": str,               # ISO 8601 datetime
    "homeTeam": str,                # Home team name
    "homeConference": str,          # Home conference
    "homeScore": int,               # Home team score (if completed)
    "awayTeam": str,                # Away team name
    "awayConference": str,          # Away conference
    "awayScore": int,               # Away team score (if completed)
    "lines": [                      # Array of betting lines
        {
            "provider": str,        # Sportsbook name (e.g., "consensus", "DraftKings")
            "spread": float,        # Point spread (negative = favorite)
            "formattedSpread": str, # Human-readable spread
            "spreadOpen": float,    # Opening spread
            "overUnder": float,     # Total points over/under
            "overUnderOpen": float, # Opening over/under
            "homeMoneyline": int,   # Home team moneyline
            "awayMoneyline": int    # Away team moneyline
        }
    ]
}
```

## Complete Data (`get_bowl_game_complete_data`)

```python
{
    "bowl_games": [
        # Array of bowl game objects (see Bowl Games schema)
    ],
    "team_stats": [
        # Array of team stat objects (see Team Season Stats schema)
    ],
    "sp_plus": [
        # Array of SP+ rating objects (see SP+ Ratings schema)
    ],
    "fpi": [
        # Array of FPI rating objects (see FPI Ratings schema)
    ],
    "betting_lines": [
        # Array of betting line objects (see Betting Lines schema)
    ]
}
```

## Key Metrics Explained

### Predicted Points Added (PPA)
Expected points added by a play compared to average. Higher is better.

### Success Rate
Percentage of plays that are "successful" (move chains on schedule). 0-1 scale.

### Explosiveness
Average EPA on successful plays. Measures big-play ability.

### Strength of Schedule (SOS)
- **In SP+**: Implicitly factored into the rating through opponent adjustments
- **In FPI**: Explicit metric showing difficulty of schedule
- **Higher values**: More difficult schedule

### Point Spread
- **Negative number**: Team is favored (e.g., -7 means favored by 7 points)
- **Positive number**: Team is underdog (e.g., +7 means underdog by 7 points)
- **Closing line**: Final spread before game starts (most accurate prediction)

## Common Queries

### Find a specific bowl game
```python
games = get_bowl_games(2023)
rose_bowl = [g for g in games if 'Rose' in g.get('venue', '')][0]
```

### Get team's strength of schedule
```python
fpi = get_fpi_ratings(2023, team="Alabama")
sos = fpi[0]['strengthOfSchedule']
```

### Get closing spread for a game
```python
lines = get_betting_lines(2023, home="Alabama", away="Georgia")
for game in lines:
    for line in game['lines']:
        if line['provider'] == 'consensus':
            closing_spread = line['spread']
```

### Compare two teams
```python
team1_sp = get_sp_plus_ratings(2023, team="Alabama")[0]
team2_sp = get_sp_plus_ratings(2023, team="Georgia")[0]
rating_diff = team1_sp['rating'] - team2_sp['rating']
```

## Notes

- Not all fields are available for all games/teams/years
- Always check for None/null values before using data
- Historical data is more complete than current/future data
- Betting lines may not be available for all games
- Some metrics only available for FBS teams
