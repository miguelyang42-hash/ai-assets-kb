import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR MAX CATCHUP ROUND
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_overseas_catchup\leads_verified_100.csv"
MASTER_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\XPES_Master_Leads_Database.csv"

def send_via_json_file(to, subject, body):
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    # Use unique payload file to avoid concurrency issues
    safe_to = to.replace("@","_").replace(".","_")
    filename = f"payload_max_{safe_to}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        
        # Absolute path call
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        
        if os.path.exists(filename):
            os.remove(filename)
        return result.returncode == 0
    except Exception as e:
        print(f"Error sending to {to}: {e}")
        return False

def get_gold_template(name, company, business, country):
    return f"""<html>
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

<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

# EXECUTION
sent_count = 0
new_master_entries = []

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if sent_count >= 100: break
            
            # Send Email
            to = row['Email']
            name = row['Name']
            company = row['Company']
            biz = row['Category']
            country = row['Country']
            
            body = get_gold_template(name, company, biz, country)
            subject = f"[Innovation] 4500V Solar Mosquito Technology for {company} ({country})"
            
            print(f"Sending to {to}...")
            if send_via_json_file(to, subject, body):
                sent_count += 1
                print(f"SUCCESS [{sent_count}]: {to}")
                # Track for Master DB
                new_master_entries.append({
                    "Company Name": company, "Website": "", "Email": to, "Phone": "",
                    "Responsible Person": name, "Main Business": biz, "Relevance": country,
                    "Status": "Sent Day 1", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                })
            else:
                print(f"FAILED: {to}")
            
            # Safety delay to prevent Gmail rate limiting for 100 emails
            time.sleep(3)

    # Sync to Master DB
    if os.path.exists(MASTER_CSV):
        with open(MASTER_CSV, mode='a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"])
            writer.writerows(new_master_entries)
    
    print(f"--- MAX CATCHUP COMPLETE: {sent_count} SENT ---")
else:
    print(f"CSV not found")
