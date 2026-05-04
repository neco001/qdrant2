import pytest
import requests
from unittest.mock import patch, Mock
from qdrant_universal import qdrant_list_collections

def test_qdrant_list_collections_success():
    """Test successful retrieval of collections from Qdrant API"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "collections": [
            {
                "name": "offers_registry",
                "vector_size": 1536,
                "point_count": 100,
                "distance": "Cosine"
            },
            {
                "name": "test_collection",
                "vector_size": 768,
                "point_count": 50,
                "distance": "Euclidean"
            }
        ]
    }

    with patch('requests.get', return_value=mock_response) as mock_get:
        result = qdrant_list_collections()
        mock_get.assert_called_once_with("http://localhost:6333/collections", timeout=5)
        expected_result = [
            {"name": "offers_registry", "vector_size": 1536, "point_count": 100, "distance_metric": "Cosine"},
            {"name": "test_collection", "vector_size": 768, "point_count": 50, "distance_metric": "Euclidean"}
        ]
        assert result == expected_result

def test_qdrant_list_collections_api_error():
    """Test that exception is raised when API returns non-200 status"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    with patch('requests.get', return_value=mock_response):
        with pytest.raises(Exception):
            qdrant_list_collections()

def test_qdrant_list_collections_request_timeout():
    """Test that timeout exception is handled properly"""
    with patch('requests.get', side_effect=requests.Timeout("Request timed out")):
        with pytest.raises(Exception):
            qdrant_list_collections()

def test_qdrant_list_collections_connection_error():
    """Test that connection error is handled properly"""
    with patch('requests.get', side_effect=requests.ConnectionError("Connection failed")):
        with pytest.raises(Exception):
            qdrant_list_collections()

def test_qdrant_list_collections_empty_collections():
    """Test behavior when no collections exist"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"collections": []}
    with patch('requests.get', return_value=mock_response):
        result = qdrant_list_collections()
        assert result == []

def test_qdrant_list_collections_missing_fields():
    """Test handling of collections with missing optional fields"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "collections": [
            {
                "name": "incomplete_collection",
                "vector_size": 128,
                "point_count": 10
                # Missing distance field - should default to "Cosine"
            }
        ]
    }
    with patch('requests.get', return_value=mock_response):
        result = qdrant_list_collections()
        assert len(result) == 1
        assert result[0]["name"] == "incomplete_collection"
        assert result[0]["vector_size"] == 128
        assert result[0]["point_count"] == 10
        assert result[0]["distance_metric"] == "Cosine"  # Default value
