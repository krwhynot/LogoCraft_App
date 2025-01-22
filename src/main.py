import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from src.gui import ImageProcessorGUI

def main():
    """Main application entry point"""
    try:
        # Enable High DPI scaling
        if hasattr(Qt.ApplicationAttribute, 'AA_EnableHighDpiScaling'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_EnableHighDpiScaling, True)
        if hasattr(Qt.ApplicationAttribute, 'AA_UseHighDpiPixmaps'):
            QApplication.setAttribute(Qt.ApplicationAttribute.AA_UseHighDpiPixmaps, True)
        
        app = QApplication(sys.argv)
        
        # Get the absolute path to the icon
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        icon_path = os.path.join(base_dir, 'HungerRush_Icon.ico')
        
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
        
        window = ImageProcessorGUI()
        window.setWindowIcon(QIcon(icon_path))  # Also set icon for the main window
        window.show()

        sys.exit(app.exec())

    except Exception as e:
        print(f"Application error: {str(e)}")
        raise

if __name__ == '__main__':
    main()