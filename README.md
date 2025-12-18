# Capital One Bowl Mania: NCAA Bowl Game Cover Probability Prediction

A data science project for predicting cover probabilities for NCAA bowl games using data from the CollegeFootballData (CFBD) API. This project implements both simple linear regression and hierarchical Bayesian regression models to analyze and predict bowl game outcomes.

## Project Overview

This project aims to:
- Fetch comprehensive NCAA football data from the CollegeFootballData API
- Conduct exploratory data analysis to understand feature distributions and relationships
- Engineer predictive features from team statistics and game data
- Build and compare multiple regression models (linear and Bayesian)
- Predict the probability that a team will cover the betting spread
- Provide a framework for making data-driven predictions in family bowl game pools

## Features

- **Data Collection**: Automated fetching of bowl game data, team statistics, advanced metrics (S&P+ ratings), and betting lines from CFBD API
- **Data Caching**: Local caching of API responses to minimize API calls
- **Exploratory Data Analysis**: Comprehensive Jupyter notebooks for understanding the data
- **Multiple Modeling Approaches**:
  - Simple Linear Regression with feature importance analysis
  - Hierarchical Bayesian Regression for uncertainty quantification
- **Cover Probability Estimation**: Predict the probability of covering the spread for any game
- **Model Evaluation**: Comprehensive metrics for assessing prediction accuracy

## Project Structure

```
capital_one_bowl_mania/
├── src/
│   └── bowl_mania/
│       ├── data/
│       │   ├── __init__.py
│       │   └── cfbd_client.py          # CFBD API client
│       ├── models/
│       │   ├── __init__.py
│       │   ├── linear_regression.py    # Linear regression model
│       │   └── bayesian_regression.py  # Bayesian regression model
│       └── utils/
│           ├── __init__.py
│           └── metrics.py              # Evaluation metrics
├── notebooks/
│   ├── 01_data_exploration.ipynb       # Exploratory data analysis
│   └── 02_modeling.ipynb               # Model building and comparison
├── data/
│   ├── raw/                            # Cached API responses
│   └── processed/                      # Processed datasets
├── tests/                              # Unit tests
├── requirements.txt                    # Python dependencies
└── README.md                           # This file
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/macks26/capital_one_bowl_mania.git
cd capital_one_bowl_mania
```

2. Create a virtual environment (recommended):
```bash
conda create -n bowl_mania python=3.9
conda activate bowl_mania
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up your CFBD API key (optional but recommended):
   - Get a free API key from [CollegeFootballData.com](https://collegefootballdata.com/)
   - Set the environment variable:
     ```bash
     export CFBD_API_KEY="your_api_key_here"
     ```
   - Or create a `.env` file:
     ```
     CFBD_API_KEY=your_api_key_here
     ```

## Quick Start

### 1. Fetch Bowl Game Data

```python
from src.bowl_mania.data import CFBDClient

# Initialize the client
client = CFBDClient()

# Fetch data for multiple years
years = [2019, 2020, 2021, 2022, 2023]
data = client.fetch_bowl_game_data(years, save_cache=True)

# Access different datasets
games = data['games']
team_stats = data['team_stats']
betting_lines = data['betting_lines']
```

### 2. Explore the Data

Open and run the exploratory data analysis notebook:
```bash
jupyter notebook notebooks/01_data_exploration.ipynb
```

This notebook will help you:
- Understand the data structure
- Visualize score distributions
- Analyze team statistics
- Identify missing values and data quality issues

### 3. Build Prediction Models

Open and run the modeling notebook:
```bash
jupyter notebook notebooks/02_modeling.ipynb
```

This notebook demonstrates:
- Feature engineering
- Training linear regression models
- Training Bayesian regression models
- Model evaluation and comparison
- Predicting cover probabilities

### 4. Use Models Programmatically

```python
from src.bowl_mania.models import LinearRegression, BayesianRegression
import pandas as pd

# Prepare your data (X = features, y = target)
X_train = pd.DataFrame(...)  # Your training features
y_train = pd.Series(...)     # Your training target

# Train a linear regression model
lr_model = LinearRegression(normalize=True)
lr_model.fit(X_train, y_train)

# Predict cover probability
actual_spread = -7.0  # Example: 7-point favorite
cover_prob = lr_model.predict_cover_probability(X_test, actual_spread)

print(f"Probability of covering {actual_spread}: {cover_prob[0]:.2%}")
```

## Data Sources

This project uses data from the [CollegeFootballData API](https://collegefootballdata.com/), which provides:
- Game results and scores
- Team statistics (offensive, defensive)
- Advanced metrics (S&P+ ratings, FPI, etc.)
- Betting lines and spreads
- Team records and rankings

## Models

### Linear Regression
- Standard linear regression with optional feature normalization
- Feature importance analysis
- Cross-validation support
- Cover probability estimation using normal distribution

### Hierarchical Bayesian Regression
- PyMC-based Bayesian modeling
- Optional hierarchical structure (e.g., by conference)
- Full posterior distributions for uncertainty quantification
- MCMC sampling with convergence diagnostics
- Credible intervals for predictions

## Modeling Assumptions

The models make several key assumptions:
1. **Linear Relationships**: Features have approximately linear relationships with point differentials
2. **Normally Distributed Errors**: Prediction errors follow a normal distribution
3. **Independence**: Games are treated as independent observations (though hierarchical models can account for some dependencies)
4. **Feature Relevance**: Selected features are meaningful predictors of game outcomes

These assumptions are examined in the exploratory data analysis notebooks.

## Evaluation Metrics

Models are evaluated using:
- **RMSE** (Root Mean Squared Error): Average prediction error in points
- **MAE** (Mean Absolute Error): Average absolute prediction error
- **R²**: Proportion of variance explained by the model
- **Cover Accuracy**: Percentage of correct cover predictions
- **Residual Analysis**: Distribution and patterns in prediction errors

## Future Enhancements

Potential improvements to the project:
- [ ] Incorporate player-level data (injuries, transfers)
- [ ] Add weather and venue data
- [ ] Implement ensemble models
- [ ] Develop a betting strategy optimizer
- [ ] Create a web interface for predictions
- [ ] Add real-time prediction updates
- [ ] Include more advanced Bayesian model structures

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and personal use.

## Disclaimer

This project is for educational and entertainment purposes only. Sports betting involves risk, and past performance does not guarantee future results. Always gamble responsibly.

## Acknowledgments

- [CollegeFootballData.com](https://collegefootballdata.com/) for providing the API
- The PyMC team for the excellent Bayesian modeling framework
- The college football analytics community for inspiration

## Contact

For questions or feedback, please open an issue on GitHub.
