class AIExplainer:
    def explain(self, attack_type: str, payload: str, severity: int) -> str:
        """
        Generates a human-readable explanation for why a request was blocked.
        """
        explanation = f"VSMK-AI Analysis detected a {attack_type} attack with severity {severity}/10. "
        
        if attack_type == "SQLi":
            explanation += "The payload contains SQL syntax characters (like quotes, semicolons, or keywords 'UNION/SELECT') which indicates an attempt to manipulate database queries."
        elif attack_type == "XSS":
            explanation += "The payload includes HTML tags (like <script>) or JavaScript event handlers (like onload/onerror), suggesting an attempt to execute malicious code in the user's browser."
        elif attack_type == "LFI":
            explanation += "The payload attempts to traverse directories ('../') or access system files (/etc/passwd), which is a clear sign of Local File Inclusion."
        elif attack_type == "CSRF":
            explanation += "The payload appears to be manipulating anti-CSRF tokens."
        elif attack_type == "Anomaly":
            explanation += "The request structure or content deviates significantly from normal traffic patterns. High usage of special characters or suspicious keywords was detected."
        else:
            explanation += "The request matched a known malicious pattern defined in the security rules."

        return explanation

explainer = AIExplainer()
