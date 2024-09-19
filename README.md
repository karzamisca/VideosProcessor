### NOTE: REMEMBER TO CHANGE FFMPEG PATH TO WHERE YOU INSTALL IT IN YOUR SYSTEM
### Video Processor
### Complie: pyinstaller -D --add-data "path\to\ffmpeg;ffmpeg-7.0.2-full_build" main.py

### Class:
#### 1. `VideoConverterApp(QWidget)`
   - **Purpose**: This is the main PyQt6 application class for the video converter. It provides the user interface (UI) for selecting input/output folders, setting the frame rate, and processing videos. It handles all the logic for converting videos using both FFmpeg and PIL (for `.webp` to `.mp4` conversion).

### Functions/Methods:
#### 1. `__init__(self)`
   - **Purpose**: Initializes the application by calling `get_ffmpeg_path()` to set the FFmpeg path and `initUI()` to set up the user interface.

#### 2. `get_ffmpeg_path(self)`
   - **Purpose**: Determines the path to the FFmpeg executable. If the application is running as a PyInstaller-built executable, it retrieves the path from the bundled resources; otherwise, it assumes the FFmpeg binary is located at `/usr/bin/ffmpeg`.

#### 3. `initUI(self)`
   - **Purpose**: Sets up the graphical user interface (GUI) layout and widgets, including buttons to select input/output folders, set the frame rate, and trigger the video processing.

#### 4. `selectInputFolder(self)`
   - **Purpose**: Opens a folder selection dialog to allow the user to choose an input folder containing the video files for processing. Updates the UI with the selected folder path.

#### 5. `selectOutputFolder(self)`
   - **Purpose**: Opens a folder selection dialog to allow the user to choose an output folder where the processed videos will be saved. Updates the UI with the selected folder path.

#### 6. `processVideos(self)`
   - **Purpose**: This is the main function that orchestrates the video processing. It checks if both input and output folders are selected, retrieves the desired frame rate, and processes the videos in the input folder by converting them to `.mp4`. If a file is a `.webp` animation, it extracts its frames and converts them to video; otherwise, it uses FFmpeg for conversion.

#### 7. `webp_to_frames(self, webp_path, output_folder)`
   - **Purpose**: Extracts frames from an animated `.webp` file and saves them as `.png` images in the specified output folder. This function handles animated images frame by frame using the PIL library.

#### 8. `frames_to_video(self, frames_folder, output_video_path, frame_rate)`
   - **Purpose**: Converts a series of `.png` frames (from a folder) into an `.mp4` video file using OpenCV. The output video uses the specified frame rate, and the resolution is based on the dimensions of the first frame.

#### 9. `convert_with_ffmpeg(self, input_path, output_path)`
   - **Purpose**: Converts video files (other than `.webp`) to `.mp4` using FFmpeg. This method runs an FFmpeg command with various encoding settings such as codec (`libx264`), quality control (`crf`), and encoding speed (`preset`). It relies on the external FFmpeg binary to perform the conversion.

