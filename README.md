# LogoCraft

LogoCraft is a professional-grade image processing application designed specifically for restaurant logo management. It provides automated conversion of logo files into multiple standardized formats with predefined dimensions optimized for various use cases.

## Features

- Clean, intuitive PyQt6-based interface
- Predefined output formats for common use cases:
  - Standard logo (300x300 PNG)
  - Small logo (136x136 PNG)
  - KD logo (140x112 PNG)
  - Report logo (155x110 BMP)
  - Thermal printer optimized format
- Live image preview
- Batch processing support
- Professional-grade image quality preservation
- Support for multiple input formats (PNG, JPEG, BMP, PSD, HEIF)

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 (primary support)

### Setup
1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd LogoCraft_App
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Building the Executable
Run the build script:
```bash
python build.py
```

The executable will be created in the `dist` directory.

## Usage

1. Launch LogoCraft
2. Click "Select Image" or drag and drop a logo file
3. Choose desired output formats (pre-selected by default)
4. Select output directory or use default
5. Click "Process Image"

## Development

### Project Structure
- `src/`: Source code directory
  - `gui/`: PyQt6 interface components
  - `processors/`: Image processing modules
  - `utils/`: Utility functions
- `build.py`: Build script
- `LogoCraft.spec`: PyInstaller configuration

### Dependencies
Main dependencies include:
- PyQt6: GUI framework
- Pillow: Core image processing
- pillow-heif: HEIF format support
- psd-tools: Photoshop file support
- numpy/scipy: Image manipulation
- scikit-image: Additional transformations

### Building from Source
1. Ensure all dependencies are installed
2. Run build script with Python 3.8+
3. Check `dist` directory for executable

## Recent Updates
- Migrated to PyQt6 for improved interface
- Implemented standardized output formats
- Enhanced preview capabilities
- Improved build process reliability
- Added professional-grade image processing pipeline

## Contributing
Contributions are welcome! Please read our contributing guidelines and submit pull requests for any enhancements.

## License
[License Information]

## Support
For support, please open an issue in the repository or contact the development team.