import logging
from src.gui.main_window import ImageProcessorGUI

def main():
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
    )
    logging.info("Starting Image Processor Application")

    # Initialize and run the GUI
    app = ImageProcessorGUI()
    app.run()

if __name__ == "__main__":
    main()
