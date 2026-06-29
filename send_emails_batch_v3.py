import subprocess
import json
import os

with open('payloads.json', 'r', encoding='utf-8') as f:
    payloads = json.load(f)

exe_path = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

for p in payloads:
    print(f"Sending to {p['to']}...")
    json_str = json.dumps(p)
    cmd = [exe_path, "call", "send_gmail_message", "--json", json_str]
    try:
        # shell=False is default, which is what we want to avoid shell parsing
        result = subprocess.run(cmd, capture_output=True, text=True)
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
    except Exception as e:
        print(f"Error: {e}")
