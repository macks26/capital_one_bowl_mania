"""
CollegeFootballData (CFBD) API Client

This module provides functions to fetch college football data from the CFBD API,
including bowl games, team season statistics, and betting lines.
"""

import os
import requests
from typing import Dict, List, Optional, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
BASE_URL = "https://api.collegefootballdata.com"
API_KEY = os.getenv("CFBD_API_KEY", "")


def _get_headers() -> Dict[str, str]:
    """
    Get headers for API requests.
    
    Returns:
        Dictionary containing request headers
    """
    headers = {
        "accept": "application/json"
    }
    if API_KEY:
        headers["Authorization"] = f"Bearer {API_KEY}"
    return headers


def _make_request(endpoint: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """
    Make a GET request to the CFBD API.
    
    Args:
        endpoint: API endpoint path
        params: Query parameters
        
    Returns:
        JSON response data
        
    Raises:
        requests.exceptions.RequestException: If the request fails
    """
    url = f"{BASE_URL}{endpoint}"
    headers = _get_headers()
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()


def get_bowl_games(year: int, season_type: str = "postseason") -> List[Dict[str, Any]]:
    """
    Get bowl games for a specific year.
    
    Args:
        year: The year to fetch bowl games for
        season_type: Type of season (default: "postseason")
        
    Returns:
        List of bowl game dictionaries containing game information
        
    Example:
        >>> games = get_bowl_games(2023)
        >>> for game in games:
        ...     print(f"{game['home_team']} vs {game['away_team']}")
    """
    endpoint = "/games"
    params = {
        "year": year,
        "seasonType": season_type
    }
    
    return _make_request(endpoint, params)


def get_team_season_stats(
    year: int,
    team: Optional[str] = None,
    conference: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get advanced team season statistics including strength of schedule metrics.
    
    Args:
        year: The year to fetch stats for
        team: Optional specific team name
        conference: Optional conference name
        
    Returns:
        List of team statistics including SOS (strength of schedule) and other advanced metrics
        
    Example:
        >>> stats = get_team_season_stats(2023, team="Alabama")
        >>> print(stats[0]['sos'])
    """
    endpoint = "/stats/season/advanced"
    params = {
        "year": year
    }
    
    if team:
        params["team"] = team
    if conference:
        params["conference"] = conference
    
    return _make_request(endpoint, params)


def get_sp_plus_ratings(year: int, team: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get SP+ ratings which include strength of schedule adjustments.
    
    SP+ is a tempo- and opponent-adjusted measure of college football efficiency.
    
    Args:
        year: The year to fetch ratings for
        team: Optional specific team name
        
    Returns:
        List of SP+ ratings including SOS metrics
        
    Example:
        >>> ratings = get_sp_plus_ratings(2023, team="Georgia")
        >>> print(ratings[0]['rating'])
    """
    endpoint = "/ratings/sp"
    params = {
        "year": year
    }
    
    if team:
        params["team"] = team
    
    return _make_request(endpoint, params)


def get_betting_lines(
    year: int,
    week: Optional[int] = None,
    season_type: str = "postseason",
    team: Optional[str] = None,
    home: Optional[str] = None,
    away: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Get betting lines for games, including closing spreads.
    
    Args:
        year: The year to fetch betting lines for
        week: Optional week number
        season_type: Type of season (default: "postseason" for bowl games)
        team: Optional specific team name
        home: Optional home team name
        away: Optional away team name
        
    Returns:
        List of games with betting line information including spreads
        
    Example:
        >>> lines = get_betting_lines(2023, season_type="postseason")
        >>> for line in lines:
        ...     if line.get('lines'):
        ...         for betting_line in line['lines']:
        ...             print(f"Spread: {betting_line.get('spread')}")
    """
    endpoint = "/lines"
    params = {
        "year": year,
        "seasonType": season_type
    }
    
    if week:
        params["week"] = week
    if team:
        params["team"] = team
    if home:
        params["home"] = home
    if away:
        params["away"] = away
    
    return _make_request(endpoint, params)


def get_fpi_ratings(year: int, team: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get FPI (Football Power Index) ratings which include strength of schedule.
    
    Args:
        year: The year to fetch ratings for
        team: Optional specific team name
        
    Returns:
        List of FPI ratings including SOS metrics
        
    Example:
        >>> ratings = get_fpi_ratings(2023)
        >>> for rating in ratings:
        ...     print(f"{rating['team']}: {rating['fpi']}")
    """
    endpoint = "/ratings/fpi"
    params = {
        "year": year
    }
    
    if team:
        params["team"] = team
    
    return _make_request(endpoint, params)


def get_bowl_game_complete_data(year: int) -> Dict[str, Any]:
    """
    Get comprehensive bowl game data including games, team stats, and betting lines.
    
    This is a convenience function that combines multiple API calls to provide
    all relevant data for bowl games in a single response.
    
    Args:
        year: The year to fetch bowl game data for
        
    Returns:
        Dictionary containing:
            - bowl_games: List of bowl games
            - team_stats: Advanced team statistics
            - sp_plus: SP+ ratings
            - fpi: FPI ratings
            - betting_lines: Betting lines including spreads
            
    Example:
        >>> data = get_bowl_game_complete_data(2023)
        >>> print(f"Found {len(data['bowl_games'])} bowl games")
    """
    result = {
        "bowl_games": get_bowl_games(year),
        "team_stats": get_team_season_stats(year),
        "sp_plus": get_sp_plus_ratings(year),
        "fpi": get_fpi_ratings(year),
        "betting_lines": get_betting_lines(year)
    }
    
    return result
