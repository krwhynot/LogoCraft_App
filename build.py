import os
import sys
import subprocess
import shutil
import venv
from pathlib import Path
import ctypes

def is_admin():
    """Check if the script is running with admin privileges"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_command(cmd, error_message, shell=False):
    """Run a command and handle any errors"""
    try:
        subprocess.run(cmd, check=True, shell=shell)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {error_message}")
        print(f"Command failed with error: {e}")
        return False
    except Exception as e:
        print(f"Error: {error_message}")
        print(f"Unexpected error: {e}")
        return False

def temporarily_disable_defender():
    """Temporarily disable Windows Defender (requires admin privileges)"""
    if not is_admin():
        print("Warning: Admin privileges required to manage Windows Defender")
        return False
    
    try:
        # Disable real-time monitoring temporarily
        subprocess.run([
            'powershell', 
            'Set-MpPreference', 
            '-DisableRealtimeMonitoring', 
            '$true'
        ], capture_output=True)
        return True
    except Exception as e:
        print(f"Failed to disable Windows Defender: {e}")
        return False

def restore_defender():
    """Re-enable Windows Defender"""
    try:
        subprocess.run([
            'powershell', 
            'Set-MpPreference', 
            '-DisableRealtimeMonitoring', 
            '$false'
        ], capture_output=True)
    except Exception as e:
        print(f"Warning: Failed to restore Windows Defender: {e}")
        print("Please ensure Windows Defender is re-enabled manually")

def build_executable():
    """Build the LogoCraft executable with proper environment setup."""
    project_dir = Path.cwd()
    venv_dir = project_dir / ".venv"
    
    print(f"Project directory: {project_dir}")
    print(f"Virtual environment directory: {venv_dir}")

    # Create virtual environment if needed
    if not venv_dir.exists():
        print("Creating virtual environment...")
        try:
            venv.create(venv_dir, with_pip=True)
        except Exception as e:
            print(f"Error creating virtual environment: {e}")
            return False
    
    # Get Python paths
    python_path = venv_dir / "Scripts" / "python.exe"
    print(f"Using Python at: {python_path}")

    # Install requirements
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

    # Temporarily disable Windows Defender
    defender_disabled = temporarily_disable_defender()
    if not defender_disabled:
        print("Warning: Building without disabling Windows Defender")
        print("You may need to add an exclusion manually if the build fails")
    
    try:
        # Build executable
        print("Building executable...")
        if not run_command(
            [str(python_path), "-m", "PyInstaller", "--clean", "LogoCraft.spec"],
            "Failed to build executable"
        ):
            return False

        # Verify the executable
        expected_exe = project_dir / "dist" / "LogoCraft.exe"
        if not expected_exe.exists():
            print(f"Error: Expected executable not found at {expected_exe}")
            return False

        print("\nBuild process completed successfully!")
        print(f"Executable can be found at: {expected_exe}")
        
        return True
    finally:
        # Always try to restore Windows Defender
        if defender_disabled:
            restore_defender()

if __name__ == "__main__":
    # Check for admin privileges
    if not is_admin():
        print("Warning: Running without admin privileges")
        print("Some security features may not work correctly")
    
    print(f"Running with Python {sys.version}")
    success = build_executable()
    
    if success:
        print("\nBuild completed successfully!")
        print("\nNext steps:")
        print("1. Test the executable")
        print("2. If Windows Defender blocks the exe, add it to exclusions")
        print("3. Verify all functionality works as expected")
    else:
        print("\nBuild failed! Please check the error messages above.")
        sys.exit(1)