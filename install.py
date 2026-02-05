#!/usr/bin/env python3

import os
import sys

def main():
    choice = input('[+] to install press (Y) to uninstall press (N) >> ')
    
    if choice.lower() in ['y', 'yes']:
        print('[+] Installing IPGhost...')
        
        # Simple dependency install
        try:
            os.system('apt install -y python3-requests python3-socks')
        except:
            pass
            
        # Create directories and copy files
        os.system('chmod 777 ipghost.py')
        os.system('mkdir -p /usr/share/ipghost')
        os.system('cp ipghost.py /usr/share/ipghost/ipghost.py')
        
        # Create executable
        with open('/usr/bin/ipghost', 'w') as f:
            f.write('#!/bin/sh\nexec python3 /usr/share/ipghost/ipghost.py "$@"')
        
        os.system('chmod +x /usr/bin/ipghost')
        os.system('chmod +x /usr/share/ipghost/ipghost.py')
        
        print('\n\nCongratulations! IPGhost is installed successfully')
        print('From now just type \x1b[6;30;42mipghost\x1b[0m in terminal')
        
    elif choice.lower() in ['n', 'no']:
        print('[+] Uninstalling IPGhost...')
        os.system('rm -rf /usr/share/ipghost')
        os.system('rm -f /usr/bin/ipghost')
        print('[!] IPGhost has been removed successfully')

if __name__ == "__main__":
    main()