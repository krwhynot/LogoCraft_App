# LogoCraft: Professional Logo Conversion Solution

## Application Overview

LogoCraft streamlines logo management for restaurant businesses, providing a professional-grade image conversion platform. Our application efficiently transforms logos across multiple formats to meet diverse business communication needs.

## Core Capabilities

### Supported Image Formats
- PNG
- JPEG
- BMP
- Photoshop Files (PSD)
- HEIF Images

### Standardized Output Configurations
- Standard logo (300x300 PNG)
- Compact logo (136x136 PNG)
- Kitchen Display logo (140x112 PNG)
- Report logo (155x110 BMP)
- Print-optimized format

## System Prerequisites

### Technical Requirements
- Operating System: Windows 10/11
- Python Version: 3.8+
- Recommended: Isolated development environment

## Implementation Guide

### Quick Setup Process

1. Repository Acquisition
   ```bash
   git clone https://github.com/krwhynot/LogoCraft_App.git
   cd LogoCraft_App
   ```

2. Environment Configuration
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # macOS/Linux
   ```

3. Dependency Installation
   ```bash
   pip install -r requirements.txt
   ```

## Operational Workflow

1. Launch Application
2. Select Source Logo
3. Choose Desired Output Formats
4. Specify Destination Directory
5. Execute Conversion

## Technical Architecture

### Key Technologies
- PyQt6: Modern UI Framework
- Pillow: Advanced Image Processing
- pillow-heif: Specialized Format Support

### Deployment
```bash
python build.py
```

