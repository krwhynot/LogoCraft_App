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
    is_thermal_printer: bool = False  # Flag for thermal printer optimization

class Config:
    """Application configuration and constants."""
    SUPPORTED_FORMATS = ('.png', '.jpeg', '.jpg', '.bmp', '.gif')
    OUTPUT_FORMATS = {
        'Logo.png': OutputFormat(
            dimensions=(300, 300),
            mode='RGBA',
            format='PNG'
        ),
        'Smalllogo.png': OutputFormat(
            dimensions=(136, 136),
            mode='RGBA',
            format='PNG'
        ),
        'KDlogo.png': OutputFormat(
            dimensions=(140, 112),
            mode='RGBA',
            format='PNG'
        ),
        'RPTlogo.bmp': OutputFormat(
            dimensions=(155, 110),
            mode='RGB',
            format='BMP',
            background=(255, 255, 255)
        ),
        'PRINTLOGO.bmp': OutputFormat(
            dimensions=(600, 256),
            mode='RGB',  # Keep original color mode
            format='BMP',
            is_thermal_printer=True  # Enable thermal printer optimizations
        )
    }
