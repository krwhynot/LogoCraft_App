"""Default configuration and format specifications."""
from src.core.config_manager import ConfigManager, FormatConfig
from src.core.image_format import OutputFormat

# Convert OutputFormat to FormatConfig for compatibility
def _to_format_config(fmt: OutputFormat) -> FormatConfig:
    return FormatConfig(
        dimensions=fmt.dimensions,
        mode=fmt.mode,
        format=fmt.format,
        colors=fmt.colors,
        background=fmt.background,
        is_thermal_printer=fmt.is_thermal_printer
    )

# Define default formats using OutputFormat
default_formats = {
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
        mode='RGB',
        format='BMP',
        is_thermal_printer=True
    )
}

# Initialize config manager with FormatConfig versions of the formats
config_manager = ConfigManager()
config_manager.config.formats = {
    key: _to_format_config(fmt) for key, fmt in default_formats.items()
}
