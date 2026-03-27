import ctypes
import sys
import os

# Exact path to your compiled C++ shared library
lib_path = "/workspaces/AI-ZeroDay-Framework/project_workspace/core_logic.so"

try:
    if not os.path.exists(lib_path):
        raise FileNotFoundError(f"Missing: {lib_path}")
    
    # Load the library using its absolute path
    core = ctypes.CDLL(lib_path)
    
    if __name__ == "__main__":
        if len(sys.argv) > 1:
            # Send test input to the C++ core
            test_input = sys.argv[1].encode('utf-8')
            core.process_data(test_input)
        else:
            print("Usage: python3 bridge.py <input_string>")

except Exception as e:
    print(f"Error: {e}")
