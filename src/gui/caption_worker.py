import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from PyQt5.QtCore import QThread, pyqtSignal
from src.core.image_processor import ImageProcessor
from src.core.speech_processor import SpeechProcessor
from src.core.caption_generator import CaptionGenerator

class CaptionWorker(QThread):
    finished = pyqtSignal(str, str)  # output, error

    def __init__(self, mode, file_path=None):
        super().__init__()
        self.mode = mode
        self.file_path = file_path
        self.image_processor = ImageProcessor()
        self.speech_processor = SpeechProcessor()
        self.caption_generator = CaptionGenerator()

    def run(self):
        try:
            if self.mode == 'voice':
                command = self.speech_processor.listen_for_command()
                if command and ('take picture' in command or 'click picture' in command):
                    image_path = self.image_processor.capture_image()
                    if image_path:
                        image = self.image_processor.process_image(image_path)
                        caption = self.caption_generator.generate_caption(image)
                        if caption:
                            self.speech_processor.speak(caption)
                            self.finished.emit(caption, '')
            elif self.mode == 'upload':
                if self.file_path:
                    image = self.image_processor.process_image(self.file_path)
                    caption = self.caption_generator.generate_caption(image)
                    if caption:
                        self.speech_processor.speak(caption)
                        self.finished.emit(caption, '')
            elif self.mode == 'webcam':
                image_path = self.image_processor.capture_image()
                if image_path:
                    image = self.image_processor.process_image(image_path)
                    caption = self.caption_generator.generate_caption(image)
                    if caption:
                        self.speech_processor.speak(caption)
                        self.finished.emit(caption, '')

        except Exception as e:
            self.finished.emit('', f'Exception: {str(e)}')

    def __del__(self):
        try:
            if self.isRunning():
                self.quit()
                self.wait()
        except:
            pass
