import subprocess
import json
import time

CLI_PATH = "accio-mcp-cli"
USER_EMAIL = "miguelyang42@gmail.com"

recipients = [
    {"name": "Matt Ray", "email": "matt.ray@orgill.com"},
    {"name": "S Thompson", "email": "sthompson@orgill.com"},
    {"name": "B Walton", "email": "bwalton@orgill.com"}
]

template = """Hi {name},
I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light. 

We've released our 2026 4500V model with Zero Electricity Cost.

Regards, Miguel Yang"""

for recipient in recipients:
    body = template.format(name=recipient["name"])
    payload = {
        "to": recipient["email"],
        "subject": "2026 Model Release: Zero Electricity Cost 4500V Model - XPES",
        "body": body,
        "user_google_email": USER_EMAIL,
        "body_format": "plain"
    }
    
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json", json.dumps(payload)]
    print(f"Sending to {recipient['email']}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {result.stdout}")
    else:
        print(f"FAILED: {result.stderr}")
    
    time.sleep(1)
