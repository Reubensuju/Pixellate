from moviepy.editor import VideoFileClip
import librosa
import numpy as np
from datetime import timedelta, datetime
import cv2

def extract_audio(video_file_path, output_audio_path):
    video = VideoFileClip(video_file_path)

    audio = video.audio

    audio.write_audiofile(output_audio_path, codec='pcm_s16le')

    video.close()
    audio.close()

def find_best_match(input_features, query_features):
    best_match = {'score': np.inf, 'index': 0}
    num_frames = input_features.shape[1] - query_features.shape[1] + 1

    for i in range(num_frames):
        current_window = input_features[:, i:i + query_features.shape[1]]
        distance = np.linalg.norm(query_features - current_window)

        if distance < best_match['score']:
            best_match['score'] = distance
            best_match['index'] = i

    return best_match['index'], best_match['score']

# Function to convert seconds into hh:mm:ss.sss format
def seconds_to_timestamp(seconds):
    td = timedelta(seconds=seconds)
    str_time = str(td)
    hours, minutes, seconds = str_time.split(':')
    seconds, microseconds = seconds.split('.')
    milliseconds = f"{int(microseconds):03d}"[:3]
    return f"{hours}:{minutes}:{seconds}.{milliseconds}"

# functions to convert the timestamp into frame number in the original video
def get_fps(video_path):
    video = cv2.VideoCapture(video_path)
    fps = video.get(cv2.CAP_PROP_FPS)
    video.release()
    return fps

def parse_timecode(time_str):
    return datetime.strptime(time_str, "%H:%M:%S.%f")

def timecode_to_frames(timecode, fps):
    time_obj = parse_timecode(timecode)
    total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second + time_obj.microsecond / 1e6
    frame_number = int(round(total_seconds * fps))
    return frame_number

original_video_path = 'dataset/originals/joker.mp4'
query_video_path = 'dataset/queries/joker_query.mp4'
extract_audio(original_video_path, 'output_original_audio.wav')
extract_audio(query_video_path, 'output_query_audio.wav')

original_audio, original_sampling_rate = librosa.load('output_original_audio.wav')
query_audio, query_sampling_rate = librosa.load('output_query_audio.wav')

input_mfcc = librosa.feature.mfcc(y=original_audio, sr=original_sampling_rate, n_mfcc=13)
query_mfcc = librosa.feature.mfcc(y=query_audio, sr=original_sampling_rate, n_mfcc=13)

start_index, similarity_score = find_best_match(input_mfcc, query_mfcc)

HOP_LENGTH = 512
fps = get_fps(original_video_path)

start_time_seconds = start_index * HOP_LENGTH / original_sampling_rate
query_duration_seconds = len(query_audio) / original_sampling_rate
end_time_seconds = start_time_seconds + query_duration_seconds

start_time = seconds_to_timestamp(start_time_seconds)
end_time = seconds_to_timestamp(end_time_seconds)
start_frame = timecode_to_frames(start_time, fps)
end_frame = timecode_to_frames(end_time, fps)

print(f"Start Time: {start_time} seconds")
print(f"End Time: {end_time} seconds")
print(f"Start Frame: {start_frame}")
print(f"End Frame: {end_frame}")


