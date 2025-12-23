import os
from pathlib import Path

# VSMK Branding
BRAND_NAME = "VSMK-AI-WAF"
VERSION = "1.0.0"
BANNER_TEXT = "VSMK-AI-WAF | Adaptive AI Web Firewall"

# Base Directories
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
RULES_DIR = BACKEND_DIR / "rules"
LOGS_DIR = BACKEND_DIR / "logs"

# Files
RULES_FILE = RULES_DIR / "rules.json"
LOG_FILE = LOGS_DIR / "attacks.log"

# Server Config
HOST = "0.0.0.0"
PORT = 8000
DEBUG = True

# Security Thresholds
CONFIDENCE_THRESHOLD = 0.8
SEVERITY_HIGH = 8
SEVERITY_MEDIUM = 5
SEVERITY_LOW = 2
