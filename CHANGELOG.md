# CHANGELOG

## SOS Sync - 2026-05-15 21:30:29

## [2026-05-15 19:21:55] ee45d031-5583-49a9-bede-6633179d4356

**Task**: Create normalize_file_path_for_qdrant() utility function

**Advice**: Add a pure function at the top of qdrant_universal.py (after imports, before get_openai_client). Logic: replace '/' with '\', collapse multiple separators, strip whitespace. Handle None/empty inputs gracefully. This function will be used by both query and index functions.

---

## [2026-05-15 19:21:55] 2dd55ed7-0e86-4589-89a3-122e4dc6b97f

**Task**: Apply normalization to qdrant_list_symbols file_path filter

**Advice**: In qdrant_list_symbols (line 253), call normalize_file_path_for_qdrant(file_path) before constructing the filter payload. Only apply the filter if the normalized path is non-empty. No changes to function signature or return type.

---

## [2026-05-15 19:21:55] 06d6edc3-683f-48c1-87c4-1170b4ddaece

**Task**: Apply normalization to qdrant_get_symbol_code file_path filter

**Advice**: In qdrant_get_symbol_code (line 211), call normalize_file_path_for_qdrant(file_path) before constructing the must filter. Ensure the normalized value is used in the exact match condition. No changes to function signature or return type.

---

## [2026-05-15 19:21:55] bff84ecf-fd33-49ad-bb94-2be7a82406e6

**Task**: Add unit tests for path normalization edge cases

**Advice**: Create tests in tests/test_path_normalization.py covering: forward slash input matches backslash index, backslash input unchanged, mixed separators normalized correctly, None/empty inputs return as-is. Use pytest. Follow existing test patterns in the project.

---

## [2026-05-15 19:21:55] e10ce0d4-0dc5-458c-ac30-2566479b3723

**Task**: Verify backward compatibility with existing queries

**Advice**: Run qdrant_list_symbols and qdrant_get_symbol_code against project-secureexampdf collection with both forward-slash and backslash paths to confirm both work. Test with: tests/test_secure_memory.py and tests\test_secure_memory.py. Both should return the same symbols.

---

## SOS Sync - 2026-05-04 16:57:35

## [2026-05-04 12:53:06] a5fcb252-6abe-41dd-b709-0cd442b6320e

**Task**: Add qdrant_list_collections tool

**Advice**: Add a new FastMCP tool that queries GET /collections and returns structured data: collection name, vector size, point count, distance metric. This is the primary feature request — agents need to discover collections before searching. Use requests.get with timeout=5. Return List[Dict] with collection metadata.

---

## [2026-05-04 12:53:06] 42878223-3e61-443e-9289-0fbcfc4a90fd

**Task**: Remove zero-padding/truncation of vectors

**Advice**: Remove lines 79-83 and 129-133 in qdrant_universal.py that pad vectors with zeros or truncate them. Instead, fetch the collection's expected size and compare against len(vector). If they mismatch, raise a clear ValueError like: DimensionMismatchError: Embedding produced 768D vectors but collection 'X' expects 1024D. This is critical — padding destroys cosine similarity.

---

## [2026-05-04 12:53:06] b7c20037-8906-4d7b-a325-f798104295f4

**Task**: Fix create_collection_if_not_exists hardcoded 1024

**Advice**: Modify create_collection_if_not_exists to accept vector_size as a parameter. Derive it from a probe embedding (len(get_embedding('probe'))) or from EMBEDDING_DIM env var. Remove the hardcoded 1024. Pass the actual size to the Qdrant PUT /collections payload.

---

## [2026-05-04 12:53:06] 4b37acf4-a000-493c-aefd-b83830340ea1

**Task**: Fix get_collection_size silent fallback to 1024

**Advice**: Replace the silent 'return 1024' fallback in get_collection_size with proper error propagation. Return None on failure and update callers to handle None explicitly — either raise an exception or trigger collection creation with correct dimensions. Never silently guess dimensions.

---

## [2026-05-04 12:53:06] 53f1240b-76f3-468b-895c-3e3e813affe5

**Task**: Add missing request timeouts

**Advice**: Add timeout=5 to all requests.get/requests.put calls that currently lack it, specifically in create_collection_if_not_exists (lines 58 and 68). This prevents indefinite hangs if Qdrant is unreachable.

---

## [2026-05-04 12:53:06] 4dfc997b-c3f4-4f8a-b76a-569fbe6ba253

**Task**: Protect text key from metadata overwrite in qdrant_store

**Advice**: In qdrant_store, metadata.update(metadata) can overwrite the 'text' key. Either validate for key conflicts and raise, or nest metadata under a separate key like 'meta'. Simple fix: check if 'text' in metadata and warn/raise.

---

