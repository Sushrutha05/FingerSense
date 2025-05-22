# FingerSense

FingerSense is a real-time webcam filter that detects when the middle finger is shown and automatically applies a Gaussian blur to censor it. It leverages OpenCV and MediaPipe for accurate hand tracking, combined with a gesture history voting system to reduce flicker and ensure smooth, reliable detection.

## Features

- Real-time middle finger detection using MediaPipe hand tracking  
- Automatic Gaussian blur applied to censor the middle finger gesture  
- Gesture history voting system to stabilize detection and minimize flicker  
- Handles hand disappearance gracefully to prevent crashes  

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/FingerSense.git
    cd FingerSense
    ````

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the webcam filter:

  ```bash
python finger_sense.py
  ```

Show your middle finger to see it blurred in real-time!

## Requirements

* Python 3.7+
* OpenCV (opencv-python==4.10.0.82)
* MediaPipe (mediapipe==0.10.21)
