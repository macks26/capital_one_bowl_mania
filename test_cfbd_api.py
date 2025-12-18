"""
Unit tests for the CFBD API client.

Note: These tests include both mock tests (that don't require internet)
and integration tests (that require internet access to the CFBD API).
"""

import unittest
from unittest.mock import patch, MagicMock
from cfbd_api import (
    _get_headers,
    _make_request,
    get_bowl_games,
    get_team_season_stats,
    get_sp_plus_ratings,
    get_fpi_ratings,
    get_betting_lines,
    get_bowl_game_complete_data,
    BASE_URL
)


class TestCFBDAPIHeaders(unittest.TestCase):
    """Test header generation."""
    
    def test_get_headers_without_api_key(self):
        """Test headers when no API key is set."""
        with patch('cfbd_api.API_KEY', ''):
            headers = _get_headers()
            self.assertIn('accept', headers)
            self.assertEqual(headers['accept'], 'application/json')
            self.assertNotIn('Authorization', headers)
    
    def test_get_headers_with_api_key(self):
        """Test headers when API key is set."""
        with patch('cfbd_api.API_KEY', 'test_key_123'):
            headers = _get_headers()
            self.assertIn('accept', headers)
            self.assertIn('Authorization', headers)
            self.assertEqual(headers['Authorization'], 'Bearer test_key_123')


class TestCFBDAPIMockRequests(unittest.TestCase):
    """Test API functions using mocked responses."""
    
    @patch('cfbd_api.requests.get')
    def test_make_request_success(self, mock_get):
        """Test successful API request."""
        mock_response = MagicMock()
        mock_response.json.return_value = [{'test': 'data'}]
        mock_response.raise_for_status = MagicMock()
        mock_get.return_value = mock_response
        
        result = _make_request('/test', {'param': 'value'})
        
        self.assertEqual(result, [{'test': 'data'}])
        mock_get.assert_called_once()
        mock_response.raise_for_status.assert_called_once()
    
    @patch('cfbd_api._make_request')
    def test_get_bowl_games(self, mock_request):
        """Test get_bowl_games function."""
        mock_data = [
            {
                'id': 1,
                'home_team': 'Alabama',
                'away_team': 'Georgia',
                'venue': 'Mercedes-Benz Stadium'
            }
        ]
        mock_request.return_value = mock_data
        
        result = get_bowl_games(2023)
        
        self.assertEqual(result, mock_data)
        mock_request.assert_called_once_with(
            '/games',
            {'year': 2023, 'seasonType': 'postseason'}
        )
    
    @patch('cfbd_api._make_request')
    def test_get_team_season_stats(self, mock_request):
        """Test get_team_season_stats function."""
        mock_data = [
            {
                'team': 'Alabama',
                'offense': {'successRate': 0.5},
                'defense': {'successRate': 0.45}
            }
        ]
        mock_request.return_value = mock_data
        
        result = get_team_season_stats(2023, team='Alabama')
        
        self.assertEqual(result, mock_data)
        mock_request.assert_called_once_with(
            '/stats/season/advanced',
            {'year': 2023, 'team': 'Alabama'}
        )
    
    @patch('cfbd_api._make_request')
    def test_get_sp_plus_ratings(self, mock_request):
        """Test get_sp_plus_ratings function."""
        mock_data = [
            {
                'team': 'Georgia',
                'rating': 28.5,
                'offense': 15.2,
                'defense': 12.3
            }
        ]
        mock_request.return_value = mock_data
        
        result = get_sp_plus_ratings(2023, team='Georgia')
        
        self.assertEqual(result, mock_data)
        mock_request.assert_called_once_with(
            '/ratings/sp',
            {'year': 2023, 'team': 'Georgia'}
        )
    
    @patch('cfbd_api._make_request')
    def test_get_fpi_ratings(self, mock_request):
        """Test get_fpi_ratings function."""
        mock_data = [
            {
                'team': 'Ohio State',
                'fpi': 18.7,
                'sos': 2.3
            }
        ]
        mock_request.return_value = mock_data
        
        result = get_fpi_ratings(2023)
        
        self.assertEqual(result, mock_data)
        mock_request.assert_called_once_with(
            '/ratings/fpi',
            {'year': 2023}
        )
    
    @patch('cfbd_api._make_request')
    def test_get_betting_lines(self, mock_request):
        """Test get_betting_lines function."""
        mock_data = [
            {
                'homeTeam': 'Alabama',
                'awayTeam': 'Georgia',
                'lines': [
                    {
                        'provider': 'consensus',
                        'spread': -3.5,
                        'overUnder': 52.5
                    }
                ]
            }
        ]
        mock_request.return_value = mock_data
        
        result = get_betting_lines(2023, season_type='postseason')
        
        self.assertEqual(result, mock_data)
        mock_request.assert_called_once_with(
            '/lines',
            {'year': 2023, 'seasonType': 'postseason'}
        )
    
    @patch('cfbd_api.get_bowl_games')
    @patch('cfbd_api.get_team_season_stats')
    @patch('cfbd_api.get_sp_plus_ratings')
    @patch('cfbd_api.get_fpi_ratings')
    @patch('cfbd_api.get_betting_lines')
    def test_get_bowl_game_complete_data(
        self,
        mock_betting,
        mock_fpi,
        mock_sp,
        mock_stats,
        mock_games
    ):
        """Test get_bowl_game_complete_data function."""
        mock_games.return_value = [{'game': 1}]
        mock_stats.return_value = [{'stats': 1}]
        mock_sp.return_value = [{'sp': 1}]
        mock_fpi.return_value = [{'fpi': 1}]
        mock_betting.return_value = [{'lines': 1}]
        
        result = get_bowl_game_complete_data(2023)
        
        self.assertIn('bowl_games', result)
        self.assertIn('team_stats', result)
        self.assertIn('sp_plus', result)
        self.assertIn('fpi', result)
        self.assertIn('betting_lines', result)
        
        mock_games.assert_called_once_with(2023)
        mock_stats.assert_called_once_with(2023)
        mock_sp.assert_called_once_with(2023)
        mock_fpi.assert_called_once_with(2023)
        mock_betting.assert_called_once_with(2023)


class TestAPIConfiguration(unittest.TestCase):
    """Test API configuration."""
    
    def test_base_url(self):
        """Test that BASE_URL is correctly configured."""
        self.assertEqual(BASE_URL, "https://api.collegefootballdata.com")


if __name__ == '__main__':
    unittest.main()
