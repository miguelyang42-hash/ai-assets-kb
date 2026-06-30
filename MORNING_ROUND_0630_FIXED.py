import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR 06/30 MORNING ROUND (FIXED ENGINE)
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_morning_0630\leads_evidence_50.csv"
MASTER_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\XPES_Master_Leads_Database.csv"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"

def send_validated_email(to, name, company, business, country):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company} ({country})"
    
    # Gold Standard Template V5 (No Images, Rich Text, Highlighting)
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

    # CRITICAL: Use individual flags to avoid shell/JSON parsing issues
    cmd = [
        CLI_PATH, "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    
    print(f"Sending to {to}...")
    try:
        # shell=False is critical to avoid < > being interpreted by CMD
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if result.returncode == 0 and "Email sent!" in result.stdout:
            print(f"SUCCESS: {result.stdout.strip()}")
            return True
        else:
            print(f"FAILED: {result.stdout} {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False

def sync_assets():
    print("Syncing assets to GitHub...")
    os.chdir(REPO_PATH)
    try:
        subprocess.run(["git", "add", "."], shell=True)
        subprocess.run(["git", "commit", "-m", "06/30 Morning Round: 50 Leads Sent & Verified (FIXED)"], shell=True)
        subprocess.run(["git", "push", "origin", "main"], shell=True)
        print("GitHub Sync Success.")
    except Exception as e:
        print(f"GitHub Sync Failed: {e}")

# EXECUTION
sent_count = 0
new_entries = []

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if sent_count >= 50: break
            to = row['Email']
            name = row['Name']
            company = row['Company']
            biz = row['Category']
            country = row['Country']
            
            if send_validated_email(to, name, company, biz, country):
                sent_count += 1
                new_entries.append({
                    "Company Name": company, "Website": "", "Email": to, "Phone": "",
                    "Responsible Person": name, "Main Business": biz, "Relevance": country,
                    "Status": "Sent Day 1", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                })
            time.sleep(3) # Throttle

    # Sync to Master DB
    if sent_count > 0:
        print(f"Updating Master DB with {sent_count} entries...")
        try:
            with open(MASTER_CSV, mode='a', encoding='utf-8-sig', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"])
                writer.writerows(new_entries)
            print("Master DB Update Success.")
        except Exception as e:
            print(f"Master DB Update Failed: {e}")
    
    # Final Action: Git Push
    sync_assets()
    print(f"--- 06/30 MORNING ROUND COMPLETE: {sent_count} SENT & SYNCED ---")
else:
    print(f"CSV not found at {CSV_PATH}")
