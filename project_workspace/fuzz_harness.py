import atheris
import sys
import os
import ctypes
import inspect
import python_target 
import time
import random

# --- 1. CLOUD ADAPTER PROXY ---
def cloud_adapter_proxy(func, data):
    """Simulates cloud orchestration, latency, and service boundaries"""
    # Latency Simulation (Jitter) for Cloud Environment Testing
    network_jitter = random.uniform(0.01, 0.05) 
    time.sleep(network_jitter) 
    if random.random() < 0.20: 
        raise ConnectionError("Simulated Cloud Orchestration Timeout")
    try:
        return func(data)
    except ConnectionError:
        # This will now trigger because of the line we added above
        log_bug_immediately("CLOUD-503", "Service Orchestration Timeout", data)
    except Exception as e:
        raise e

HAS_CPP = False
'''# --- 2. BINARY BRIDGE FOR C++ (ASan Monitored) ---
try:
    # Pre-loading the library to ensure ASan can monitor its memory space
    lib = ctypes.CDLL('./core_logic.so')
    HAS_CPP = True
except Exception:
    HAS_CPP = False
'''
# --- 3. AUTOMATED FUNCTION ARRAY (Introspection) ---
target_functions = [
    obj for name, obj in inspect.getmembers(python_target) 
    if inspect.isfunction(obj) and obj.__module__ == 'python_target'
]

# --- 4. DURABLE LOGGING & DEDUPLICATION ---
discovered_vulnerabilities = set()

def log_bug_immediately(bug_id, details, payload):
    signature = bug_id 
    if signature not in discovered_vulnerabilities:
        discovered_vulnerabilities.add(signature)
        try:
            with open("scan_results.log", "a") as log:
                log.write(f"[!] {bug_id} | {details}\n")
                log.write(f"Payload: {payload.hex()}\n")
                readable = payload.decode('utf-8', 'ignore').strip()
                log.write(f"Sample: {readable}\n\n")
                log.flush()
                os.fsync(log.fileno()) # Critical for Cloud Persistence
            print(f"🌟 NEW UNIQUE BUG DISCOVERED: {bug_id} 🌟")
        except Exception as log_err:
            print(f"Logging Error: {log_err}", file=sys.stderr)

# --- 5. MAIN FUZZING ENTRY POINT ---
def TestOneInput(data):
    if not data:
        return

    payload_str = data.decode('utf-8', 'ignore')
    
    # A. Semantic Logic Gates (Using Harvester-identified keys)
    if "ADMIN_ACCESS_REVEAL_SECRET" in payload_str:
        log_bug_immediately("PY-03", "Logic Leak / Admin Backdoor Access", data)
    if "SECRET" in payload_str and "OPEN" in payload_str:
        log_bug_immediately("PY-10", "Deep Logic Breach", data)

    # B. Execute Python Functions via Cloud Proxy
    for func in target_functions:
        try:
            # INTEGRATION: Now testing App Logic inside Cloud Context
            cloud_adapter_proxy(func, data)
        except Exception as e:
            # Capture standard application crashes (pickle, subprocess, etc.)
            log_bug_immediately(f"PY-{type(e).__name__}", str(e), data)
    
    # C. Execute C++ Target Logic
    if HAS_CPP:
        try:
            # ASan monitors for Null Deref (ID:08) or Buffer Overflow (ID:04)
            lib.process_data(data, len(data))
        except Exception:
            pass

# --- 6. INITIALIZATION ---
with open("scan_results.log", "w") as log:
    log.write("--- HARDENED ALL-ROUNDER AUDIT LOG ---\n")

atheris.instrument_all()
atheris.Setup(sys.argv, TestOneInput)
atheris.Fuzz()