# vuln_app.py
# ---------------------------------------------------------
# Intentionally vulnerable Python application for
# fuzzing, RL-guided mutation, and zero-day research
# ---------------------------------------------------------
# DO NOT USE IN PRODUCTION
# Python 3.9+
# ---------------------------------------------------------

import os
import json
import pickle
import yaml
from jinja2 import Template

# ==============================
# BUG-01: Unsafe YAML Deserialization (RCE)
# ==============================
def bug_01_yaml(user_input: bytes):
    """
    CWE-502: Deserialization of Untrusted Data
    """
    if user_input.startswith(b"YAML:"):
        payload = user_input[5:].decode(errors="ignore")
        print("[BUG-01] Unsafe YAML load")
        yaml.load(payload, Loader=None)   # ❌ UNSAFE


# ==============================
# BUG-02: Jinja2 Template Injection
# ==============================
def bug_02_template(user_input: bytes):
    """
    CWE-94: Code Injection
    """
    if user_input.startswith(b"TPL:"):
        template_code = user_input[4:].decode(errors="ignore")
        print("[BUG-02] Rendering untrusted template")
        t = Template(template_code)        # ❌ UNSAFE
        t.render()


# ==============================
# BUG-03: Path Traversal
# ==============================
def bug_03_path(user_input: bytes):
    """
    CWE-22: Path Traversal
    """
    if user_input.startswith(b"FILE:"):
        path = user_input[5:].decode(errors="ignore")
        print("[BUG-03] Opening file:", path)
        with open(path, "r") as f:         # ❌ NO SANITIZATION
            f.read()


# ==============================
# BUG-04: Pickle Deserialization (Critical RCE)
# ==============================
def bug_04_pickle(user_input: bytes):
    """
    CWE-502: Arbitrary Code Execution
    """
    if user_input.startswith(b"PKL:"):
        data = user_input[4:]
        print("[BUG-04] Unsafe pickle.loads")
        pickle.loads(data)                 # ❌ RCE


# ==============================
# BUG-05: Logic-Based Authorization Bypass
# ==============================
def bug_05_logic(user_input: bytes):
    """
    CWE-840: Business Logic Error
    """
    if user_input.startswith(b"AUTH:"):
        parts = user_input.decode(errors="ignore").split(":")
        if len(parts) > 2 and parts[1] == "ADMIN":
            if "OPEN" in parts[2]:
                print("[BUG-05] ADMIN ACCESS GRANTED")
                print("SECRET = ZERO_DAY_MASTER_KEY")  # ❌ INFO LEAK


# ==============================
# Dispatcher (Fuzz Entry Point)
# ==============================
def process_input(data: bytes):
    bug_01_yaml(data)
    bug_02_template(data)
    bug_03_path(data)
    bug_04_pickle(data)
    bug_05_logic(data)


# ==============================
# Manual Test Entry
# ==============================
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python vuln_app.py <payload>")
        sys.exit(1)

    process_input(sys.argv[1].encode())
