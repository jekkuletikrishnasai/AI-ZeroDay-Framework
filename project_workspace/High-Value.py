import os

# Define the "Grammar" for our target app.py
templates = [
    "yaml: !!python/object/apply:os.system ['id']",
    "tpl: {{7*7}}",
    "xml: <!DOCTYPE root [<!ENTITY x 'bug'>]>",
    "fetch: http://localhost/",
    "req: https://google.com",
    "img: /dev/urandom"
]

os.makedirs('corpus', exist_ok=True)

# Generate high-value structural seeds
for i, template in enumerate(templates):
    with open(f'corpus/high_val_{i}', 'w') as f:
        f.write(template)

print(f"✅ Created {len(templates)} High-Value structural seeds.")