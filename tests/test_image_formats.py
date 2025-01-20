from PIL import Image
import os
import sys
import shutil

# Add project root to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.processors.image_processor import ImageProcessor

def create_test_image(size, format_name, color=(255, 0, 0, 255)):
    """Create a test image with specified size and format"""
    # Create an image with a red rectangle for visibility
    img = Image.new('RGBA', size, (255, 255, 255, 0))  # Transparent background
    draw_size = (min(size[0]-20, size[1]-20), min(size[0]-20, size[1]-20))
    rect = Image.new('RGBA', draw_size, color)
    img.paste(rect, (10, 10))

    # Save in specified format
    test_path = f"tests/test_images/test_{size[0]}x{size[1]}.{format_name.lower()}"
    os.makedirs(os.path.dirname(test_path), exist_ok=True)

    if format_name.upper() == 'JPEG':
        # Convert to RGB for JPEG
        img = img.convert('RGB')

    img.save(test_path, format_name.upper())
    return test_path

def test_printlogo_conversion():
    """Test PRINTLOGO conversion with various image formats and sizes"""
    # Create output directory
    output_dir = "tests/output"
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    # Test cases: (width, height, format)
    test_cases = [
        # Square images
        (100, 100, 'PNG'),    # Small square
        (300, 300, 'PNG'),    # Medium square
        (500, 500, 'PNG'),    # Large square

        # Landscape images
        (400, 200, 'PNG'),    # 2:1 ratio
        (600, 300, 'PNG'),    # 2:1 ratio, larger
        (800, 200, 'PNG'),    # 4:1 ratio

        # Portrait images
        (200, 400, 'PNG'),    # 1:2 ratio
        (300, 600, 'PNG'),    # 1:2 ratio, larger
        (200, 800, 'PNG'),    # 1:4 ratio

        # Different formats
        (300, 300, 'JPEG'),   # JPEG format
        (400, 300, 'BMP'),    # BMP format

        # Odd sizes
        (123, 456, 'PNG'),    # Random dimensions
        (999, 111, 'PNG'),    # Extreme aspect ratio
    ]

    print("\nTesting PRINTLOGO conversion with various formats and sizes:")
    print("-" * 60)

    for width, height, format_name in test_cases:
        # Create test image
        input_path = create_test_image((width, height), format_name)
        output_path = os.path.join(output_dir, f"printlogo_{width}x{height}.bmp")

        try:
            # Convert image
            ImageProcessor.convert_printlogo_to_bmp_specs(input_path, output_path)

            # Verify output
            output_img = Image.open(output_path)

            # Check specifications
            assert output_img.size == (600, 256), f"Wrong canvas size: {output_img.size}"
            assert output_img.mode == 'RGB', f"Wrong color mode: {output_img.mode}"

            print(f"✓ {format_name} {width}x{height} -> Success")

        except Exception as e:
            print(f"✗ {format_name} {width}x{height} -> Failed: {str(e)}")
            raise

    print("\nAll tests completed successfully!")

if __name__ == "__main__":
    test_printlogo_conversion()
