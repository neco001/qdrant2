# Qdrant Universal MCP Server

A specialized [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server designed for seamless interaction with [Qdrant](https://qdrant.tech/) vector databases.

## Why this one if so many others are available?

Most MCP servers for Qdrant are either too rigid (hardcoded dimensions) or too simple. This one is built for **real-world agentic workflows**:

- **Zero-Configuration Collections**: Just call `qdrant_store` on a new collection name. The server will generate an embedding, detect its dimensions, and create the collection with the correct configuration automatically. No manual setup required.
- **Universal Embedding Proxy**: Works with any OpenAI-compatible API. You can switch between OpenAI, DashScope, or local models (like Ollama/vLLM) just by changing the environment variables.
- **Search Integrity**: Many implementations "fix" dimension mismatches by adding zeros (padding), which destroys search accuracy. This server enforces strict dimension checks, ensuring your vector space remains clean and your searches accurate.
- **Agentic Visibility**: Includes introspection tools (`qdrant_list_collections`, `qdrant_scroll`) that allow LLMs to discover existing data structures and "look inside" collections, making them much more effective at autonomous data management.

## Features

- **Universal Search & Store**: Seamlessly interact with any Qdrant collection using natural language.
- **Smart Collection Creation**: Automatically derives vector dimensions from your chosen embedding model during first-time storage.
- **OpenAI-Compatible**: Use any provider (OpenAI, DashScope, Local LLMs) as long as it follows the OpenAI embedding API standard.
- **Full Introspection**: Tools for agents to list collections, check metadata, and scroll through records.

## Tools

- `qdrant_search`: Search for similar texts in a collection.
- `qdrant_store`: Store text and metadata in a collection (creates collection if missing).
- `qdrant_list_collections`: List all available collections and their stats.
- `qdrant_scroll`: Browse through points in a collection.

---

## Better Together

This MCP server handles the _retrieval_ and _management_ of vectors, but it works best when your data is already indexed.

Pair it with **[Qdrant Sentinel](https://github.com/neco001/Qdrant_Sentinel.git)** — an automated codebase indexer that watches your local projects and keeps them synced with Qdrant in real-time. Together, they provide a seamless "memory" for your AI agents.

---

## Prerequisites

Before using this MCP server, you need a running Qdrant instance and an Embedding API provider.

### 1. Set Up Qdrant (Vector Database)

#### Option A: Local Setup (Docker) - Recommended

The easiest way to run Qdrant locally is via Docker:

```bash
docker run -d \
  --name qdrant \
  --restart unless-stopped \
  -p 6333:6333 \
  -v qdrant_data:/qdrant/storage \
  qdrant/qdrant
```

#### Option B: Qdrant Cloud - Free Tier Available

1. Sign up at [Qdrant Cloud](https://cloud.qdrant.io/).
2. Create a free cluster.
3. Copy your **Cluster URL** and **API Key**.

### 2. Set Up an Embedding Provider

This server requires an OpenAI-compatible embedding API.

- **Qwen (DashScope) - Recommended**: Excellent performance and full OpenAI compatibility. Get your key from [Aliyun DashScope](https://dashscope.console.aliyun.com/).
- **OpenAI**: Get an API key from [OpenAI Dashboard](https://platform.openai.com/).
- **Google Gemini**: Get an API key from [Google AI Studio](https://aistudio.google.com/). Use an OpenAI-compatible proxy or their native OpenAI-compatible endpoint.
- **Local (Ollama/vLLM)**: Run Ollama locally and use `http://localhost:11434/v1` as your base URL.

## Setup

### Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
# Qdrant URL (default: http://localhost:6333)
QDRANT_URL=http://localhost:6333

# Embedding API Configuration (OpenAI-compatible)
EMBEDDING_API_KEY=your_api_key_here
EMBEDDING_BASE_URL=your_base_url_here
EMBEDDING_MODEL_NAME=your_embedding_model_here
```

### Installation

Using `uv` (recommended):

```bash
uv sync
```

Or using `pip`:

```bash
pip install .
```

## Usage

### Running the server

```bash
python qdrant_universal.py
```

### Integration with Claude Desktop

Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "qdrant-universal": {
      "command": "python",
      "args": ["path/to/qdrant_universal.py"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "EMBEDDING_API_KEY": "your_api_key_here",
        "EMBEDDING_BASE_URL": "your_base_url_here",
        "EMBEDDING_MODEL_NAME": "your_embedding_model_here"
      }
    }
  }
}
```

### Integration with Antigravity

Add this to your `%APPDATA%\.gemini\antigravity\mcp_config.json`:

```json
{
  "mcpServers": {
    "qdrant-universal": {
      "command": "uv",
      "args": ["run", "path/to/qdrant_universal.py"],
      "env": {
        "QDRANT_URL": "http://localhost:6333",
        "EMBEDDING_API_KEY": "your_api_key_here",
        "EMBEDDING_BASE_URL": "your_base_url_here",
        "EMBEDDING_MODEL_NAME": "your_embedding_model_here"
      }
    }
  }
}
```

## Development

Run tests:

```bash
pytest
```

## License

MIT
