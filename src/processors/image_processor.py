import logging
from PIL import Image
from src.core.image_format import OutputFormat

logger = logging.getLogger(__name__)

class ImageProcessor:
    @staticmethod
    def load_image(file_path: str) -> Image.Image:
        """Load an image file."""
        return Image.open(file_path)

    @staticmethod
    def _prepare_rgba_image(image: Image.Image) -> Image.Image:
        """Convert image to RGBA and apply white background."""
        img = image.convert('RGBA')
        background = Image.new('RGBA', img.size, (255, 255, 255, 255))
        return Image.alpha_composite(background, img)

    @staticmethod
    def _calculate_bounded_dimensions(width: int, height: int, max_size: int) -> tuple[int, int]:
        """Calculate dimensions maintaining aspect ratio within bounds."""
        aspect_ratio = width / height
        new_width = max_size if aspect_ratio > 1 else int(max_size * aspect_ratio)
        new_height = int(max_size / aspect_ratio) if aspect_ratio > 1 else max_size
        return new_width, new_height

    @staticmethod
    def _create_centered_image(img: Image.Image, canvas_size: tuple[int, int], 
                             background_color: tuple[int, int, int] = (255, 255, 255)) -> Image.Image:
        """Create a new image with the input image centered on it."""
        canvas = Image.new('RGB', canvas_size, background_color)
        x_offset = (canvas_size[0] - img.width) // 2
        y_offset = (canvas_size[1] - img.height) // 2
        canvas.paste(img, (x_offset, y_offset))
        return canvas

    @staticmethod
    def _save_bmp_with_dpi(image: Image.Image, output_path: str, dpi: tuple[int, int] = (203, 203)) -> None:
        """Save image in BMP format with specified DPI."""
        image.save(output_path, 'BMP', dpi=dpi)

    @staticmethod
    def convert_printlogo_to_bmp_specs(input_path: str, output_path: str) -> None:
        """Convert image to PRINTLOGO BMP format (600x256, 203 DPI)."""
        with Image.open(input_path) as source_img:
            img = ImageProcessor._prepare_rgba_image(source_img)
            new_width, new_height = ImageProcessor._calculate_bounded_dimensions(img.width, img.height, 256)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            final_image = ImageProcessor._create_centered_image(img, (600, 256))
            ImageProcessor._save_bmp_with_dpi(final_image, output_path)

    @staticmethod
    def convert_rptlogo_to_bmp_specs(image: Image.Image, output_path: str) -> None:
        """Convert image to RPTlogo BMP format (155x110, 203 DPI)."""
        img = ImageProcessor._prepare_rgba_image(image)
        img = img.resize((155, 110), Image.Resampling.LANCZOS)
        final_image = ImageProcessor._create_centered_image(img, (155, 110))
        ImageProcessor._save_bmp_with_dpi(final_image, output_path)

    @staticmethod
    def _process_standard_image(image: Image.Image, format_spec: OutputFormat) -> Image.Image:
        """Process image according to standard format specifications."""
        processed_image = image.resize(format_spec.dimensions, Image.Resampling.LANCZOS)
        processed_image = processed_image.convert(format_spec.mode)

        if format_spec.background:
            background = Image.new(format_spec.mode, format_spec.dimensions, format_spec.background)
            background.paste(processed_image, (0, 0), processed_image if format_spec.mode == 'RGBA' else None)
            processed_image = background

        if format_spec.colors:
            processed_image = processed_image.convert('P', palette=Image.ADAPTIVE, colors=format_spec.colors)

        return processed_image

    @staticmethod
    def _get_save_kwargs(format_spec: OutputFormat) -> dict:
        """Get optimized save parameters based on format."""
        return {
            'format': format_spec.format,
            'quality': 95 if format_spec.format == 'JPEG' else None,
            'optimize': True if format_spec.format in ['PNG', 'JPEG'] else None,
            'dpi': (203, 203) if format_spec.format == 'BMP' else None
        }

    @staticmethod
    def process_image(image: Image.Image, format_spec: OutputFormat, output_name: str) -> None:
        """Process an image according to format specifications."""
        try:
            if format_spec.format == 'BMP':
                if format_spec.is_thermal_printer:
                    # Handle PRINTLOGO format
                    import tempfile, os
                    temp_path = None
                    try:
                        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                            temp_path = temp_file.name
                            image.save(temp_path, 'PNG')
                        ImageProcessor.convert_printlogo_to_bmp_specs(temp_path, output_name)
                    finally:
                        if temp_path and os.path.exists(temp_path):
                            try:
                                os.unlink(temp_path)
                            except Exception as e:
                                logger.warning(f"Failed to delete temporary file {temp_path}: {e}")
                elif format_spec.dimensions == (155, 110):
                    ImageProcessor.convert_rptlogo_to_bmp_specs(image, output_name)
            else:
                processed_image = ImageProcessor._process_standard_image(image, format_spec)
                save_kwargs = ImageProcessor._get_save_kwargs(format_spec)
                processed_image.save(output_name, **{k: v for k, v in save_kwargs.items() if v is not None})

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise
