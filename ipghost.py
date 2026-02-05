#!/usr/bin/env python3
"""
IPGhost - Advanced Tor IP Changer
A sophisticated tool for automatic IP address rotation using Tor network
Created by Ashwin Asthana
"""

import os
import sys
import time
import json
import signal
import logging
import platform
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Installing required dependencies...")
    try:
        # Try system packages first
        subprocess.check_call(['apt', 'install', '-y', 'python3-requests', 'python3-socks'])
    except (subprocess.CalledProcessError, FileNotFoundError):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests[socks]"])
        except subprocess.CalledProcessError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "requests[socks]"])
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry

class IPGhost:
    def __init__(self):
        self.config_file = Path.home() / ".ipghost" / "config.json"
        self.log_file = Path.home() / ".ipghost" / "ipghost.log"
        self.setup_directories()
        self.setup_logging()
        self.config = self.load_config()
        self.session = self.create_session()
        self.running = True
        
    def setup_directories(self):
        """Create necessary directories"""
        config_dir = Path.home() / ".ipghost"
        config_dir.mkdir(exist_ok=True)
        
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        default_config = {
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
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return {**default_config, **config}
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}. Using defaults.")
                
        self.save_config(default_config)
        return default_config
        
    def save_config(self, config: Dict[str, Any]):
        """Save configuration to file"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
            
    def create_session(self) -> requests.Session:
        """Create requests session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=self.config["max_retries"],
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
        
    def check_tor_installation(self) -> bool:
        """Check if Tor is installed"""
        try:
            result = subprocess.run(['tor', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
            
    def install_tor(self) -> bool:
        """Install Tor based on the operating system"""
        system = platform.system().lower()
        
        try:
            if system == "linux":
                # Check for different package managers
                if subprocess.run(['which', 'apt'], capture_output=True).returncode == 0:
                    subprocess.run(['sudo', 'apt', 'update'], check=True)
                    subprocess.run(['sudo', 'apt', 'install', 'tor', '-y'], check=True)
                elif subprocess.run(['which', 'yum'], capture_output=True).returncode == 0:
                    subprocess.run(['sudo', 'yum', 'install', 'tor', '-y'], check=True)
                elif subprocess.run(['which', 'pacman'], capture_output=True).returncode == 0:
                    subprocess.run(['sudo', 'pacman', '-S', 'tor', '--noconfirm'], check=True)
                    
            elif system == "darwin":  # macOS
                if subprocess.run(['which', 'brew'], capture_output=True).returncode == 0:
                    subprocess.run(['brew', 'install', 'tor'], check=True)
                else:
                    self.logger.error("Homebrew not found. Please install Homebrew first.")
                    return False
                    
            elif system == "windows":
                self.logger.error("Please install Tor Browser or Tor service manually on Windows")
                return False
                
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to install Tor: {e}")
            return False
            
    def start_tor_service(self) -> bool:
        """Start Tor service"""
        system = platform.system().lower()
        
        try:
            if system == "linux":
                subprocess.run(['sudo', 'systemctl', 'start', 'tor'], check=True)
                subprocess.run(['sudo', 'systemctl', 'enable', 'tor'], check=True)
            elif system == "darwin":
                subprocess.run(['brew', 'services', 'start', 'tor'], check=True)
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to start Tor service: {e}")
            return False
            
    def get_current_ip(self) -> Optional[str]:
        """Get current IP address through Tor proxy"""
        proxies = {
            'http': f'socks5://127.0.0.1:{self.config["tor_port"]}',
            'https': f'socks5://127.0.0.1:{self.config["tor_port"]}'
        }
        
        for url in self.config["check_ip_urls"]:
            try:
                response = self.session.get(
                    url, 
                    proxies=proxies, 
                    timeout=self.config["timeout"]
                )
                if response.status_code == 200:
                    return response.text.strip()
            except Exception as e:
                self.logger.debug(f"Failed to get IP from {url}: {e}")
                continue
                
        return None
        
    def change_ip(self) -> bool:
        """Change IP by reloading Tor circuit"""
        system = platform.system().lower()
        
        try:
            if system == "linux":
                subprocess.run(['sudo', 'systemctl', 'reload', 'tor'], check=True)
            elif system == "darwin":
                subprocess.run(['brew', 'services', 'restart', 'tor'], check=True)
            else:
                # Fallback: send NEWNYM signal to Tor control port
                self.send_newnym_signal()
                
            time.sleep(2)  # Wait for circuit to establish
            return True
        except subprocess.CalledProcessError as e:
            self.logger.error(f"Failed to reload Tor: {e}")
            return False
            
    def send_newnym_signal(self):
        """Send NEWNYM signal to Tor control port"""
        try:
            import socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('127.0.0.1', self.config["control_port"]))
                s.send(b'AUTHENTICATE\r\n')
                s.recv(1024)
                s.send(b'SIGNAL NEWNYM\r\n')
                s.recv(1024)
        except Exception as e:
            self.logger.debug(f"Failed to send NEWNYM signal: {e}")
            
    def signal_handler(self, signum, frame):
        """Handle interrupt signals"""
        self.logger.info("\nReceived interrupt signal. Shutting down gracefully...")
        self.running = False
        
    def display_banner(self):
        """Display application banner"""
        banner = """
\033[1;32m
 ██▓ ██▓███    ▄████  ██░ ██  ▒█████   ██████ ▄▄▄█████▓
▓██▒▓██░  ██▒ ██▒ ▀█▒▓██░ ██▒▒██▒  ██▒▒██    ▒ ▓  ██▒ ▓▒
▒██▒▓██░ ██▓▒▒██░▄▄▄░▒██▀▀██░▒██░  ██▒░ ▓██▄   ▒ ▓██░ ▒░
░██░▒██▄█▓▒ ▒░▓█  ██▓░▓█ ░██ ▒██   ██░  ▒   ██▒░ ▓██▓ ░ 
░██░▒██▒ ░  ░░▒▓███▀▒░▓█▒░██▓░ ████▓▒░▒██████▒▒  ▒██▒ ░ 
░▓  ▒▓▒░ ░  ░ ░▒   ▒  ▒ ░░▒░▒░ ▒░▒░▒░ ▒ ▒▓▒ ▒ ░  ▒ ░░   
 ▒ ░░▒ ░       ░   ░  ▒ ░▒░ ░  ░ ▒ ▒░ ░ ░▒  ░ ░    ░    
 ▒ ░░░       ░ ░   ░  ░  ░░ ░░ ░ ░ ▒  ░  ░  ░    ░      
 ░                 ░  ░  ░  ░    ░ ░        ░           
\033[0m
\033[1;36mAdvanced Tor IP Rotation Tool v3.0\033[0m
\033[1;33mSecure • Fast • Reliable\033[0m
\033[1;90mby Ashwin Asthana\033[0m
        """
        print(banner)
        
    def run(self):
        """Main execution function"""
        # Setup signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        self.display_banner()
        
        # Check Tor installation
        if not self.check_tor_installation():
            self.logger.info("Tor not found. Installing...")
            if not self.install_tor():
                self.logger.error("Failed to install Tor. Please install manually.")
                return
                
        # Start Tor service
        if not self.start_tor_service():
            self.logger.error("Failed to start Tor service.")
            return
            
        self.logger.info("Waiting for Tor to initialize...")
        time.sleep(5)
        
        # Get initial IP
        initial_ip = self.get_current_ip()
        if not initial_ip:
            self.logger.error("Failed to connect through Tor. Check your configuration.")
            return
            
        self.logger.info(f"Initial IP: {initial_ip}")
        self.logger.info("Configure your browser/application to use SOCKS5 proxy: 127.0.0.1:9050")
        
        # Get user preferences
        try:
            interval = int(input("\n[+] IP change interval in seconds [60]: ") or "60")
            count_input = input("[+] Number of IP changes [0 for infinite]: ") or "0"
            count = int(count_input) if count_input.isdigit() else 0
        except ValueError:
            self.logger.error("Invalid input. Using defaults.")
            interval, count = 60, 0
            
        self.logger.info(f"Starting IP rotation every {interval} seconds...")
        if count == 0:
            self.logger.info("Running indefinitely. Press Ctrl+C to stop.")
        else:
            self.logger.info(f"Will change IP {count} times.")
            
        # Main loop
        changes = 0
        while self.running and (count == 0 or changes < count):
            try:
                time.sleep(interval)
                if not self.running:
                    break
                    
                if self.change_ip():
                    new_ip = self.get_current_ip()
                    if new_ip and new_ip != initial_ip:
                        changes += 1
                        self.logger.info(f"[{changes}] IP changed to: {new_ip}")
                        initial_ip = new_ip
                    else:
                        self.logger.warning("IP change may have failed or same IP assigned")
                else:
                    self.logger.error("Failed to change IP")
                    
            except KeyboardInterrupt:
                break
                
        self.logger.info("IPGhost stopped. Stay anonymous!")

def main():
    """Entry point"""
    try:
        ghost = IPGhost()
        ghost.run()
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()