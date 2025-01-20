# LogoCraft Repository Map

## 📂 Project Structure

### Root Directory
- `README.md`: Project overview and documentation
- `REPO_MAP.md`: Detailed repository structure
- `requirements.txt`: Python package dependencies
- `build.py`: PyInstaller build script
- `run.py`: Application entry point
- `file_version_info.txt`: Windows executable metadata
- `HungerRush_Icon.ico`: Application icon
- `logocraft.log`: Application log file
- `.gitignore`: Version control ignore rules

### Configuration and Migration Docs
- `Project Migration Requirements and Setup.md`: PyQt6 migration details
- `PyQt6 Migration Testing Strategy.md`: Testing approach documentation

### Source Code (`src/`)
```
src/
│
├── gui/                    # User Interface Components
│   ├── main_window.py      # Primary application window
│   ├── dialogs.py          # Custom dialog implementations
│   └── widgets.py          # Reusable widget components
│
├── processors/             # Image Processing Logic
│   ├── image_converter.py  # Core conversion algorithms
│   ├── format_handlers.py  # Output format specifications
│   └── quality_control.py  # Image quality preservation
│
└── utils/                  # Utility Functions
    ├── config.py           # Configuration management
    ├── logging.py          # Logging utilities
    └── helpers.py          # General helper functions
```

### Virtual Environment
- `.venv/`: Python virtual environment
  - Contains isolated project dependencies

## 🔧 Development Workflow
1. Virtual Environment Setup
2. Dependency Installation
3. Testing
4. Build Process
5. Executable Generation

## 🧪 Testing Framework
- Unit Testing: Individual component verification
- Integration Testing: Cross-component interactions
- Performance Testing: Resource utilization

## 🚀 Build and Deployment
- `build.py`: Handles PyInstaller packaging
- Generates standalone executable in `dist/` directory

## 📦 Dependency Management
- `requirements.txt`: Tracks all Python package dependencies
- Key dependencies include PyQt6, Pillow, pillow-heif

## 🔄 Migration Notes
- Transitioned from previous GUI framework to PyQt6
- Maintained core image processing logic
- Enhanced user interface and performance