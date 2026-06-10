import json
import os

class IntentAnalyzer:
    def __init__(self, policy_path="config/security_policies.json"):
        # Load our security guidelines safely
        if os.path.exists(policy_path):
            with open(policy_path, 'r') as f:
                self.policy = json.load(f)
        else:
            # Fallback policy if file isn't loaded yet
            self.policy = {
                "allowed_actions": ["read_file", "semantic_search"],
                "blocked_actions": ["execute_bash", "delete_file"],
                "strict_mode": True
            }

    def inspect_intent(self, proposed_action, parameters):
        """
        Inspects the AI Agent's intention before execution.
        Prevents Logic Injection and malicious tool usage.
        """
        print(f"[🔍 IntentShield Monitoring]: Agent wants to execute action: '{proposed_action}'")
        
        # Rule 1: Check against explicitly blocked critical tools
        if proposed_action in self.policy["blocked_actions"]:
            return {"status": "BLOCKED", "reason": f"Action '{proposed_action}' violates safety constraints."}
            
        # Rule 2: Check for logical injection indicators (e.g., directory traversal)
        if proposed_action == "read_file" and "system_root" in parameters:
            return {"status": "BLOCKED", "reason": "Logic Injection Detected: Agent attempted unauthorized directory traversal."}

        return {"status": "ALLOWED", "reason": "Intent matches safe structural boundaries."}
