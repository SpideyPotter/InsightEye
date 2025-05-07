# InsightEye

An intelligent image captioning application that combines computer vision and natural language processing to generate descriptive captions for images. InsightEye offers a user-friendly interface with multiple input methods.

## Features

- 🎤 Voice Command Recognition
  - Capture images using voice commands ("take picture" or "click picture")
  - Real-time speech-to-text conversion
  - Voice feedback for generated captions

- 📸 Webcam Integration
  - Direct webcam capture
  - Automatic image processing
  - Timestamp-based image management

- 📁 Image Upload
  - Support for local image files
  - Automatic image processing
  - Preview in the application

- 🤖 AI-Powered Caption Generation
  - State-of-the-art image captioning model
  - Natural language descriptions
  - Text-to-speech capability

- 📱 User Interface
  - Modern PyQt5-based GUI
  - Real-time status updates
  - Loading indicators
  - Error handling and notifications

## Project Structure

```
InsightEye/
├── models/                  # Pre-trained model files
├── src/
│   ├── core/              # Core functionality
│   │   ├── image_processor.py
│   │   ├── speech_processor.py
│   │   └── caption_generator.py
│   ├── gui/               # GUI components
│   │   ├── caption_app.py
│   │   └── caption_worker.py
│   └── main.py            # Application entry point
├── requirements.txt        # Project dependencies
├── .gitignore             # Git ignore file
└── README.md              # Project documentation
```

## Installation

1. Clone the repository
2. Create a virtual environment (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Place the pre-trained model files (`processor.pkl` and `model.pkl`) in the `models` directory
```

3. Place the pre-trained model files (`processor.pkl` and `model.pkl`) in the `models` directory

## Running the Application

```bash
python src/main.py
```

## Features

- Voice command recognition
- Webcam image capture
- Image upload
- Image caption generation
- Text-to-speech output
- PyQt5-based GUI interface
- Error handling and logging
- Thread-safe operation
