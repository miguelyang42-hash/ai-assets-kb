import subprocess
import csv
import time
import os

# FINAL GOLD STANDARD ENGINE: Python with shell=False
# Ensures zero HTML mangling on Windows

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_morning\leads_morning_50.csv"
USER_EMAIL = "miguelyang42@gmail.com"
IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"

def send_gold_email(to, name, company, business, country):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company} ({country})"
    
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>I noticed {company}'s leadership in {business} within the {country} market, and I'm reaching out with a breakthrough for your 2026 lineup.</p>

<p>As a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>, we have just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>

<p><b>Key Innovations for {country}:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for extreme outdoor durability.</li>
</ul>

<p><img src="{IMAGE_URL}" width="300" alt="Product Image" style="display: block; margin: 20px 0;"></p>

<p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>

<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

    cmd = [
        CLI_PATH, "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    
    print(f"Sending to {to} ({name})...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if result.returncode == 0:
            print(f"SUCCESS: {to}")
            return True
        else:
            print(f"FAILED: {to} | Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 50: break
            if send_gold_email(row['Email'], row['Name'], row['Company'], row['Category'], row['Country']):
                count += 1
            time.sleep(3) # Throttle to prevent Gmail spam detection
    print(f"--- MORNING ROUND COMPLETE: {count} SENT ---")
else:
    print(f"CSV not found at {CSV_PATH}")
