import pytest
from unittest.mock import Mock, patch
from qdrant_universal import qdrant_search

@pytest.fixture
def mock_globals():
    with patch('qdrant_universal.get_embedding') as mock_emb, \
         patch('qdrant_universal.validate_qdrant_collection') as mock_val, \
         patch('qdrant_universal._http_session') as mock_session:
        mock_emb.return_value = [0.1] * 1024
        yield mock_session

def test_qdrant_search_accepts_filter_metadata(mock_globals):
    """Test that qdrant_search accepts filter_metadata parameter"""
    mock_response = Mock()
    mock_response.json.return_value = {
        "result": [{"id": 1, "payload": {"text": "test"}}]
    }
    mock_response.status_code = 200
    mock_globals.post.return_value = mock_response

    # Call qdrant_search with filter_metadata
    # We use collection_name that doesn't need quote for simplicity in comparison
    result = qdrant_search(
        query="test query",
        collection_name="test_collection",
        filter_metadata={"language": "python", "symbol_type": "function"}
    )

    # Verify the call was made
    assert mock_globals.post.called
    args, kwargs = mock_globals.post.call_args
    
    # Verify the payload contains the correct filter structure
    payload = kwargs['json']
    assert 'filter' in payload
    expected_filter = {
        "must": [
            {
                "key": "language",
                "match": {"value": "python"}
            },
            {
                "key": "symbol_type",
                "match": {"value": "function"}
            }
        ]
    }
    assert payload['filter'] == expected_filter

def test_qdrant_search_without_filter_metadata(mock_globals):
    """Test that qdrant_search works without filter_metadata (backward compatibility)"""
    mock_response = Mock()
    mock_response.json.return_value = {"result": []}
    mock_response.status_code = 200
    mock_globals.post.return_value = mock_response

    # Call without filter_metadata
    qdrant_search(
        query="search query",
        collection_name="test_collection"
    )

    # Get the actual call
    _, kwargs = mock_globals.post.call_args
    payload = kwargs['json']

    # Filter should not be present when no filter_metadata is provided
    assert 'filter' not in payload
