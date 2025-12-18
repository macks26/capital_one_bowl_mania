"""
CollegeFootballData API Client

This module provides a client for interacting with the CollegeFootballData.com API
to fetch NCAA football data for bowl game predictions.
"""

import os
from typing import Optional, List, Dict, Any
import pandas as pd
from pathlib import Path
import cfbd
from cfbd.rest import ApiException


class CFBDClient:
    """Client for interacting with the CollegeFootballData API via `cfbd` library"""

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

        # Configure cfbd client (Bearer auth)
        self.configuration = cfbd.Configuration(host=self.BASE_URL)
        # cfbd-python expects Bearer token set via access_token
        if self.api_key:
            self.configuration.access_token = self.api_key

        # Persistent API client and specific API interfaces
        self.api_client = cfbd.ApiClient(self.configuration)
        self.games_api = cfbd.GamesApi(self.api_client)
        self.stats_api = cfbd.StatsApi(self.api_client)
        self.ratings_api = cfbd.RatingsApi(self.api_client)
        self.betting_api = cfbd.BettingApi(self.api_client)
        self.adjusted_api = cfbd.AdjustedMetricsApi(self.api_client)

        self.cache_dir = Path(cache_dir) if cache_dir else Path('data/raw')
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _to_dataframe(response: Any) -> pd.DataFrame:
        """
        Convert cfbd API response (list of models) into a pandas DataFrame.

        Tries `.to_dict()` for pydantic models; falls back to `vars()` if needed.
        """
        if response is None:
            return pd.DataFrame()
        try:
            # List of pydantic models
            return pd.DataFrame([item.to_dict() for item in response])
        except Exception:
            try:
                # Already JSON-like
                return pd.DataFrame(response)
            except Exception:
                # Fallback using vars
                return pd.DataFrame([vars(item) for item in response])
    
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
        try:
            resp = self.games_api.get_games(year=year, season_type=season_type, team=team)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_games failed: {e}")
    
    def get_team_stats(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch team statistics for a specific year.
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with team statistics
        """
        try:
            resp = self.stats_api.get_team_stats(year=year, team=team)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_team_stats failed: {e}")
    
    def get_advanced_team_stats(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch advanced team statistics (S&P+ ratings, etc.).
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with advanced team statistics
        """
        try:
            resp = self.stats_api.get_advanced_season_stats(year=year, team=team)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_advanced_team_stats failed: {e}")

    def get_adjusted_team_season_stats(self, year: int, team: Optional[str] = None,
                                       conference: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch opponent-adjusted team season metrics (Weighted EPA, Success Rates, etc.).

        Args:
            year: Season year
            team: Optionally filter by team name
            conference: Optionally filter by conference abbreviation

        Returns:
            DataFrame with adjusted team season metrics
        """
        try:
            resp = self.adjusted_api.get_adjusted_team_season_stats(year=year, team=team, conference=conference)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_adjusted_team_season_stats failed: {e}")
    
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
        try:
            resp = self.betting_api.get_lines(year=year, season_type=season_type, team=team)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_betting_lines failed: {e}")
    
    def get_team_records(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch team records for a specific year.
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with team records
        """
        try:
            resp = self.games_api.get_records(year=year, team=team)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_team_records failed: {e}")
    
    def get_sp_ratings(self, year: int, team: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch SP+ ratings for teams.
        
        Args:
            year: Season year
            team: Optionally filter by team name
            
        Returns:
            DataFrame with SP+ ratings
        """
        try:
            resp = self.ratings_api.get_sp(year=year, team=team)
            return self._to_dataframe(resp)
        except ApiException as e:
            raise RuntimeError(f"CFBD get_sp_ratings failed: {e}")
    
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
            'adjusted_team_metrics': [],
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
            except Exception as e:
                print(f"Advanced stats not available for {year}: {e}")
            
            # Get adjusted team metrics (opponent-adjusted)
            try:
                adjusted_stats = self.get_adjusted_team_season_stats(year)
                all_data['adjusted_team_metrics'].append(adjusted_stats)
            except Exception as e:
                print(f"Adjusted team metrics not available for {year}: {e}")

            # Get betting lines
            try:
                betting_lines = self.get_betting_lines(year, season_type='postseason')
                all_data['betting_lines'].append(betting_lines)
            except Exception as e:
                print(f"Betting lines not available for {year}: {e}")
            
            # Get SP+ ratings
            try:
                sp_ratings = self.get_sp_ratings(year)
                all_data['sp_ratings'].append(sp_ratings)
            except Exception as e:
                print(f"SP+ ratings not available for {year}: {e}")
        
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
