import unittest
from PIL import Image
import os
import sys
import tempfile
import shutil
import numpy as np

# Add project root to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.processors.image_processor import ImageProcessor

class TestFileFormats(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test resources"""
        cls.test_dir = "tests/format_test_resources"
        cls.output_dir = "tests/format_test_output"
        os.makedirs(cls.test_dir, exist_ok=True)
        os.makedirs(cls.output_dir, exist_ok=True)

        # Create test images in different formats
        cls.create_test_images()

    @classmethod
    def tearDownClass(cls):
        """Clean up test resources"""
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
                time.sleep(0.1)

    @classmethod
    def create_test_images(cls):
        """Create test images in various formats with different characteristics"""
        # Base sizes for testing different aspect ratios
        sizes = [
            (300, 300),  # Square
            (400, 200),  # Landscape
            (200, 400)   # Portrait
        ]

        # Create a gradient pattern
        def create_gradient_image(size):
            img = Image.new('RGB', size)
            for x in range(size[0]):
                for y in range(size[1]):
                    r = int(255 * x / size[0])
                    g = int(255 * y / size[1])
                    b = 100
                    img.putpixel((x, y), (r, g, b))
            return img

        # Create a test pattern with transparency
        def create_transparent_image(size):
            img = Image.new('RGBA', size, (0, 0, 0, 0))
            # Add some visible content
            for x in range(size[0]):
                for y in range(size[1]):
                    if (x + y) % 2 == 0:
                        img.putpixel((x, y), (255, 0, 0, 128))
            return img

        formats = {
            'JPEG': {'mode': 'RGB', 'ext': '.jpg'},
            'PNG': {'mode': 'RGBA', 'ext': '.png'},
            'GIF': {'mode': 'P', 'ext': '.gif'},
            'WEBP': {'mode': 'RGBA', 'ext': '.webp'},
            'TIFF': {'mode': 'RGB', 'ext': '.tiff'}
        }

        cls.test_files = {}

        for format_name, format_info in formats.items():
            format_files = []
            for size in sizes:
                # Create both gradient and transparent versions
                if format_info['mode'] == 'RGBA':
                    img = create_transparent_image(size)
                else:
                    img = create_gradient_image(size)
                    if format_info['mode'] == 'P':
                        img = img.convert('P', palette=Image.ADAPTIVE)

                filename = f"test_{size[0]}x{size[1]}{format_info['ext']}"
                filepath = os.path.join(cls.test_dir, filename)
                img.save(filepath, format=format_name)
                format_files.append(filepath)

            cls.test_files[format_name] = format_files

    def verify_output_image(self, output_path):
        """Verify that the output image meets all requirements"""
        with Image.open(output_path) as img:
            # Check basic requirements
            self.assertEqual(img.size, (600, 256), "Output size should be 600x256")
            self.assertEqual(img.mode, 'RGB', "Output should be RGB mode")

            # Check DPI
            dpi = img.info.get('dpi')
            self.assertIsNotNone(dpi, "DPI information should be present")
            self.assertAlmostEqual(dpi[0], 203, delta=1, msg="Horizontal DPI should be 203")
            self.assertAlmostEqual(dpi[1], 203, delta=1, msg="Vertical DPI should be 203")

            # Verify image is not empty (has non-white pixels)
            pixels = list(img.getdata())
            has_content = any(pixel != (255, 255, 255) for pixel in pixels)
            self.assertTrue(has_content, "Output image should contain non-white pixels")

    def test_jpeg_conversion(self):
        """Test JPEG format conversion"""
        print("\nTesting JPEG format conversion:")
        for input_path in self.test_files['JPEG']:
            print(f"Processing {os.path.basename(input_path)}")
            output_path = os.path.join(self.output_dir, f"output_{os.path.basename(input_path)}.bmp")
            ImageProcessor.convert_printlogo_to_bmp_specs(input_path, output_path)
            self.verify_output_image(output_path)

    def test_png_conversion(self):
        """Test PNG format conversion with transparency"""
        print("\nTesting PNG format conversion:")
        for input_path in self.test_files['PNG']:
            print(f"Processing {os.path.basename(input_path)}")
            output_path = os.path.join(self.output_dir, f"output_{os.path.basename(input_path)}.bmp")
            ImageProcessor.convert_printlogo_to_bmp_specs(input_path, output_path)
            self.verify_output_image(output_path)

    def test_gif_conversion(self):
        """Test GIF format conversion"""
        print("\nTesting GIF format conversion:")
        for input_path in self.test_files['GIF']:
            print(f"Processing {os.path.basename(input_path)}")
            output_path = os.path.join(self.output_dir, f"output_{os.path.basename(input_path)}.bmp")
            ImageProcessor.convert_printlogo_to_bmp_specs(input_path, output_path)
            self.verify_output_image(output_path)

    def test_webp_conversion(self):
        """Test WebP format conversion"""
        print("\nTesting WebP format conversion:")
        for input_path in self.test_files['WEBP']:
            print(f"Processing {os.path.basename(input_path)}")
            output_path = os.path.join(self.output_dir, f"output_{os.path.basename(input_path)}.bmp")
            ImageProcessor.convert_printlogo_to_bmp_specs(input_path, output_path)
            self.verify_output_image(output_path)

    def test_tiff_conversion(self):
        """Test TIFF format conversion"""
        print("\nTesting TIFF format conversion:")
        for input_path in self.test_files['TIFF']:
            print(f"Processing {os.path.basename(input_path)}")
            output_path = os.path.join(self.output_dir, f"output_{os.path.basename(input_path)}.bmp")
            ImageProcessor.convert_printlogo_to_bmp_specs(input_path, output_path)
            self.verify_output_image(output_path)

if __name__ == '__main__':
    unittest.main(verbosity=2)
