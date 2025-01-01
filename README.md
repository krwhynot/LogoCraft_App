# Image Processor Application

A Python desktop application for batch processing images into multiple formats and sizes, with a user-friendly GUI interface.

## Features

- Preview images before processing
- Multiple output formats:
  - Logo.png (300x300)
  - Smalllogo.png (136x136)
  - KDlogo.png (140x112)
  - RPTlogo.bmp (135x110)
  - PRINTLOGO.bmp (Thermal Printer Optimized)
- Progress tracking during processing
- Support for various input formats (PNG, JPEG, BMP, GIF)
- Optimized output for different use cases including thermal printing

## Requirements

- Python 3.x
- Pillow (PIL)
- tkinter (usually comes with Python)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd LogoCraft_App
```

2. Install dependencies:
```bash
pip install pillow
```

## Project Structure

```
LogoCraft_App/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration and format specifications
│   ├── gui/
│   │   ├── __init__.py
│   │   └── main_window.py   # GUI implementation
│   ├── processors/
│   │   ├── __init__.py
│   │   └── image_processor.py # Image processing logic
│   └── utils/
│       ├── __init__.py
│       └── validators.py     # Input validation utilities
└── README.md
```

## Usage

1. Run the application:
```powershell
$env:PYTHONPATH = $PWD; python -m src.main
```

2. Using the application:
   - Click "Select Image" to choose an input image
   - Select desired output formats using checkboxes
   - Choose an output directory
   - Click "Process Image" to generate the outputs
   - Progress bar will show processing status

## Output Formats

1. **Logo.png (300x300)**
   - Full-size logo in PNG format
   - Preserves transparency
   - Best for web use

2. **Smalllogo.png (136x136)**
   - Reduced size logo
   - Maintains transparency
   - Suitable for thumbnails

3. **KDlogo.png (140x112)**
   - Custom dimension logo
   - Preserves transparency
   - Optimized for specific display areas

4. **RPTlogo.bmp (135x110)**
   - Bitmap format
   - White background
   - Compatible with legacy systems

5. **PRINTLOGO.bmp**
   - Thermal printer optimized
   - 1-bit color depth
   - Specifically designed for receipt printers

## Error Handling

The application includes comprehensive error handling for:
- Invalid input files
- Unsupported file formats
- Write permission issues
- Processing failures

Error messages are displayed in pop-up dialogs and logged for troubleshooting.