#!/usr/bin/env python3
"""
Setup script for Octopus Ink Slime game.
This script installs required dependencies, sets up the game environment, and creates shortcuts.
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path


def print_header(message):
    """Print a formatted header message."""
    print("\n" + "=" * 60)
    print(f" {message}")
    print("=" * 60)


def print_step(message):
    """Print a step message."""
    print(f"\n>> {message}")


def check_python_version():
    """Check if the Python version is compatible."""
    print_step("Checking Python version...")
    
    major, minor = sys.version_info[:2]
    if major < 3 or (major == 3 and minor < 7):
        print(f"Error: Python 3.7 or higher is required. You have {major}.{minor}.")
        return False
        
    print(f"Python version {major}.{minor} is compatible.")
    return True


def install_dependencies():
    """Install required dependencies using pip."""
    print_step("Installing dependencies...")
    
    dependencies = [
        "pygame>=2.0.0",
        "psutil>=5.8.0",
        "numpy>=1.19.0",
        "pillow>=8.0.0",  # For image processing
    ]
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + dependencies)
        print("Dependencies installed successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def create_directories():
    """Create necessary directories if they don't exist."""
    print_step("Creating directories...")
    
    directories = [
        "assets/images",
        "assets/sounds",
        "assets/fonts",
        "assets/animations",
        "assets/sprite_sheets",
        "logs",
        "data",
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    return True


def create_desktop_shortcut():
    """Create a desktop shortcut for the game."""
    print_step("Creating desktop shortcut...")
    
    # Get the desktop path
    if platform.system() == "Windows":
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop_path, "Octopus Ink Slime.lnk")
        
        try:
            # Create a Windows shortcut
            import winshell
            from win32com.client import Dispatch
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = sys.executable
            shortcut.Arguments = os.path.abspath("main.py")
            shortcut.WorkingDirectory = os.path.abspath(".")
            shortcut.IconLocation = os.path.abspath("assets/images/icon.ico")
            shortcut.save()
            
            print(f"Created desktop shortcut at: {shortcut_path}")
            return True
        except ImportError:
            print("Could not create Windows shortcut. Please install pywin32 and winshell.")
            return False
        except Exception as e:
            print(f"Error creating Windows shortcut: {e}")
            return False
    
    elif platform.system() == "Linux":
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        shortcut_path = os.path.join(desktop_path, "octopus-ink-slime.desktop")
        
        try:
            # Create a Linux .desktop file
            with open(shortcut_path, "w") as f:
                f.write("[Desktop Entry]\n")
                f.write("Type=Application\n")
                f.write("Name=Octopus Ink Slime\n")
                f.write(f"Exec={sys.executable} {os.path.abspath('main.py')}\n")
                f.write(f"Path={os.path.abspath('.')}\n")
                f.write("Terminal=false\n")
                f.write("Categories=Game;\n")
                
            # Make the .desktop file executable
            os.chmod(shortcut_path, 0o755)
            
            print(f"Created desktop shortcut at: {shortcut_path}")
            return True
        except Exception as e:
            print(f"Error creating Linux shortcut: {e}")
            return False
    
    elif platform.system() == "Darwin":  # macOS
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        app_path = os.path.join(desktop_path, "Octopus Ink Slime.app")
        
        try:
            # Create a macOS .app bundle
            os.makedirs(os.path.join(app_path, "Contents", "MacOS"), exist_ok=True)
            
            # Create the launcher script
            with open(os.path.join(app_path, "Contents", "MacOS", "launcher.sh"), "w") as f:
                f.write("#!/bin/bash\n")
                f.write(f"cd {os.path.abspath('.')}\n")
                f.write(f"{sys.executable} {os.path.abspath('main.py')}\n")
                
            # Make the launcher script executable
            os.chmod(os.path.join(app_path, "Contents", "MacOS", "launcher.sh"), 0o755)
            
            # Create the Info.plist file
            with open(os.path.join(app_path, "Contents", "Info.plist"), "w") as f:
                f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                f.write('<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n')
                f.write('<plist version="1.0">\n')
                f.write('<dict>\n')
                f.write('    <key>CFBundleExecutable</key>\n')
                f.write('    <string>launcher.sh</string>\n')
                f.write('    <key>CFBundleIdentifier</key>\n')
                f.write('    <string>com.octopus.inkslime</string>\n')
                f.write('    <key>CFBundleName</key>\n')
                f.write('    <string>Octopus Ink Slime</string>\n')
                f.write('    <key>CFBundlePackageType</key>\n')
                f.write('    <string>APPL</string>\n')
                f.write('</dict>\n')
                f.write('</plist>\n')
                
            print(f"Created desktop shortcut at: {app_path}")
            return True
        except Exception as e:
            print(f"Error creating macOS shortcut: {e}")
            return False
    
    else:
        print(f"Unsupported platform: {platform.system()}")
        return False


def setup_game():
    """Set up the game environment."""
    print_step("Setting up game environment...")
    
    # Create a configuration file
    config_path = "config.ini"
    if not os.path.exists(config_path):
        with open(config_path, "w") as f:
            f.write("[Graphics]\n")
            f.write("fullscreen = False\n")
            f.write("resolution = 800x600\n")
            f.write("vsync = True\n")
            f.write("\n")
            f.write("[Audio]\n")
            f.write("music_volume = 0.7\n")
            f.write("sound_volume = 1.0\n")
            f.write("\n")
            f.write("[Controls]\n")
            f.write("move_up = UP\n")
            f.write("move_down = DOWN\n")
            f.write("move_left = LEFT\n")
            f.write("move_right = RIGHT\n")
            f.write("shoot = SPACE\n")
            f.write("pause = ESCAPE\n")
            f.write("debug = F3\n")
            
        print(f"Created configuration file: {config_path}")
    
    # Create a high scores file
    scores_path = "data/highscores.json"
    if not os.path.exists(scores_path):
        os.makedirs(os.path.dirname(scores_path), exist_ok=True)
        with open(scores_path, "w") as f:
            f.write("{\n")
            f.write('    "scores": []\n')
            f.write("}\n")
            
        print(f"Created high scores file: {scores_path}")
    
    return True


def make_executable():
    """Make the main.py file executable."""
    print_step("Making main.py executable...")
    
    try:
        # Make main.py executable
        os.chmod("main.py", 0o755)
        print("Made main.py executable.")
        return True
    except Exception as e:
        print(f"Error making main.py executable: {e}")
        return False


def main():
    """Main setup function."""
    print_header("Octopus Ink Slime - Setup")
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("Warning: Some dependencies could not be installed.")
        
    # Create directories
    create_directories()
    
    # Set up game environment
    setup_game()
    
    # Make main.py executable
    if platform.system() != "Windows":
        make_executable()
    
    # Create desktop shortcut
    create_desktop_shortcut()
    
    print_header("Setup Complete!")
    print("\nYou can now run the game by executing:")
    print(f"  {sys.executable} main.py")
    
    if platform.system() == "Windows":
        print("\nOr double-click on the desktop shortcut.")
    else:
        print("\nOr use the desktop shortcut.")
    
    print("\nEnjoy playing Octopus Ink Slime!")


if __name__ == "__main__":
    main()