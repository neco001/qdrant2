import pytest
from unittest.mock import Mock, patch
from qdrant_universal import qdrant_list_symbols

@pytest.fixture
def mock_session():
    with patch('qdrant_universal._http_session') as mock:
        yield mock

def test_qdrant_list_symbols_exists_and_calls_scroll(mock_session):
    """Test that qdrant_list_symbols calls the scroll API."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": {
            "points": [
                {"payload": {"symbol_name": "func1", "symbol_type": "function"}},
                {"payload": {"symbol_name": "class1", "symbol_type": "class"}},
                {"payload": {"symbol_name": "func1", "symbol_type": "function"}} # Duplicate
            ]
        }
    }
    mock_session.post.return_value = mock_response

    result = qdrant_list_symbols(collection_name="test_collection")

    # Verify unique symbols are returned
    assert len(result) == 2
    assert {"symbol_name": "func1", "symbol_type": "function"} in result
    assert {"symbol_name": "class1", "symbol_type": "class"} in result

    # Verify API call
    args, kwargs = mock_session.post.call_args
    assert "/collections/test_collection/points/scroll" in args[0]
    payload = kwargs['json']
    assert isinstance(payload['with_payload'], list)
    assert "symbol_name" in payload['with_payload']

def test_qdrant_list_symbols_with_filter(mock_session):
    """Test that file_path filter is applied if provided."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": {"points": []}}
    mock_session.post.return_value = mock_response

    qdrant_list_symbols(collection_name="test_collection", file_path="main.py")

    _, kwargs = mock_session.post.call_args
    payload = kwargs['json']
    assert "filter" in payload
    assert payload["filter"]["must"][0]["key"] == "file_path"
    assert payload["filter"]["must"][0]["match"]["value"] == "main.py"
