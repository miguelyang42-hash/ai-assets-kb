import subprocess
import json
import csv
import os
import time

# STRESS TEST CONFIG
CSV_PATH = "XPES_Customer_Assets/stress_test/max_leads.csv"
USER_EMAIL = "miguelyang42@gmail.com"
MAX_COUNT = 50 

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
        "accio-mcp-cli", "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True, shell=True)
    return result.returncode == 0

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        count = 0
        start_time = time.time()
        for row in reader:
            if count >= MAX_COUNT: break
            # Mapping headers from Sub-agent format
            target_email = row.get('Email')
            target_name = row.get('Name')
            target_company = row.get('Company')
            target_business = row.get('Category')
            
            if target_email and send_email(target_email, target_name, target_company, target_business):
                count += 1
                print(f"[{count}] SUCCESS: {target_email}")
            else:
                print(f"FAILED: {target_email}")
            time.sleep(0.5) 
        
        duration = time.time() - start_time
        print(f"--- TEST COMPLETE ---")
        print(f"Total Sent: {count}")
        print(f"Total Time: {duration:.2f} seconds")
        print(f"Average Speed: {count/(duration/60):.2f} emails/min")
else:
    print(f"CSV not found")
