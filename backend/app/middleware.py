import time
import json
import logging
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from backend.ai.classifier import classifier
from backend.ai.explainer import explainer
from config.settings import LOG_FILE

# Setup logging
logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
logger = logging.getLogger("vsmk.waf")
logger.addHandler(file_handler)

class WafMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Skip checking the dashboard APIs and static files to avoid self-blocking
        if request.url.path.startswith("/api/dashboard") or request.url.path.startswith("/dashboard"):
             return await call_next(request)

        # 1. Capture Request Data
        payload = ""
        
        # Check query params
        if request.query_params:
            payload += str(request.query_params)

        # Check body (careful with consuming stream)
        # For simplicity in this demo, we read small bodies. 
        # In production, we'd clone the stream.
        try:
            body_bytes = await request.body()
            if body_bytes:
                payload += body_bytes.decode('utf-8', errors='ignore')
        except Exception:
            pass # Body reading failed or empty

        # 2. AI Analysis
        attack_type, confidence, severity, rule_id = classifier.classify(payload)

        # 3. Decision
        if attack_type:
            # Generate Explanation
            explanation = explainer.explain(attack_type, payload, severity)
            
            # Log the attack
            log_entry = {
                "timestamp": time.time(),
                "ip": request.client.host,
                "path": request.url.path,
                "attack_type": attack_type,
                "severity": severity,
                "payload": payload[:200], # Truncate for log
                "explanation": explanation
            }
            logger.warning(json.dumps(log_entry))
            
            # Block Request
            return Response(
                content=json.dumps({
                    "error": "Request Blocked by VSMK-AI-WAF",
                    "attack_type": attack_type,
                    "reason": explanation,
                    "severity": severity
                }),
                status_code=403,
                media_type="application/json"
            )

        # Allow Request
        response = await call_next(request)
        return response
