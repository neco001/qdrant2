import pytest
import requests
from unittest.mock import patch, Mock
from qdrant_universal import qdrant_list_collections

def test_qdrant_list_collections_success():
    """Test successful retrieval of collections from Qdrant API"""
    # Mock /collections response
    mock_list_response = Mock()
    mock_list_response.status_code = 200
    mock_list_response.json.return_value = {
        "result": {
            "collections": [
                {"name": "coll1"},
                {"name": "coll2"}
            ]
        }
    }

    # Mock /collections/{name} responses
    mock_detail1 = Mock()
    mock_detail1.status_code = 200
    mock_detail1.json.return_value = {
        "result": {
            "config": {"params": {"vectors": {"size": 1536}}},
            "points_count": 100
        }
    }

    mock_detail2 = Mock()
    mock_detail2.status_code = 200
    mock_detail2.json.return_value = {
        "result": {
            "config": {"params": {"vectors": {"size": 768, "distance": "Euclidean"}}},
            "points_count": 50
        }
    }

    with patch('requests.get', side_effect=[mock_list_response, mock_detail1, mock_detail2]) as mock_get:
        result = qdrant_list_collections()
        assert mock_get.call_count == 3
        expected_result = [
            {"name": "coll1", "vector_size": 1536, "point_count": 100, "distance_metric": "Cosine"},
            {"name": "coll2", "vector_size": 768, "point_count": 50, "distance_metric": "Euclidean"}
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

def test_qdrant_list_collections_empty_collections():
    """Test behavior when no collections exist"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": {"collections": []}}
    with patch('requests.get', return_value=mock_response):
        result = qdrant_list_collections()
        assert result == []

def test_qdrant_list_collections_partial_failure():
    """Test handling when some detail requests fail"""
    mock_list_response = Mock()
    mock_list_response.status_code = 200
    mock_list_response.json.return_value = {
        "result": {
            "collections": [{"name": "fail_coll"}]
        }
    }

    mock_detail_fail = Mock()
    mock_detail_fail.status_code = 500

    with patch('requests.get', side_effect=[mock_list_response, mock_detail_fail]):
        result = qdrant_list_collections()
        assert len(result) == 1
        assert result[0]["name"] == "fail_coll"
        assert result[0]["vector_size"] == 0 # Fallback value
