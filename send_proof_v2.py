import subprocess
import json
import os

# DEFINITIVE FIX: Use a JSON file to transfer data to MCP CLI
# This bypasses all Windows Shell redirection (< >) and character escaping issues (\u0020)

USER_EMAIL = "miguelyang42@gmail.com"
IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"

def send_perfect_proof_email(to, name):
    subject = "[RE-TEST] Gold Standard Format Verification - Miguel Yang"
    
    # HTML content with proper formatting and signature
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>This is a <b>Gold Standard</b> format test. Key features of our 2026 4500V Solar Model:</p>
<ul>
    <li><b>4500V Grid</b>: Industrial grade power.</li>
    <li><b>Zero Electricity Cost</b>: 100% Solar powered.</li>
</ul>

<p><img src="{IMAGE_URL}" width="300" alt="Solar Mosquito Lamp" style="display: block; margin: 20px 0;"></p>

<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    
    # Save to file
    with open('proof_payload.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    # Call MCP using --json-file
    cmd = [
        r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd",
        "call", "send_gmail_message", "--json-file", "proof_payload.json"
    ]
    
    print(f"Sending perfect proof to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# Run self-test
if send_perfect_proof_email(USER_EMAIL, "Miguel"):
    print("SUCCESS: Proof email sent to your inbox.")
else:
    print("FAILED: Check script errors.")
