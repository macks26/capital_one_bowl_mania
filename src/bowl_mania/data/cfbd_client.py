"""CollegeFootballData API Client

This module provides a client for interacting with the CollegeFootballData.com API
to fetch NCAA football data for bowl game predictions.
"""

import os
import json
from typing import Optional, List, Dict, Any
import pandas as pd
import requests
from pathlib import Path


class CFBDClient:
    """Client for interacting with the CollegeFootballData API"""
    
    BASE_URL = "https://api.collegefootballdata.com"
    
    def __init__(self, api_key: Optional[str] = None, cache_dir: Optional[str] = None):
        """
        Initialize the CFBD API client.
        
        Args:
            api_key: API key for CollegeFootballData. If not provided, will look for
                    CFBD_API_KEY environment variable.
            cache_dir: Directory to cache API responses. Defaults to data/raw.
        """
        self.api_key = api_key or os.getenv('CFBD_API_KEY')
        if not self.api_key:
            print("Warning: No API key provided. Some endpoints may be rate-limited.")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}' if self.api_key else '',
            'accept': 'application/json'
        }
        
        self.cache_dir = Path(cache_dir) if cache_dir else Path('data/raw')
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """
        Make a request to the CFBD API.
        
        Args:
            endpoint: API endpoint path
            params: Query parameters
            
        Returns:
            JSON response data
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_games(self, year: int, season_type: str = 'postseason', 
                  team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch game data for a specific year.
        
        Args:
            year: Season year
            season_type: Type of games ('regular', 'postseason', or 'both')
            team: Optionally filter by team name
            
        Returns:
            DataFrame with game information
        """
        params = {
            'year': year,
            'seasonType': season_type
        }
        if team:
            params['team'] = team
            
        data = self._make_request('/games', params)
        return pd.DataFrame(data)
    
    def get_team_stats(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch team statistics for a specific year.
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with team statistics
        """
        params = {'year': year}
        if team:
            params['team'] = team
            
        data = self._make_request('/stats/season', params)
        return pd.DataFrame(data)
    
    def get_advanced_team_stats(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch advanced team statistics (S&P+ ratings, etc.).
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with advanced team statistics
        """
        params = {'year': year}
        if team:
            params['team'] = team
            
        data = self._make_request('/stats/season/advanced', params)
        return pd.DataFrame(data)
    
    def get_betting_lines(self, year: int, season_type: str = 'postseason',
                         team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch betting lines for games.
        
        Args:
            year: Season year
            season_type: Type of games ('regular', 'postseason', or 'both')
            team: Optionally filter by team name
            
        Returns:
            DataFrame with betting line information
        """
        params = {
            'year': year,
            'seasonType': season_type
        }
        if team:
            params['team'] = team
            
        data = self._make_request('/lines', params)
        return pd.DataFrame(data)
    
    def get_team_records(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch team records for a specific year.
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with team records
        """
        params = {'year': year}
        if team:
            params['team'] = team
            
        data = self._make_request('/records', params)
        return pd.DataFrame(data)
    
    def get_sp_ratings(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch SP+ ratings for teams.
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with SP+ ratings
        """
        params = {'year': year}
        if team:
            params['team'] = team
            
        data = self._make_request('/ratings/sp', params)
        return pd.DataFrame(data)
    
    def save_to_cache(self, data: pd.DataFrame, filename: str):
        """
        Save DataFrame to cache directory.
        
        Args:
            data: DataFrame to save
            filename: Name of the file (will be saved as CSV)
        """
        filepath = self.cache_dir / filename
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    
    def load_from_cache(self, filename: str) -> pd.DataFrame:
        """
        Load DataFrame from cache directory.
        
        Args:
            filename: Name of the file to load
            
        Returns:
            DataFrame loaded from cache
        """
        filepath = self.cache_dir / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Cache file not found: {filepath}")
        return pd.read_csv(filepath)
    
    def fetch_bowl_game_data(self, years: List[int], save_cache: bool = True) -> Dict[str, pd.DataFrame]:
        """
        Fetch comprehensive bowl game data for multiple years.
        
        Args:
            years: List of years to fetch data for
            save_cache: Whether to save data to cache
            
        Returns:
            Dictionary containing different types of data
        """
        all_data = {
            'games': [],
            'team_stats': [],
            'advanced_stats': [],
            'betting_lines': [],
            'sp_ratings': []
        }
        
        for year in years:
            print(f"Fetching data for {year}...")
            
            # Get bowl games
            games = self.get_games(year, season_type='postseason')
            all_data['games'].append(games)
            
            # Get team stats
            team_stats = self.get_team_stats(year)
            all_data['team_stats'].append(team_stats)
            
            # Get advanced stats
            try:
                advanced_stats = self.get_advanced_team_stats(year)
                all_data['advanced_stats'].append(advanced_stats)
            except:
                print(f"Advanced stats not available for {year}")
            
            # Get betting lines
            try:
                betting_lines = self.get_betting_lines(year, season_type='postseason')
                all_data['betting_lines'].append(betting_lines)
            except:
                print(f"Betting lines not available for {year}")
            
            # Get SP+ ratings
            try:
                sp_ratings = self.get_sp_ratings(year)
                all_data['sp_ratings'].append(sp_ratings)
            except:
                print(f"SP+ ratings not available for {year}")
        
        # Combine data from all years
        combined_data = {
            key: pd.concat(values, ignore_index=True) if values else pd.DataFrame()
            for key, values in all_data.items()
        }
        
        # Save to cache if requested
        if save_cache:
            for key, df in combined_data.items():
                if not df.empty:
                    self.save_to_cache(df, f"{key}.csv")
        
        return combined_data
