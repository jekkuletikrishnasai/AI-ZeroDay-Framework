import re
import os

def generate_dictionary(target_path, dict_path):
    with open(target_path, 'r', errors='ignore') as f:
        content = f.read()

    # BROAD SCAN: Find every alphanumeric word 3+ chars long
    # This captures function names like 'demo_yaml' and keys like 'SUPERUSER'
    all_words = re.findall(r'[a-zA-Z_][a-zA-Z0-9_]{2,}', content)
    
    # STRING SCAN: Capture everything inside quotes (single or double)
    quoted_strings = re.findall(r'["\'](.*?)["\']', content)

    # Combine and Filter
    raw_keys = all_words + quoted_strings
    clean_keys = []
    for k in raw_keys:
        # Filter out Python keywords and short noise
        if k not in ["import", "from", "print", "None", "True", "False"] and 3 < len(k) < 30:
            clean_keys.append(k)

    unique_keys = sorted(list(set(clean_keys)))

    with open(dict_path, 'w') as f:
        for key in unique_keys:
            f.write(f'"{key}"\n')
            
    print(f"✅ Deep Intelligence: {len(unique_keys)} logic keys harvested into {dict_path}")

if __name__ == "__main__":
    generate_dictionary("./python_target.py", "zero_day.dict")