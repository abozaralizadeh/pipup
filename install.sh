#!/bin/bash
# Installation script for pipup

echo "Installing pipup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Install pipup in development mode
pip3 install -e .

echo "Installation complete!"
echo "You can now use 'pipup' command to update your requirements.txt files."
echo ""
echo "Usage examples:"
echo "  pipup requirements.txt"
echo "  pipup requirements.txt --dry-run"
echo "  pipup requirements-dev.txt"
