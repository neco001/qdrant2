import os
import requests
from typing import Dict, Any, List
from openai import OpenAI
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Qdrant Universal")

# Configuration from environment variables
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://api.openai.com/v1")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-v4")

def get_embedding(text: str) -> List[float]:
    """Get embedding for text using OpenAI-compatible API."""
    if not EMBEDDING_API_KEY:
        raise ValueError("EMBEDDING_API_KEY is not set")
        
    client = OpenAI(
        api_key=EMBEDDING_API_KEY,
        base_url=EMBEDDING_BASE_URL
    )
    
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL_NAME
    )
    
    return response.data[0].embedding

def create_collection_if_not_exists(collection_name: str):
    """Create Qdrant collection if it doesn't exist."""
    response = requests.get(f"{QDRANT_URL}/collections/{collection_name}")
    if response.status_code == 200:
        return
        
    # Default to 1024 dims for new collections (DashScope standard)
    config = {
        "vectors": {
            "size": 1024,
            "distance": "Cosine"
        }
    }
    res = requests.put(f"{QDRANT_URL}/collections/{collection_name}", json=config)
    if res.status_code != 200:
        raise Exception(f"Failed to create collection: {res.text}")

def get_collection_size(collection_name: str) -> int:
    """Fetch the expected vector size for a collection from Qdrant."""
    response = requests.get(f"{QDRANT_URL}/collections/{collection_name}")
    if response.status_code != 200:
        return 1024  # Default fallback
    
    config = response.json().get("result", {}).get("config", {})
    params = config.get("params", {})
    vectors = params.get("vectors", {})
    
    if isinstance(vectors, dict):
        return vectors.get("size", 1024)
    return 1024

@mcp.tool()
def qdrant_search(query: str, collection_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    """Search for similar texts in a Qdrant collection. Automatically adjusts dimensions."""
    vector = get_embedding(query)
    target_size = get_collection_size(collection_name)
    
    # Adjust dimensions to match collection schema
    if len(vector) != target_size:
        if len(vector) < target_size:
            vector.extend([0.0] * (target_size - len(vector)))
        else:
            vector = vector[:target_size]

    search_payload = {
        "vector": vector,
        "limit": limit,
        "with_payload": True
    }
    
    response = requests.post(
        f"{QDRANT_URL}/collections/{collection_name}/points/search",
        json=search_payload
    )
    
    if response.status_code != 200:
        raise Exception(f"Search failed for collection '{collection_name}' (target size {target_size}): {response.text}")
        
    return [hit["payload"] for hit in response.json().get("result", [])]

@mcp.tool()
def qdrant_store(text: str, metadata: Dict[str, Any], collection_name: str) -> str:
    """Store text and metadata in a Qdrant collection. Automatically adjusts dimensions."""
    create_collection_if_not_exists(collection_name)
    vector = get_embedding(text)
    target_size = get_collection_size(collection_name)
    
    # Adjust dimensions
    if len(vector) != target_size:
        if len(vector) < target_size:
            vector.extend([0.0] * (target_size - len(vector)))
        else:
            vector = vector[:target_size]

    import uuid
    point_id = str(uuid.uuid4())
    
    payload = {"text": text}
    payload.update(metadata)
    
    point = {
        "points": [
            {
                "id": point_id,
                "vector": vector,
                "payload": payload
            }
        ]
    }
    
    response = requests.put(
        f"{QDRANT_URL}/collections/{collection_name}/points?wait=true",
        json=point
    )
    
    if response.status_code != 200:
        raise Exception(f"Store failed for collection '{collection_name}' (target size {target_size}): {response.text}")
        
    return f"Stored successfully in {collection_name} (size {target_size}) with ID: {point_id}"

if __name__ == "__main__":
    mcp.run()
