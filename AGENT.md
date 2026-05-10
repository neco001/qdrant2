# 🤖 AGENT.md: How to use this MCP Server

If you are an AI agent using this server, follow these protocols to maximize retrieval quality and minimize token waste.

## 🚀 Quick Start
This server provides **Semantic Codebase Memory**. It works best when paired with **Qdrant Sentinel** (background indexer).

### 1. Identify Your Context
Check which project you are in and find the corresponding Qdrant collection:
- `qdrant_list_collections`: Run this once to see available "memories".
- Collection names follow the pattern: `project-<folder_name_lowercase>`.

### 2. The "Search First" Protocol
Before using `grep` or browsing directories, use semantic search:
- `qdrant_search(query="how is X implemented", collection_name="project-foo")`
- Use `filter_metadata` to narrow results (e.g., `{"symbol_type": "function_definition"}`).

### 3. Structural Reconstruction (AST)
If you need to understand a specific function or class implementation:
1. **List symbols**: `qdrant_list_symbols(collection_name="...", file_path="...")` to find exact names.
2. **Fetch code**: `qdrant_get_symbol_code(...)` to get the full, clean implementation.
   > [!TIP]
   > Use `qdrant_get_symbol_code` instead of `view_file` for large files. It only returns the relevant symbol logic, saving thousands of context tokens.

### 4. Continuous Indexing
If you make significant changes to the codebase:
- Sentinel will re-index in the background.
- You can manually call `qdrant_store` to update specific "memories" instantly.
- Run `qdrant_optimize_collection` if you add new metadata fields you want to filter by.

---
*Built for autonomous agents by Antigravity (Google DeepMind Team).*
