from PIL import Image
from src.config import OutputFormat

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
    def convert_printlogo_to_bmp_specs(input_path: str, output_path: str) -> None:
        """Convert image to PRINTLOGO BMP format (600x256, 203 DPI)."""
        with Image.open(input_path) as source_img:
            img = ImageProcessor._prepare_rgba_image(source_img)
            
            # Calculate dimensions for 256x256 bounded resize
            max_size = 256
            aspect_ratio = img.width / img.height
            new_width = max_size if aspect_ratio > 1 else int(max_size * aspect_ratio)
            new_height = int(max_size / aspect_ratio) if aspect_ratio > 1 else max_size
            
            # Resize and prepare final image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            final_image = Image.new('RGB', (600, 256), (255, 255, 255))
            
            # Center the image
            x_offset = 300 - (new_width // 2)
            y_offset = (256 - new_height) // 2
            final_image.paste(img, (x_offset, y_offset))
            
            # Save with specific DPI
            final_image.save(output_path, 'BMP', dpi=(203, 203))

    @staticmethod
    def convert_rptlogo_to_bmp_specs(image: Image.Image, output_path: str) -> None:
        """Convert image to RPTlogo BMP format (155x110, 203 DPI)."""
        img = ImageProcessor._prepare_rgba_image(image)
        img = img.resize((155, 110), Image.Resampling.LANCZOS)
        
        canvas = Image.new('RGB', (155, 110), (255, 255, 255))
        canvas.paste(img, (0, 0))
        canvas.save(output_path, 'BMP', dpi=(203, 203))

    @staticmethod
    def process_image(image: Image.Image, format_spec: OutputFormat, output_name: str) -> None:
        """Process an image according to format specifications."""
        try:
            if format_spec.format == 'BMP':
                if format_spec.is_thermal_printer:
                    # Handle PRINTLOGO format
                    import tempfile, os
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
                        temp_path = temp_file.name
                        image.save(temp_path, 'PNG')
                        try:
                            ImageProcessor.convert_printlogo_to_bmp_specs(temp_path, output_name)
                        finally:
                            os.unlink(temp_path)
                elif format_spec.dimensions == (155, 110):
                    ImageProcessor.convert_rptlogo_to_bmp_specs(image, output_name)
            else:
                # Standard image processing
                processed_image = image.resize(format_spec.dimensions, Image.Resampling.LANCZOS)
                processed_image = processed_image.convert(format_spec.mode)

                if format_spec.background:
                    background = Image.new(format_spec.mode, format_spec.dimensions, format_spec.background)
                    background.paste(processed_image, (0, 0), processed_image if format_spec.mode == 'RGBA' else None)
                    processed_image = background

                if format_spec.colors:
                    processed_image = processed_image.convert('P', palette=Image.ADAPTIVE, colors=format_spec.colors)

                # Save with optimized parameters
                save_kwargs = {
                    'format': format_spec.format,
                    'quality': 95 if format_spec.format == 'JPEG' else None,
                    'optimize': True if format_spec.format in ['PNG', 'JPEG'] else None
                }
                processed_image.save(output_name, **{k: v for k, v in save_kwargs.items() if v is not None})

        except Exception as e:
            print(f"Error processing image: {str(e)}")
            raise