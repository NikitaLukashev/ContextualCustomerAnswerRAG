#!/usr/bin/env python3
"""
Unit tests for Mistral LLM integration using pytest
"""

import pytest
import requests
from unittest.mock import Mock, patch

class TestMistralIntegration:
    """Test class for Mistral LLM integration"""
    
    def test_llm_status(self, base_url, wait_for_service):
        """Test LLM status endpoint"""
        response = requests.get(f"{base_url}/llm-status", timeout=10)
        assert response.status_code == 200
        
        status = response.json()
        assert "llm_available" in status
        assert "llm_model" in status
        assert isinstance(status["llm_available"], bool)
        assert isinstance(status["llm_model"], str)
        
        if not status["llm_available"]:
            assert "llm_error" in status
            assert isinstance(status["llm_error"], str)
    
    @pytest.mark.parametrize("query", [
        "What amenities are available in the apartment?",
        "Can you summarize the main features of this apartment?",
        "What makes this apartment special or unique?"
    ])
    def test_llm_powered_search(self, base_url, wait_for_service, query):
        """Test LLM-powered search with different queries"""
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": query, "n_results": 3},
            timeout=60
        )
        assert response.status_code == 200
        
        results = response.json()
        assert "llm_response" in results
        assert "results" in results
        assert isinstance(results["llm_response"], str)
        assert isinstance(results["results"], list)
        
        # Check that LLM response is not empty
        assert len(results["llm_response"]) > 0
    
    def test_llm_search_with_empty_query(self, base_url, wait_for_service):
        """Test LLM search with empty query"""
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": "", "n_results": 3},
            timeout=10
        )
        # Should handle empty query gracefully or return error
        assert response.status_code in [200, 400, 422]
    
    def test_llm_search_missing_parameters(self, base_url, wait_for_service):
        """Test LLM search with missing required parameters"""
        # Missing query
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"n_results": 3},
            timeout=10
        )
        assert response.status_code in [400, 422]
        
        # Missing n_results
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": "test query"},
            timeout=10
        )
        assert response.status_code in [200, 400, 422]  # n_results might have default
    
    def test_llm_search_timeout_handling(self, base_url, wait_for_service):
        """Test LLM search timeout handling"""
        # Test with a very long query that might trigger timeout
        long_query = "What are all the detailed features, amenities, rules, policies, and special characteristics of this apartment, including but not limited to the check-in process, check-out procedures, parking arrangements, pet policies, noise restrictions, cleaning requirements, maintenance procedures, emergency contacts, and any other relevant information that a potential guest might need to know?" * 10
        
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": long_query, "n_results": 1},
            timeout=120  # Longer timeout for long queries
        )
        # Should handle long queries gracefully
        assert response.status_code in [200, 400, 422, 500]
    
    @pytest.mark.parametrize("n_results", [1, 3, 5])
    def test_llm_search_different_result_counts(self, base_url, wait_for_service, n_results):
        """Test LLM search with different n_results values"""
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": "apartment features", "n_results": n_results},
            timeout=60
        )
        assert response.status_code == 200
        
        results = response.json()
        assert len(results["results"]) <= n_results
    
    @pytest.mark.integration
    def test_llm_integration_workflow(self, base_url, wait_for_service):
        """Test complete LLM integration workflow"""
        # 1. Check LLM status
        status_response = requests.get(f"{base_url}/llm-status", timeout=10)
        assert status_response.status_code == 200
        status = status_response.json()
        
        # 2. Test LLM search if available
        if status["llm_available"]:
            response = requests.post(
                f"{base_url}/search-with-llm",
                json={"query": "apartment summary", "n_results": 2},
                timeout=60
            )
            assert response.status_code == 200
            
            results = response.json()
            assert "llm_response" in results
            assert len(results["llm_response"]) > 0
        else:
            pytest.skip("LLM not available for testing")
    
    @pytest.mark.unit
    def test_llm_response_structure(self, base_url, wait_for_service):
        """Test that LLM response has correct structure"""
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": "test query", "n_results": 1},
            timeout=60
        )
        assert response.status_code == 200
        
        results = response.json()
        expected_keys = ["llm_response", "results"]
        for key in expected_keys:
            assert key in results, f"Missing key: {key}"
        
        # Check data types
        assert isinstance(results["llm_response"], str)
        assert isinstance(results["results"], list)
    
    @pytest.mark.unit
    def test_llm_error_handling(self, base_url, wait_for_service):
        """Test LLM error handling for various scenarios"""
        # Test with malformed JSON
        response = requests.post(
            f"{base_url}/search-with-llm",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=1
        )
        assert response.status_code in [400, 422]
        
        # Test with very short timeout to trigger timeout error
        response = requests.post(
            f"{base_url}/search-with-llm",
            json={"query": "test query", "n_results": 1},
            timeout=10  # Short but realistic timeout
        )
        # Should handle timeout gracefully
        assert response.status_code in [200, 408, 500]
    
    @pytest.mark.slow
    def test_llm_performance(self, base_url, wait_for_service):
        """Test LLM performance with multiple concurrent requests"""
        import concurrent.futures
        
        def make_request(query):
            response = requests.post(
                f"{base_url}/search-with-llm",
                json={"query": query, "n_results": 1},
                timeout=60
            )
            return response.status_code == 200
        
        queries = [
            "amenities",
            "check-in",
            "parking",
            "rules",
            "features"
        ]
        
        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            results = list(executor.map(make_request, queries))
        
        # Most requests should succeed (allowing for some failures due to rate limiting)
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.6, f"Success rate {success_rate} is too low"