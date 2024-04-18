import numpy as np
import cv2
import time
import os

prev_gray = None  # Define prev_gray as a global variable
prev_points = None  # Store previous frame points

def draw_lines(img, points1, points2, status):
    """
    Draw lines between the original points and new points after motion, ensuring all points are valid.
    """
    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    if points1 is not None and points2 is not None and status is not None:
        for p1, p2, s in zip(points1, points2, status):
            if s:
                x1, y1 = int(p1[0]), int(p1[1])
                x2, y2 = int(p2[0]), int(p2[1])
                cv2.line(img_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(img_bgr, (x1, y1), 3, (0, 255, 0), -1)
    return img_bgr

def process_frame(frame):
    global prev_gray, prev_points  # Access the global variables
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if prev_gray is not None and prev_points is not None:
        # Calculate optical flow
        next_points, status, _ = cv2.calcOpticalFlowPyrLK(prev_gray, gray, prev_points, None)

        if next_points is not None:
            # Filter out the points with a '1' in status array
            good_new = next_points[status == 1]
            good_old = prev_points[status == 1]

            if good_new.size > 0 and good_old.size > 0:
                # Draw the tracks
                img = draw_lines(gray, good_old, good_new, status[status == 1])
                cv2.imshow('Optical Flow - PyrLK', img)

        # Re-detect points to track if too few remain
        if good_new.size < 50:
            prev_points = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=30)
        else:
            prev_points = good_new.reshape(-1, 1, 2)

    prev_gray = gray  # Update prev_gray for the next frame

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Unable to open video file.")
        return

    frame_count = 0
    skip_frames = 5  # Process every 5th frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Clear the output
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Processing frame: " + str(frame_count))

        if frame_count % skip_frames == 0:
            process_frame(frame)
        
        frame_count += 1

        key = cv2.waitKey(5)
        if key == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()

# Example usage
process_video('dataset/queries/query1.mp4')
