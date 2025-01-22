from PIL import Image
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class OutputFormat:
    """Defines specifications for each output format."""
    dimensions: Tuple[int, int]
    mode: str
    format: str
    colors: Optional[int] = None
    background: Optional[Tuple[int, int, int]] = None
    is_thermal_printer: bool = False
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ImageFormat:
    """Base class for image format handling"""
    def __init__(self, format_spec: OutputFormat):
        self.format_spec = format_spec
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def process(self, image: Image.Image) -> Image.Image:
        """Common processing pipeline"""
        try:
            self.logger.info(f"Processing image with format: {self.format_spec.format}")
            processed = self._resize(image)
            processed = self._convert_color_mode(processed)
            processed = self._apply_background(processed)
            processed = self._optimize_colors(processed)
            return processed
        except Exception as e:
            self.logger.error(f"Error in processing pipeline: {str(e)}")
            raise
    
    def _resize(self, image: Image.Image) -> Image.Image:
        """Resize image according to format specifications"""
        try:
            return image.resize(self.format_spec.dimensions, Image.Resampling.LANCZOS)
        except Exception as e:
            self.logger.error(f"Error resizing image: {str(e)}")
            raise
    
    def _convert_color_mode(self, image: Image.Image) -> Image.Image:
        """Convert image to specified color mode"""
        try:
            return image.convert(self.format_spec.mode)
        except Exception as e:
            self.logger.error(f"Error converting color mode: {str(e)}")
            raise
    
    def _apply_background(self, image: Image.Image) -> Image.Image:
        """Apply background if specified in format"""
        if not self.format_spec.background:
            return image
            
        try:
            background = Image.new(
                self.format_spec.mode, 
                self.format_spec.dimensions, 
                self.format_spec.background
            )
            background.paste(
                image, 
                (0, 0), 
                image if self.format_spec.mode == 'RGBA' else None
            )
            return background
        except Exception as e:
            self.logger.error(f"Error applying background: {str(e)}")
            raise
    
    def _optimize_colors(self, image: Image.Image) -> Image.Image:
        """Optimize colors if specified in format"""
        if not self.format_spec.colors:
            return image
            
        try:
            return image.convert('P', palette=Image.ADAPTIVE, colors=self.format_spec.colors)
        except Exception as e:
            self.logger.error(f"Error optimizing colors: {str(e)}")
            raise
    
    def save(self, image: Image.Image, output_path: str) -> None:
        """Save image with format-specific optimizations"""
        try:
            save_kwargs = self._get_save_kwargs()
            image.save(output_path, **save_kwargs)
            self.logger.info(f"Image saved successfully to: {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving image: {str(e)}")
            raise
    
    def _get_save_kwargs(self) -> Dict[str, Any]:
        """Get format-specific save parameters"""
        kwargs = {'format': self.format_spec.format}
        
        if self.format_spec.format == 'JPEG':
            kwargs['quality'] = 95
        if self.format_spec.format in ['PNG', 'JPEG']:
            kwargs['optimize'] = True
            
        return kwargs

class ThermalPrinterFormat(ImageFormat):
    """Specialized handling for thermal printer format"""
    def process(self, image: Image.Image) -> Image.Image:
        """Process image for thermal printer output"""
        try:
            self.logger.info("Processing image for thermal printer format")
            img = self._prepare_rgba_image(image)
            return self._create_thermal_layout(img)
        except Exception as e:
            self.logger.error(f"Error in thermal printer processing: {str(e)}")
            raise
    
    def _prepare_rgba_image(self, image: Image.Image) -> Image.Image:
        """Prepare image with white background"""
        try:
            img = image.convert('RGBA')
            background = Image.new('RGBA', img.size, (255, 255, 255, 255))
            return Image.alpha_composite(background, img)
        except Exception as e:
            self.logger.error(f"Error preparing RGBA image: {str(e)}")
            raise
    
    def _create_thermal_layout(self, image: Image.Image) -> Image.Image:
        """Create layout optimized for thermal printer"""
        try:
            max_size = 256
            aspect_ratio = image.width / image.height
            new_width = max_size if aspect_ratio > 1 else int(max_size * aspect_ratio)
            new_height = int(max_size / aspect_ratio) if aspect_ratio > 1 else max_size
            
            img = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            final_image = Image.new('RGB', (600, 256), (255, 255, 255))
            
            x_offset = 300 - (new_width // 2)
            y_offset = (256 - new_height) // 2
            final_image.paste(img, (x_offset, y_offset))
            
            return final_image
        except Exception as e:
            self.logger.error(f"Error creating thermal layout: {str(e)}")
            raise
    
    def save(self, image: Image.Image, output_path: str) -> None:
        """Save image with thermal printer specifications"""
        try:
            image.save(output_path, 'BMP', dpi=(203, 203))
            self.logger.info(f"Thermal printer image saved to: {output_path}")
        except Exception as e:
            self.logger.error(f"Error saving thermal printer image: {str(e)}")
            raise
