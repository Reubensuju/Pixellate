import numpy as np
import cv2
import time
import threading
import os

prevgray = None  # Define prevgray as a global variable

def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T

    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)

    img_bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(img_bgr, lines, 0, (0, 255, 0))

    for (x1, y1), (_x2, _y2) in lines:
        cv2.circle(img_bgr, (x1, y1), 1, (0, 255, 0), -1)

    return img_bgr

def draw_hsv(flow):
    h, w = flow.shape[:2]
    fx, fy = flow[:,:,0], flow[:,:,1]

    ang = np.arctan2(fy, fx) + np.pi
    v = np.sqrt(fx*fx+fy*fy)

    hsv = np.zeros((h, w, 3), np.uint8)
    hsv[...,0] = ang*(180/np.pi/2)
    hsv[...,1] = 255
    hsv[...,2] = np.minimum(v*4, 255)
    bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    return bgr

def process_frame(frame):
    global prevgray  # Access the global prevgray variable
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if prevgray is not None:
        flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        cv2.imshow('flow', draw_flow(gray, flow))
        cv2.imshow('flow HSV', draw_hsv(flow))
    prevgray = gray  # Update prevgray for the next frame

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
process_video('dataset/originals/joker.mp4')
