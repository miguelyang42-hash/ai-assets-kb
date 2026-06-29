import subprocess
import json
import csv
import time
import os

# DEFINITIVE GOLD STANDARD PLAYBOOK SCRIPT
# Uses exact user template + verified Alibaba image URL

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"
GOLDEN_IMAGE = "https://sc02.alicdn.com/kf/H8e7cedfb014d48649ed8a741c41c47daZ.jpg"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_morning\leads_morning_50.csv"

def send_perfect_lead_email(to, name, company, business):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company}"
    
    # EXACT TEMPLATE FROM USER IMAGE
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>I am writing to you regarding {company}'s leadership in {business}.</p>

<p>We are a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>. I want to share our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>

<p><b>Performance Highlights:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for outdoor durability.</li>
</ul>

<p>Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.</p>

<div style="margin: 20px 0;">
    <img src="{GOLDEN_IMAGE}" width="600" alt="Solar Mosquito Killer Lamp">
</div>

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
    
    # Use a unique file per recipient to avoid race conditions or lock issues
    temp_filename = f"payload_{to.replace('@','_').replace('.','_')}.json"
    with open(temp_filename, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", temp_filename]
    
    print(f"Sending to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    # Clean up
    if os.path.exists(temp_filename):
        os.remove(temp_filename)
        
    return result.returncode == 0

# EXECUTION
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 50: break
            if send_perfect_lead_email(row['Email'], row['Name'], row['Company'], row['Category']):
                count += 1
                print(f"SUCCESS [{count}]: {row['Email']}")
            else:
                print(f"FAILED: {row['Email']}")
            time.sleep(3) # Safe delay
    print(f"--- GOLD STANDARD ROUND FINISHED: {count} SENT ---")
else:
    print(f"CSV not found")
