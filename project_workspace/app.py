import os
import yaml
import jinja2
import pickle
import subprocess
from xml import etree

def process_logic(data):
    """
    DEEP MAZE LOGIC: Designed for RL-based Fuzzing.
    Requires specific prefixes and nested conditions to reach 'vulnerable sinks'.
    """
    if len(data) < 4:
        return

    # --- LAYER 1: PROTOCOL IDENTIFICATION ---
    # The fuzzer must first learn to use these 4 prefixes.
    
    # 1. YAML LAYER (Nested Complexity)
    if data.startswith(b"YML:"):
        payload = data[4:]
        if len(payload) > 10: # Length Gate
            if b"UNSAFE" in payload: # Logic Gate
                # VULNERABLE SINK: Unsafe YAML Load
                yaml.unsafe_load(payload)
                print("[BUG_FOUND] PY-YML | Unsafe YAML reached")

    # 2. TEMPLATE LAYER (Stateful Parsing)
    elif data.startswith(b"TPL:"):
        payload = data[4:].decode('utf-8', 'ignore')
        if ":" in payload: # Structural Gate
            parts = payload.split(":")
            if parts[0] == "RENDER": # Semantic Gate
                # VULNERABLE SINK: Server Side Template Injection
                jinja2.Template(parts[1]).render()
                print("[BUG_FOUND] PY-TPL | SSTI reached")

    # 3. SECURE AUTH LAYER (The 'Maze' Backdoor)
    elif data.startswith(b"AUTH:"):
        # This requires 3 specific mutations in a row to win
        if b"ADMIN" in data:
            if b"SECRET" in data:
                if b"REVEAL" in data:
                    # VULNERABLE SINK: Logic Breach / Information Leak
                    print("[BUG_FOUND] PY-AUTH | Backdoor opened!")
                    print("[SECRET] KEY: AI-ZERO-DAY-TOKEN-99")

    # 4. PICKLE LAYER (High Risk Deserialization)
    elif data.startswith(b"PKL:"):
        if len(data) > 64: # Size-dependent behavior
            # VULNERABLE SINK: Insecure Deserialization
            pickle.loads(data[4:])
            print("[BUG_FOUND] PY-PKL | Deserialization triggered")

    # 5. FILE LAYER (Path Traversal)
    elif data.startswith(b"FILE:"):
        path = data[5:].decode('utf-8', 'ignore')
        if "../" in path: # Traversal check
            # VULNERABLE SINK: Arbitrary File Read
            if os.path.exists(path):
                with open(path, 'r') as f:
                    content = f.read(10)
                    print(f"[BUG_FOUND] PY-FILE | Read: {content}")

# --- KEEPING CLI STRUCTURE FOR HARVESTER COMPATIBILITY ---
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Deep Maze Vulnerable App")
    parser.add_argument("--data", help="Input data for processing")
    args = parser.parse_args()
    if args.data:
        process_logic(args.data.encode())

if __name__ == "__main__":
    main()