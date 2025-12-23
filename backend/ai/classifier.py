import re
import json
import logging
from typing import Dict, Tuple, Optional
from config.settings import RULES_FILE

logger = logging.getLogger("vsmk.ai.classifier")

class AIClassifier:
    def __init__(self):
        self.rules = self.load_rules()
        self.learning_buffer = {}  # Tracks suspicious but non-blocked payloads for learning

    def load_rules(self):
        try:
            if not RULES_FILE.exists():
                logger.warning(f"Rules file not found at {RULES_FILE}")
                return []
            with open(RULES_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading rules: {e}")
            return []

    def classify(self, payload: str) -> Tuple[Optional[str], float, int, str]:
        """
        Analyzes payload against rules and heuristic logic.
        Returns: (Attack Type, Confidence, Severity, Rule ID)
        """
        if not payload:
            return None, 0.0, 0, ""

        # 1. Pattern Matching (Knowledge-based)
        for rule in self.rules:
            try:
                if re.search(rule['pattern'], payload):
                    return rule['type'], 0.95, rule['severity'], rule['id']
            except re.error:
                logger.error(f"Invalid regex in rule {rule['id']}")
                continue

        # 2. Heuristic Analysis (AI Reasoning Simulation)
        # Check for high entropy or suspicious character combinations not covered by explicit rules
        suspicious_score = self._heuristic_score(payload)
        
        if suspicious_score > 0.7:
             # "Learn" this pattern (In a real system, this would update the model)
             self._learn_pattern(payload)
             return "Anomaly", suspicious_score, 5, "ai-heuristic-001"

        return None, 0.0, 0, ""

    def _heuristic_score(self, payload: str) -> float:
        score = 0.0
        # Keywords that are suspicious but not enough for a block on their own
        keywords = ['admin', 'root', 'sleep', 'benchmark', 'waitfor', 'alert', 'prompt']
        
        for kw in keywords:
            if kw in payload.lower():
                score += 0.2
        
        # Check for abundance of special characters
        special_chars = sum(1 for c in payload if not c.isalnum() and not c.isspace())
        if len(payload) > 0 and (special_chars / len(payload)) > 0.3:
            score += 0.4
            
        return min(score, 1.0)

    def _learn_pattern(self, payload: str):
        # In a real AI system, this would feed the neural network
        # Here we just log it as a potential new rule candidate
        logger.info(f"AI Learning: Suspicious payload detected: {payload[:50]}...")

classifier = AIClassifier()
