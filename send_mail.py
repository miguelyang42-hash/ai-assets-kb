import subprocess
import json

with open('payload.json', 'r', encoding='utf-8') as f:
    payload = f.read()

cmd = ['accio-mcp-cli', 'call', 'send_gmail_message', '--json', payload]
result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
print(result.stderr)
