"""Modeling modules for regression analysis"""

from .linear_regression import LinearRegression

try:
    from .bayesian_regression import BayesianRegression
    __all__ = ['LinearRegression', 'BayesianRegression']
except ImportError:
    # PyMC not installed, Bayesian regression not available
    __all__ = ['LinearRegression']
