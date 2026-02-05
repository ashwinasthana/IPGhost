# IPGhost 👻

**Advanced Tor IP Rotation Tool**  
*Created by Ashwin Asthana*

IPGhost is a sophisticated, cross-platform tool for automatic IP address rotation using the Tor network. It's designed with security, reliability, and ease of use in mind.

## ✨ Features

- **Cross-Platform**: Works on Linux, macOS, and Windows
- **Automatic Installation**: Installs and configures Tor automatically
- **Smart Retry Logic**: Robust error handling and retry mechanisms
- **Configuration Management**: JSON-based configuration with sensible defaults
- **Logging**: Comprehensive logging to file and console
- **Multiple IP Services**: Uses multiple IP checking services for reliability
- **Graceful Shutdown**: Handles interrupts cleanly
- **Service Management**: Automatic Tor service start/stop/reload

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd IPGhost
   ```

2. **Install IPGhost:**
   ```bash
   # Linux/macOS (requires sudo)
   sudo python3 install.py install
   
   # Windows (run as administrator)
   python install.py install
   ```

3. **Run IPGhost:**
   ```bash
   # Linux/macOS
   ipghost
   
   # Windows
   ipghost.bat
   ```

### Manual Usage

If you prefer not to install system-wide:

```bash
python3 ipghost.py
```

## 📋 Requirements

- Python 3.6+
- Tor (automatically installed if not present)
- Internet connection

### Python Dependencies
- `requests[socks]` (automatically installed)

## 🔧 Configuration

IPGhost creates a configuration file at `~/.ipghost/config.json` with the following options:

```json
{
  "tor_port": 9050,
  "control_port": 9051,
  "check_ip_urls": [
    "http://checkip.amazonaws.com",
    "http://ipinfo.io/ip",
    "http://icanhazip.com"
  ],
  "timeout": 10,
  "max_retries": 3
}
```

## 🖥️ Usage

### Basic Usage

1. **Start IPGhost:**
   ```bash
   ipghost
   ```

2. **Configure your browser/application:**
   - Set SOCKS5 proxy to: `127.0.0.1:9050`

3. **Set rotation parameters:**
   - IP change interval (default: 60 seconds)
   - Number of changes (0 for infinite)

### Browser Configuration

#### Firefox
1. Go to Settings → Network Settings
2. Select "Manual proxy configuration"
3. Set SOCKS Host: `127.0.0.1`, Port: `9050`
4. Select "SOCKS v5"

#### Chrome
Use with proxy extensions or command line:
```bash
google-chrome --proxy-server="socks5://127.0.0.1:9050"
```

## 📊 Management Commands

### Check Installation Status
```bash
python3 install.py status
```

### Uninstall
```bash
sudo python3 install.py uninstall  # Linux/macOS
python install.py uninstall        # Windows
```

## 🔍 Troubleshooting

### Common Issues

1. **"Tor not found" error:**
   - IPGhost will attempt to install Tor automatically
   - On some systems, manual installation may be required

2. **Permission denied:**
   - Run installer with `sudo` on Linux/macOS
   - Run as administrator on Windows

3. **Connection timeout:**
   - Check if Tor service is running
   - Verify firewall settings
   - Try different IP checking URLs

4. **IP not changing:**
   - Tor may assign the same exit node
   - Wait longer between changes
   - Check Tor logs for issues

### Logs

Logs are stored at `~/.ipghost/ipghost.log` and include:
- IP change events
- Error messages
- Service status updates

## 🛡️ Security Notes

- IPGhost routes traffic through Tor for anonymity
- Always verify your IP has changed before sensitive activities
- Use HTTPS websites when possible for additional security
- Be aware of DNS leaks - consider using Tor Browser for maximum security

## 🔄 Comparison with Original

IPGhost improves upon the original Auto_Tor_IP_changer with:

| Feature | Original | IPGhost |
|---------|----------|---------|
| Cross-platform | Linux only | Linux, macOS, Windows |
| Error handling | Basic | Comprehensive |
| Configuration | Hardcoded | JSON config file |
| Logging | Print statements | Professional logging |
| Installation | Manual | Automated installer |
| Service management | Basic | Advanced |
| Code quality | Basic | Production-ready |
| Documentation | Minimal | Comprehensive |

## 📝 License

This project is open source. Use responsibly and in accordance with local laws.

## ⚠️ Disclaimer

This tool is for educational and legitimate privacy purposes only. Users are responsible for complying with all applicable laws and regulations. The authors are not responsible for any misuse of this software.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review the logs at `~/.ipghost/ipghost.log`
3. Open an issue with detailed information about your system and the problem