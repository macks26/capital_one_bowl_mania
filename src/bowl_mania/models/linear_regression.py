"""Simple Linear Regression Model for Bowl Game Predictions

This module provides a wrapper around scikit-learn's linear regression
for predicting bowl game cover probabilities.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression as SKLinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, train_test_split
from scipy.stats import norm
from typing import Optional, Tuple, Dict, Any


class LinearRegression:
    """Linear regression model for predicting point spreads and cover probabilities"""
    
    def __init__(self, normalize: bool = True):
        """
        Initialize the linear regression model.
        
        Args:
            normalize: Whether to standardize features before fitting
        """
        self.model = SKLinearRegression()
        self.scaler = StandardScaler() if normalize else None
        self.normalize = normalize
        self.feature_names = None
        self.is_fitted = False
        
    def fit(self, X: pd.DataFrame, y: pd.Series) -> 'LinearRegression':
        """
        Fit the linear regression model.
        
        Args:
            X: Feature matrix
            y: Target variable (e.g., point spread)
            
        Returns:
            Self
        """
        self.feature_names = list(X.columns)
        
        if self.normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X.values
            
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        return self
    
    def predict(self, X: pd.DataFrame) -> np.ndarray:
        """
        Predict point spreads.
        
        Args:
            X: Feature matrix
            
        Returns:
            Array of predictions
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
            
        if self.normalize:
            X_scaled = self.scaler.transform(X)
        else:
            X_scaled = X.values
            
        return self.model.predict(X_scaled)
    
    def predict_cover_probability(self, X: pd.DataFrame, actual_spread: float,
                                  spread_std: Optional[float] = None) -> np.ndarray:
        """
        Predict the probability of covering the spread.
        
        Args:
            X: Feature matrix
            actual_spread: The actual betting line spread
            spread_std: Standard deviation of prediction error. If None, uses
                       residual standard error from training.
                       
        Returns:
            Array of cover probabilities
        """
        predicted_spread = self.predict(X)
        
        if spread_std is None:
            # Use a default value or estimate from training residuals
            spread_std = 10.0  # typical point spread standard deviation
        
        # Calculate probability that predicted spread beats actual spread
        z_score = (predicted_spread - actual_spread) / spread_std
        cover_prob = norm.cdf(z_score)
        
        return cover_prob
    
    def cross_validate(self, X: pd.DataFrame, y: pd.Series, 
                      cv: int = 5) -> Dict[str, float]:
        """
        Perform cross-validation on the model.
        
        Args:
            X: Feature matrix
            y: Target variable
            cv: Number of cross-validation folds
            
        Returns:
            Dictionary with cross-validation metrics
        """
        if self.normalize:
            X_scaled = self.scaler.fit_transform(X)
        else:
            X_scaled = X.values
            
        scores = cross_val_score(self.model, X_scaled, y, cv=cv, 
                                scoring='neg_mean_squared_error')
        
        return {
            'mean_mse': -scores.mean(),
            'std_mse': scores.std(),
            'rmse': np.sqrt(-scores.mean())
        }
    
    def get_feature_importance(self) -> pd.DataFrame:
        """
        Get feature coefficients as a measure of importance.
        
        Returns:
            DataFrame with feature names and their coefficients
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        importance_df = pd.DataFrame({
            'feature': self.feature_names,
            'coefficient': self.model.coef_,
            'abs_coefficient': np.abs(self.model.coef_)
        })
        
        return importance_df.sort_values('abs_coefficient', ascending=False)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """
        Evaluate model performance on test data.
        
        Args:
            X: Feature matrix
            y: True target values
            
        Returns:
            Dictionary with evaluation metrics
        """
        predictions = self.predict(X)
        residuals = y - predictions
        
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(residuals))
        r2 = self.model.score(
            self.scaler.transform(X) if self.normalize else X.values, 
            y
        )
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'r2': r2,
            'residual_std': np.std(residuals)
        }
