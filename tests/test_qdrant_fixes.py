"""Tests for qdrant fixes - empty query validation and path normalization preservation."""
import pytest
from unittest.mock import Mock, patch
from qdrant_universal import qdrant_search, normalize_file_path_for_qdrant


class TestEmptyQueryValidation:
    """Test suite for empty query validation in qdrant_search()."""

    @pytest.fixture
    def mock_globals(self):
        """Mock external dependencies for qdrant_search."""
        with patch('qdrant_universal.get_embedding') as mock_emb, \
             patch('qdrant_universal.validate_qdrant_collection') as mock_val, \
             patch('qdrant_universal._http_session') as mock_session:
            mock_emb.return_value = [0.1] * 1024
            yield mock_session

    def test_empty_string_query_raises_valueerror(self, mock_globals):
        """Empty string query should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            qdrant_search("", "test-collection")

    def test_whitespace_only_query_raises_valueerror(self, mock_globals):
        """Whitespace-only query should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            qdrant_search("   ", "test-collection")

    def test_tabs_only_query_raises_valueerror(self, mock_globals):
        """Tabs-only query should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            qdrant_search("\t\t", "test-collection")

    def test_newlines_only_query_raises_valueerror(self, mock_globals):
        """Newlines-only query should raise ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            qdrant_search("\n\n", "test-collection")

    def test_valid_query_works(self, mock_globals):
        """Valid query should work normally."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": []}
        mock_response.status_code = 200
        mock_globals.post.return_value = mock_response

        result = qdrant_search("valid query", "test-collection")
        assert result == []


class TestPathNormalizationPreservesSeparators:
    """Test suite for path normalization that preserves path separators."""

    def test_forward_slashes_preserved(self):
        """Forward slashes should be preserved for cross-platform compatibility."""
        # This is the CORRECT behavior - data stored with forward slashes
        # should be searchable with forward slashes
        assert normalize_file_path_for_qdrant("src/gui/views/file.py") == "src/gui/views/file.py"

    def test_backslashes_preserved(self):
        """Backslashes should be preserved for Windows paths."""
        assert normalize_file_path_for_qdrant("src\\gui\\views\\file.py") == "src\\gui\\views\\file.py"

    def test_whitespace_trimmed(self):
        """Whitespace should be trimmed."""
        assert normalize_file_path_for_qdrant("  src/gui/file.py  ") == "src/gui/file.py"

    def test_none_returns_none(self):
        """None input should return None."""
        assert normalize_file_path_for_qdrant(None) is None

    def test_empty_string_returns_empty(self):
        """Empty string should return empty string."""
        assert normalize_file_path_for_qdrant("") == ""

    def test_whitespace_only_returns_empty(self):
        """Whitespace-only input should return empty string."""
        assert normalize_file_path_for_qdrant("   ") == ""

    def test_mixed_separators_preserved(self):
        """Mixed separators should be preserved (not converted)."""
        # This allows searching for paths that may have mixed separators
        assert normalize_file_path_for_qdrant("src/gui\\views/file.py") == "src/gui\\views/file.py"


class TestFilterMetadataWithStringInput:
    """Test that filter_metadata works when passed as JSON string (MCP framework quirk)."""

    @pytest.fixture
    def mock_globals(self):
        """Mock external dependencies for qdrant_search."""
        with patch('qdrant_universal.get_embedding') as mock_emb, \
             patch('qdrant_universal.validate_qdrant_collection') as mock_val, \
             patch('qdrant_universal._http_session') as mock_session:
            mock_emb.return_value = [0.1] * 1024
            yield mock_session

    def test_filter_metadata_as_json_string(self, mock_globals):
        """filter_metadata passed as JSON string should be parsed correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": []}
        mock_response.status_code = 200
        mock_globals.post.return_value = mock_response

        # MCP framework passes dict as JSON string
        result = qdrant_search(
            query="test",
            collection_name="test-collection",
            filter_metadata='{"file_path": "src/main.py", "symbol_type": "function"}'
        )

        # Verify the call was made with parsed filter
        args, kwargs = mock_globals.post.call_args
        payload = kwargs['json']
        assert 'filter' in payload
        assert payload['filter']['must'][0]['key'] == 'file_path'
        assert payload['filter']['must'][0]['match']['value'] == 'src/main.py'

    def test_filter_metadata_as_dict(self, mock_globals):
        """filter_metadata passed as dict should work correctly."""
        mock_response = Mock()
        mock_response.json.return_value = {"result": []}
        mock_response.status_code = 200
        mock_globals.post.return_value = mock_response

        result = qdrant_search(
            query="test",
            collection_name="test-collection",
            filter_metadata={"file_path": "src/main.py"}
        )

        # Verify the call was made
        args, kwargs = mock_globals.post.call_args
        payload = kwargs['json']
        assert 'filter' in payload