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
                if not command:
                    self.finished.emit('', 'Failed to receive a voice command. Please try again.')
                    return
                
                if 'take picture' in command or 'click picture' in command:
                    image_path = self.image_processor.capture_image()
                    if not image_path:
                        self.finished.emit('', 'Failed to capture an image from the webcam.')
                        return
                        
                    image = self.image_processor.process_image(image_path)
                    if not image:
                        self.finished.emit('', f'Failed to process the captured image at {image_path}.')
                        return
                        
                    caption = self.caption_generator.generate_caption(image)
                    if not caption:
                        self.finished.emit('', 'Failed to generate a caption for the image.')
                        return
                        
                    self.speech_processor.speak(caption)
                    self.finished.emit(caption, '')
                else:
                    self.finished.emit('', f'Unrecognized command: "{command}". Please try saying "take picture".')
                    
            elif self.mode == 'upload':
                if not self.file_path:
                    self.finished.emit('', 'No file was selected for upload.')
                    return
                    
                image = self.image_processor.process_image(self.file_path)
                if not image:
                    self.finished.emit('', f'Failed to process the uploaded image at {self.file_path}.')
                    return
                    
                caption = self.caption_generator.generate_caption(image)
                if not caption:
                    self.finished.emit('', 'Failed to generate a caption for the image.')
                    return
                    
                self.speech_processor.speak(caption)
                self.finished.emit(caption, '')
                
            elif self.mode == 'webcam':
                image_path = self.image_processor.capture_image()
                if not image_path:
                    self.finished.emit('', 'Failed to capture an image from the webcam.')
                    return
                    
                image = self.image_processor.process_image(image_path)
                if not image:
                    self.finished.emit('', f'Failed to process the captured image at {image_path}.')
                    return
                    
                caption = self.caption_generator.generate_caption(image)
                if not caption:
                    self.finished.emit('', 'Failed to generate a caption for the image.')
                    return
                    
                self.speech_processor.speak(caption)
                self.finished.emit(caption, '')
                
            else:
                self.finished.emit('', f'Unknown mode: {self.mode}')

        except Exception as e:
            import traceback
            error_msg = f'Exception: {str(e)}\n{traceback.format_exc()}'
            print(f"❌ Error in CaptionWorker: {error_msg}")
            self.finished.emit('', error_msg)

    def __del__(self):
        try:
            if self.isRunning():
                self.quit()
                self.wait()
        except:
            pass
