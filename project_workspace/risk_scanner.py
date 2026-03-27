from ghidra.app.script import GhidraScript

# List of dangerous functions to flag
BANNED = ["strcpy", "strcat", "gets", "sprintf"]

def run():
    print("\n--- [AI-ZeroDay] Starting Static Risk Scan ---")
    fm = currentProgram.getFunctionManager()
    funcs = fm.getFunctions(True) 
    
    for f in funcs:
        if f.getName() in BANNED:
            print("[ALERT] Dangerous Function Found: {} at {}".format(f.getName(), f.getEntryPoint()))
    print("--- [AI-ZeroDay] Scan Complete ---\n")

run()
