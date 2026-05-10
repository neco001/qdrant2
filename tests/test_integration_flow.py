import pytest
from unittest.mock import Mock, patch
from qdrant_universal import qdrant_store, qdrant_search, qdrant_get_symbol_code

@pytest.fixture
def mock_session():
    with patch('qdrant_universal._http_session') as mock:
        yield mock

def test_full_retrieval_flow(mock_session):
    """
    Integration-style test for the full flow:
    1. Verify qdrant_store calls Qdrant properly.
    2. Verify qdrant_search works with filters.
    3. Verify qdrant_get_symbol_code reconstructs correctly.
    """
    # 1. Mock store
    with patch('qdrant_universal.get_embedding') as mock_emb, \
         patch('qdrant_universal.validate_qdrant_collection') as mock_val:
        
        mock_emb.return_value = [0.1] * 1024
        mock_val.return_value = True
        mock_session.put.return_value = Mock(status_code=200)

        store_res = qdrant_store(
            text="chunk 1",
            metadata={"symbol_name": "foo", "chunk_index": 0},
            collection_name="test_coll"
        )
        assert "Stored in test_coll" in store_res

    # 2. Mock search
    with patch('qdrant_universal.get_embedding') as mock_emb, \
         patch('qdrant_universal.validate_qdrant_collection') as mock_val:
        
        mock_emb.return_value = [0.1] * 1024
        mock_val.return_value = True
        mock_session.post.return_value = Mock(
            status_code=200,
            json=lambda: {"result": [{"payload": {"text": "found code", "symbol_name": "foo"}}]}
        )

        search_res = qdrant_search(
            query="find foo",
            collection_name="test_coll",
            filter_metadata={"symbol_name": "foo"}
        )
        assert search_res[0]["symbol_name"] == "foo"

    # 3. Mock reconstruction
    mock_session.post.return_value = Mock(
        status_code=200,
        json=lambda: {
            "result": {
                "points": [
                    {"payload": {"chunk_index": 1, "text": " part 2"}},
                    {"payload": {"chunk_index": 0, "text": "part 1"}}
                ]
            }
        }
    )

    code = qdrant_get_symbol_code(
        collection_name="test_coll",
        symbol_name="foo",
        file_path="foo.py"
    )
    assert code == "part 1 part 2"
