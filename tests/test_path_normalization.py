"""Tests for path normalization utility function."""
import pytest
from qdrant_universal import normalize_file_path_for_qdrant


class TestNormalizeFilePathForQdrant:
    """Test suite for normalize_file_path_for_qdrant() function."""

    def test_none_input_returns_none(self):
        """None input should return None."""
        assert normalize_file_path_for_qdrant(None) is None

    def test_empty_string_returns_empty(self):
        """Empty string should return empty string."""
        assert normalize_file_path_for_qdrant("") == ""

    def test_forward_slashes_converted_to_backslashes(self):
        """Forward slashes should be converted to backslashes."""
        assert normalize_file_path_for_qdrant("tests/test_file.py") == "tests\\test_file.py"

    def test_multiple_forward_slashes_converted(self):
        """Multiple forward slashes should be converted."""
        assert normalize_file_path_for_qdrant("a/b/c/d.py") == "a\\b\\c\\d.py"

    def test_backslashes_preserved(self):
        """Backslashes should be preserved."""
        assert normalize_file_path_for_qdrant("tests\\test_file.py") == "tests\\test_file.py"

    def test_mixed_slashes_normalized(self):
        """Mixed slashes should be normalized to backslashes."""
        assert normalize_file_path_for_qdrant("tests/test\\file.py") == "tests\\test\\file.py"

    def test_multiple_consecutive_backslashes_collapsed(self):
        """Multiple consecutive backslashes should be collapsed."""
        assert normalize_file_path_for_qdrant("tests\\\\test_file.py") == "tests\\test_file.py"

    def test_multiple_consecutive_mixed_slashes_collapsed(self):
        """Multiple consecutive mixed slashes should be collapsed."""
        assert normalize_file_path_for_qdrant("tests///test\\\\file.py") == "tests\\test\\file.py"

    def test_leading_trailing_whitespace_stripped(self):
        """Leading and trailing whitespace should be stripped."""
        assert normalize_file_path_for_qdrant("  tests/test_file.py  ") == "tests\\test_file.py"

    def test_windows_absolute_path_normalized(self):
        """Windows absolute path should be normalized."""
        result = normalize_file_path_for_qdrant("C:/Users/test/file.py")
        assert result == "C:\\Users\\test\\file.py"

    def test_complex_path_normalized(self):
        """Complex path with various edge cases should be normalized."""
        result = normalize_file_path_for_qdrant("  a//b\\c///d\\\\e.py  ")
        assert result == "a\\b\\c\\d\\e.py"

    def test_normalize_unc_path(self):
        """UNC paths must preserve leading double-backslash."""
        result = normalize_file_path_for_qdrant("\\\\server\\share\\file.py")
        assert result == "\\\\server\\share\\file.py"

    def test_normalize_unc_path_with_forward_slashes(self):
        """UNC paths with forward slashes should be converted."""
        result = normalize_file_path_for_qdrant("//server/share/file.py")
        assert result == "\\\\server\\share\\file.py"

    def test_normalize_whitespace_only(self):
        """Whitespace-only input should return empty string."""
        assert normalize_file_path_for_qdrant("   ") == ""
