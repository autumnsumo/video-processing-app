import cv2
import os

def extract_frames(video_path, output_dir, interval=1):
    """
    Extract frames from a video at specified intervals and save as images.
    
    Args:
        video_path (str): Path to the input video file.
        output_dir (str): Directory to save frame images.
        interval (float): Time interval between frames in seconds (default: 1).
    
    Returns:
        int: Number of frames extracted.
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Failed to open video: {video_path}")
    
    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    if fps == 0:
        cap.release()
        raise ValueError("Invalid FPS in video")
    
    frame_interval = int(fps * interval)  # Number of frames to skip for 'interval' seconds
    frame_count = 0  # Counter for extracted frames
    frame_number = 0  # Frame index in video
    
    # Read frames from the video
    while cap.isOpened():
        ret, frame = cap.read()  # Read the next frame
        if not ret:  # End of video
            break
        
        # Save frame at specified intervals
        if frame_number % frame_interval == 0:
            output_path = os.path.join(output_dir, f"frame_{frame_count:04d}.jpg")
            cv2.imwrite(output_path, frame)  # Save frame as JPEG
            frame_count += 1
        
        frame_number += 1
    
    # Release the video capture object
    cap.release()
    
    return frame_count