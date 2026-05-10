---
name: qdrantmcp
description: codebase memory
---

# Skill: Semantic Codebase Memory (Qdrant)

## Description

This skill enables the agent to utilize a persistent, vector-backed semantic memory to navigate large or multiple codebases. It moves beyond keyword matching by understanding the intent and meaning behind code snippets.

## Capabilities

- **Semantic Search**: Finding logic based on description rather than exact names.
- **Cross-Project Discovery**: Identifying patterns or implementations in projects not currently open.
- **Instant Context**: Rapidly getting up to speed on a new or forgotten module.

## Tool Mapping

The following tools are provided by the `qdrant2` MCP server:

- `mcp_qdrant2_qdrant_search`: Primary search tool with metadata filtering.
- `mcp_qdrant2_qdrant_list_symbols`: High-level structural discovery.
- `mcp_qdrant2_qdrant_get_symbol_code`: Precise code reconstruction.
- `mcp_qdrant2_qdrant_list_collections`: Infrastructure discovery.
- `mcp_qdrant2_qdrant_scroll`: Raw data browsing.

## Operational Rules

### 1. The "Search First" Principle

If a user's request involves finding code, understanding an existing implementation, or asking "how does X work?", **ALWAYS** start with a semantic search before using `grep` or `list_dir`.

### 2. Structural Awareness (AST-Enhanced)

For complex codebase analysis, use the "Map then Reconstruct" pattern:
1. **Discovery**: Call `qdrant_list_symbols` to get a list of classes/functions in a specific file or the whole project.
2. **Context**: Call `qdrant_get_symbol_code` to retrieve the full, clean implementation of a specific symbol without reading the whole file. This is much more token-efficient than `view_file` for large modules.

### 3. Formulating Queries

When calling `mcp_qdrant2_qdrant_search`:
- **Query**: Use natural language descriptions (e.g., "authentication middleware with JWT").
- **Metadata Filters**: Use `filter_metadata` to narrow down results by `language`, `symbol_type` (e.g., `function_definition`), or `file_path`.
- **Collection**: Standard format is `project-<name_lowercase>`.

### 4. Handling Results

- Use the `text` field for quick logic verification.
- Use `file_path` to open the file in the editor if edits are needed.
- If results seem incomplete, use `qdrant_get_symbol_code` to ensure you have the full logic.

---

_Note: This skill relies on the Qdrant Universal MCP server (qdrant2)._
