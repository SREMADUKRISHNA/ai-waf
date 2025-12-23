#!/usr/bin/env python3
import sys
import os
import time
import argparse
import uvicorn
from pathlib import Path

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from config.settings import BANNER_TEXT, HOST, PORT, VERSION

RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"

def print_banner():
    print(CYAN + BOLD + "="*60 + RESET)
    print(CYAN + BOLD + f"  {BANNER_TEXT}" + RESET)
    print(CYAN + f"  Version: {VERSION}" + RESET)
    print(CYAN + BOLD + "="*60 + RESET)
    print("")

def start_server():
    print_banner()
    print(f"{GREEN}[*] Initializing VSMK AI Engine...{RESET}")
    time.sleep(1) # Simulate loading
    print(f"{GREEN}[*] Loading Adaptive Rules...{RESET}")
    print(f"{GREEN}[*] Starting WAF Server on http://{HOST}:{PORT}{RESET}")
    print(f"{YELLOW}[!] Dashboard available at http://{HOST}:{PORT}/dashboard{RESET}")
    print(f"{YELLOW}[!] Press Ctrl+C to stop{RESET}")
    print("")
    
    try:
        uvicorn.run("backend.app.main:app", host=HOST, port=PORT, log_level="error")
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Stopping VSMK-WAF...{RESET}")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(description="VSMK-AI-WAF CLI")
    parser.add_argument('action', choices=['start'], help="Action to perform")
    
    if len(sys.argv) < 2:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    
    if args.action == 'start':
        start_server()

if __name__ == "__main__":
    main()
