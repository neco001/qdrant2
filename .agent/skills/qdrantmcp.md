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

- `mcp_qdrant2_qdrant_search`: The primary search tool.
- `mcp_qdrant2_qdrant_list_collections`: To identify which projects are indexed.
- `mcp_qdrant2_qdrant_scroll`: To browse content within a specific project.

## Operational Rules

### 1. The "Search First" Principle

If a user's request involves finding code, understanding an existing implementation, or asking "how does X work?", **ALWAYS** start with a semantic search before using `grep` or `list_dir`.

### 2. Formulating Queries

When calling `mcp_qdrant2_qdrant_search`:

- **Query**: Use natural language descriptions (e.g., "authentication middleware with JWT", "database connection pool").
- **Collection**: Derive the collection name from the project name using the format `project-<name_lowercase>`.
- **Limit**: Start with a limit of 5 to 10 results to maintain focus.

### 3. Handling Results

- Use the `text` field of the results to answer the user or to decide which files to open for deeper analysis.
- Use `file_path` from metadata to navigate to the exact location in the filesystem.

### 4. Intent Recognition

Trigger this skill automatically if the user mentions:

- "Where is..." / "Find me..."
- "How did I do..." / "Show me an example of..."
- "Explain the logic of..."

---

_Note: This skill relies on the Qdrant Universal MCP server (qdrant2)._
