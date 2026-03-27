import gymnasium as gym
from fuzz_env import FuzzEnv
import os
import numpy as np

def clean_text(input_bytes):
    return "".join([chr(b) if 31 < b < 127 else "." for b in input_bytes])

env = FuzzEnv()

# Wipe old failed patterns to start clean
if os.path.exists("pattern_bank.txt"):
    os.remove("pattern_bank.txt")

print("\n🕵️ --- STARTING REAL-WORLD ZERO-DAY AUDIT ---")
print("Target: 10 Hidden Bugs | Method: RL-Guided Coverage")

for i in range(100000): # 100k steps for deep exploration
    action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    
    # Only print when something actually happens
    if reward > 0.1:
        print(f"[*] Step {i:05} | Bug/Path Found! | Reward: {reward:5.1f} | Data: [{clean_text(obs[:15])}]")

    if terminated:
        print(f"\n[💥] ZERO-DAY EXPLOIT CONFIRMED AT STEP {i}!")
        print(f"Payload: {obs.tobytes().hex()}")
        # To find ALL 10 bugs, you would reset env.best_reward here and continue
        break 

    if i % 10000 == 0:
        print(f"Status: {i} steps completed...")

print("--- AUDIT COMPLETE ---")