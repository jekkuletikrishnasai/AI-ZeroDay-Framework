import subprocess
import os

CRASH_DIR = "out_dir/default/crashes"
TARGET = "./target_prog"

print("\n🕵️ --- ZERO-DAY CRASH ANALYSIS REPORT ---")

crashes = [f for f in os.listdir(CRASH_DIR) if f.startswith("id")]

for crash_file in crashes:
    path = os.path.join(CRASH_DIR, crash_file)
    
    # Run the target with the crashing input
    result = subprocess.run([TARGET, path], capture_output=True, text=True)
    
    print(f"\n[!] Analyzing Crash: {crash_file}")
    print(f"    Payload: {open(path, 'rb').read()[:30]}...")
    
    # Check for our 'Secret' flags in the output
    if "[SECRET]" in result.stdout:
        print("    ✅ BUG IDENTIFIED: Logic/Privilege Leak Found!")
    if "Segmentation fault" in result.stderr or result.returncode != 0:
        print("    💥 BUG IDENTIFIED: Memory Corruption / Buffer Overflow!")