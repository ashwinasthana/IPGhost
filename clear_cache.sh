#!/bin/bash

# IPGhost Cache Cleaner
echo "Clearing all caches..."

# Clear Python cache
rm -rf __pycache__ *.pyc
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -delete 2>/dev/null

# Clear old config
rm -rf ~/.ipghost 2>/dev/null

# Clear system installations
sudo rm -rf /usr/share/ipghost 2>/dev/null
sudo rm -f /usr/bin/ipghost 2>/dev/null
sudo rm -f /usr/local/bin/ipghost 2>/dev/null

# Clear any running processes
sudo pkill -f ipghost 2>/dev/null

echo "✓ All caches cleared!"
echo "Now run: python3 ipghost.py"