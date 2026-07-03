import subprocess
import csv
import time
import os
from datetime import datetime

# CONFIGURATION
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

def get_expert_v6_template(name, company, business, country):
    return f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>
<p>Given {company}'s leadership in {business} within the {country} market, I’ll keep this brief.</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>Our new <b>2026 4500V Industrial-Grade Solar Model</b> is a current category killer.</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

def send_via_subprocess(to, subject, body):
    cmd = [
        CLI_PATH, "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    print(f"RC: {result.returncode}")
    print(f"OUT: {result.stdout}")
    print(f"ERR: {result.stderr}")
    return result.returncode == 0

# Test with 2 real emails from the afternoon batch
send_via_subprocess("matt.ray@orgill.com", "Test Round", get_expert_v6_template("Matt Ray", "Orgill", "Outdoor", "US"))
send_via_subprocess("sthompson@orgill.com", "Test Round", get_expert_v6_template("S Thompson", "Orgill", "Outdoor", "US"))
