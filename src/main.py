import sys
import os

# Add project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5.QtWidgets import QApplication
from src.gui.caption_app import CaptionApp

def main():
    app = QApplication(sys.argv)
    window = CaptionApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
