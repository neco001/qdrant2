import pytest
from unittest.mock import Mock, patch
from qdrant_universal import qdrant_optimize_collection

@pytest.fixture
def mock_session():
    with patch('qdrant_universal._http_session') as mock:
        yield mock

def test_qdrant_optimize_collection_calls_put_for_fields(mock_session):
    """Test that qdrant_optimize_collection calls PUT for all metadata fields."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_session.put.return_value = mock_response

    qdrant_optimize_collection(collection_name="test_collection")

    expected_fields = {'language', 'symbol_type', 'file_path', 'symbol_name'}
    actual_fields = set()

    assert mock_session.put.call_count == 4
    for call in mock_session.put.call_args_list:
        args, kwargs = call
        assert "/collections/test_collection/index" in args[0]
        payload = kwargs['json']
        actual_fields.add(payload['field_name'])
        assert payload['field_schema'] == 'keyword'

    assert actual_fields == expected_fields
