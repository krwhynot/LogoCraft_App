from PIL import Image
from src.config import OutputFormat

class ImageProcessor:
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """Load an image file."""
        return Image.open(file_path)

    @staticmethod
    def process_image(image: Image.Image, format_spec: OutputFormat, output_name: str) -> Image.Image:
        """Process an image based on the output format specifications."""
        # Resize and convert to specified mode
        processed_image = image.resize(format_spec.dimensions, Image.Resampling.LANCZOS)
        processed_image = processed_image.convert(format_spec.mode)

        # Handle background for non-transparent formats
        if format_spec.background:
            background = Image.new(format_spec.mode, format_spec.dimensions, format_spec.background)
            background.paste(processed_image, (0, 0), processed_image if format_spec.mode == 'RGBA' else None)
            processed_image = background

        # Handle color reduction for BMP
        if format_spec.colors:
            processed_image = processed_image.convert('P', palette=Image.ADAPTIVE, colors=format_spec.colors)

        return processed_image
