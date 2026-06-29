import subprocess
import json
import os

with open('payloads.json', 'r', encoding='utf-8') as f:
    payloads = json.load(f)

for p in payloads:
    print(f"Sending to {p['to']}...")
    json_str = json.dumps(p)
    # On Windows, we need to be careful with the command
    # Try calling via shell=True for alias/shim resolution
    cmd = f'accio-mcp-cli call send_gmail_message --json "{json_str.replace(\'"\', \'\\\\"\')}"'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)
    print(result.stderr)
