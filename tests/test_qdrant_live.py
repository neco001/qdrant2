import requests
import json

# Test the qdrant_list_collections endpoint
response = requests.get("http://localhost:6333/collections", timeout=5)

if response.status_code == 200:
    data = response.json()
    collections = data.get("result", {}).get("collections", [])
    
    result = []
    for coll in collections:
        coll_name = coll.get("name", "")
        # Fetch detailed info for each collection
        try:
            detail_response = requests.get(
                f"http://localhost:6333/collections/{coll_name}",
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
                    "distance_metric": params.get("distance", "Cosine")
                })
            else:
                result.append({
                    "name": coll_name,
                    "vector_size": 0,
                    "point_count": 0,
                    "distance_metric": "Cosine"
                })
        except Exception as e:
            result.append({
                "name": coll_name,
                "vector_size": 0,
                "point_count": 0,
                "distance_metric": "Cosine"
            })
    
    print(f"Found {len(result)} collections:")
    for coll in result:
        print(f"  - {coll['name']}: {coll['vector_size']} dims, {coll['point_count']} points, {coll['distance_metric']}")
else:
    print(f"Error: {response.status_code} - {response.text}")
