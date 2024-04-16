import numpy as np
import librosa
import librosa.display
from scipy.signal import correlate
from fastdtw import fastdtw
import matplotlib.pyplot as plt
from moviepy.editor import VideoFileClip

def extract_audio_from_video(video_path, audio_format='wav'):
    """
    Extracts the audio from a video file and saves it as a temporary WAV file.
    """
    video = VideoFileClip(video_path)
    audio_path = "temp_audio." + audio_format
    video.audio.write_audiofile(audio_path, codec='pcm_s16le')  # codec for 16-bit PCM
    return audio_path

def plot_mfccs(audio_path):
    # Load audio file with librosa; default sample rate is 22050 Hz
    y, sr = librosa.load(audio_path)
    
    # Compute the MFCCs for the audio signal; default is 20 MFCCs
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    # mfccs = mfccs[:5]
    
    # Plotting the MFCCs
    # plt.figure(figsize=(10, 4))
    # librosa.display.specshow(mfccs, x_axis='time', sr=sr)
    # plt.colorbar()
    # plt.title('MFCC')
    # plt.tight_layout()
    # plt.show()

    return mfccs

def find_matching_index(large_array, small_array):
    # Check if the dimensions match correctly
    if small_array.shape[0] != large_array.shape[0]:
        raise ValueError("The first dimension of small_array must match the first dimension of large_array.")
    
    # Vectorized comparison of the small_array with every column in large_array
    matches = np.all(large_array == small_array[:, np.newaxis], axis=0)

    # Find the first index where all elements match
    matching_indices = np.where(matches)[0]
    
    if matching_indices.size > 0:
        return matching_indices[0]
    else:
        return -1  # Return -1 if no match is found

# Example usage - Replace 'path_to_your_audio_file.wav' with the actual audio file path
# audio_path = extract_audio_from_video('dataset/queries/joker_query.mp4')
mfcc_output_orig = plot_mfccs('joker.wav')
mfcc_output_query = plot_mfccs('joker_query.wav')
print("Shape of MFCC output orig:", mfcc_output_orig.shape)
print("Shape of MFCC output query:", mfcc_output_query[:, 2].shape)
# print(mfcc_output[0])

start_index = find_matching_index(mfcc_output_orig, mfcc_output_query[:, 1])
print("Start sample index in original audio:", start_index)