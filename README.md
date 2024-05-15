# Pixellate
#### A search and indexing tool for Video/Audio
Pixellate is a Python-based tool designed to facilitate searching and indexing of video and audio files. It offers functionalities for identifying shot boundaries, extracting image hashes, analyzing audio features, detecting motion, and playing videos with a custom-built player.

### Features
1. Shot Boundary Detection: Identify shot boundaries in a video file to segment it into distinct scenes.
1. Image Hashing: Compute perceptual hashes for frames in a video to enable content-based image retrieval.
1. Audio Analysis: Extract audio features and perform similarity searches to identify matching audio segments.
1. Motion Detection: Analyze motion features in videos to determine similarities between sequences.
1. Custom Video Player: Play video files with playback control options like play, pause, stop, and skip.

### Installation and Execution
To install Pixellate, follow these steps:

1. Clone the repository: ```git clone https://github.com/Reubensuju/Pixellate.git```
1. Navigate to the project directory: cd pixellate
1. Install dependencies: pip install -r requirements.txt
1. Navigate to the directory workflow: cd src/workflow
1. Run ```workflow.ipynb```