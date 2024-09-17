import sys
import os
import tempfile
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QMessageBox, QSpinBox
)
from PIL import Image
import cv2
import shutil

class VideoConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.ffmpeg_path = self.get_ffmpeg_path()  # Get the bundled FFmpeg path
        self.initUI()
    #Path to ffmpeg, change it as needed
    def get_ffmpeg_path(self):
        """Find the path to the FFmpeg executable in the bundled application."""
        if getattr(sys, 'frozen', False):
            # If we're inside the PyInstaller executable
            base_path = sys._MEIPASS  # Temporary path where PyInstaller bundles data
            ffmpeg_path = os.path.join(base_path, 'ffmpeg-7.0.2-full_build','bin' ,'ffmpeg.exe')
        else:
            # Running in a normal Python environment
            ffmpeg_path = os.path.abspath('/usr/bin/ffmpeg')

        return ffmpeg_path

    def initUI(self):
        layout = QVBoxLayout()
        # Widgets
        self.inputLabel = QLabel("Input folder: None")
        self.outputLabel = QLabel("Output folder: None")
        self.selectInputButton = QPushButton("Select Input Folder")
        self.selectOutputButton = QPushButton("Select Output Folder")
        self.processButton = QPushButton("Process Videos")
        self.frameRateLabel = QLabel("Frame rate:")
        self.frameRateSpinBox = QSpinBox()
        self.frameRateSpinBox.setRange(1, 120)
        self.frameRateSpinBox.setValue(30)

        # Layout setup
        layout.addWidget(self.inputLabel)
        layout.addWidget(self.selectInputButton)
        layout.addWidget(self.outputLabel)
        layout.addWidget(self.selectOutputButton)
        layout.addWidget(self.frameRateLabel)
        layout.addWidget(self.frameRateSpinBox)
        layout.addWidget(self.processButton)

        self.selectInputButton.clicked.connect(self.selectInputFolder)
        self.selectOutputButton.clicked.connect(self.selectOutputFolder)
        self.processButton.clicked.connect(self.processVideos)

        self.setLayout(layout)
        self.setWindowTitle('Video Converter')
        self.resize(400, 250)
        self.show()

    def selectInputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Input Folder")
        if folder:
            self.inputFolder = folder
            self.inputLabel.setText(f"Input folder: {folder}")

    def selectOutputFolder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.outputFolder = folder
            self.outputLabel.setText(f"Output folder: {folder}")

    def processVideos(self):
        if not hasattr(self, 'inputFolder') or not hasattr(self, 'outputFolder'):
            QMessageBox.warning(self, "Warning", "Please select both input and output folders.")
            return

        frame_rate = self.frameRateSpinBox.value()
        
        with tempfile.TemporaryDirectory() as temp_dir:
            video_files = [f for f in os.listdir(self.inputFolder) if f.endswith(('.webp', '.mp4', '.avi', '.mov', '.mkv'))]
            if not video_files:
                QMessageBox.warning(self, "Warning", "No supported video files found in the input folder.")
                return
            
            for video_file in video_files:
                video_path = os.path.join(self.inputFolder, video_file)
                output_video_path = os.path.join(self.outputFolder, os.path.splitext(video_file)[0] + '.mp4')
                
                if video_file.endswith('.webp'):
                    self.webp_to_frames(video_path, temp_dir)
                    self.frames_to_video(temp_dir, output_video_path, frame_rate)
                else:
                    self.convert_with_ffmpeg(video_path, output_video_path)
        
        QMessageBox.information(self, "Success", "Processing completed.")

    def webp_to_frames(self, webp_path, output_folder):
        with Image.open(webp_path) as img:
            if getattr(img, "is_animated", False):
                for frame_number in range(img.n_frames):
                    img.seek(frame_number)
                    frame = img.copy()
                    frame.save(f"{output_folder}/frame_{frame_number:03d}.png", "PNG")

    def frames_to_video(self, frames_folder, output_video_path, frame_rate):
        frame_files = sorted([f for f in os.listdir(frames_folder) if f.endswith('.png')])
        if not frame_files:
            return
        first_frame = cv2.imread(os.path.join(frames_folder, frame_files[0]))
        height, width, _ = first_frame.shape
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        video_writer = cv2.VideoWriter(output_video_path, fourcc, frame_rate, (width, height))
        for frame_file in frame_files:
            frame_path = os.path.join(frames_folder, frame_file)
            frame = cv2.imread(frame_path)
            video_writer.write(frame)
        video_writer.release()

    def convert_with_ffmpeg(self, input_path, output_path):
        command = [
            self.ffmpeg_path,
            '-i', input_path,
            '-vf', 'fps=30',
            '-c:v', 'libx264',
            '-crf', '23',
            '-preset', 'medium',
            output_path
        ]
        subprocess.run(command, check=True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = VideoConverterApp()
    sys.exit(app.exec())
