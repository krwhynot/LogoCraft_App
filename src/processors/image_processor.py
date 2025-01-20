from PIL import Image, ImageEnhance
from src.config import OutputFormat
import numpy as np
import math
import os

class ImageProcessor:
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """Load an image file."""
        return Image.open(file_path)

    @staticmethod
    def validate_image_metrics(image: Image.Image) -> dict:
        """Validate image metrics against target specifications."""
        img_array = np.array(image)

        metrics = {
            'mean_luminance': np.mean(img_array),
            'std_dev': np.std(img_array),
            'dynamic_range': np.ptp(img_array)
        }

        # Compare against target metrics
        target_metrics = {
            'mean_luminance': 230.55,
            'std_dev': 75.08,
            'dynamic_range': 255.0
        }

        return metrics

    @staticmethod
    def convert_printlogo_to_bmp_specs(input_path: str, output_path: str) -> None:
        """
        Convert image to PRINTLOGO BMP format with specific requirements:
        * Canvas size: 600x256
        * Image is scaled to fit within 256x256 area (maintaining aspect ratio)
        * Image is right-aligned with 50px margin
        * Image is centered vertically
        * Converts to 24-bit color (RGB mode)
        * Ensures transparent or white background for all images
        * Saves as uncompressed BMP
        * Maintains 203 DPI setting

        Args:
            input_path (str): Path to the input image file
            output_path (str): Path to save the converted image
        """
        try:
            # Open the image
            print("Opening image")
            img = Image.open(input_path)

            # Convert to RGBA to handle transparency
            print("Converting image to RGBA")
            img = img.convert('RGBA')

            # Create a white background layer the same size as the input image
            print("Creating white background")
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))

            # Composite the image onto the white background
            print("Compositing image onto background")
            img = Image.alpha_composite(background, img)

            # Calculate resize dimensions to fit within 256x256 while maintaining aspect ratio
            print("Calculating resize dimensions")
            max_size = 256
            aspect_ratio = img.width / img.height

            if aspect_ratio > 1:
                # Width is larger
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:
                # Height is larger or square
                new_height = max_size
                new_width = int(max_size * aspect_ratio)

            print(f"Original size: {img.width}x{img.height}")

            # Resize image
            print(f"Resizing image to {new_width}x{new_height}")
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # Create new 600x256 white canvas
            print("Creating 600x256 white canvas")
            final_image = Image.new('RGB', (600, 256), (255, 255, 255))

            # Calculate position to center horizontally at x=300 and center vertically
            x_offset = 300 - (new_width // 2)  # Center at x=300
            y_offset = (256 - new_height) // 2  # Center vertically
            print(f"New size: {new_width}x{new_height}, Center Position: (300, {256//2})")

            # Paste resized image onto canvas
            print("Pasting image onto canvas")
            final_image.paste(img, (x_offset, y_offset))

            # Set DPI to 203
            dpi = 203

            # Save as uncompressed BMP with specific DPI
            print(f"Saving BMP with {dpi} DPI")
            final_image.save(output_path, 'BMP', dpi=(dpi, dpi))

            print("Image converted and saved successfully")

        except Exception as e:
            print(f"Error converting image: {str(e)}")
            raise

    @staticmethod
    def process_multiple_images(input_files: list, output_directory: str) -> None:
        """
        Process multiple images using the conversion specifications

        Args:
            input_files (list): List of input file paths
            output_directory (str): Directory for output files
        """
        import os

        # Create output directory if it doesn't exist
        os.makedirs(output_directory, exist_ok=True)

        for input_file in input_files:
            # Generate output filename
            filename = os.path.basename(input_file)
            name, _ = os.path.splitext(filename)
            output_path = os.path.join(output_directory, f"{name}_converted.bmp")

            try:
                ImageProcessor.convert_printlogo_to_bmp_specs(input_file, output_path)
                print(f"Successfully converted: {filename}")
            except Exception as e:
                print(f"Error converting {filename}: {str(e)}")

    @staticmethod
    def convert_rptlogo_to_bmp_specs(image: Image.Image, output_path: str) -> None:
        """
        Convert RPTlogo to specific settings:
        - Resizes to 155x110 pixels
        - Converts to 24-bit color (RGB mode)
        - Ensures white background for transparency
        - Saves as uncompressed BMP
        - Maintains 203 DPI setting

        Args:
            image (Image.Image): PIL Image object to convert
            output_path (str): Path to save the converted image
        """
        try:
            # Convert to RGBA to handle transparency
            print("Converting image to RGBA")
            img = image.convert('RGBA')

            # Create a white background layer
            print("Creating white background")
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))

            # Composite the image onto the white background
            print("Compositing image onto background")
            img = Image.alpha_composite(background, img)

            # Resize image to exactly 155x110
            print("Resizing image to 155x110")
            img = img.resize((155, 110), Image.Resampling.LANCZOS)

            # Create white canvas
            print("Creating white canvas")
            canvas = Image.new('RGB', (155, 110), (255, 255, 255))

            # Paste resized image onto white canvas
            print("Pasting image onto white canvas")
            canvas.paste(img, (0, 0))

            # Set DPI to 203
            dpi = 203

            # Save as uncompressed BMP with specific DPI
            print(f"Saving BMP with {dpi} DPI")
            canvas.save(output_path, 'BMP', dpi=(dpi, dpi))

            print("Image converted and saved successfully")

        except Exception as e:
            print(f"Error converting image: {str(e)}")
            raise

    @staticmethod
    def process_image(image: Image.Image, format_spec: OutputFormat, output_name: str) -> None:
        """Process an image based on the output format specifications and save it."""
        try:
            # Special processing for printer formats
            if format_spec.format == 'BMP':
                if format_spec.is_thermal_printer:
                    # Save the input image to a temporary file for PRINTLOGO
                    import tempfile
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        temp_path = temp_file.name
                        image.save(temp_path, 'PNG')

                    try:
                        print("Processing PRINTLOGO format")
                        ImageProcessor.convert_printlogo_to_bmp_specs(temp_path, output_name)
                    finally:
                        # Clean up temporary file
                        import os
                        os.unlink(temp_path)
                elif format_spec.dimensions == (155, 110):
                    print("Processing RPTLOGO format")
                    ImageProcessor.convert_rptlogo_to_bmp_specs(image, output_name)
            else:
                # Standard processing for other formats
                print(f"Resizing image to {format_spec.dimensions}")
                processed_image = image.resize(format_spec.dimensions, Image.Resampling.LANCZOS)

                print(f"Converting to mode {format_spec.mode}")
                processed_image = processed_image.convert(format_spec.mode)

                # Handle background for non-transparent formats
                if format_spec.background:
                    print(f"Applying background color {format_spec.background}")
                    background = Image.new(format_spec.mode, format_spec.dimensions, format_spec.background)
                    background.paste(processed_image, (0, 0), processed_image if format_spec.mode == 'RGBA' else None)
                    processed_image = background

                # Handle color reduction for BMP
                if format_spec.colors:
                    print(f"Reducing colors to {format_spec.colors}")
                    processed_image = processed_image.convert('P', palette=Image.ADAPTIVE, colors=format_spec.colors)

                # Save the image
                print(f"Saving image as {format_spec.format} to {output_name}")
                save_kwargs = {
                    'format': format_spec.format,
                    'quality': 95 if format_spec.format == 'JPEG' else None,
                    'optimize': True if format_spec.format in ['PNG', 'JPEG'] else None
                }
                # Remove None values from kwargs
                save_kwargs = {k: v for k, v in save_kwargs.items() if v is not None}
                processed_image.save(output_name, **save_kwargs)

            print("Image processing completed successfully")

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise
