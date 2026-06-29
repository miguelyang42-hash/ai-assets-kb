import subprocess
import json
import csv
import os
import time

# FIX: shell=False to avoid CMD redirection issues with HTML tags
# FIX: Full list of leads for catch-up and verification

CSV_PATH = "XPES_Customer_Assets/stress_test/max_leads.csv"
USER_EMAIL = "miguelyang42@gmail.com"

IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"

def send_email(to, name, company, business):
    subject = f"[Direct Factory] 4500V Solar Mosquito Technology for {company} 2026 Lineup"
    
    body = f"""
    <html>
    <body>
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
    <p><img src="{IMAGE_URL}" width="200" alt="Solar Mosquito Lamp"></p>
    <p>Would you be open to a quick look at our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>
    <br>
    <p>Best regards,</p>
    <p><b>Miguel Yang</b><br>
    Business Development Manager<br>
    <b>Guangdong Xingpu Energy Saving Light</b></p>
    </body>
    </html>
    """
    
    cmd = [
        r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd", "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    
    # CRITICAL: shell=False on Windows with list to prevent CMD from mangling < and >
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if result.returncode == 0:
        print(f"SUCCESS: {to} | Output: {result.stdout.strip()}")
        return True
    else:
        print(f"FAILED: {to} | Error: {result.stderr.strip()}")
        return False

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            if count >= 50: break
            target_email = row.get('Email')
            target_name = row.get('Name')
            target_company = row.get('Company')
            target_business = row.get('Category')
            
            if target_email and send_email(target_email, target_name, target_company, target_business):
                count += 1
            time.sleep(2) # Prevent Gmail rate limiting
    print(f"Finished! Total verified sent: {count}")
else:
    print(f"CSV not found")
