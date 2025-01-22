# LogoCraft Installation Guide

## System Requirements

### Windows
- Windows 10 or later
- Python 3.8 or later
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### macOS
- macOS 10.14 (Mojave) or later
- Python 3.8 or later
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space

### Linux
- Modern Linux distribution (Ubuntu 20.04+, Fedora 34+, etc.)
- Python 3.8 or later
- 4GB RAM minimum (8GB recommended)
- 500MB free disk space
- X11 or Wayland display server

## Prerequisites

1. **Python Installation**
   - Download and install Python 3.8 or later from [python.org](https://python.org)
   - Ensure Python is added to your system PATH
   - Verify installation:
     ```bash
     python --version
     ```

2. **Development Tools**
   - Windows: Microsoft Visual C++ Build Tools (for PyQt6)
   - Linux: Required packages for PyQt6:
     ```bash
     # Ubuntu/Debian
     sudo apt-get install python3-dev build-essential libgl1-mesa-dev

     # Fedora
     sudo dnf install python3-devel gcc mesa-libGL-devel
     ```
   - macOS: Xcode Command Line Tools:
     ```bash
     xcode-select --install
     ```

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/LogoCraft_App.git
   cd LogoCraft_App
   ```

2. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS/Linux
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Environment Setup**
   - No .env file is required for basic operation
   - The application uses default configurations in `src/config.py`
   - Output directory defaults to user's Desktop

2. **Application Settings**
   - Default image formats are configured in `src/config.py`
   - Supported formats:
     - PNG (300×300, 136×136, 140×112)
     - BMP (155×110, 600×256 thermal printer format)

## Running the Application

1. **Development Mode**
   ```bash
   # Ensure virtual environment is activated
   python run.py
   ```

2. **Building Executable (Optional)**
   ```bash
   # Windows
   python build.py

   # Output will be in dist/LogoCraft.exe
   ```

## Troubleshooting

### Common Issues

1. **PyQt6 Installation Errors**
   - Windows:
     ```bash
     pip install --upgrade pip
     pip install PyQt6 --force-reinstall
     ```
   - Linux:
     ```bash
     # Ensure Qt dependencies are installed
     sudo apt-get install qt6-base-dev  # Ubuntu/Debian
     sudo dnf install qt6-qtbase-devel  # Fedora
     ```

2. **Image Processing Errors**
   - Ensure Pillow is properly installed:
     ```bash
     pip uninstall Pillow
     pip install Pillow
     ```

3. **Permission Issues**
   - Windows: Run as administrator if needed
   - Linux/macOS: Check file permissions:
     ```bash
     chmod +x run.py
     ```

### Verification

To verify the installation:

1. Run the application:
   ```bash
   python run.py
   ```

2. Test image processing:
   - Load any image file
   - Select output formats
   - Process the image
   - Check output files on Desktop

## Support

For additional support:
1. Check the [ARCHITECTURE.md](ARCHITECTURE.md) for system understanding
2. Review error logs in the application output
3. Submit issues on the project repository

## Updating

To update the application:

1. Pull latest changes:
   ```bash
   git pull origin main
   ```

2. Update dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

## Development Setup (Optional)

For development work:

1. Install development dependencies:
   ```bash
   pip install pytest pytest-qt pytest-cov
   ```

2. Run tests:
   ```bash
   pytest tests/
   ```

3. Code formatting tools:
   ```bash
   pip install black isort
   black .
   isort .
