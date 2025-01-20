import unittest
from PIL import Image
import os
import sys
import tempfile
import shutil

# Add project root to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.processors.image_processor import ImageProcessor

class TestImageProcessor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources that can be shared across tests"""
        cls.test_dir = "tests/test_resources"
        cls.output_dir = "tests/test_output"
        os.makedirs(cls.test_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)

        # Create test images with different properties
        cls.create_test_images()

    @classmethod
    def tearDownClass(cls):
        """Clean up test resources"""
        # Add delay and retry for file cleanup
        import time
        max_retries = 3
        for _ in range(max_retries):
            try:
                if os.path.exists(cls.test_dir):
                    shutil.rmtree(cls.test_dir)
                if os.path.exists(cls.output_dir):
                    shutil.rmtree(cls.output_dir)
                break
            except PermissionError:
                time.sleep(0.1)  # Wait for file handles to be released

    @classmethod
    def create_test_images(cls):
        """Create various test images with different properties"""
        # Create a basic square image
        img = Image.new('RGBA', (100, 100), (255, 0, 0, 255))
        cls.square_image_path = os.path.join(cls.test_dir, "square.png")
        img.save(cls.square_image_path)

        # Create a transparent image
        img = Image.new('RGBA', (100, 100), (0, 0, 0, 0))
        cls.transparent_image_path = os.path.join(cls.test_dir, "transparent.png")
        img.save(cls.transparent_image_path)

        # Create a gradient image
        img = Image.new('RGB', (256, 256))
        for x in range(256):
            for y in range(256):
                img.putpixel((x, y), (x, y, 100))
        cls.gradient_image_path = os.path.join(cls.test_dir, "gradient.png")
        img.save(cls.gradient_image_path)

    def test_load_image(self):
        """Test image loading functionality"""
        img = ImageProcessor.load_image(self.square_image_path)
        self.assertIsInstance(img, Image.Image)
        self.assertEqual(img.size, (100, 100))
        self.assertEqual(img.mode, 'RGBA')

    def test_transparency_handling(self):
        """Test transparency handling in conversion"""
        output_path = os.path.join(self.output_dir, "transparent_test.bmp")
        ImageProcessor.convert_printlogo_to_bmp_specs(self.transparent_image_path, output_path)

        # Check if output exists and has correct properties
        self.assertTrue(os.path.exists(output_path))
        with Image.open(output_path) as output_img:
            self.assertEqual(output_img.mode, 'RGB')  # Should be converted to RGB
            self.assertEqual(output_img.size, (600, 256))  # Should have correct dimensions

    def test_color_preservation(self):
        """Test color accuracy in conversion"""
        output_path = os.path.join(self.output_dir, "gradient_test.bmp")
        ImageProcessor.convert_printlogo_to_bmp_specs(self.gradient_image_path, output_path)

        # Check if output maintains color fidelity
        with Image.open(output_path) as output_img:
            self.assertEqual(output_img.mode, 'RGB')

            # Sample some pixels to verify color preservation
            # Note: Colors will be scaled due to resizing, so we check for presence
            # of variation rather than exact values
            pixels = list(output_img.getdata())
            unique_colors = len(set(pixels))
            self.assertGreater(unique_colors, 1000)  # Should have many unique colors

    def test_dimension_constraints(self):
        """Test if output dimensions are correct"""
        output_path = os.path.join(self.output_dir, "dimension_test.bmp")
        ImageProcessor.convert_printlogo_to_bmp_specs(self.square_image_path, output_path)

        with Image.open(output_path) as output_img:
            self.assertEqual(output_img.size, (600, 256))

    def test_dpi_settings(self):
        """Test if DPI settings are correctly applied"""
        output_path = os.path.join(self.output_dir, "dpi_test.bmp")
        ImageProcessor.convert_printlogo_to_bmp_specs(self.square_image_path, output_path)

        # Close any open file handles before cleanup
        output_img = None
        try:
            output_img = Image.open(output_path)
            dpi = output_img.info.get('dpi')
            self.assertIsNotNone(dpi)
            # PIL's info['dpi'] already returns DPI values
            dpi_x = dpi[0]
            dpi_y = dpi[1]
            self.assertAlmostEqual(dpi_x, 203, delta=1)
            self.assertAlmostEqual(dpi_y, 203, delta=1)
        finally:
            if output_img:
                output_img.close()

    def test_centering(self):
        """Test if image is correctly centered"""
        output_path = os.path.join(self.output_dir, "centering_test.bmp")
        ImageProcessor.convert_printlogo_to_bmp_specs(self.square_image_path, output_path)

        with Image.open(output_path) as output_img:
            # Convert to binary (black and white) to easily find content
            binary = output_img.convert('L').point(lambda x: 0 if x < 128 else 255, '1')

            # Find content boundaries
            bbox = binary.getbbox()
            if bbox:
                center_x = (bbox[0] + bbox[2]) // 2
                self.assertAlmostEqual(center_x, 300, delta=5)  # Should be centered at x=300

    def test_error_handling(self):
        """Test error handling for invalid inputs"""
        with self.assertRaises(Exception):
            ImageProcessor.convert_printlogo_to_bmp_specs("nonexistent.png", "output.bmp")

if __name__ == '__main__':
    unittest.main(verbosity=2)
