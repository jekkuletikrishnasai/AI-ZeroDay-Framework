import os

class PreventionShield:
    def __init__(self, log_file="scan_results.log"):
        self.blocked_hex_signatures = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                for line in f:
                    # Look for the hex payloads you just verified in your log
                    if line.startswith("Payload: "):
                        sig = line.replace("Payload: ", "").strip()
                        if sig not in self.blocked_hex_signatures:
                            self.blocked_hex_signatures.append(sig)
        
        print(f"🛡️  [SHIELD] Virtual Patching Active. {len(self.blocked_hex_signatures)} signatures loaded.")

    def is_safe(self, incoming_data):
        # Convert the incoming network traffic to hex for a 1:1 match
        incoming_hex = incoming_data.hex()
        
        for signature in self.blocked_hex_signatures:
            if signature in incoming_hex:
                print(f"🚫 [BLOCK] Known Exploit Detected: {signature[:10]}...")
                return False
        return True