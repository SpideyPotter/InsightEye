import sys
import os
import traceback
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QLabel, QFileDialog, QTextEdit, QHBoxLayout,
    QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSlot
from .caption_worker import CaptionWorker

class CaptionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('InsightEye - Intelligent Image Captioning')
        self.setGeometry(100, 100, 700, 500)
        self.layout = QVBoxLayout()
        
        # Global exception handler to prevent app from crashing
        sys.excepthook = self.excepthook

        # Status bar at the top
        self.status_bar = QLabel()
        self.status_bar.setStyleSheet("color: #666; font-size: 12px;")
        self.layout.addWidget(self.status_bar)

        self.info_label = QLabel('Choose an option:')
        self.layout.addWidget(self.info_label)

        btn_layout = QHBoxLayout()
        self.voice_btn = QPushButton('Voice Command')
        self.voice_btn.clicked.connect(self.handle_voice)
        btn_layout.addWidget(self.voice_btn)

        self.upload_btn = QPushButton('Upload Image')
        self.upload_btn.clicked.connect(self.handle_upload)
        btn_layout.addWidget(self.upload_btn)

        self.webcam_btn = QPushButton('Take Picture (Webcam)')
        self.webcam_btn.clicked.connect(self.handle_webcam)
        btn_layout.addWidget(self.webcam_btn)

        self.layout.addLayout(btn_layout)

        # Loading indicator
        self.loading_label = QLabel()
        self.loading_label.hide()
        self.layout.addWidget(self.loading_label)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.image_label)

        self.caption_box = QTextEdit()
        self.caption_box.setReadOnly(True)
        self.layout.addWidget(self.caption_box)

        self.setLayout(self.layout)
        self.worker = None

    def show_loading(self, show=True):
        """Show or hide the loading indicator"""
        if show:
            self.loading_label.setText("Processing... Please wait")
            self.loading_label.show()
            self.voice_btn.setEnabled(False)
            self.upload_btn.setEnabled(False)
            self.webcam_btn.setEnabled(False)
        else:
            self.loading_label.hide()
            self.voice_btn.setEnabled(True)
            self.upload_btn.setEnabled(True)
            self.webcam_btn.setEnabled(True)

    def handle_voice(self):
        self.info_label.setText('Listening for voice command...')
        self.caption_box.setText('')
        self.start_worker('voice')

    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', 'images', 'Images (*.png *.jpg *.jpeg *.bmp)')
        if file_path:
            self.image_label.setPixmap(QPixmap(file_path).scaled(300, 300, Qt.KeepAspectRatio))
            self.info_label.setText('Generating caption for uploaded image...')
            self.caption_box.setText('')
            self.start_worker('upload', file_path)

    def handle_webcam(self):
        self.info_label.setText('Capturing image from webcam...')
        self.caption_box.setText('')
        self.start_worker('webcam')

    def start_worker(self, mode, file_path=None):
        # Clean up any existing worker
        try:
            if self.worker:
                if self.worker.isRunning():
                    try:
                        self.worker.finished.disconnect()
                    except Exception:
                        pass
                    self.worker.quit()
                    self.worker.wait(1000)  # Wait with timeout to avoid hanging
                try:
                    self.worker.deleteLater()
                except Exception:
                    pass
                self.worker = None
        except Exception as e:
            print(f"Error cleaning up worker: {str(e)}")
            self.worker = None

        # Show loading indicator
        self.show_loading(True)
        
        try:
            # Create and start the worker
            self.worker = CaptionWorker(mode, file_path)
            self.worker.finished.connect(self.on_worker_finished)
            self.worker.start()
        except Exception as e:
            self.show_loading(False)
            error_msg = f"Failed to start worker: {str(e)}"
            print(error_msg)
            self.status_bar.setText(error_msg)
            QMessageBox.critical(self, "Error", error_msg)

    def on_worker_finished(self, output, error):
        self.show_loading(False)
        
        # Check if we still have a valid worker reference
        if not self.worker:
            return
            
        worker_mode = self.worker.mode
        
        if worker_mode == 'webcam':
            # Get the absolute path to the images directory
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            images_dir = os.path.join(base_dir, 'images')
            
            # Ensure the directory exists
            if os.path.exists(images_dir):
                # Get the latest captured image filename
                try:
                    files = [f for f in os.listdir(images_dir) if f.startswith('captured_image_')]
                    if files:
                        latest_file = max(files, key=lambda f: os.path.getctime(os.path.join(images_dir, f)))
                        image_path = os.path.join(images_dir, latest_file)
                        self.image_label.setPixmap(QPixmap(image_path).scaled(300, 300, Qt.KeepAspectRatio))
                except Exception as e:
                    print(f"Error displaying image: {str(e)}")

        if error:
            self.caption_box.setText(f"Error occurred:\n{error}")
            self.info_label.setText("An error occurred.")
            self.status_bar.setText(f"Error: {error[:50]}...")
        else:
            self.caption_box.setText(output)
            self.info_label.setText("Operation completed.")
            self.status_bar.setText("Ready")

        # Store the worker temporarily to avoid it being garbage collected
        temp_worker = self.worker
        self.worker = None
        
        # Use a safer cleanup approach for the worker
        if temp_worker:
            # Disconnect signals first
            try:
                temp_worker.finished.disconnect()
            except:
                pass
            
            # Then delete the worker later
            temp_worker.deleteLater()

    def excepthook(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions to prevent app from closing"""
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        print(f"Uncaught exception: {error_msg}")
        
        # Show error dialog but keep app running
        QMessageBox.critical(self, 
                           "An error occurred", 
                           f"The application encountered an error but will continue running.\n\nError details:\n{str(exc_value)}")
        
        # Make sure UI is responsive
        self.show_loading(False)
        self.status_bar.setText(f"Error: {str(exc_value)[:50]}...")
        
        # Clean up any potentially running worker
        try:
            if self.worker and self.worker.isRunning():
                self.worker.quit()
                self.worker.wait(1000)
                self.worker.deleteLater()
                self.worker = None
        except:
            self.worker = None
