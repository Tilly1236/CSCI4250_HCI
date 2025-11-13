import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class CameraScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget

        self.layout = QVBoxLayout()

        # Title
        self.title = QLabel("Live Camera Feed")
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Camera feed label
        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        # Stop and Back buttons
        self.stop_button = QPushButton("Stop Camera")
        self.stop_button.clicked.connect(self.stop_camera)
        self.layout.addWidget(self.stop_button)

        self.back_button = QPushButton("Back to Menu")
        self.back_button.clicked.connect(lambda: self.stacked_widget.setCurrentIndex(0))
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

        # Timer for updating frames
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Start camera
        self.cap = cv2.VideoCapture(0)
        self.timer.start(30)  # 30 ms per frame (~33 FPS)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(convert_to_Qt_format)
            self.image_label.setPixmap(pixmap.scaled(640, 480, Qt.KeepAspectRatio))

    def stop_camera(self):
        self.timer.stop()
        self.cap.release()
        self.image_label.clear()
