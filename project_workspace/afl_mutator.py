import random

def init(seed):
    return {"mutations": 0}

def fuzz(*args):
    # Determine the buffer based on the caller (AFL++ or Atheris)
    if len(args) == 4:
        mutated = bytearray(args[1] if isinstance(args[1], (bytes, bytearray)) else args[0])
        max_size = args[3]
    else:
        mutated = bytearray(args[0])
        max_size = len(args[0])

    # RL STRATEGY: Injecting "Semantic Keys" to bypass logic gates
    if random.random() < 0.4:
        strategic_payloads = [
            b"ADMIN_ACCESS", b"ADMIN!12345", b"DEBUG_ON", 
            b"YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY", b"%s%s%s%s", 
            b"PKL:cos\nsystem", b"SQL:' OR '1'='1"
        ]
        p = random.choice(strategic_payloads)
        if len(mutated) >= len(p):
            mutated[0:len(p)] = p
    else:
        if len(mutated) > 0:
            idx = random.randint(0, min(len(mutated) - 1, 64))
            mutated[idx] = random.randint(0, 255)
            
    return bytes(mutated[:max_size])