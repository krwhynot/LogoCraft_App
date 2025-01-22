"""Configuration management system for LogoCraft."""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional
import json
import os
import logging
from pathlib import Path

@dataclass
class FormatConfig:
    dimensions: tuple[int, int]
    mode: str
    format: str
    colors: Optional[int] = None
    background: Optional[tuple[int, int, int]] = None
    is_thermal_printer: bool = False

@dataclass
class AppConfig:
    formats: Dict[str, FormatConfig] = field(default_factory=dict)
    supported_formats: tuple[str, ...] = ('.png', '.jpeg', '.jpg', '.bmp', '.gif', '.tiff', '.webp')
    preview_size: int = 250
    default_output_dir: str = field(default_factory=lambda: str(Path.home() / "Desktop"))
    
    def to_dict(self) -> dict:
        return {
            "formats": {k: vars(v) for k, v in self.formats.items()},
            "supported_formats": self.supported_formats,
            "preview_size": self.preview_size,
            "default_output_dir": self.default_output_dir
        }

class ConfigManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.logger = logging.getLogger(__name__)
            self.config = AppConfig()
            self.initialized = True
    
    def load_config(self, config_path: str) -> None:
        try:
            with open(config_path) as f:
                data = json.load(f)
                self.config = self._parse_config(data)
                self.logger.info("Configuration loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading config: {e}")
            raise
    
    def save_config(self, config_path: str) -> None:
        try:
            config_dir = os.path.dirname(config_path)
            os.makedirs(config_dir, exist_ok=True)
            
            with open(config_path, 'w') as f:
                json.dump(self.config.to_dict(), f, indent=2)
                self.logger.info("Configuration saved successfully")
        except Exception as e:
            self.logger.error(f"Error saving config: {e}")
            raise
    
    def _parse_config(self, data: dict) -> AppConfig:
        formats = {}
        for key, fmt_data in data.get('formats', {}).items():
            formats[key] = FormatConfig(**fmt_data)
        
        return AppConfig(
            formats=formats,
            supported_formats=tuple(data.get('supported_formats', self.config.supported_formats)),
            preview_size=data.get('preview_size', self.config.preview_size),
            default_output_dir=data.get('default_output_dir', self.config.default_output_dir)
        )
    
    def get_format(self, key: str) -> Optional[FormatConfig]:
        return self.config.formats.get(key)
    
    def validate_format(self, format_key: str) -> bool:
        return format_key in self.config.formats