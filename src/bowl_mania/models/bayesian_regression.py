"""Hierarchical Bayesian Regression Model for Bowl Game Predictions

This module provides hierarchical Bayesian regression models using PyMC
for predicting bowl game cover probabilities with uncertainty quantification.
"""

import numpy as np
import pandas as pd
import pymc as pm
import arviz as az
from typing import Optional, Dict, Any, Tuple


class BayesianRegression:
    """Hierarchical Bayesian regression model for bowl game predictions"""
    
    def __init__(self, hierarchical: bool = False):
        """
        Initialize the Bayesian regression model.
        
        Args:
            hierarchical: Whether to use hierarchical structure (e.g., by conference or team)
        """
        self.hierarchical = hierarchical
        self.model = None
        self.trace = None
        self.feature_names = None
        self.group_var = None
        self.is_fitted = False
        
    def build_simple_model(self, X: pd.DataFrame, y: pd.Series) -> pm.Model:
        """
        Build a simple (non-hierarchical) Bayesian linear regression model.
        
        Args:
            X: Feature matrix
            y: Target variable
            
        Returns:
            PyMC model
        """
        n_features = X.shape[1]
        
        with pm.Model() as model:
            # Priors for regression coefficients
            beta = pm.Normal('beta', mu=0, sigma=10, shape=n_features)
            alpha = pm.Normal('alpha', mu=0, sigma=10)
            
            # Prior for model error
            sigma = pm.HalfNormal('sigma', sigma=10)
            
            # Expected value
            mu = alpha + pm.math.dot(X.values, beta)
            
            # Likelihood
            y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y.values)
            
        return model
    
    def build_hierarchical_model(self, X: pd.DataFrame, y: pd.Series,
                                 group: pd.Series) -> pm.Model:
        """
        Build a hierarchical Bayesian regression model.
        
        Args:
            X: Feature matrix
            y: Target variable
            group: Group variable (e.g., conference, team)
            
        Returns:
            PyMC model
        """
        n_features = X.shape[1]
        
        # Encode groups
        group_idx, groups = pd.factorize(group)
        n_groups = len(groups)
        
        with pm.Model() as model:
            # Hyperpriors for group-level effects
            mu_alpha = pm.Normal('mu_alpha', mu=0, sigma=10)
            sigma_alpha = pm.HalfNormal('sigma_alpha', sigma=5)
            
            mu_beta = pm.Normal('mu_beta', mu=0, sigma=10, shape=n_features)
            sigma_beta = pm.HalfNormal('sigma_beta', sigma=5, shape=n_features)
            
            # Group-level priors
            alpha = pm.Normal('alpha', mu=mu_alpha, sigma=sigma_alpha, shape=n_groups)
            beta = pm.Normal('beta', mu=mu_beta, sigma=sigma_beta, shape=(n_groups, n_features))
            
            # Model error
            sigma = pm.HalfNormal('sigma', sigma=10)
            
            # Expected value (with group-specific intercepts and slopes)
            mu = alpha[group_idx] + pm.math.sum(X.values * beta[group_idx], axis=1)
            
            # Likelihood
            y_obs = pm.Normal('y_obs', mu=mu, sigma=sigma, observed=y.values)
            
        return model
    
    def fit(self, X: pd.DataFrame, y: pd.Series, 
            group: Optional[pd.Series] = None,
            draws: int = 2000, tune: int = 1000, 
            chains: int = 4, **kwargs) -> 'BayesianRegression':
        """
        Fit the Bayesian regression model using MCMC sampling.
        
        Args:
            X: Feature matrix
            y: Target variable
            group: Optional group variable for hierarchical model
            draws: Number of samples to draw
            tune: Number of tuning samples
            chains: Number of MCMC chains
            **kwargs: Additional arguments passed to pm.sample()
            
        Returns:
            Self
        """
        self.feature_names = list(X.columns)
        
        if self.hierarchical and group is not None:
            self.group_var = group
            self.model = self.build_hierarchical_model(X, y, group)
        else:
            self.model = self.build_simple_model(X, y)
        
        with self.model:
            self.trace = pm.sample(draws=draws, tune=tune, chains=chains, 
                                  return_inferencedata=True, **kwargs)
        
        self.is_fitted = True
        return self
    
    def predict(self, X: pd.DataFrame, group: Optional[pd.Series] = None,
                return_samples: bool = False) -> np.ndarray:
        """
        Predict point spreads with the fitted model.
        
        Args:
            X: Feature matrix
            group: Group variable (required if hierarchical model)
            return_samples: If True, returns full posterior samples
            
        Returns:
            Predictions (mean or samples)
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        with self.model:
            if self.hierarchical and group is not None:
                group_idx, _ = pd.factorize(group)
                # Use posterior predictive for hierarchical models
                # This is a simplified version - in practice, you'd want to handle
                # new groups carefully
                pass
            
            # Posterior predictive sampling
            posterior_predictive = pm.sample_posterior_predictive(
                self.trace, 
                var_names=['y_obs']
            )
            
        predictions = posterior_predictive['y_obs'].values
        
        if return_samples:
            return predictions
        else:
            return predictions.mean(axis=(0, 1))
    
    def predict_cover_probability(self, X: pd.DataFrame, actual_spread: float,
                                  group: Optional[pd.Series] = None) -> np.ndarray:
        """
        Predict probability of covering the spread using posterior distribution.
        
        Args:
            X: Feature matrix
            actual_spread: The actual betting line spread
            group: Group variable (required if hierarchical model)
            
        Returns:
            Array of cover probabilities
        """
        # Get full posterior samples
        samples = self.predict(X, group, return_samples=True)
        
        # For each prediction, calculate proportion of samples > actual_spread
        cover_prob = (samples > actual_spread).mean(axis=(0, 1))
        
        return cover_prob
    
    def get_summary(self) -> pd.DataFrame:
        """
        Get summary statistics of the posterior distribution.
        
        Returns:
            DataFrame with posterior summary
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        summary = az.summary(self.trace)
        return summary
    
    def plot_trace(self, var_names: Optional[list] = None):
        """
        Plot trace plots for model parameters.
        
        Args:
            var_names: List of variable names to plot. If None, plots all.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        az.plot_trace(self.trace, var_names=var_names)
    
    def plot_posterior(self, var_names: Optional[list] = None):
        """
        Plot posterior distributions.
        
        Args:
            var_names: List of variable names to plot. If None, plots all.
        """
        if not self.is_fitted:
            raise ValueError("Model must be fitted first")
            
        az.plot_posterior(self.trace, var_names=var_names)
    
    def evaluate(self, X: pd.DataFrame, y: pd.Series,
                group: Optional[pd.Series] = None) -> Dict[str, float]:
        """
        Evaluate model performance.
        
        Args:
            X: Feature matrix
            y: True target values
            group: Group variable (required if hierarchical model)
            
        Returns:
            Dictionary with evaluation metrics
        """
        predictions = self.predict(X, group)
        residuals = y.values - predictions
        
        mse = np.mean(residuals ** 2)
        rmse = np.sqrt(mse)
        mae = np.mean(np.abs(residuals))
        
        return {
            'mse': mse,
            'rmse': rmse,
            'mae': mae,
            'residual_std': np.std(residuals)
        }
