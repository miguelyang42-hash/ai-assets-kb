import subprocess
import json
import csv
import os
import time

# NEW TARGET: leads_now/leads_10.csv
CSV_PATH = "XPES_Customer_Assets/leads_now/leads_10.csv"
USER_EMAIL = "miguelyang42@gmail.com"

IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"

def send_email(to, name, company, business):
    subject = f"[Innovation] 2026 Solar 4500V Technology for {company}?"
    
    body = f"""
    <html>
    <body>
    <p>Hi {name},</p>
    <p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
    <p>I noticed {company}'s leadership in {business} and wanted to share a breakthrough.</p>
    <p>Since 2020, our factory has pioneered <b>Solar Mosquito Killer Lamps</b>. We've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It matches the killing power of traditional AC units with <b>Zero Electricity Cost</b>.</p>
    <p><b>Key Innovations:</b></p>
    <ul>
        <li><b>4500V Grid</b>: Industrial grade power.</li>
        <li><b>3-Day Battery</b>: Works even in cloudy weather.</li>
        <li><b>Self-Cleaning</b>: Lower maintenance.</li>
    </ul>
    <p><img src="{IMAGE_URL}" width="200" alt="Solar Mosquito Lamp"></p>
    <p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>
    <br>
    <p>Best regards,</p>
    <p><b>Miguel Yang</b><br>
    Business Development Manager<br>
    <b>Guangdong Xingpu Energy Saving Light</b></p>
    </body>
    </html>
    """
    
    cmd = [
        "accio-mcp-cli", "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    
    print(f"Sending to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {to}")
        return True
    else:
        print(f"FAILED: {to}")
        return False

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if send_email(row['Email'], row['Responsible Person'], row['Company Name'], row['Main Business']):
                count += 1
            time.sleep(2)
    print(f"Finished! Total sent: {count}")
else:
    print(f"CSV not found: {CSV_PATH}")
