import subprocess
import json
import csv
import time
import os

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"
GOLDEN_IMAGE_URL = "https://sc02.alicdn.com/kf/H8e7cedfb014d48649ed8a741c41c47daZ.jpg"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_morning\leads_morning_50.csv"

def send_robust_text_email(to, name, company, business):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company}"
    
    body = f"""Hi {name},

I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light.

I am writing to you regarding {company}'s leadership in {business}.

Since 2020, our factory has pioneered Solar Mosquito Killer Lamps. Our 2026 4500V Industrial-Grade Solar Model matches traditional AC grid units with Zero Electricity Cost.

Performance Highlights:
- 4500V High-Voltage Grid: Consistent industrial-grade kill power.
- 3-Day Battery Backup: Optimized for cloudy weather.
- IP65 Waterproofing: Perfect for outdoor durability.

Did you do the market survey for your local market selling? I would like to share our quotation and local hotsale model with you.

Product Preview: {GOLDEN_IMAGE_URL}

Best regards,

Miguel Yang
Business Development Manager
Guangdong Xingpu Energy Saving Light"""

    # CALL CLI WITH SEPARATE ARGUMENTS (No shell, no JSON mangling)
    cmd = [
        CLI_PATH, "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--user_google_email", USER_EMAIL
    ]
    
    print(f"Sending text copy to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if result.returncode == 0:
        print(f"SUCCESS: {to}")
        return True
    else:
        print(f"FAILED: {to} | Error: {result.stderr}")
        return False

# EXECUTE TOP 20 TO ENSURE VOLUME
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 20: break
            if send_robust_text_email(row['Email'], row['Name'], row['Company'], row['Category']):
                count += 1
            time.sleep(3)
    print(f"--- ROBUST TEXT ROUND FINISHED: {count} SENT ---")
else:
    print(f"CSV not found")
