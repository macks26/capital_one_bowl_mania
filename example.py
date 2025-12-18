"""
Example script demonstrating basic usage of the Bowl Mania prediction system.

This script shows how to:
1. Fetch data from the CFBD API
2. Prepare data for modeling
3. Train a simple linear regression model
4. Make cover probability predictions
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from bowl_mania.data import CFBDClient
from bowl_mania.models import LinearRegression


def main():
    """Run a simple example prediction workflow."""
    
    print("=" * 60)
    print("Bowl Mania - Cover Probability Prediction Example")
    print("=" * 60)
    
    # Step 1: Initialize the CFBD client
    print("\n1. Initializing CFBD API client...")
    client = CFBDClient()
    
    # Step 2: Fetch bowl game data
    print("\n2. Fetching bowl game data...")
    print("   (This may take a few moments...)")
    
    years = [2022, 2023]  # Recent years
    try:
        data = client.fetch_bowl_game_data(years, save_cache=True)
        print(f"   Successfully fetched data for {years}")
        print(f"   - Games: {len(data['games'])} records")
        print(f"   - Team Stats: {len(data['team_stats'])} records")
    except Exception as e:
        print(f"   Error fetching data: {e}")
        print("   Note: You may need to set up your CFBD API key")
        print("   See README.md for instructions")
        return
    
    # Step 3: Display sample data
    print("\n3. Sample game data:")
    games = data['games']
    if not games.empty and len(games) > 0:
        sample = games.head(3)
        print(f"   Showing first 3 games:")
        for idx, row in sample.iterrows():
            print(f"   - Game {idx}: {row.get('home_team', 'N/A')} vs {row.get('away_team', 'N/A')}")
    else:
        print("   No game data available")
    
    # Step 4: Information about next steps
    print("\n4. Next Steps:")
    print("   For detailed analysis and modeling:")
    print("   - Run: jupyter notebook notebooks/01_data_exploration.ipynb")
    print("   - Then: jupyter notebook notebooks/02_modeling.ipynb")
    
    print("\n" + "=" * 60)
    print("Example completed successfully!")
    print("=" * 60)


if __name__ == "__main__":
    main()
