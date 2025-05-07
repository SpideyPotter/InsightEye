import cv2
import numpy as np
from PIL import Image
import os
from datetime import datetime

class ImageProcessor:
    def __init__(self):
        pass

    def capture_image(self):
        """Capture an image from webcam"""
        print("🎥 Attempting to access webcam...")
        # Try multiple camera indices
        for i in range(3):  # Try cameras 0, 1, and 2
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                print(f"✅ Found camera at index {i}")
                break
        else:
            print('❌ Could not find any webcam')
            return None

        try:
            print("✅ Webcam opened. Capturing frame...")
            # Capture multiple frames to ensure good quality
            for _ in range(5):
                ret, frame = cap.read()
            
            if ret:
                # Ensure images directory exists
                os.makedirs('images', exist_ok=True)
                
                # Add timestamp to filename to avoid overwriting
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join('images', f'captured_image_{timestamp}.jpg')
                
                # Ensure we can write to the file
                try:
                    cv2.imwrite(filename, frame)
                    print(f'📷 Image saved as {filename}')
                    return filename
                except Exception as e:
                    print(f'❌ Error saving image: {str(e)}')
                    return None
            else:
                print('❌ Failed to capture image')
                return None
        finally:
            cap.release()

    def process_image(self, image_path):
        """Process an image for caption generation"""
        # Get absolute path to the images directory
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        images_dir = os.path.join(base_dir, 'images')
        
        # If the path is relative, join it with the images directory
        if not os.path.isabs(image_path):
            image_path = os.path.join(images_dir, os.path.basename(image_path))
        
        # Make sure we have an absolute path
        image_path = os.path.abspath(image_path)
        
        if not os.path.isfile(image_path):
            print(f"❌ Invalid image path: {image_path}")
            return None

        img = cv2.imread(image_path)
        if img is None:
            print("❌ Failed to read image")
            return None

        return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
