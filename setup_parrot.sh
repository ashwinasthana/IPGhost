#!/bin/bash

echo "🦜 IPGhost Setup for Parrot OS"
echo "================================"

# Clear any old installations
echo "[1/5] Clearing old installations..."
sudo rm -rf /usr/share/ipghost 2>/dev/null
sudo rm -f /usr/bin/ipghost 2>/dev/null
sudo rm -rf ~/.ipghost 2>/dev/null
rm -rf __pycache__ *.pyc 2>/dev/null

# Install dependencies
echo "[2/5] Installing dependencies..."
sudo apt update
sudo apt install -y python3-requests python3-socks tor

# Start and enable Tor
echo "[3/5] Setting up Tor service..."
sudo systemctl enable tor
sudo systemctl start tor

# Clear Python cache
echo "[4/5] Clearing Python cache..."
find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -delete 2>/dev/null

# Make executable
echo "[5/5] Setting permissions..."
chmod +x ipghost.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 Run IPGhost:"
echo "   sudo python3 ipghost.py"
echo ""
echo "🌐 Configure your browser:"
echo "   SOCKS5 proxy: 127.0.0.1:9050"