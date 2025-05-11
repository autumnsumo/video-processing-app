
# 🎥 Video Processing API

A **FastAPI** application for uploading videos, extracting frames, computing color histogram features, and retrieving similar frames using **Qdrant** for vector search.

---

## 🚀 Features

- **📤 Upload Videos:** Upload `.mp4` files.
- **🖼 Frame Extraction:** Extract JPEG frames every second.
- **📊 Feature Vectors:** Compute 192-dimensional color histograms per frame.
- **🔍 Similarity Search:** Search frames using vector similarity.
- **🖼 Frame Retrieval:** Retrieve individual frame images by ID.

---

## ⚙️ Requirements

- Python 3.12  
- Conda (Miniconda/Anaconda)  
- Docker (for running Qdrant)  
- Git  

---

## 🛠 Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd video-processing-app
```

### 2. Create and Activate Conda Environment

```bash
conda create -n video-app python=3.12
conda activate video-app
```

### 3. Install Dependencies

```bash
conda install -c conda-forge opencv
pip install fastapi uvicorn python-multipart qdrant-client numpy
```

### 4. Start Qdrant with Docker

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

> 💡 Use `-d` to run Qdrant in detached mode: `docker run -d ...`

### 5. Run the FastAPI Server

Open a **new terminal** and activate your environment:

```bash
conda activate video-app
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 🌐 Access the API

Open in your browser: [http://localhost:8000/docs](http://localhost:8000/docs)

Explore interactive API docs using **Swagger UI**.

---

## 📡 API Endpoints

### 🔹 `POST /upload-video/`

- **Input:** MP4 video file  
- **Output:**
  ```json
  {
    "filename": "sample.mp4",
    "num_frames": 120,
    "status": "processed"
  }
  ```

### 🔹 `POST /search-frames/`

- **Input:** JSON with a 192-dim vector and optional `limit`
- **Output:**
  ```json
  {
    "results": [
      {
        "frame_id": 12,
        "image_path": "frames/sample_frames/frame_0012.jpg",
        "feature_vector": [...],
        "score": 0.987
      },
      ...
    ]
  }
  ```

### 🔹 `GET /frame-image/{frame_id}`

- **Input:** Frame ID (e.g., `1`)
- **Output:** JPEG image (e.g., `frame_0001.jpg`)

---

## 🧪 Example Usage

### Upload a Video

```bash
curl -X POST -F "file=@sample.mp4" http://localhost:8000/upload-video/
```

### Search for Similar Frames

```bash
curl -X POST -H "Content-Type: application/json"   -d '{"vector": [0.0052, ..., 0.0048], "limit": 5}'   http://localhost:8000/search-frames/
```

### Retrieve a Frame Image

```bash
curl http://localhost:8000/frame-image/1 --output frame_0001.jpg
```

---

## 📌 Assumptions

- Videos must be in `.mp4` format.
- Frames are named as `frame_XXXX.jpg`.
- Qdrant must be running on `localhost:6333`.
- Feature vectors use color histograms with **64 bins per RGB channel**.

---

## ⚠️ Limitations

- Color histograms do **not** capture objects or textures.
- Large videos may take time to process.
- Requires Qdrant to be running **before** starting the app.

---

## 📁 Project Structure (Simplified)

```
video-processing-app/
├── app/
│   ├── main.py               # FastAPI app
│   ├── video_processor.py    # Frame extraction logic
│   ├── feature_extractor.py  # Vector generation
│   └── vector_db.py          # Qdrant interaction
├── uploads/                  # Uploaded videos
├── frames/                   # Extracted frame images
└── frontend/                 # Static UI files (optional)
```

---

## 🧠 Inspired By

- Content-based image retrieval
- Vector databases (Qdrant)
- Simple color-based similarity search

---

## 📬 Contributions & Feedback

PRs and issues are welcome! Open to improvements like:
- Deep learning-based feature extraction (CNNs)
- Batch uploads
- UI dashboard
