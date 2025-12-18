"""
Basic tests for the Bowl Mania package.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

import pytest
import pandas as pd
import numpy as np
from bowl_mania.data import CFBDClient
from bowl_mania.models import LinearRegression
from bowl_mania.utils import calculate_metrics, evaluate_predictions

# Try to import BayesianRegression (optional dependency)
try:
    from bowl_mania.models import BayesianRegression
    BAYESIAN_AVAILABLE = True
except ImportError:
    BAYESIAN_AVAILABLE = False


class TestCFBDClient:
    """Tests for CFBD API client."""
    
    def test_client_initialization(self):
        """Test that client can be initialized."""
        client = CFBDClient()
        assert client is not None
        assert client.BASE_URL == "https://api.collegefootballdata.com"
    
    def test_cache_directory_creation(self):
        """Test that cache directory is created."""
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            client = CFBDClient(cache_dir=tmpdir)
            assert Path(tmpdir).exists()


class TestLinearRegression:
    """Tests for Linear Regression model."""
    
    def test_model_initialization(self):
        """Test that model can be initialized."""
        model = LinearRegression(normalize=True)
        assert model is not None
        assert model.normalize is True
        assert model.is_fitted is False
    
    def test_model_fitting(self):
        """Test that model can be fitted with sample data."""
        # Create sample data
        X = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        y = pd.Series(np.random.randn(100))
        
        model = LinearRegression(normalize=True)
        model.fit(X, y)
        
        assert model.is_fitted is True
        assert model.feature_names == ['feature1', 'feature2']
    
    def test_model_prediction(self):
        """Test that model can make predictions."""
        # Create sample data
        X_train = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        y_train = pd.Series(np.random.randn(100))
        
        X_test = pd.DataFrame({
            'feature1': np.random.randn(20),
            'feature2': np.random.randn(20)
        })
        
        model = LinearRegression(normalize=True)
        model.fit(X_train, y_train)
        predictions = model.predict(X_test)
        
        assert len(predictions) == 20
        assert isinstance(predictions, np.ndarray)
    
    def test_cover_probability_prediction(self):
        """Test cover probability calculation."""
        X_train = pd.DataFrame({
            'feature1': np.random.randn(100),
            'feature2': np.random.randn(100)
        })
        y_train = pd.Series(np.random.randn(100))
        
        X_test = pd.DataFrame({
            'feature1': np.random.randn(20),
            'feature2': np.random.randn(20)
        })
        
        model = LinearRegression(normalize=True)
        model.fit(X_train, y_train)
        
        cover_probs = model.predict_cover_probability(X_test, actual_spread=-7.0)
        
        assert len(cover_probs) == 20
        assert all(0 <= p <= 1 for p in cover_probs)


@pytest.mark.skipif(not BAYESIAN_AVAILABLE, reason="PyMC not installed")
class TestBayesianRegression:
    """Tests for Bayesian Regression model."""
    
    def test_model_initialization(self):
        """Test that model can be initialized."""
        model = BayesianRegression(hierarchical=False)
        assert model is not None
        assert model.hierarchical is False
        assert model.is_fitted is False
    
    def test_simple_model_building(self):
        """Test that simple model can be built."""
        X = pd.DataFrame({
            'feature1': np.random.randn(50),
            'feature2': np.random.randn(50)
        })
        y = pd.Series(np.random.randn(50))
        
        model = BayesianRegression(hierarchical=False)
        pm_model = model.build_simple_model(X, y)
        
        assert pm_model is not None


class TestMetrics:
    """Tests for utility metrics."""
    
    def test_calculate_metrics(self):
        """Test metric calculation."""
        y_true = np.array([1, 2, 3, 4, 5])
        y_pred = np.array([1.1, 2.1, 2.9, 4.2, 4.8])
        
        metrics = calculate_metrics(y_true, y_pred)
        
        assert 'mse' in metrics
        assert 'rmse' in metrics
        assert 'mae' in metrics
        assert 'r2' in metrics
        assert all(isinstance(v, (int, float)) for v in metrics.values())
    
    def test_evaluate_predictions(self):
        """Test prediction evaluation DataFrame creation."""
        y_true = np.array([10, 15, 20])
        y_pred = np.array([11, 14, 21])
        
        eval_df = evaluate_predictions(y_true, y_pred)
        
        assert isinstance(eval_df, pd.DataFrame)
        assert len(eval_df) == 3
        assert 'actual' in eval_df.columns
        assert 'predicted' in eval_df.columns
        assert 'residual' in eval_df.columns


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
