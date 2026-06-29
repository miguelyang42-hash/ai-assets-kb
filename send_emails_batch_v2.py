import subprocess
import json
import os

with open('payloads.json', 'r', encoding='utf-8') as f:
    payloads = json.load(f)

for p in payloads:
    print(f"Sending to {p['to']}...")
    json_str = json.dumps(p)
    # Using a list for arguments to avoid shell issues
    # Note: we might need shell=True if accio-mcp-cli is a batch/cmd script on Windows
    # but we can try without first or find its location
    cmd = ["accio-mcp-cli", "call", "send_gmail_message", "--json", json_str]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
        print(result.stdout)
        print(result.stderr)
    except Exception as e:
        print(f"Error: {e}")
