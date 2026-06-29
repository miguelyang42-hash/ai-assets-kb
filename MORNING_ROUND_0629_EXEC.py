import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR 06/29 MORNING ROUND
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_morning_0629\leads_evidence_50.csv"
MASTER_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\XPES_Master_Leads_Database.csv"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"

def send_validated_email(to, name, company, business, country):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company} ({country})"
    
    # Gold Standard Template V5 (No Images, Rich Text)
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
    
    fn = f"payload_morn_{to.replace('@','_').replace('.','_')}.json"
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if os.path.exists(fn): os.remove(fn)
    return result.returncode == 0

def sync_assets():
    print("Syncing assets to GitHub...")
    # Navigate to repo
    os.chdir(REPO_PATH)
    subprocess.run(["git", "add", "XPES_Customer_Assets/"], shell=True)
    subprocess.run(["git", "commit", "-m", f"Sync: 06/29 Morning Round - 50 Leads Added"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)

# EXECUTION
sent_count = 0
new_master_entries = []

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if sent_count >= 50: break
            if send_validated_email(row['Email'], row['Name'], row['Company'], row['Category'], row['Country']):
                sent_count += 1
                print(f"SUCCESS [{sent_count}]: {row['Email']}")
                new_master_entries.append({
                    "Company Name": row['Company'], "Website": "", "Email": row['Email'], "Phone": "",
                    "Responsible Person": row['Name'], "Main Business": row['Category'], "Relevance": row['Country'],
                    "Status": "Sent Day 1", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                })
            time.sleep(3)

    # Sync to Master DB
    if os.path.exists(MASTER_CSV):
        with open(MASTER_CSV, mode='a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"])
            writer.writerows(new_master_entries)
    
    # Final Action: Git Push
    sync_assets()
    print(f"--- 06/29 MORNING ROUND COMPLETE: {sent_count} SENT & SYNCED ---")
else:
    print(f"CSV not found")
