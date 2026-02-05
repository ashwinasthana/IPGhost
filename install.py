#!/usr/bin/env python3
"""
IPGhost Installer
Easy installation and management script for IPGhost
"""

import os
import sys
import shutil
import platform
import subprocess
from pathlib import Path

class IPGhostInstaller:
    def __init__(self):
        self.system = platform.system().lower()
        self.script_dir = Path(__file__).parent.absolute()
        self.install_dir = Path("/usr/local/bin") if self.system != "windows" else Path.home() / "AppData" / "Local" / "IPGhost"
        self.config_dir = Path.home() / ".ipghost"
        
    def check_permissions(self) -> bool:
        """Check if we have necessary permissions"""
        if self.system == "windows":
            return True
        return os.geteuid() == 0
        
    def install_dependencies(self):
        """Install Python dependencies"""
        print("Installing Python dependencies...")
        try:
            # Try system package manager first
            system = platform.system().lower()
            if system == "linux":
                # Try apt first (Debian/Ubuntu/Parrot)
                if subprocess.run(['which', 'apt'], capture_output=True).returncode == 0:
                    try:
                        subprocess.check_call(['apt', 'install', '-y', 'python3-requests', 'python3-socks'])
                        print("✓ Dependencies installed via apt")
                        return True
                    except subprocess.CalledProcessError:
                        pass
                        
            # Fallback to pip with --break-system-packages if needed
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "requests[socks]"])
                print("✓ Dependencies installed via pip")
            except subprocess.CalledProcessError:
                # Try with --break-system-packages for externally managed environments
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--break-system-packages", "requests[socks]"])
                print("✓ Dependencies installed via pip (system override)")
                
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to install dependencies: {e}")
            print("Please install manually: apt install python3-requests python3-socks")
            return False
        return True
        
    def create_executable(self):
        """Create executable script"""
        if self.system == "windows":
            # Create batch file for Windows
            batch_content = f"""@echo off
python "{self.install_dir / 'ipghost.py'}" %*
"""
            batch_file = self.install_dir / "ipghost.bat"
            with open(batch_file, 'w') as f:
                f.write(batch_content)
            print(f"✓ Created executable: {batch_file}")
        else:
            # Create shell script for Unix-like systems
            shell_content = f"""#!/bin/bash
exec python3 "{self.install_dir / 'ipghost.py'}" "$@"
"""
            shell_file = Path("/usr/local/bin/ipghost")
            with open(shell_file, 'w') as f:
                f.write(shell_content)
            os.chmod(shell_file, 0o755)
            print(f"✓ Created executable: {shell_file}")
            
    def install(self):
        """Install IPGhost"""
        print("🔧 Installing IPGhost...")
        
        # Check permissions
        if not self.check_permissions() and self.system != "windows":
            print("✗ This script requires root privileges. Please run with sudo.")
            return False
            
        # Create directories
        self.install_dir.mkdir(parents=True, exist_ok=True)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Install dependencies
        if not self.install_dependencies():
            return False
            
        # Copy main script
        source_script = self.script_dir / "ipghost.py"
        if source_script.exists():
            shutil.copy2(source_script, self.install_dir / "ipghost.py")
            print(f"✓ Copied main script to {self.install_dir}")
        else:
            print("✗ ipghost.py not found in current directory")
            return False
            
        # Create executable
        self.create_executable()
        
        # Set permissions
        if self.system != "windows":
            os.chmod(self.install_dir / "ipghost.py", 0o755)
            
        print("\n🎉 IPGhost installed successfully!")
        print("\nUsage:")
        if self.system == "windows":
            print("  ipghost.bat")
        else:
            print("  ipghost")
        print("\nConfiguration directory:", self.config_dir)
        return True
        
    def uninstall(self):
        """Uninstall IPGhost"""
        print("🗑️  Uninstalling IPGhost...")
        
        # Check permissions
        if not self.check_permissions() and self.system != "windows":
            print("✗ This script requires root privileges. Please run with sudo.")
            return False
            
        # Remove files
        files_to_remove = []
        if self.system == "windows":
            files_to_remove.extend([
                self.install_dir / "ipghost.py",
                self.install_dir / "ipghost.bat"
            ])
        else:
            files_to_remove.extend([
                self.install_dir / "ipghost.py",
                Path("/usr/local/bin/ipghost")
            ])
            
        for file_path in files_to_remove:
            if file_path.exists():
                file_path.unlink()
                print(f"✓ Removed {file_path}")
                
        # Remove install directory if empty
        if self.install_dir.exists() and not any(self.install_dir.iterdir()):
            self.install_dir.rmdir()
            print(f"✓ Removed directory {self.install_dir}")
            
        # Ask about config directory
        keep_config = input("Keep configuration directory? [Y/n]: ").lower()
        if keep_config in ['n', 'no']:
            if self.config_dir.exists():
                shutil.rmtree(self.config_dir)
                print(f"✓ Removed configuration directory {self.config_dir}")
                
        print("✓ IPGhost uninstalled successfully!")
        return True
        
    def status(self):
        """Check installation status"""
        print("📊 IPGhost Installation Status")
        print("-" * 30)
        
        # Check main script
        main_script = self.install_dir / "ipghost.py"
        print(f"Main script: {'✓' if main_script.exists() else '✗'} {main_script}")
        
        # Check executable
        if self.system == "windows":
            executable = self.install_dir / "ipghost.bat"
        else:
            executable = Path("/usr/local/bin/ipghost")
        print(f"Executable: {'✓' if executable.exists() else '✗'} {executable}")
        
        # Check config directory
        print(f"Config dir: {'✓' if self.config_dir.exists() else '✗'} {self.config_dir}")
        
        # Check dependencies
        try:
            import requests
            print("Dependencies: ✓ requests[socks]")
        except ImportError:
            print("Dependencies: ✗ requests[socks] not installed")
            
        # Check Tor
        try:
            result = subprocess.run(['tor', '--version'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.split('\n')[0]
                print(f"Tor: ✓ {version}")
            else:
                print("Tor: ✗ Not working properly")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            print("Tor: ✗ Not installed")

def main():
    """Main function"""
    installer = IPGhostInstaller()
    
    if len(sys.argv) < 2:
        print("IPGhost Installer")
        print("Usage:")
        print("  python3 install.py install   - Install IPGhost")
        print("  python3 install.py uninstall - Uninstall IPGhost")
        print("  python3 install.py status    - Check installation status")
        return
        
    action = sys.argv[1].lower()
    
    if action == "install":
        installer.install()
    elif action == "uninstall":
        installer.uninstall()
    elif action == "status":
        installer.status()
    else:
        print(f"Unknown action: {action}")
        print("Available actions: install, uninstall, status")

if __name__ == "__main__":
    main()