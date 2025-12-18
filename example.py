"""
Example script demonstrating usage of the CFBD API client.

This script shows how to fetch bowl game data, team statistics,
and betting lines from the CollegeFootballData API.
"""

import json
import requests
from cfbd_api import (
    get_bowl_games,
    get_team_season_stats,
    get_sp_plus_ratings,
    get_fpi_ratings,
    get_betting_lines,
    get_bowl_game_complete_data
)


def print_section(title: str):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def main():
    """Main function demonstrating API usage."""
    # Set the year for which to fetch data
    year = 2023
    
    print(f"Fetching College Football Bowl Game Data for {year}")
    
    # Example 1: Get bowl games
    print_section("Bowl Games")
    try:
        bowl_games = get_bowl_games(year)
        print(f"Found {len(bowl_games)} bowl games")
        
        # Display first 3 games as examples
        for i, game in enumerate(bowl_games[:3], 1):
            print(f"\nGame {i}:")
            print(f"  {game.get('away_team', 'TBD')} @ {game.get('home_team', 'TBD')}")
            print(f"  Venue: {game.get('venue', 'N/A')}")
            print(f"  Start Date: {game.get('start_date', 'N/A')}")
            if game.get('home_points') is not None:
                print(f"  Score: {game.get('away_team')} {game.get('away_points')} - "
                      f"{game.get('home_team')} {game.get('home_points')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching bowl games: {e}")
    
    # Example 2: Get team season stats
    print_section("Team Season Statistics (Advanced)")
    try:
        team_stats = get_team_season_stats(year)
        print(f"Found statistics for {len(team_stats)} teams")
        
        # Display first 3 teams as examples
        for i, stats in enumerate(team_stats[:3], 1):
            print(f"\nTeam {i}: {stats.get('team', 'Unknown')}")
            print(f"  Conference: {stats.get('conference', 'N/A')}")
            
            # Display relevant offensive and defensive stats
            offense = stats.get('offense', {})
            defense = stats.get('defense', {})
            
            print(f"  Offense:")
            print(f"    Success Rate: {offense.get('successRate', 'N/A')}")
            print(f"    Explosiveness: {offense.get('explosiveness', 'N/A')}")
            
            print(f"  Defense:")
            print(f"    Success Rate: {defense.get('successRate', 'N/A')}")
            print(f"    Explosiveness: {defense.get('explosiveness', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching team stats: {e}")
    
    # Example 3: Get SP+ ratings (includes SOS)
    print_section("SP+ Ratings (Strength of Schedule Adjusted)")
    try:
        sp_ratings = get_sp_plus_ratings(year)
        print(f"Found SP+ ratings for {len(sp_ratings)} teams")
        
        # Display top 5 teams
        for i, rating in enumerate(sp_ratings[:5], 1):
            print(f"\n{i}. {rating.get('team', 'Unknown')}")
            print(f"   Overall Rating: {rating.get('rating', 'N/A')}")
            print(f"   Offense: {rating.get('offense', 'N/A')}")
            print(f"   Defense: {rating.get('defense', 'N/A')}")
            print(f"   Special Teams: {rating.get('specialTeams', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching SP+ ratings: {e}")
    
    # Example 4: Get FPI ratings
    print_section("FPI Ratings (includes SOS)")
    try:
        fpi_ratings = get_fpi_ratings(year)
        print(f"Found FPI ratings for {len(fpi_ratings)} teams")
        
        # Display top 5 teams
        for i, rating in enumerate(fpi_ratings[:5], 1):
            print(f"\n{i}. {rating.get('team', 'Unknown')}")
            print(f"   FPI: {rating.get('fpi', 'N/A')}")
            print(f"   Strength of Schedule: {rating.get('sos', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching FPI ratings: {e}")
    
    # Example 5: Get betting lines for bowl games
    print_section("Betting Lines (Bowl Games)")
    try:
        betting_lines = get_betting_lines(year, season_type="postseason")
        print(f"Found betting lines for {len(betting_lines)} games")
        
        # Display first 5 games with betting lines
        count = 0
        for game in betting_lines:
            if count >= 5:
                break
            
            lines = game.get('lines', [])
            if lines:
                print(f"\n{game.get('awayTeam', 'TBD')} @ {game.get('homeTeam', 'TBD')}")
                
                # Look for the consensus or closing line
                for line in lines:
                    provider = line.get('provider', 'Unknown')
                    spread = line.get('spread')
                    over_under = line.get('overUnder')
                    
                    if spread is not None or over_under is not None:
                        print(f"  {provider}:")
                        if spread is not None:
                            print(f"    Spread: {spread}")
                        if over_under is not None:
                            print(f"    Over/Under: {over_under}")
                        count += 1
                        break
    except requests.exceptions.RequestException as e:
        print(f"Error fetching betting lines: {e}")
    
    # Example 6: Get complete data in one call
    print_section("Complete Bowl Game Data (All-in-One)")
    try:
        complete_data = get_bowl_game_complete_data(year)
        
        print(f"Summary of Complete Data:")
        print(f"  Bowl Games: {len(complete_data.get('bowl_games', []))}")
        print(f"  Team Stats: {len(complete_data.get('team_stats', []))}")
        print(f"  SP+ Ratings: {len(complete_data.get('sp_plus', []))}")
        print(f"  FPI Ratings: {len(complete_data.get('fpi', []))}")
        print(f"  Betting Lines: {len(complete_data.get('betting_lines', []))}")
        
        # Optionally save to file
        output_file = f"bowl_data_{year}.json"
        with open(output_file, 'w') as f:
            json.dump(complete_data, f, indent=2)
        print(f"\nComplete data saved to: {output_file}")
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching complete data: {e}")
    
    print("\n" + "=" * 80)
    print("Done!")
    print("=" * 80)


if __name__ == "__main__":
    main()
