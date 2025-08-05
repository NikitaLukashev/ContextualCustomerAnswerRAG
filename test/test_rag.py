# Test suite - Comprehensive testing framework
#!/usr/bin/env python3
"""
Unit tests for RAG system endpoints using pytest
"""

import pytest
import requests
from unittest.mock import Mock, patch

class TestRAGHandler:
    """Test class for RAG system functionality"""
    
    def test_health_check(self, base_url, wait_for_service):
        """Test health check endpoint"""
        response = requests.get(f"{base_url}/health", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_collection_info(self, base_url, wait_for_service):
        """Test collection info endpoint"""
        response = requests.get(f"{base_url}/info", timeout=10)
        assert response.status_code == 200
        
        info = response.json()
        assert "collection_name" in info
        assert "document_count" in info
        assert isinstance(info["document_count"], int)
        assert info["document_count"] >= 0
    
    def test_sample_queries(self, base_url, wait_for_service):
        """Test sample queries endpoint"""
        response = requests.get(f"{base_url}/sample-queries", timeout=10)
        assert response.status_code == 200
        
        data = response.json()
        assert "sample_queries" in data
        queries = data["sample_queries"]
        assert isinstance(queries, list)
        assert len(queries) > 0
        
        # Check that queries are strings
        for query in queries:
            assert isinstance(query, str)
            assert len(query) > 0
    
    @pytest.mark.parametrize("query", [
        "What amenities are available in the apartment?",
        "What are the check-in and check-out times?",
        "Is there parking available?",
        "What are the house rules?"
    ])
    def test_search_functionality(self, base_url, wait_for_service, query):
        """Test search functionality with different queries"""
        response = requests.post(
            f"{base_url}/search",
            json={"query": query, "n_results": 3},
            timeout=30
        )
        assert response.status_code == 200
        
        results = response.json()
        assert "total_results" in results
        assert "results" in results
        assert isinstance(results["total_results"], int)
        assert isinstance(results["results"], list)
        
        # Check that we have results
        assert results["total_results"] > 0
        assert len(results["results"]) > 0
    
    def test_search_with_invalid_query(self, base_url, wait_for_service):
        """Test search with invalid query"""
        response = requests.post(
            f"{base_url}/search",
            json={"query": "", "n_results": 3},
            timeout=10
        )
        # Should handle empty query gracefully or return error
        assert response.status_code in [200, 400, 422]
    
    def test_search_with_invalid_n_results(self, base_url, wait_for_service):
        """Test search with invalid n_results parameter"""
        response = requests.post(
            f"{base_url}/search",
            json={"query": "test query", "n_results": -1},
            timeout=10
        )
        # Should handle invalid n_results gracefully or return error
        assert response.status_code in [200, 400, 422]
    
    def test_search_missing_parameters(self, base_url, wait_for_service):
        """Test search with missing required parameters"""
        # Missing query
        response = requests.post(
            f"{base_url}/search",
            json={"n_results": 3},
            timeout=10
        )
        assert response.status_code in [400, 422]
        
        # Missing n_results
        response = requests.post(
            f"{base_url}/search",
            json={"query": "test query"},
            timeout=10
        )
        assert response.status_code in [200, 400, 422]  # n_results might have default
    
    @pytest.mark.parametrize("n_results", [1, 5, 10])
    def test_search_different_result_counts(self, base_url, wait_for_service, n_results):
        """Test search with different n_results values"""
        response = requests.post(
            f"{base_url}/search",
            json={"query": "apartment", "n_results": n_results},
            timeout=30
        )
        assert response.status_code == 200
        
        results = response.json()
        assert len(results["results"]) <= n_results
    
    @pytest.mark.integration
    def test_complete_search_workflow(self, base_url, wait_for_service):
        """Test complete search workflow from query to results"""
        # 1. Check system health
        health_response = requests.get(f"{base_url}/health", timeout=10)
        assert health_response.status_code == 200
        
        # 2. Get collection info
        info_response = requests.get(f"{base_url}/info", timeout=10)
        assert info_response.status_code == 200
        info = info_response.json()
        assert info["document_count"] > 0
        
        # 3. Get sample queries
        queries_response = requests.get(f"{base_url}/sample-queries", timeout=10)
        assert queries_response.status_code == 200
        sample_queries = queries_response.json()["sample_queries"]
        assert len(sample_queries) > 0
        
        # 4. Test search with first sample query
        first_query = sample_queries[0]
        search_response = requests.post(
            f"{base_url}/search",
            json={"query": first_query, "n_results": 3},
            timeout=30
        )
        assert search_response.status_code == 200
        
        # 5. Verify search returned results
        search_results = search_response.json()
        assert search_results["total_results"] > 0
    
    @pytest.mark.unit
    def test_search_response_structure(self, base_url, wait_for_service):
        """Test that search response has correct structure"""
        response = requests.post(
            f"{base_url}/search",
            json={"query": "test query", "n_results": 1},
            timeout=10
        )
        assert response.status_code == 200
        
        results = response.json()
        expected_keys = ["total_results", "results"]
        for key in expected_keys:
            assert key in results, f"Missing key: {key}"
        
        # Check data types
        assert isinstance(results["total_results"], int)
        assert isinstance(results["results"], list)
    
    @pytest.mark.unit
    def test_error_handling(self, base_url, wait_for_service):
        """Test error handling for various scenarios"""
        # Test with malformed JSON
        response = requests.post(
            f"{base_url}/search",
            data="invalid json",
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        assert response.status_code in [400, 422]
        
        # Test with invalid endpoint
        response = requests.get(f"{base_url}/invalid-endpoint", timeout=10)
        assert response.status_code == 404
