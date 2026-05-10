import pytest
from unittest.mock import Mock, patch
from qdrant_universal import qdrant_get_symbol_code

@pytest.fixture
def mock_session():
    with patch('qdrant_universal._http_session') as mock:
        yield mock

def test_qdrant_get_symbol_code_reconstructs_correctly(mock_session):
    """Test that qdrant_get_symbol_code reconstructs code from sorted chunks."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "result": {
            "points": [
                {
                    "payload": {
                        "chunk_index": 2,
                        "text": "    return 'world'\n",
                        "symbol_name": "bar",
                        "file_path": "file.py"
                    }
                },
                {
                    "payload": {
                        "chunk_index": 0,
                        "text": "def bar():\n",
                        "symbol_name": "bar",
                        "file_path": "file.py"
                    }
                },
                {
                    "payload": {
                        "chunk_index": 1,
                        "text": "    print('hello')\n",
                        "symbol_name": "bar",
                        "file_path": "file.py"
                    }
                }
            ]
        }
    }
    mock_session.post.return_value = mock_response

    result = qdrant_get_symbol_code(
        collection_name="test_collection",
        symbol_name="bar",
        file_path="file.py"
    )

    expected = "def bar():\n    print('hello')\n    return 'world'\n"
    assert result == expected

    # Verify API call filters
    _, kwargs = mock_session.post.call_args
    payload = kwargs['json']
    filters = payload['filter']['must']
    
    # Check if symbol_name and file_path are in filters
    filter_keys = [f['key'] for f in filters]
    assert "symbol_name" in filter_keys
    assert "file_path" in filter_keys

def test_qdrant_get_symbol_code_empty(mock_session):
    """Test behavior when no chunks are found."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"result": {"points": []}}
    mock_session.post.return_value = mock_response

    result = qdrant_get_symbol_code(
        collection_name="test_collection",
        symbol_name="none",
        file_path="none.py"
    )
    assert result == ""
