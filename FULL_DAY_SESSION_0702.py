import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"
MASTER_CSV = r"G:\XPES_Customer_Assets\XPES_Master_Leads_Database_Updated.csv"

# DATA SOURCES
SOURCE_MORNING = r"G:\XPES_Customer_Assets\leads_morning_0702\leads_evidence_50.csv"
SOURCE_AFTERNOON = r"G:\XPES_Customer_Assets\leads_afternoon_0702\leads_verified_50.csv"

# RECIPIENTS TO EXCLUDE
REPLIED_EMAILS = ["sydney.goh@bunnings.com.au"]

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

def get_day12_body(name, company):
    return f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>
<p>Market data shows a significant shift toward "Zero Electricity" outdoor gear in 2026.</p>
<p>One of our partners recently reported a <b>28% higher conversion rate</b> on their solar listing compared to their standard AC version. Our <b>4500V Solar tech</b> is proving to be the primary driver for high-margin "Green Growth" this season.</p>
<p>Given {company}'s market reach, I thought you'd be interested in seeing the ROI projections for adding this industrial solar unit to your lineup before the next peak period.</p>
<p>Would you like me to send over our 2026 Market Success Report and pricing?</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

def send_via_json(to, subject, body):
    payload = {"to": to, "subject": subject, "body": body, "body_format": "html", "user_google_email": USER_EMAIL}
    safe_to = to.replace("@","_").replace(".","_")
    filename = f"payload_0702_{safe_to}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if os.path.exists(filename): os.remove(filename)
        return result.returncode == 0 and "Email sent!" in result.stdout
    except Exception as e:
        print(f"Error: {e}")
        return False

# --- EXECUTION ---
new_sent = 0
fup_sent = 0
master_rows = []

# 1. READ MASTER DATA
if os.path.exists(MASTER_CSV):
    with open(MASTER_CSV, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            master_rows.append(row)

# 2. SEND DAY 12 FOLLOW-UPS (Due for June 23rd batch)
targets_fup_12 = ["rrh228@verizon.net", "mhousman@flowtron.com", "zoconnell@helenoftroy.com", "yuriy@tbi-pro.com", "mliu@miloenterprises.com"]
for row in master_rows:
    email = row['Email'].strip().lower()
    if email in targets_fup_12 and "Sent Day 5" in row['Status'] and email not in REPLIED_EMAILS:
        print(f"Sending Day 12 Follow-up to {email}...")
        if send_via_json(email, f"Market Momentum: Why Solar is leading 2026 for {row['Company Name']}", get_day12_body(row['Responsible Person'], row['Company Name'])):
            row['Status'] = "Sent Day 12"
            row['Last Contacted'] = datetime.now().strftime("%Y-%m-%d")
            fup_sent += 1
        time.sleep(3)

# 3. SEND NEW OUTREACH (Morning + Afternoon)
new_sources = [SOURCE_MORNING, SOURCE_AFTERNOON]
for src in new_sources:
    if os.path.exists(src):
        with open(src, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                to = row['Email']
                if send_via_json(to, f"Expand {row['Company']}'s 2026 catalog with high-margin Solar Insect Control", get_expert_v6_template(row['Name'], row['Company'], row['Category'], row['Country'])):
                    new_sent += 1
                    print(f"NEW SENT: {to}")
                    # Add to master
                    master_rows.append({
                        "Company Name": row['Company'], "Website": "", "Email": to, "Phone": "",
                        "Responsible Person": row['Name'], "Main Business": row['Category'], "Relevance": row['Country'],
                        "Status": "Sent Expert V6", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                    })
                time.sleep(3)

# 4. SAVE MASTER DB
with open(MASTER_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(master_rows)

# 5. GIT SYNC
print("Syncing to GitHub...")
os.chdir(REPO_PATH)
try:
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", f"Full Day Round 07/02: {new_sent} New, {fup_sent} Followups"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)
    print("GitHub Sync Done.")
except Exception as e:
    print(f"Git Error: {e}")

print(f"COMPLETED: {new_sent} New, {fup_sent} Followups.")
