"""Bowl Mania package for NCAA bowl game predictions"""

from .data import CFBDClient
from .models import LinearRegression

try:
    from .models import BayesianRegression
    __all__ = ['CFBDClient', 'LinearRegression', 'BayesianRegression']
except ImportError:
    # BayesianRegression not available (PyMC not installed)
    __all__ = ['CFBDClient', 'LinearRegression']
