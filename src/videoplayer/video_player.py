import sys
import vlc
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import *

class VideoPlayer(QtWidgets.QMainWindow):
    def __init__(self, master, video_path):
        super().__init__(master)
        self.setWindowTitle("PyQt VLC Video Player")
        
        # Create a VLC player instance
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        # Create a new QWidget for the window central widget
        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Create a QVBoxLayout for the QWidget layout
        self.layout = QtWidgets.QVBoxLayout()
        self.layout_button = QtWidgets.QHBoxLayout()

       

        self.central_widget.setLayout(self.layout)
       

        # Create a frame and assign the VLC player to this frame
        self.frame = QtWidgets.QFrame()
        self.layout.addWidget(self.frame)
        if sys.platform == "win32":
            self.player.set_hwnd(self.frame.winId())

        btn_size = QSize(150, 50)
        # Add Play/Pause, Stop, and Skip buttons
        self.play_button = QtWidgets.QPushButton("Play/Pause")
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.play_button.setStyleSheet("background-color: green; font-size: 20px;")
        self.play_button.setFixedSize(btn_size)
        self.layout_button.addWidget(self.play_button)
        
        self.stop_button = QtWidgets.QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop_player)
        self.stop_button.setStyleSheet("background-color: red; font-size: 20px")
        self.stop_button.setFixedSize(btn_size)
        self.layout_button.addWidget(self.stop_button)
        
        self.skip_button = QtWidgets.QPushButton("Skip")
        self.skip_button.clicked.connect(self.skip_to)
        self.skip_button.setStyleSheet("background-color: yellow; font-size: 20px")
        self.skip_button.setFixedSize(btn_size)
        self.layout_button.addWidget(self.skip_button)

        self.layout.addLayout(self.layout_button)

        # Load the video file
        self.media = self.instance.media_new(video_path)
        self.player.set_media(self.media)
        
        # Adjust the window size and show the player
        self.setGeometry(100, 100, 1400, 900)
        self.show()

    def toggle_play_pause(self):
        if self.player.is_playing():
            self.player.pause()
        else:
            self.player.play()
    
    def stop_player(self):
        self.player.stop()
    
    def skip_to(self):
        fps = self.player.get_fps()

        frame_number, okPressed = QtWidgets.QInputDialog.getInt(self, "Skip to frame","Frame number:", 0, 0, 100000, 1)
        
        if okPressed:
            ms_time = (frame_number / fps) * 1000
            self.player.set_time(int(ms_time))

def main():
    app = QtWidgets.QApplication(sys.argv)
    video_path = 'dataset/originals/spiderman.mp4'  # Replace with your video file path
    player = VideoPlayer(None, video_path)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
