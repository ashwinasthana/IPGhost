#!/usr/bin/env python3
"""
IPGhost - Advanced Tor IP Changer
Created by Ashwin Asthana
"""

import time
import os
import subprocess

try:
    import requests
except ImportError:
    print('[+] Installing requests...')
    os.system('apt install -y python3-requests python3-socks')
    import requests

def get_ip():
    """Get current IP through Tor proxy"""
    try:
        response = requests.get(
            'http://checkip.amazonaws.com',
            proxies={'http': 'socks5://127.0.0.1:9050', 'https': 'socks5://127.0.0.1:9050'},
            timeout=10
        )
        return response.text.strip()
    except:
        return None

def shutdown_animation():
    """Cool shutdown animation"""
    import sys
    
    # Clear screen and show shutdown message
    os.system("clear")
    
    # Animated shutdown sequence
    messages = [
        "\n\033[1;31m[!] Shutting down IPGhost...\033[0m",
        "\033[1;33m[*] Cleaning up connections...\033[0m",
        "\033[1;36m[*] Securing your tracks...\033[0m",
        "\033[1;32m[✓] All connections closed safely\033[0m"
    ]
    
    for msg in messages:
        print(msg)
        time.sleep(0.8)
    
    # Cool ASCII art goodbye
    goodbye = """
\033[1;35m
    ╔═══════════════════════════════════╗
    ║                                   ║
    ║     👻 IPGhost Session Ended 👻    ║
    ║                                   ║
    ║    Stay Anonymous, Stay Safe!     ║
    ║                                   ║
    ║         by Ashwin Asthana         ║
    ║                                   ║
    ╚═══════════════════════════════════╝
\033[0m
    """
    
    print(goodbye)
    
    # Typing effect for final message
    final_msg = "\033[1;32mYour digital footprints have been ghosted... 👻\033[0m"
    for char in final_msg:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.05)
    
    print("\n")

def change_ip():
    """Change IP and show result"""
    os.system("service tor reload")
    new_ip = get_ip()
    if new_ip:
        print(f'[+] Your IP has been Changed to : {new_ip}')
    else:
        print('[!] Could not get new IP')
    """Display banner"""
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

def main():
    os.system("clear")
    display_banner()
    
    # Start Tor
    os.system("service tor start")
    time.sleep(3)
    
    print("\033[1;32;40m change your SOCKS to 127.0.0.1:9050 \n")
    
    # Get initial IP
    initial_ip = get_ip()
    if initial_ip:
        print(f"[+] Current IP: {initial_ip}")
    else:
        print("[!] Could not get current IP, but continuing...")
    
    # Get user input
    interval = input("\n[+] IP change interval in seconds [60]: ") or "60"
    count = input("[+] Number of IP changes [0 for infinite]: ") or "0"
    
    try:
        interval = int(interval)
        count = int(count)
        
        if count == 0:
            print("Starting infinite IP change. Press Ctrl+C to stop.")
            while True:
                try:
                    time.sleep(interval)
                    change_ip()
                except KeyboardInterrupt:
                    shutdown_animation()
                    break
        else:
            for _ in range(count):
                time.sleep(interval)
                change_ip()
                
    except ValueError:
        print("Invalid input. Please enter valid numbers.")

if __name__ == "__main__":
    main()