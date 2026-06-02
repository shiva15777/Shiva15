#!/usr/bin/env python3
"""
Hermus Setup Script

This script helps set up and run the Hermus audio processing tool.
"""

import os
import sys
import subprocess
import platform

def check_python():
    """Check Python version"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor} detected")

def check_ffmpeg():
    """Check if FFmpeg is installed"""
    try:
        subprocess.run(['ffmpeg', '-version'], 
                      capture_output=True, check=True)
        print("✅ FFmpeg is installed")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg is not installed")
        print("\nInstall FFmpeg:")
        if platform.system() == "Windows":
            print("  - Download: https://ffmpeg.org/download.html")
            print("  - Or: choco install ffmpeg")
        elif platform.system() == "Darwin":
            print("  - Run: brew install ffmpeg")
        else:
            print("  - Run: sudo apt-get install ffmpeg")
        return False

def create_directories():
    """Create necessary directories"""
    dirs = ['uploads', 'outputs', 'temp', 'static', 'templates', 'utils']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)
    print("✅ Directories created")

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import librosa
        import soundfile
        import pydub
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def main():
    print("🎵 Hermus Setup")
    print("=" * 50)
    
    check_python()
    check_ffmpeg()
    create_directories()
    
    if not check_dependencies():
        print("\nInstall dependencies with:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("✅ Setup complete!")
    print("\nTo start the application:")
    print("  python app.py")
    print("\nThen open: http://localhost:5000")

if __name__ == '__main__':
    main()