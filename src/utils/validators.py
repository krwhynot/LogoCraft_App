import os
from pathlib import Path
from src.config import Config

def is_valid_file(file_path: str) -> bool:
    """Check if the file exists and is a supported format."""
    path = Path(file_path)
    return path.exists() and path.suffix.lower() in Config.SUPPORTED_FORMATS

def is_valid_directory(directory_path: str) -> bool:
    """Check if the directory exists and is writable."""
    path = Path(directory_path)
    return path.exists() and path.is_dir() and os.access(directory_path, os.W_OK)
