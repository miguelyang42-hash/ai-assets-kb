import subprocess
import json
import csv
import time
import os

# CONFIGURATION FOR MORNING SESSION (06/23)
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_morning_0623\leads_verified_50.csv"
GOLDEN_IMAGE = "https://sc02.alicdn.com/kf/H8e7cedfb014d48649ed8a741c41c47daZ.jpg"

def send_perfect_morning_email(to, name, company, business, country):
    subject = f"[Innovation] 2026 Solar 4500V Mosquito Technology for {company} ({country})"
    
    # EXACT TEMPLATE: HD Thumbnail + Rich Text + Miguel Yang Signature
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>I noticed {company}'s leadership in {business} within the {country} market, and I am reaching out with a breakthrough for your 2026 lineup.</p>

<p>As a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>, we have just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>

<p><b>Performance Highlights:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for extreme outdoor durability.</li>
</ul>

<p>Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.</p>

<div style="margin: 20px 0;">
    <img src="{GOLDEN_IMAGE}" width="300" alt="Solar Mosquito Killer Lamp" style="border: 1px solid #ddd; border-radius: 4px;">
    <p style="font-size: 11px; color: #999;">XPES 4500V Industrial Solar Unit</p>
</div>

<br>
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
    
    # Save to unique file to bypass shell issues
    fn = f"payload_0623_{to.replace('@','_').replace('.','_')}.json"
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
    
    print(f"Sending to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if os.path.exists(fn): os.remove(fn)
    
    return result.returncode == 0

# --- EXECUTION ---
if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 50: break
            if send_perfect_morning_email(row['Email'], row['Name'], row['Company'], row['Category'], row['Country']):
                print(f"SUCCESS [{count+1}]: {row['Email']}")
                count += 1
            else:
                print(f"FAILED: {row['Email']}")
            time.sleep(3) # Throttle
    print(f"--- 06/23 MORNING ROUND COMPLETED: {count} SENT ---")
else:
    print(f"CSV not found at {CSV_PATH}")
