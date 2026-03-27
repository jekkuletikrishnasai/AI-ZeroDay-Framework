import os
import pickle
import sqlite3
import subprocess
import base64

def process_request(data):
    # BUG 1: Command Injection
    if data.startswith(b"CMD:"):
        # THE ORACLE SIGNAL
        print("[BUG_FOUND] ID:PY-01 | TYPE: Command Injection | STATUS: EXPLOITED")
        cmd = data[4:].decode('utf-8', errors='ignore')
        os.system(f"echo Processing {cmd}") 

    # BUG 2: Insecure Deserialization
    elif data.startswith(b"PKL:"):
        print("[BUG_FOUND] ID:PY-02 | TYPE: Deserialization | STATUS: EXPLOITED")
        pickle.loads(data[4:])

    # BUG 3: Hidden Admin Backdoor
    elif data == b"ADMIN_ACCESS_REVEAL_SECRET":
        print("[BUG_FOUND] ID:PY-03 | TYPE: Logic Leak | STATUS: EXPLOITED")
        print("[SECRET] Key: PY-ZDR-9922")

    # BUG 4: Subprocess Injection
    elif data.startswith(b"RUN:"):
        print("[BUG_FOUND] ID:PY-04 | TYPE: Subprocess RCE | STATUS: EXPLOITED")
        subprocess.run(data[4:], shell=True)

    # BUG 5: Format String / Template Injection
    elif data.startswith(b"FMT:"):
        print("[BUG_FOUND] ID:PY-05 | TYPE: Template Injection | STATUS: EXPLOITED")
        print(data[4:].decode('utf-8', errors='ignore').format(globals()))
    if b"SECRET" in data:
        if b"OPEN" in data:
            print("[BUG_FOUND] ID:PY-06 | TYPE: Deep Logic Breach")