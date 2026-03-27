import gymnasium as gym
from gymnasium import spaces
import numpy as np
import ctypes
import io
import sys

class FuzzEnv(gym.Env):
    def __init__(self):
        super(FuzzEnv, self).__init__()
        self.action_space = spaces.MultiDiscrete([64, 256])
        self.observation_space = spaces.Box(low=0, high=255, shape=(64,), dtype=np.uint8)
        self.lib = ctypes.CDLL('./core_logic.so')
        
        self.best_input = np.zeros((64,), dtype=np.uint8)
        self.best_reward = 0.0
        self.discovered_paths = set() # AFL-style coverage tracker

    def step(self, action):
        # SMART MUTATION: 80% focus on the first 16 bytes (The "Command" zone)
        if np.random.rand() < 0.8:
            idx = np.random.randint(0, 16)
        else:
            idx = action[0]
        val = action[1]

        test_input = self.best_input.copy()
        test_input[idx] = val
        input_bytes = bytes(test_input)

        # CAPTURE OUTPUT & EXECUTE
        reward = 0.1
        terminated = False
        captured_output = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured_output

        try:
            # We use the return value as a 'Path Signature' (Coverage)
            path_sig = self.lib.process_data(input_bytes)
            sys.stdout = old_stdout
            output = captured_output.getvalue()

            # --- THE REWARD ORACLE ---
            # 1. New Path Discovery (AFL Logic)
            if path_sig not in self.discovered_paths and path_sig > 0:
                self.discovered_paths.add(path_sig)
                reward += 20.0 # Reward for exploring a new room
            
            # 2. Logic Bug Detection
            if "[SECRET]" in output:
                reward += 100.0
                terminated = True
            elif "[INFO]" in output:
                reward += 50.0

        except Exception:
            # 3. Crash Detection (Zero-Day!)
            sys.stdout = old_stdout
            reward = 500.0
            terminated = True

        # Persistence
        if reward > self.best_reward:
            self.best_reward = reward
            self.best_input = test_input.copy()
            with open("pattern_bank.txt", "a") as f:
                f.write(f"{input_bytes.hex()}\n")
            print(f"✨ NEW PATH DISCOVERED! Reward: {reward}")

        return self.best_input, reward, terminated, False, {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        return self.best_input, {}