import sys
import logging
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from src.gui import ImageProcessorGUI

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logocraft.log'),
        logging.StreamHandler()  # Also log to console
    ]
)
logger = logging.getLogger(__name__)

def main():
    """Main application entry point"""
    try:
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon('HungerRush_Icon.ico'))

        window = ImageProcessorGUI()
        window.show()

        logger.info("Application started successfully")
        sys.exit(app.exec())

    except Exception as e:
        logger.error(f"Application error: {str(e)}", exc_info=True)
        raise

if __name__ == '__main__':
    main()
