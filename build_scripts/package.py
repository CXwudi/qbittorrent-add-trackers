#!/usr/bin/env python3
"""Package the application using PyInstaller."""

import subprocess
import sys


def main():
    """Package the application."""
    cmd = [
        "pyinstaller",
        "--onefile",
        "--name", "qbittorrent-add-trackers",
        "src/qbittorrent_add_trackers/main.py"
    ]
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd)
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()