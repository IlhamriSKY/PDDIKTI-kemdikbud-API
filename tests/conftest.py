"""
Pytest configuration and fixtures for PDDIKTI API testing

This file provides shared test configuration and fixtures for all PDDIKTI API tests.
Includes API client fixture and common test setup to ensure consistent testing environment.

Fixtures provided:
- api_client: Pre-configured PDDIKTI API client instance
- Common path setup for module imports
"""

import pytest
import sys
import os

# Add parent directory to path for importing the API
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture(scope="session")
def api_client():
    """Provide API client instance for tests"""
    from pddiktipy.api import api
    client = api()
    yield client
    client.close()

@pytest.fixture
def test_timeout():
    """Provide timeout for network tests"""
    return 30  # seconds

@pytest.fixture
def sample_keywords():
    """Provide sample keywords for testing"""
    return {
        'student': 'Ilham',
        'lecturer': 'Ridwan', 
        'university': 'Unika',
        'program': 'Sistem Informasi'
    }