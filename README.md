# VSMK-AI-WAF (Adaptive AI Web Firewall)

VSMK-AI-WAF is a production-grade, AI-driven Web Application Firewall designed to detect and block OWASP Top 10 vulnerabilities (SQLi, XSS, CSRF, LFI) using a hybrid approach of regex pattern matching and heuristic analysis.

## Features

*   **Real-time Interception**: Middleware-based traffic inspection.
*   **AI/Heuristic Engine**: Scores payloads based on entropy, keywords, and structure.
*   **Explainable Security**: Provides human-readable reasons for every block.
*   **Live Dashboard**: Auto-refreshing UI showing attack stats and logs.
*   **Zero-Config**: Ready to run out of the box.

## Directory Structure

```
ai-waf/
│── backend/          # Core logic
│   ├── app/          # FastAPI app & routes
│   ├── ai/           # Classification & Explanation engines
│   ├── rules/        # JSON security rules
│   ├── logs/         # Attack logs
│── frontend/         # Dashboard UI
│── cli/              # CLI Launcher
│── config/           # Settings
```

## Installation

1.  **Prerequisites**: Python 3.9+
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Start the WAF**:
    ```bash
    python3 cli/vsmk_waf.py start
    ```

2.  **Access Dashboard**:
    Open [http://localhost:8000/dashboard](http://localhost:8000/dashboard)

3.  **Test Protection**:
    Try sending a malicious payload:
    ```bash
    # SQL Injection Test
    curl -X POST "http://localhost:8000/vulnerable" -d '{"user": "admin", "pass": "' OR 1=1 --"}'
    
    # XSS Test
    curl "http://localhost:8000/vulnerable?q=<script>alert(1)</script>"
    ```

## Logic Explanation

The WAF operates in 3 stages:
1.  **Pattern Match**: Checks against `backend/rules/rules.json` for known signatures.
2.  **Heuristic Analysis**: If no signature matches, the `AIClassifier` calculates a suspicious score based on keyword density and character entropy.
3.  **Decision**: If severity > threshold, the request is blocked (403 Forbidden) and logged with an explanation.

## License

Proprietary - VSMK Cyber Security.
