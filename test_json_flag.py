import subprocess
import json
import os

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"

def send_via_json_flag(to, subject, body):
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    json_str = json.dumps(payload)
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json", json_str]
    # In python subprocess, passing a string that contains quotes can be tricky on Windows.
    # We use shell=False and list.
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    print(f"OUT: {result.stdout}")
    print(f"ERR: {result.stderr}")
    return result.returncode == 0

send_via_json_flag("miguelyang42@gmail.com", "JSON Flag Test", "<b>Success!</b>")
