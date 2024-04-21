import cv2
import numpy as np
from datetime import timedelta

def extract_color_histograms(video_path, bins=(8, 8, 8)):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    histograms = []

    fps = video.get(cv2.CAP_PROP_FPS)  # Frames per second
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))  # Total number of frames in the video
    
    while True:
        ret, frame = video.read()
        if not ret:
            break
        
        # Convert the frame to HSV color space (more robust than RGB)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Calculate the histogram and normalize it
        hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        histograms.append(hist.flatten())
    
    video.release()
    return np.array(histograms), fps, total_frames

def find_best_match(input_histograms, query_histograms):
    max_corr = 0
    best_frame = -1
    
    for i in range(len(input_histograms) - len(query_histograms) + 1):
        corr = sum([cv2.compareHist(input_histograms[i+j], query_histograms[j], cv2.HISTCMP_CORREL)
                    for j in range(len(query_histograms))])
        
        if corr > max_corr:
            max_corr = corr
            best_frame = i
    return best_frame

def frame_to_timestamp(frame_number, fps):
    total_seconds = frame_number / fps
    td = timedelta(seconds=total_seconds)
    hours, remainder = divmod(td.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int(td.microseconds / 1000)
    formatted_timestamp = f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    return formatted_timestamp

# Paths to your video files
input_video_path = 'dataset/originals/joker_3.mp4'
query_video_path = 'dataset/queries/joker_query.mp4'

# Extract color histograms
input_histograms, input_fps, input_total_frames = extract_color_histograms(input_video_path)
print(input_total_frames)
query_histograms, query_fps, query_total_frames = extract_color_histograms(query_video_path)
print(query_total_frames)

# Find the best match
starting_frame = find_best_match(input_histograms, query_histograms)
starting_timestamp = frame_to_timestamp(starting_frame, input_fps)

ending_frame = starting_frame + query_total_frames - 1  # -1 because we start counting from starting_frame
ending_timestamp = frame_to_timestamp(ending_frame, input_fps)

print(f"Start Time: {starting_timestamp}")
print(f"End Time: {ending_timestamp}")
print(f"Start Frame: {starting_frame}")
print(f"End Frame: {ending_frame}")