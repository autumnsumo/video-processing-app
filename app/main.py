from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import os
import aiofiles
from app.video_processor import extract_frames
from app.feature_extractor import process_frames, compute_color_histogram
from app.vector_db import initialize_qdrant_collection, store_feature_vectors, search_similar_frames

app = FastAPI()

# Define directories
UPLOAD_DIR = "uploads"
FRAME_DIR = "frames"
STATIC_DIR = "frontend"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(FRAME_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (update for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_index():
    """
    Serve the React UI.
    """
    index_path = os.path.join(STATIC_DIR, "index.html")
    if not os.path.exists(index_path):
        raise HTTPException(status_code=404, detail="UI not found")
    return FileResponse(index_path)

@app.post("/upload-video/")
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video, extract frames, compute feature vectors, and store in Qdrant.
    """
    # Validate file type
    if not file.filename.lower().endswith('.mp4'):
        raise HTTPException(status_code=400, detail="Only MP4 files are supported")
    
    try:
        # Save video
        video_path = os.path.join(UPLOAD_DIR, file.filename)
        async with aiofiles.open(video_path, "wb") as f:
            await f.write(await file.read())
        
        # Extract frames
        frame_dir = os.path.join(FRAME_DIR, file.filename.replace('.mp4', '_frames'))
        num_frames = extract_frames(video_path, frame_dir, interval=1)
        if num_frames == 0:
            raise HTTPException(status_code=500, detail="No frames extracted from video")
        
        # Compute and store feature vectors
        feature_vectors = process_frames(frame_dir)
        collection_name = "frames"
        initialize_qdrant_collection(collection_name, vector_size=192)
        store_feature_vectors(collection_name, feature_vectors)
        
        return {
            "filename": file.filename,
            "num_frames": num_frames,
            "status": "processed"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing video: {str(e)}")

class SearchRequest(BaseModel):
    vector: List[float]
    limit: int = 5

@app.post("/search-frames/")
async def search_frames(request: SearchRequest):
    """
    Search for frames similar to the given feature vector.
    """
    try:
        # Validate vector size
        if len(request.vector) != 192:
            raise HTTPException(status_code=400, detail="Feature vector must have 192 dimensions")
        
        # Search Qdrant
        collection_name = "frames"
        results = search_similar_frames(collection_name, request.vector, request.limit)
        
        return {"results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching frames: {str(e)}")

@app.get("/frame-image/{frame_id}")
async def get_frame_image(frame_id: int):
    """
    Serve a frame image by its ID.
    """
    try:
        # Construct image path (assumes frame_XXXX.jpg naming)
        frame_path = None
        for root, _, files in os.walk(FRAME_DIR):
            for file in files:
                if file == f"frame_{frame_id:04d}.jpg":
                    frame_path = os.path.join(root, file)
                    break
            if frame_path:
                break
        
        if not frame_path or not os.path.exists(frame_path):
            raise HTTPException(status_code=404, detail="Frame not found")
        
        return FileResponse(frame_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving frame: {str(e)}")

@app.get("/compute-vector/{frame_id}")
async def compute_vector(frame_id: int):
    """
    Compute the feature vector for a given frame ID.
    """
    try:
        # Construct image path (assumes frame_XXXX.jpg naming)
        frame_path = None
        for root, _, files in os.walk(FRAME_DIR):
            for file in files:
                if file == f"frame_{frame_id:04d}.jpg":
                    frame_path = os.path.join(root, file)
                    break
            if frame_path:
                break
        
        if not frame_path or not os.path.exists(frame_path):
            raise HTTPException(status_code=404, detail="Frame not found")
        
        # Compute feature vector using the same method as in feature_extractor.py
        vector = compute_color_histogram(frame_path)
        return {"vector": vector.tolist()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error computing vector: {str(e)}")
