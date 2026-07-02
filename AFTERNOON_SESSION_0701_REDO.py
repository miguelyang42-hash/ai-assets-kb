import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
MASTER_CSV = r"G:\XPES_Customer_Assets\XPES_Master_Leads_Database_Updated.csv"
NEW_LEADS_CSV = r"G:\XPES_Customer_Assets\leads_afternoon_0701\leads_verified_50.csv"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"

# RECIPIENTS WHO HAVE REPLIED (DO NOT FOLLOW UP)
REPLIED_EMAILS = ["sydney.goh@bunnings.com.au"]

def send_via_json(to, subject, body):
    payload = {"to": to, "subject": subject, "body": body, "body_format": "html", "user_google_email": USER_EMAIL}
    # Unique temp file
    safe_to = to.replace("@","_").replace(".","_")
    filename = f"payload_af_redo_{safe_to}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
        # shell=False to avoid CMD mangling
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if os.path.exists(filename): os.remove(filename)
        return result.returncode == 0 and "Email sent!" in result.stdout
    except:
        return False

def get_expert_v6_template(name, company, business, country):
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

def get_followup_v6_template(name, company):
    return f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>Just checking if you had a chance to review my previous note regarding the <b>2,000 units/day</b> sales traction we're seeing with our <b>4500V Solar tech</b>.</p>

<p>Skeptical about solar vs grid-powered units? Our 2026 industrial model maintains a consistent <b>4500V discharge even after 3 cloudy days</b>, matching the performance of standard AC units without the cable hassle or electricity cost.</p>

<p>Given {company}'s focus on high-performance outdoor solutions, I'd like to share our <b>technical comparison report</b> and wholesale pricing structure.</p>

<p>Would this be of interest for your upcoming procurement review?</p>

<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

# --- EXECUTION ---
new_sent = 0
followup_sent = 0
master_rows = []

# 1. READ MASTER DATA
if os.path.exists(MASTER_CSV):
    with open(MASTER_CSV, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            master_rows.append(row)

# 2. IDENTIFY AND SEND FOLLOW-UPS
# Target those sent Day 1/Day 5 previously but haven't replied
for row in master_rows:
    email = row['Email'].strip().lower()
    status = row.get('Status', '')
    if status in ["Sent Day 1", "Sent Day 5", "Sent Expert V6"] and email not in [e.lower() for e in REPLIED_EMAILS]:
        # For this turn, we follow up on key targets
        print(f"Sending Follow-up to {email}...")
        if send_via_json(email, f"Follow-up: Solar vs. AC Grid performance for {row['Company Name']}", get_followup_v6_template(row['Responsible Person'], row['Company Name'])):
            row['Status'] = "Follow-up V6"
            row['Last Contacted'] = datetime.now().strftime("%Y-%m-%d")
            followup_sent += 1
        time.sleep(3)

# 3. SEND NEW LEADS
if os.path.exists(NEW_LEADS_CSV):
    with open(NEW_LEADS_CSV, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if new_sent >= 50: break
            to = row['Email']
            name = row['Name']
            company = row['Company']
            biz = row['Category']
            country = row['Country']
            
            print(f"Sending Day 1 to {to}...")
            if send_via_json(to, f"Expand {company}'s 2026 catalog with high-margin Solar Insect Control", get_expert_v6_template(name, company, biz, country)):
                new_sent += 1
                master_rows.append({
                    "Company Name": company, "Website": "", "Email": to, "Phone": "",
                    "Responsible Person": name, "Main Business": biz, "Relevance": country,
                    "Status": "Sent Expert V6", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                })
            time.sleep(3)

# 4. SAVE MASTER DATABASE
with open(MASTER_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(master_rows)

# 5. GIT SYNC
print("Syncing to GitHub...")
os.chdir(REPO_PATH)
try:
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", f"Afternoon Round 07/01 REDO: {new_sent} New, {followup_sent} Followups"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)
    print("GitHub Sync Done.")
except Exception as e:
    print(f"Git Error: {e}")

print(f"FINISHED: {new_sent} New, {followup_sent} Followups.")
