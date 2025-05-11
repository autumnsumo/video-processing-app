import cv2
import numpy as np
import os

def compute_color_histogram(image_path):
    """
    Compute a 192-dimensional color histogram for an image (64 bins per RGB channel).
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Could not load image at {image_path}")
    
    # Convert to RGB (OpenCV loads as BGR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Compute histograms for each channel
    bins = 64
    hist_r = cv2.calcHist([img], [0], None, [bins], [0, 256]).flatten()
    hist_g = cv2.calcHist([img], [1], None, [bins], [0, 256]).flatten()
    hist_b = cv2.calcHist([img], [2], None, [bins], [0, 256]).flatten()
    
    # Concatenate histograms
    hist = np.concatenate([hist_r, hist_g, hist_b])
    
    # Normalize the histogram
    total = hist.sum()
    if total > 0:
        hist = hist / total
    
    return hist

def process_frames(frame_dir):
    """
    Process all frames in a directory and compute their feature vectors.
    """
    feature_vectors = []
    for filename in sorted(os.listdir(frame_dir)):
        if filename.endswith('.jpg'):
            frame_path = os.path.join(frame_dir, filename)
            frame_id = int(filename.split('_')[1].split('.')[0])  # e.g., frame_0001.jpg -> 1
            try:
                vector = compute_color_histogram(frame_path)
                feature_vectors.append({
                    "frame_id": frame_id,
                    "image_path": frame_path,
                    "feature_vector": vector.tolist()
                })
            except Exception as e:
                print(f"Error processing {frame_path}: {str(e)}")
    return feature_vectors
