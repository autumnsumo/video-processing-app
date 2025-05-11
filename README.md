Video Processing API
This is a FastAPI application for processing videos, computing feature vectors, and retrieving similar frames, built for the internship assignment.
Features

Video Processing: Upload an MP4 video, extract frames every second, and save as JPEG images.
Feature Vectors: Compute 192-dimensional color histograms for each frame.
Vector Storage: Store feature vectors in Qdrant for similarity search.
Retrieval: Query for frames similar to a given feature vector and retrieve images.

Requirements

Python 3.12
Conda (Miniconda/Anaconda)
Docker (for Qdrant)
Git

Setup Instructions

Clone the Repository:
git clone <repository-url>
cd video-processing-app


Create and Activate Conda Environment:
conda create -n video-app python=3.12
conda activate video-app


Install Dependencies:
conda install -c conda-forge opencv
pip install fastapi uvicorn python-multipart qdrant-client numpy


Install and Run Qdrant:

Install Docker Desktop (Windows/macOS) or Docker (Linux).
Run Qdrant:docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant


Keep the terminal open or run in detached mode (-d flag).


Run the FastAPI Application:In a new terminal (with video-app activated):
uvicorn app.main:app --host 0.0.0.0 --port 8000


Access the API:

Open a browser to http://localhost:8000/docs for the Swagger UI.
Test endpoints:
POST /upload-video/: Upload an MP4 file.
POST /search-frames/: Search with a 192-dimensional vector.
GET /frame-image/{frame_id}: Retrieve a frame image.





API Endpoints

POST /upload-video/:
Input: MP4 file.
Output: JSON with filename, number of frames, and status.


POST /search-frames/:
Input: JSON with vector (list of 192 floats) and optional limit (default 5).
Output: JSON with list of matching frames (frame_id, image_path, feature_vector, score).


GET /frame-image/{frame_id}:
Input: Frame ID (integer).
Output: JPEG image file.



Example Usage

Upload a video:curl -X POST -F "file=@sample.mp4" http://localhost:8000/upload-video/


Search for similar frames (example vector):curl -X POST -H "Content-Type: application/json" -d '{"vector": [0.0052, ..., 0.0048], "limit": 5}' http://localhost:8000/search-frames/


Get a frame image:curl http://localhost:8000/frame-image/1 --output frame_0001.jpg



Assumptions

Videos are in MP4 format.
Frames are saved as frame_XXXX.jpg.
Qdrant runs locally on port 6333.
Feature vectors are 192-dimensional (64 bins per RGB channel).

Limitations

Color histograms may not capture complex patterns (e.g., objects, textures).
Large videos may slow down processing.
Qdrant must be running before starting the app.

Notes

Ensure the Git repository link is accessible (public or shared with reviewers).
Test all endpoints with sample videos before submission.
Deadline: Monday, May 12, 2025, 12 noon IST.

