import subprocess
import json
import csv
import os
import time
import sys

# Configuration for Catch-up
CSV_PATH = "XPES_Customer_Assets/leads_catchup/leads_60.csv"
USER_EMAIL = "miguelyang42@gmail.com"
MAX_EMAILS = 60 # Catch-up for Jun 19, 20, 21

IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"

def send_email(to, name, company, business):
    # Subject with Highlighting
    subject = f"[Urgent Innovation] High-Efficiency Solar 4500V Technology for {company} 2026"
    
    # HTML Body with Highlighting and Image
    body = f"""
    <html>
    <body>
    <p>Hi {name},</p>
    <p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
    <p>I apologize if this reaches you at a busy time, but I noticed {company}'s focus on {business} and wanted to share a breakthrough.</p>
    <p>Since 2020, our factory has pioneered <b>Solar Mosquito Killer Lamps</b>. We've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
    <p><b>Why leading brands are switching:</b></p>
    <ul>
        <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade performance.</li>
        <li><b>Advanced Solar Charging</b>: Full power even after <b>3 cloudy days</b>.</li>
        <li><b>Self-Cleaning Feature</b>: Significant reduction in maintenance complaints.</li>
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
    
    # Avoid printing name with special characters to prevent encoding errors on Windows shell
    print(f"Sending to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {to}")
        return True
    else:
        print(f"FAILED: {to} | Error: {result.stderr}")
        return False

# Execution
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        sent_count = 0
        for row in reader:
            if sent_count >= MAX_EMAILS: break
            
            success = send_email(row['Email'], row['Responsible Person'], row['Company Name'], row['Main Business'])
            if success: sent_count += 1
            time.sleep(2) 
    print(f"--- Finished! Total sent in this run: {sent_count} ---")
else:
    print(f"CSV not found at {CSV_PATH}")
