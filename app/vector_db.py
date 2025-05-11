from qdrant_client import QdrantClient
from qdrant_client.http import models

def initialize_qdrant_collection(collection_name, vector_size):
    """
    Initialize a Qdrant collection for storing feature vectors.
    """
    client = QdrantClient("localhost", port=6333)
    
    # Check if collection exists, if not create it
    try:
        client.get_collection(collection_name)
    except:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE
            )
        )

def store_feature_vectors(collection_name, feature_vectors):
    """
    Store feature vectors in Qdrant.
    """
    client = QdrantClient("localhost", port=6333)
    
    points = [
        models.PointStruct(
            id=vector["frame_id"],
            vector=vector["feature_vector"],
            payload={
                "image_path": vector["image_path"],
                "frame_id": vector["frame_id"]
            }
        )
        for vector in feature_vectors
    ]
    
    client.upsert(
        collection_name=collection_name,
        points=points
    )
    
    # Force indexing by optimizing the collection
    client.optimize_collection(collection_name)

def search_similar_frames(collection_name, query_vector, limit=5):
    """
    Search for similar frames in Qdrant.
    """
    client = QdrantClient("localhost", port=6333)
    
    search_result = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=limit,
        with_payload=True,
        with_vectors=False
    )
    
    results = [
        {
            "frame_id": hit.payload["frame_id"],
            "image_path": hit.payload["image_path"],
            "score": hit.score
        }
        for hit in search_result
    ]
    
    return results
