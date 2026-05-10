import os
from unittest.mock import patch, MagicMock
import pytest
from openai import OpenAI

# Note: We import after patch in individual tests where needed or mock the module globally
# For now, let's try to run the tests and see where it fails (RED phase)

def test_embedding_base_url_default():
    """Test that EMBEDDING_BASE_URL defaults correctly when not set"""
    with patch.dict(os.environ, {}, clear=True):
        # We need to reload or re-import the module to see the effect of os.environ changes on constants
        import importlib
        import qdrant_universal
        importlib.reload(qdrant_universal)
        assert qdrant_universal.EMBEDDING_BASE_URL == 'https://dashscope-intl.aliyuncs.com/compatible-mode/v1'

def test_get_openai_client_custom_config():
    """Test that get_openai_client uses correct base_url and api_key"""
    with patch.dict(os.environ, {
        'EMBEDDING_API_KEY': 'test-api-key',
        'EMBEDDING_BASE_URL': 'https://custom-base-url.com/v1'
    }):
        import importlib
        import qdrant_universal
        importlib.reload(qdrant_universal)
        # Reset the global client
        qdrant_universal._openai_client = None
        client = qdrant_universal.get_openai_client()
        
        assert isinstance(client, OpenAI)
        assert str(client.base_url).rstrip('/') == 'https://custom-base-url.com/v1'
        assert client.api_key == 'test-api-key'

def test_validate_qdrant_collection_matching_size():
    """Test that validation passes when vector sizes match"""
    from qdrant_universal import validate_qdrant_collection
    
    with patch('qdrant_universal._http_session.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "config": {
                    "params": {
                        "vectors": {"size": 1024}
                    }
                }
            }
        }
        mock_get.return_value = mock_response
        
        # This should not raise an exception
        validate_qdrant_collection("test_collection", 1024)

def test_validate_qdrant_collection_mismatched_size():
    """Test that validation raises error when vector sizes don't match"""
    from qdrant_universal import validate_qdrant_collection
    with patch('qdrant_universal._http_session.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "config": {
                    "params": {
                        "vectors": {"size": 512}
                    }
                }
            }
        }
        mock_get.return_value = mock_response
        
        with pytest.raises(ValueError, match="Dimension mismatch"):
            validate_qdrant_collection("test_collection", 1024)
