# Recipe: RB-001 - Qdrant MCP Critical Fixes

## Status: IN PROGRESS

## Problem Statement

Three critical issues in qdrant_universal.py:

1. **Empty query validation** - `qdrant_search` accepts empty string causing API error 400
2. **Path normalization mismatch** - `normalize_file_path_for_qdrant` converts forward slashes to backslashes, causing silent search failures
3. **API discoverability** - Missing docstrings cause user confusion about `filter_metadata` parameter

## Traceability Matrix

| Issue ID | Requirement | Implementation | Test |
|----------|-------------|----------------|------|
| I1 | Validate empty query | `qdrant_search` line 132 | `test_empty_query_validation` |
| I2 | Fix path normalization | `normalize_file_path_for_qdrant` line 12 | `test_path_normalization` |
| I3 | Add docstrings | All public functions | N/A |

## Implementation Plan

### DATA Layer
- No database changes required

### LOGIC Layer (Python)

#### Fix 1: Empty Query Validation
**File**: `qdrant_universal.py`
**Location**: Line 132-133

```python
# BEFORE
def qdrant_search(query: str, collection_name: str, limit: int = 5, filter_metadata: Any = None) -> List[Dict[str, Any]]:
    vector = get_embedding(query)

# AFTER
def qdrant_search(query: str, collection_name: str, limit: int = 5, filter_metadata: Any = None) -> List[Dict[str, Any]]:
    """
    Search for code in a Qdrant collection using semantic search.
    
    Args:
        query: Natural language search query (required, cannot be empty)
        collection_name: Name of the Qdrant collection
        limit: Maximum number of results (default: 5)
        filter_metadata: Optional dict to filter results, e.g. {"file_path": "src/main.py", "symbol_type": "function_definition"}
    
    Example:
        qdrant_search("authentication logic", "project-myapp", filter_metadata={"file_path": "auth.py"})
    
    Raises:
        ValueError: If query is empty or whitespace-only
    """
    if not query or not query.strip():
        raise ValueError("query parameter cannot be empty or whitespace-only")
    vector = get_embedding(query)
```

#### Fix 2: Path Normalization
**File**: `qdrant_universal.py`
**Location**: Line 12-31

**Decision**: Remove aggressive normalization. Keep only whitespace trimming.

```python
# BEFORE
def normalize_file_path_for_qdrant(raw_path: str) -> str:
    """Normalize file path for Qdrant storage by replacing forward slashes with backslashes and collapsing multiple separators."""
    if raw_path is None:
        return raw_path
    
    raw_path = raw_path.strip()
    if raw_path == "":
        return raw_path
    
    # Replace all forward slashes with backslashes
    normalized = raw_path.replace("/", "\\")
    
    # Collapse multiple consecutive backslashes into a single backslash
    # Preserve leading double-backslash for UNC paths
    if normalized.startswith("\\\\"):
        normalized = "\\\\" + re.sub(r"\\+", r"\\", normalized[2:])
    else:
        normalized = re.sub(r"\\+", r"\\", normalized)
    
    return normalized

# AFTER
def normalize_file_path_for_qdrant(raw_path: str) -> str:
    """
    Normalize file path for Qdrant storage.
    
    Only trims whitespace - does NOT convert path separators.
    This ensures cross-platform compatibility where data may be stored
    with forward slashes (Linux/Mac) or backslashes (Windows).
    
    Args:
        raw_path: The file path to normalize
        
    Returns:
        Trimmed path string, or None/empty string as-is
    """
    if raw_path is None:
        return raw_path
    
    return raw_path.strip()
```

#### Fix 3: Add Docstrings to All Public Functions
Add comprehensive docstrings with usage examples to:
- `qdrant_search`
- `qdrant_scroll`
- `qdrant_store`
- `qdrant_get_symbol_code`
- `qdrant_list_symbols`
- `qdrant_optimize_collection`
- `qdrant_list_collections`

### UI Layer
- N/A (MCP server, no UI)

## Test Plan

### Test 1: Empty Query Validation
```python
def test_empty_query_validation():
    """Test that empty query raises ValueError"""
    with pytest.raises(ValueError, match="cannot be empty"):
        qdrant_search("", "test-collection")
    
    with pytest.raises(ValueError, match="cannot be empty"):
        qdrant_search("   ", "test-collection")
```

### Test 2: Path Normalization
```python
def test_path_normalization_preserves_separators():
    """Test that path normalization does not change separators"""
    assert normalize_file_path_for_qdrant("src/gui/views/file.py") == "src/gui/views/file.py"
    assert normalize_file_path_for_qdrant("src\\gui\\views\\file.py") == "src\\gui\\views\\file.py"
    assert normalize_file_path_for_qdrant("  src/gui/file.py  ") == "src/gui/file.py"
```

### Test 3: Integration Test
```python
def test_search_with_filter_metadata():
    """Test that filter_metadata works correctly"""
    # This test requires a running Qdrant instance
    # Mock or skip if not available
    pass
```

## Rollback Plan
If issues arise, revert to previous commit. The changes are isolated to:
- `qdrant_universal.py` (single file)
- No database schema changes
- No external API changes

## Definition of Done
- [ ] All tests pass
- [ ] Empty query validation works
- [ ] Path normalization preserves separators
- [ ] Docstrings added to all public functions
- [ ] No regression in existing functionality