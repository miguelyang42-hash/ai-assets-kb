import subprocess
import json
import os

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"

payload = {
    "to": USER_EMAIL,
    "subject": "Format Verification Round",
    "body": "Hi, this is a format verification.",
    "body_format": "html",
    "user_google_email": USER_EMAIL
}

with open('debug_payload.json', 'w') as f:
    json.dump(payload, f)

cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", "debug_payload.json"]
result = subprocess.run(cmd, capture_output=True, text=True, shell=False)

print(f"RC: {result.returncode}")
print(f"OUT: {result.stdout}")
print(f"ERR: {result.stderr}")
