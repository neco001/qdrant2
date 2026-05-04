# CHANGELOG

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

