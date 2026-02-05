# IPGhost 👻

**Advanced Tor IP Rotation Tool**  
*Created by Ashwin Asthana*

IPGhost is a powerful, cross-platform tool for automatic IP address rotation using the Tor network. Built for privacy enthusiasts and security professionals who need reliable IP anonymization.

## ✨ Features

- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Simple Installation**: One-command setup with automatic dependency handling
- **Fast IP Rotation**: Quick and reliable IP address changes
- **Clean Interface**: Professional terminal UI with colored output
- **Automatic Tor Management**: Handles Tor service startup and configuration
- **Flexible Timing**: Customizable rotation intervals
- **Graceful Shutdown**: Clean exit with Ctrl+C handling

## 🚀 Quick Start

### Universal Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd ipghost
   ```

2. **Install dependencies:**
   ```bash
   # Linux (Debian/Ubuntu/Parrot)
   sudo apt install python3-requests python3-socks tor
   
   # Linux (Red Hat/CentOS)
   sudo yum install python3-requests python3-socks tor
   
   # macOS
   brew install tor && pip3 install requests[socks]
   
   # Windows
   pip install requests[socks]
   # + Install Tor Browser manually
   ```

3. **Run IPGhost:**
   ```bash
   sudo python3 ipghost.py
   ```

## 📋 Requirements

- Python 3.6+
- Tor (automatically installed)
- Internet connection

### Dependencies
- `python3-requests`
- `python3-socks`

**Note for Debian/Ubuntu/Parrot users:** Dependencies are automatically installed via apt.

## 🖥️ Usage

1. **Start IPGhost:**
   ```bash
   ipghost
   ```

2. **Configure your browser:**
   - Set SOCKS5 proxy to: `127.0.0.1:9050`

3. **Set parameters:**
   - IP change interval (default: 60 seconds)
   - Number of changes (0 for infinite)

### Browser Configuration

#### Firefox
1. Settings → Network Settings
2. Manual proxy configuration
3. SOCKS Host: `127.0.0.1`, Port: `9050`
4. Select SOCKS v5

#### Chrome
```bash
google-chrome --proxy-server="socks5://127.0.0.1:9050"
```

## 🔧 Configuration

IPGhost automatically creates configuration files in `~/.ipghost/` with optimal settings for:
- Tor port configuration
- IP checking services
- Timeout settings
- Retry logic

## 🔍 Troubleshooting

### Common Issues

1. **Dependencies error:**
   ```bash
   sudo apt install python3-requests python3-socks
   ```

2. **Permission denied:**
   - Run installer with `sudo`

3. **Tor connection timeout:**
   ```bash
   sudo systemctl restart tor
   # Wait 30 seconds, then retry
   ```

4. **IP not changing:**
   - Wait longer between changes
   - Check network connectivity
   - Restart Tor service

### Logs

Check logs at: `~/.ipghost/ipghost.log`

## 🛡️ Security Notes

- Routes all traffic through Tor network
- Verify IP changes before sensitive activities
- Use HTTPS websites for additional security
- Consider Tor Browser for maximum anonymity

## 📊 Cross-Platform Compatibility

| OS | Status | Setup Command |
|---|---|---|
| **Linux (Debian/Ubuntu/Parrot)** | ✅ Full Support | `sudo apt install python3-requests python3-socks tor` |
| **Linux (Red Hat/CentOS)** | ✅ Full Support | `sudo yum install python3-requests python3-socks tor` |
| **Linux (Arch)** | ✅ Full Support | `sudo pacman -S python-requests python-socks tor` |
| **macOS** | ✅ Full Support | `brew install tor && pip3 install requests[socks]` |
| **Windows** | ⚠️ Manual Setup | Install Tor Browser + `pip install requests[socks]` |

### Universal Setup

**For any Linux distribution:**
```bash
# Clone and setup
git clone <repository-url>
cd ipghost

# Install dependencies (choose your package manager)
sudo apt install python3-requests python3-socks tor     # Debian/Ubuntu/Parrot
sudo yum install python3-requests python3-socks tor     # Red Hat/CentOS
sudo pacman -S python-requests python-socks tor         # Arch Linux

# Run IPGhost
sudo python3 ipghost.py
```

**For macOS:**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install dependencies
brew install tor
pip3 install requests[socks]

# Run IPGhost
sudo python3 ipghost.py
```

**For Windows:**
1. Install [Tor Browser](https://www.torproject.org/download/)
2. Install Python dependencies: `pip install requests[socks]`
3. Run: `python ipghost.py`

## 🎯 Use Cases

- **Privacy Protection**: Anonymous web browsing
- **Security Testing**: Penetration testing and research
- **Geo-restriction Bypass**: Access region-locked content
- **Development**: Testing applications with different IPs
- **Research**: Academic and security research

## 📝 License

Open source project. Use responsibly and in accordance with local laws.

## ⚠️ Disclaimer

This tool is for educational and legitimate privacy purposes only. Users must comply with all applicable laws and regulations. The author is not responsible for any misuse.

## 🤝 Contributing

Contributions welcome! Submit pull requests or open issues for:
- Bug reports
- Feature requests
- Documentation improvements
- Code optimizations

## 📞 Support

Having issues?
1. Check the troubleshooting section above
2. Review logs at `~/.ipghost/ipghost.log`
3. Open an issue with system details and error messages

---

**IPGhost** - Your digital anonymity companion 👻