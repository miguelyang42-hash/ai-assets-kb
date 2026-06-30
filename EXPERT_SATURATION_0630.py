import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR EXPERT SATURATION ROUND (100 EMAILS)
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"
MASTER_CSV = r"G:\XPES_Customer_Assets\XPES_Master_Leads_Database_Updated.csv"

# DATA SOURCES
SOURCE_EVENING = r"G:\XPES_Customer_Assets\leads_evening_0630\leads_verified_50.csv"
SOURCE_MORNING = r"G:\XPES_Customer_Assets\leads_morning_0630\leads_evidence_50.csv"

def get_expert_template_v6(name, company, business, country):
    # Foreign Trade Expert V6: Professional, Direct, High-Margin Focus
    return f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>Given {company}'s leadership in {business} within the {country} market, I’ll keep this brief.</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>. Since 2020, we have been a direct-to-factory partner specializing in advanced Solar Mosquito control for top global brands.</p>

<p>Our new <b>2026 4500V Industrial-Grade Solar Model</b> is a current category killer in the US, averaging over <b>2,000 units sold per day</b>. It allows your brand to instantly capture the eco-friendly segment with zero electricity cost for the consumer.</p>

<p><b>Why this is a strategic add-on for your 2026 lineup:</b></p>
<ul>
    <li><b>Commercial-Grade Power</b>: 4500V high-voltage grid (Matches AC grid units).</li>
    <li><b>Hassle-Free Tech</b>: Dusk-to-dawn sensors for true "set-and-forget" convenience.</li>
    <li><b>Turnkey Compliance</b>: Fully compliant with <b>EPA, FCC, and RoHS</b> regulations.</li>
</ul>

<p>Would you be open to a quick look at the technical data sheet and our 2026 wholesale pricing?</p>

<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

def send_expert_via_json(to, subject, body):
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    safe_to = to.replace("@","_").replace(".","_")
    filename = f"payload_exp_{safe_to}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
        # shell=False to ensure no mangling
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if os.path.exists(filename): os.remove(filename)
        # Verify success string in output
        return result.returncode == 0 and "Email sent!" in result.stdout
    except:
        return False

# 1. PREPARE 100 EXPERT LEADS
leads_to_send = []

# Load Evening (New 50)
if os.path.exists(SOURCE_EVENING):
    with open(SOURCE_EVENING, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads_to_send.append(row)

# Load Morning (50 - these were botched earlier, need expert redo)
if os.path.exists(SOURCE_MORNING):
    with open(SOURCE_MORNING, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads_to_send.append(row)
            if len(leads_to_send) >= 100: break

# 2. EXECUTE 100 SENDINGS
sent_count = 0
new_master_entries = []

print(f"Starting 100 Email Expert Redo Round...")
for lead in leads_to_send:
    to = lead['Email']
    name = lead['Name']
    company = lead['Company']
    biz = lead['Category']
    country = lead['Country']
    
    subject = f"Expand {company}'s 2026 catalog with high-margin Solar Insect Control"
    body = get_expert_template_v6(name, company, biz, country)
    
    if send_expert_via_json(to, subject, body):
        sent_count += 1
        print(f"DONE [{sent_count}]: {to}")
        new_master_entries.append({
            "Company Name": company, "Website": "", "Email": to, "Phone": "",
            "Responsible Person": name, "Main Business": biz, "Relevance": country,
            "Status": "Sent Expert V6", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
        })
    else:
        print(f"FAIL: {to}")
    
    time.sleep(4) # Throttling for 100 consecutive emails

# 3. UPDATE MASTER DATABASE
if os.path.exists(MASTER_CSV):
    try:
        with open(MASTER_CSV, mode='a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"])
            writer.writerows(new_master_entries)
        print("Master DB Updated.")
    except Exception as e:
        print(f"DB Update Error: {e}")

# 4. FINAL GIT SYNC
print("Pushing to GitHub Knowledge Base...")
os.chdir(REPO_PATH)
subprocess.run(["git", "add", "."], shell=True)
subprocess.run(["git", "commit", "-m", "Expert Redo: 100 Sent with V6 Pro Template"], shell=True)
subprocess.run(["git", "push", "origin", "main"], shell=True)

print(f"--- 100 EMAIL SATURATION COMPLETED ---")
