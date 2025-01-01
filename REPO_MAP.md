# LogoCraft Repository Structure

## Overview
LogoCraft is a professional image processing application designed for restaurant logo format conversion. The application uses PyQt6 for its GUI and supports multiple image formats with predefined output sizes optimized for various use cases.

## Directory Structure

```
LogoCraft_App/
├── .git/                  # Git repository data
├── .venv/                 # Python virtual environment
├── src/                   # Source code directory
│   ├── gui/              # GUI components
│   │   ├── __init__.py   # GUI package initialization
│   │   └── main_window.py # Main application window implementation
│   ├── processors/       # Image processing components
│   ├── utils/           # Utility functions
│   ├── __init__.py      # Main package initialization
│   └── main.py          # Application entry point
├── build.py              # Build script for creating executable
├── requirements.txt      # Python package dependencies
├── LogoCraft.spec        # PyInstaller specification file
├── HungerRush_Icon.ico   # Application icon
├── README.md            # Project documentation
└── REPO_MAP.md          # This file - repository structure documentation
```

## Key Components

### GUI (PyQt6-based)
- `main_window.py`: Implements the main application window with:
  - Image preview area
  - Predefined output format options
  - Directory selection
  - Process control and progress tracking

### Build System
- `build.py`: Handles executable creation with:
  - Virtual environment management
  - Dependency installation
  - PyInstaller compilation
  - Windows Defender management for build process

### Configuration
- `requirements.txt`: Manages project dependencies including:
  - PyQt6 for GUI
  - Pillow for image processing
  - Additional format support (HEIF, PSD)
  - Image processing libraries (numpy, scipy, scikit-image)

### Resources
- `HungerRush_Icon.ico`: Application icon file
- `LogoCraft.spec`: PyInstaller configuration for executable creation

## Recent Updates
- Migrated GUI framework from Tkinter to PyQt6
- Implemented new interface layout matching specification
- Added predefined output formats with specific dimensions
- Updated build configuration for PyQt6 compatibility
- Enhanced preview capabilities and file handling