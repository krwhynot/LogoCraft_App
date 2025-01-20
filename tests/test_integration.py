import unittest
from PIL import Image
import os
import sys
import tempfile
import shutil
from PyQt6.QtWidgets import QApplication

# Add project root to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.processors.image_processor import ImageProcessor
from src.config import OutputFormat, Config
from src.gui.main_window import ImageProcessorGUI

class TestImageProcessingWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        cls.test_dir = "tests/integration_resources"
        cls.output_dir = "tests/integration_output"
        os.makedirs(cls.test_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)

        # Create test resources
        cls.create_test_resources()

        # Initialize QApplication for GUI tests
        cls.app = QApplication([])

    @classmethod
    def tearDownClass(cls):
        """Clean up test resources"""
        shutil.rmtree(cls.test_dir)
        shutil.rmtree(cls.output_dir)
        cls.app.quit()

    @classmethod
    def create_test_resources(cls):
        """Create test resources for integration testing"""
        # Create various test images
        sizes = [(300, 300), (400, 200), (200, 400)]
        for width, height in sizes:
            img = Image.new('RGBA', (width, height), (255, 0, 0, 255))
            filename = f"test_{width}x{height}.png"
            img.save(os.path.join(cls.test_dir, filename))

    def test_complete_workflow(self):
        """Test complete image processing workflow"""
        # 1. Load image
        input_path = os.path.join(self.test_dir, "test_300x300.png")
        image = ImageProcessor.load_image(input_path)
        self.assertIsInstance(image, Image.Image)

        # 2. Process for all formats
        for format_name, format_spec in Config.OUTPUT_FORMATS.items():
            output_path = os.path.join(self.output_dir, format_name)
            ImageProcessor.process_image(image, format_spec, output_path)

            # Verify output exists and has correct properties
            self.assertTrue(os.path.exists(output_path))
            output_img = Image.open(output_path)
            self.assertEqual(output_img.size, format_spec.dimensions)
            self.assertEqual(output_img.mode, format_spec.mode)

    def test_gui_initialization(self):
        """Test GUI initialization and basic functionality"""
        window = ImageProcessorGUI()

        # Check initial state
        self.assertFalse(window.process_button.isEnabled())
        self.assertTrue(all(cb.isChecked() for cb in window.format_checks.values()))

        # Check format options
        self.assertEqual(
            set(window.format_checks.keys()),
            {'Logo.png', 'Smalllogo.png', 'KDlogo.png', 'RPTlogo.bmp', 'PRINTLOGO.bmp'}
        )

    def test_file_operations(self):
        """Test file operations workflow"""
        # Create a temporary directory structure
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create test file
            test_file = os.path.join(temp_dir, "test.png")
            img = Image.new('RGBA', (300, 300), (255, 0, 0, 255))
            img.save(test_file)

            # 2. Process file for each format
            for format_name, format_spec in Config.OUTPUT_FORMATS.items():
                output_path = os.path.join(temp_dir, format_name)

                # Load and process
                image = ImageProcessor.load_image(test_file)
                ImageProcessor.process_image(image, format_spec, output_path)

                # Verify output
                self.assertTrue(os.path.exists(output_path))
                self.assertTrue(os.path.getsize(output_path) > 0)

    def test_error_recovery(self):
        """Test error handling and recovery in workflow"""
        # Test with invalid input
        with self.assertRaises(Exception):
            ImageProcessor.load_image("nonexistent.png")

        # Test with invalid format spec
        invalid_format = OutputFormat(
            dimensions=(0, 0),  # Invalid dimensions
            mode='INVALID',
            format='INVALID'
        )

        with self.assertRaises(Exception):
            image = Image.new('RGB', (100, 100))
            ImageProcessor.process_image(image, invalid_format, "output.png")

    def test_cross_component_interaction(self):
        """Test interaction between different components"""
        window = ImageProcessorGUI()

        # 1. Simulate file selection
        test_file = os.path.join(self.test_dir, "test_300x300.png")
        window.process_selected_file(test_file)

        # Check if UI updated correctly
        self.assertTrue(window.process_button.isEnabled())
        self.assertFalse(window.preview_label.pixmap().isNull())

        # 2. Check output directory handling
        test_output_dir = os.path.join(self.output_dir, "test_output")
        window.dir_path.setText(test_output_dir)

        # Verify directory handling
        self.assertEqual(window.dir_path.text(), test_output_dir)

if __name__ == '__main__':
    unittest.main(verbosity=2)
