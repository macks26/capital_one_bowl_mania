"""Utility functions for model evaluation and metrics

This module provides functions for calculating various metrics
for evaluating bowl game prediction models.
"""

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from typing import Dict, Any, Optional


def calculate_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate comprehensive regression metrics.
    
    Args:
        y_true: True target values
        y_pred: Predicted values
        
    Returns:
        Dictionary with various metrics
    """
    residuals = y_true - y_pred
    
    metrics = {
        'mse': mean_squared_error(y_true, y_pred),
        'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
        'mae': mean_absolute_error(y_true, y_pred),
        'r2': r2_score(y_true, y_pred),
        'residual_std': np.std(residuals),
        'mean_residual': np.mean(residuals),
        'median_residual': np.median(residuals)
    }
    
    return metrics


def calculate_cover_accuracy(predicted_winners: np.ndarray, 
                             actual_winners: np.ndarray) -> float:
    """
    Calculate accuracy of cover predictions.
    
    Args:
        predicted_winners: Predicted cover winners (1 if favorite covers, 0 if not)
        actual_winners: Actual cover winners
        
    Returns:
        Accuracy percentage
    """
    return np.mean(predicted_winners == actual_winners)


def evaluate_predictions(y_true: np.ndarray, y_pred: np.ndarray,
                        actual_spreads: Optional[np.ndarray] = None) -> pd.DataFrame:
    """
    Create a detailed evaluation DataFrame.
    
    Args:
        y_true: True point differentials
        y_pred: Predicted point differentials
        actual_spreads: Actual betting lines (optional)
        
    Returns:
        DataFrame with evaluation results
    """
    eval_df = pd.DataFrame({
        'actual': y_true,
        'predicted': y_pred,
        'residual': y_true - y_pred,
        'abs_residual': np.abs(y_true - y_pred)
    })
    
    if actual_spreads is not None:
        eval_df['spread'] = actual_spreads
        eval_df['actual_covers'] = (y_true > actual_spreads).astype(int)
        eval_df['predicted_covers'] = (y_pred > actual_spreads).astype(int)
        eval_df['correct_cover'] = (eval_df['actual_covers'] == eval_df['predicted_covers']).astype(int)
    
    return eval_df


def calculate_profit(cover_probabilities: np.ndarray, 
                     actual_covers: np.ndarray,
                     bet_threshold: float = 0.55,
                     bet_size: float = 100.0) -> Dict[str, float]:
    """
    Calculate profit/loss from betting strategy.
    
    Args:
        cover_probabilities: Predicted probabilities of covering
        actual_covers: Actual cover results (1 if covered, 0 if not)
        bet_threshold: Minimum probability to place a bet
        bet_size: Size of each bet
        
    Returns:
        Dictionary with profit metrics
    """
    # Only bet when probability exceeds threshold
    bets_placed = cover_probabilities >= bet_threshold
    n_bets = bets_placed.sum()
    
    if n_bets == 0:
        return {
            'total_profit': 0,
            'roi': 0,
            'win_rate': 0,
            'n_bets': 0
        }
    
    # Calculate wins/losses (assuming -110 odds)
    wins = (bets_placed & (actual_covers == 1)).sum()
    losses = n_bets - wins
    
    # Profit calculation (win $100 on win, lose $110 on loss)
    total_profit = (wins * bet_size) - (losses * bet_size * 1.1)
    total_wagered = n_bets * bet_size
    roi = (total_profit / total_wagered * 100) if total_wagered > 0 else 0
    
    return {
        'total_profit': total_profit,
        'roi': roi,
        'win_rate': wins / n_bets if n_bets > 0 else 0,
        'n_bets': n_bets,
        'wins': wins,
        'losses': losses
    }


def residual_analysis(residuals: np.ndarray) -> Dict[str, Any]:
    """
    Perform residual analysis.
    
    Args:
        residuals: Model residuals
        
    Returns:
        Dictionary with residual analysis results
    """
    from scipy import stats
    
    # Normality test
    _, normality_p = stats.normaltest(residuals)
    
    # Calculate percentiles
    percentiles = np.percentile(residuals, [25, 50, 75])
    
    analysis = {
        'mean': np.mean(residuals),
        'std': np.std(residuals),
        'min': np.min(residuals),
        'max': np.max(residuals),
        'q25': percentiles[0],
        'median': percentiles[1],
        'q75': percentiles[2],
        'skewness': stats.skew(residuals),
        'kurtosis': stats.kurtosis(residuals),
        'normality_p_value': normality_p,
        'is_normal': normality_p > 0.05
    }
    
    return analysis
