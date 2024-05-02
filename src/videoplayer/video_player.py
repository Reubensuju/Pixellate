import sys
import vlc
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import *

class VideoPlayer(QtWidgets.QMainWindow):
    def __init__(self, master, video_path):
        super().__init__(master)
        self.setWindowTitle("PyQt VLC Video Player")
    
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.central_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout_button = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.frame = QtWidgets.QFrame()
        self.layout.addWidget(self.frame)
        if sys.platform == "win32":
            self.player.set_hwnd(self.frame.winId())

        btn_size = QSize(150, 50)
    


        self.play_button = QtWidgets.QPushButton()
        self.play_button.clicked.connect(self.toggle_play_pause)
        self.play_button.setFixedSize(btn_size)
        pixmap = QPixmap("src/videoplayer/play.png")
        self.play_button.setIcon(QIcon(pixmap))
        self.play_button.setIconSize(btn_size)
        self.layout_button.addWidget(self.play_button)
        
        self.stop_button = QtWidgets.QPushButton()
        self.stop_button.clicked.connect(self.stop_player)
        self.stop_button.setFixedSize(btn_size)
        pixmap = QPixmap("src/videoplayer/stop.png")
        self.stop_button.setIcon(QIcon(pixmap))
        self.stop_button.setIconSize(btn_size)
        self.layout_button.addWidget(self.stop_button)
        
        self.skip_button = QtWidgets.QPushButton()
        self.skip_button.clicked.connect(self.skip_to)
        self.skip_button.setFixedSize(btn_size)
        pixmap = QPixmap("src/videoplayer/fastfwd.png")
        self.skip_button.setIcon(QIcon(pixmap))
        self.skip_button.setIconSize(btn_size)
        self.layout_button.addWidget(self.skip_button)


        self.layout.addLayout(self.layout_button)


        self.media = self.instance.media_new(video_path)
        self.player.set_media(self.media)
    
        self.setGeometry(100, 100, 1400, 900)
        self.show()

    def toggle_play_pause(self):
        btn_size = QSize(150, 50)
        if self.player.is_playing():
            self.player.pause()
            pixmap = QPixmap("src/videoplayer/play.png")
            self.play_button.setIcon(QIcon(pixmap))
            self.play_button.setIconSize(btn_size)
        else:
            self.player.play()
            pixmap = QPixmap("src/videoplayer/pause.png")
            self.play_button.setIcon(QIcon(pixmap))
            self.play_button.setIconSize(btn_size)
    
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
    video_path = 'dataset/originals/video1.mp4' 
    player = VideoPlayer(None, video_path)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
