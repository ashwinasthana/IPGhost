#!/bin/bash

# IPGhost Launcher Script
# Quick launcher for IPGhost with environment checks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "  ██▓ ██▓███    ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓"
echo " ▓██▒▓██░  ██▒ ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒"
echo " ▒██▒▓██░ ██▓▒▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░"
echo " ░██░▒██▄█▓▒ ▒░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ "
echo " ░██░▒██▒ ░  ░░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ "
echo " ░▓  ▒▓▒░ ░  ░ ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   "
echo "  ▒ ░░▒ ░       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    "
echo "  ▒ ░░░       ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░      "
echo "  ░                 ░  ░  ░  ░    ░ ░        ░           "
echo -e "${NC}"
echo -e "${GREEN}IPGhost Launcher - by Ashwin Asthana${NC}"
echo

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Check if ipghost.py exists
if [ ! -f "ipghost.py" ]; then
    echo -e "${RED}Error: ipghost.py not found in current directory${NC}"
    exit 1
fi

# Check if requirements are installed
echo -e "${YELLOW}Checking dependencies...${NC}"
if ! python3 -c "import requests" &> /dev/null; then
    echo -e "${YELLOW}Installing requirements...${NC}"
    python3 -m pip install -r requirements.txt
fi

echo -e "${GREEN}Starting IPGhost...${NC}"
echo

# Launch IPGhost
python3 ipghost.py