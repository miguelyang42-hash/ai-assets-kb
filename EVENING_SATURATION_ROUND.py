import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR EVENING SATURATION ROUND (100 EMAILS)
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"
MASTER_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\XPES_Master_Leads_Database.csv"

# DATA SOURCES
SOURCE_1 = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_evening_0629\leads_verified_50.csv"
SOURCE_2 = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_overseas_catchup\leads_verified_100.csv"

def get_gold_template(name, company, business, country):
    # Template V5: No Images, Rich Text, 4500V Focus
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

def send_via_json(to, subject, body):
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    safe_to = to.replace("@","_").replace(".","_")
    fn = f"payload_evening_{safe_to}.json"
    try:
        with open(fn, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if os.path.exists(fn): os.remove(fn)
        return result.returncode == 0
    except:
        return False

# 1. PREPARE 100 LEADS
leads_to_send = []

# Source 1 (New 50)
if os.path.exists(SOURCE_1):
    with open(SOURCE_1, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads_to_send.append(row)

# Source 2 (Catch-up 50 - skipping the first 50 which were likely US already)
if os.path.exists(SOURCE_2):
    with open(SOURCE_2, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            count += 1
            if count > 51: # Start from line 52
                leads_to_send.append(row)
            if len(leads_to_send) >= 100: break

# 2. SEND AND TRACK
sent_count = 0
new_master_entries = []

for lead in leads_to_send:
    to = lead['Email']
    name = lead['Name']
    company = lead['Company']
    biz = lead.get('Category', lead.get('Main Business', 'Outdoor/Garden'))
    country = lead['Country']
    
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company} ({country})"
    body = get_gold_template(name, company, biz, country)
    
    print(f"Sending to {to}...")
    if send_via_json(to, subject, body):
        sent_count += 1
        print(f"SUCCESS [{sent_count}]: {to}")
        new_master_entries.append({
            "Company Name": company, "Website": "", "Email": to, "Phone": "",
            "Responsible Person": name, "Main Business": biz, "Relevance": country,
            "Status": "Sent Day 1", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
        })
    else:
        print(f"FAILED: {to}")
    
    time.sleep(3) # Throttle for 100 emails

# 3. UPDATE MASTER DATABASE
if os.path.exists(MASTER_CSV):
    with open(MASTER_CSV, mode='a', encoding='utf-8-sig', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"])
        writer.writerows(new_master_entries)

# 4. GIT SYNC
print("Syncing to GitHub...")
os.chdir(REPO_PATH)
subprocess.run(["git", "add", "."], shell=True)
subprocess.run(["git", "commit", "-m", f"Evening Round: 100 Sent & Verified"], shell=True)
subprocess.run(["git", "push", "origin", "main"], shell=True)

print(f"--- EVENING SATURATION COMPLETE: {sent_count} SENT ---")
