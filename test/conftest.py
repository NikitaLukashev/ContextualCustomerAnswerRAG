"""
Pytest configuration and fixtures for RAG system tests
"""

import os
import pytest
import time
import requests

@pytest.fixture
def base_url():
    """Fixture to provide the base URL for testing"""
    return os.getenv('TEST_BASE_URL', 'http://localhost:8000')

@pytest.fixture
def wait_for_service():
    """Fixture to wait for the service to be ready"""
    base_url = os.getenv('TEST_BASE_URL', 'http://localhost:8000')
    
    # Wait for service to be ready
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = requests.get(f"{base_url}/health", timeout=5)
            if response.status_code == 200:
                break
        except:
            pass
        
        time.sleep(2)
        attempt += 1
    
    if attempt >= max_attempts:
        pytest.fail("Service did not become ready within expected time")
    
    return True
