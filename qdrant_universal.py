import os
import requests
import uuid
import threading
from typing import Dict, Any, List, Optional
from openai import OpenAI
from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("Qdrant Universal")

# Configuration from environment variables
QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
EMBEDDING_API_KEY = os.getenv("EMBEDDING_API_KEY", "")
EMBEDDING_BASE_URL = os.getenv("EMBEDDING_BASE_URL", "https://api.openai.com/v1")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-v4")

# Initialize global clients
_openai_client: Optional[OpenAI] = None
_collection_lock = threading.Lock()

def get_openai_client() -> OpenAI:
    """Lazy initialization of the OpenAI client."""
    global _openai_client
    if _openai_client is None:
        if not EMBEDDING_API_KEY:
            raise ValueError("EMBEDDING_API_KEY is not set")
        _openai_client = OpenAI(
            api_key=EMBEDDING_API_KEY,
            base_url=EMBEDDING_BASE_URL
        )
    return _openai_client

def get_embedding(text: str) -> List[float]:
    """Get embedding for text using OpenAI-compatible API."""
    client = get_openai_client()
    
    response = client.embeddings.create(
        input=text,
        model=EMBEDDING_MODEL_NAME
    )
    
    return response.data[0].embedding

def get_collection_size(collection_name: str) -> Optional[int]:
    """Fetch the expected vector size for a collection from Qdrant. Returns None if collection doesn't exist."""
    try:
        response = requests.get(f"{QDRANT_URL}/collections/{collection_name}", timeout=5)
        if response.status_code != 200:
            return None
        
        data = response.json().get("result", {})
        vectors = data.get("config", {}).get("params", {}).get("vectors", {})
        
        if isinstance(vectors, dict):
            if "size" in vectors:
                return vectors["size"]
            for v in vectors.values():
                if isinstance(v, dict) and "size" in v:
                    return v["size"]
        return None
    except Exception:
        return None

def create_collection_if_not_exists(collection_name: str, vector_size: int):
    """Create Qdrant collection if it doesn't exist with specified vector size."""
    with _collection_lock:
        response = requests.get(f"{QDRANT_URL}/collections/{collection_name}", timeout=5)
        if response.status_code == 200:
            return
            
        config = {
            "vectors": {
                "size": vector_size,
                "distance": "Cosine"
            }
        }
        res = requests.put(f"{QDRANT_URL}/collections/{collection_name}", json=config, timeout=5)
        if res.status_code != 200:
            # If it was created by another process in the meantime, it might fail.
            # We check again to be sure.
            response = requests.get(f"{QDRANT_URL}/collections/{collection_name}", timeout=5)
            if response.status_code == 200:
                return
            raise Exception(f"Failed to create collection: {res.text}")

@mcp.tool()
def qdrant_search(query: str, collection_name: str, limit: int = 5) -> List[Dict[str, Any]]:
    vector = get_embedding(query)
    target_size = get_collection_size(collection_name)
    
    if target_size is None:
        raise ValueError(f"Collection '{collection_name}' does not exist.")

    if len(vector) != target_size:
        raise ValueError(
            f"Dimension mismatch: Embedding produced {len(vector)}D vector, "
            f"but collection '{collection_name}' expects {target_size}D. "
            "Padding/truncation is disabled to preserve search quality."
        )

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
        raise Exception(f"Search failed for {collection_name} (size {target_size}): {response.text}")
        
    return [hit["payload"] for hit in response.json().get("result", [])]

@mcp.tool()
def qdrant_scroll(collection_name: str, limit: int = 10, offset: Optional[str] = None) -> Dict[str, Any]:
    """Scroll through records in a Qdrant collection (introspection tool)."""
    payload = {
        "limit": limit,
        "with_payload": True,
        "with_vectors": False
    }
    if offset:
        payload["offset"] = offset
        
    response = requests.post(
        f"{QDRANT_URL}/collections/{collection_name}/points/scroll",
        json=payload
    )
    
    if response.status_code != 200:
        raise Exception(f"Scroll failed: {response.text}")
        
    return response.json().get("result", {})

@mcp.tool()
def qdrant_store(text: str, metadata: Dict[str, Any], collection_name: str) -> str:
    vector = get_embedding(text)
    target_size = get_collection_size(collection_name)
    
    if target_size is None:
        # Create collection with the size of the current embedding
        create_collection_if_not_exists(collection_name, len(vector))
        target_size = len(vector)
    elif len(vector) != target_size:
        raise ValueError(
            f"Dimension mismatch: Embedding produced {len(vector)}D vector, "
            f"but existing collection '{collection_name}' expects {target_size}D."
        )

    point_id = str(uuid.uuid4())
    
    if "text" in metadata:
        raise ValueError("Metadata cannot contain 'text' key as it is reserved for the document content.")
        
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
        raise Exception(f"Store failed: {response.text}")
        
    return f"Stored in {collection_name} (size {target_size}) with ID: {point_id}"

@mcp.tool()
def qdrant_list_collections() -> List[Dict[str, Any]]:
    """List all collections in Qdrant with their metadata."""
    response = requests.get(
        f"{QDRANT_URL}/collections",
        timeout=5
    )
    
    if response.status_code != 200:
        raise Exception(f"Failed to list collections: {response.text}")
    
    data = response.json()
    collections = data.get("result", {}).get("collections", [])
    
    result = []
    for coll in collections:
        coll_name = coll.get("name", "")
        # Fetch detailed info for each collection to get vector_size and point_count
        try:
            detail_response = requests.get(
                f"{QDRANT_URL}/collections/{coll_name}",
                timeout=5
            )
            if detail_response.status_code == 200:
                detail_data = detail_response.json()
                result_config = detail_data.get("result", {})
                config = result_config.get("config", {})
                params = config.get("params", {})
                vectors = params.get("vectors", {})
                
                result.append({
                    "name": coll_name,
                    "vector_size": vectors.get("size", 0) if isinstance(vectors, dict) else 0,
                    "point_count": result_config.get("points_count", 0),
                    "distance_metric": vectors.get("distance", "Cosine") if isinstance(vectors, dict) else "Cosine"
                })
            else:
                # Fallback to minimal info if detailed request fails
                result.append({
                    "name": coll_name,
                    "vector_size": 0,
                    "point_count": 0,
                    "distance_metric": "Cosine"
                })
        except Exception:
            # Fallback on error
            result.append({
                "name": coll_name,
                "vector_size": 0,
                "point_count": 0,
                "distance_metric": "Cosine"
            })
    
    return result

if __name__ == "__main__":
    mcp.run()
