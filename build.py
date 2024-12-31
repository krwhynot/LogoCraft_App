import os
import sys
import subprocess
import shutil
import venv
from pathlib import Path

def verify_icon():
    """Verify that the icon file exists and is accessible."""
    icon_path = Path("HungerRush_Icon.ico")
    if not icon_path.exists():
        print(f"Error: Icon file not found at {icon_path.absolute()}")
        return False
    try:
        with open(icon_path, 'rb') as f:
            # Just try to read the file to ensure it's accessible
            f.read(10)
        return True
    except Exception as e:
        print(f"Error accessing icon file: {e}")
        return False

def run_command(cmd, error_message):
    """Run a command and handle any errors"""
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message}")
        print(f"Command failed with error: {e}")
        return False
    except Exception as e:
        print(f"Error: {error_message}")
        print(f"Unexpected error: {e}")
        return False

def build_executable():
    """Build the LogoCraft executable with proper environment setup."""
    # Get the absolute path to the project directory
    project_dir = Path.cwd()
    venv_dir = project_dir / ".venv"

    print(f"Project directory: {project_dir}")
    print(f"Virtual environment directory: {venv_dir}")

    # Verify icon file first
    print("Verifying icon file...")
    if not verify_icon():
        return False

    # Create virtual environment if it doesn't exist
    if not venv_dir.exists():
        print("Creating virtual environment...")
        try:
            venv.create(venv_dir, with_pip=True)
        except Exception as e:
            print(f"Error creating virtual environment: {e}")
            return False

    # Get the path to the Python executable in the virtual environment
    if os.name == 'nt':  # Windows
        python_path = venv_dir / "Scripts" / "python.exe"
        pip_path = venv_dir / "Scripts" / "pip.exe"
    else:  # Unix-like
        python_path = venv_dir / "bin" / "python"
        pip_path = venv_dir / "bin" / "pip"

    print(f"Using Python at: {python_path}")
    print(f"Using pip at: {pip_path}")

    if not python_path.exists():
        print(f"Error: Python executable not found at {python_path}")
        return False

    # Install required packages
    print("Installing dependencies...")
    if not run_command(
        [str(python_path), "-m", "pip", "install", "-r", "requirements.txt"],
        "Failed to install requirements"
    ):
        return False

    print("Installing PyInstaller...")
    if not run_command(
        [str(python_path), "-m", "pip", "install", "pyinstaller"],
        "Failed to install PyInstaller"
    ):
        return False

    # Clean previous builds
    print("Cleaning previous builds...")
    for dir_name in ['build', 'dist']:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)

    # Run PyInstaller
    print("Building executable...")
    if not run_command(
        [str(python_path), "-m", "PyInstaller", "--clean", "LogoCraft.spec"],
        "Failed to build executable"
    ):
        return False

    # Verify the executable was created
    expected_exe = project_dir / "dist" / "LogoCraft.exe"
    if not expected_exe.exists():
        print(f"Error: Expected executable not found at {expected_exe}")
        return False

    print("\nBuild process completed successfully!")
    print(f"Executable can be found at: {expected_exe}")
    print("\nRecommended next steps:")
    print("1. Test the executable by double-clicking it")
    print("2. Try processing a test image to verify functionality")
    print("3. Check that the icon appears correctly")
    return True

if __name__ == "__main__":
    # Ensure we're running with the correct Python version
    print(f"Running with Python {sys.version}")
    if build_executable():
        print("\nBuild completed successfully!")
    else:
        print("\nBuild failed! Please check the error messages above.")
        sys.exit(1)
