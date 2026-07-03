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
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"

# DATA SOURCES
SOURCE_MORN = r"G:\XPES_Customer_Assets\leads_morning_0703\leads_verified_50.csv"
SOURCE_AFTR = r"G:\XPES_Customer_Assets\leads_afternoon_0703\leads_verified_50.csv"

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

def get_followup_template(name, company):
    return f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>
<p>Market data shows a significant shift toward "Zero Electricity" outdoor gear in 2026. Our <b>4500V Solar tech</b> is leading the segment with <b>2,000 units/day</b> sales traction.</p>
<p>Our 2026 industrial model maintains a consistent <b>4500V discharge even after 3 cloudy days</b>. Matches AC performance without cables.</p>
<p>Given {company}'s market reach, I'd like to share the 2026 technical TDS and ROI comparison.</p>
<p>Would this be useful for your next review?</p>
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
    filename = f"payload_july03_{safe_to}.json"
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        if os.path.exists(filename): os.remove(filename)
        return result.returncode == 0 and "Email sent!" in result.stdout
    except:
        return False

# --- EXECUTION ---
sent_new = 0
sent_follow = 0
master_rows = []
if os.path.exists(MASTER_CSV):
    with open(MASTER_CSV, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader: master_rows.append(row)

# 1. SEND NEW LEADS (Morning + Afternoon)
sources = [SOURCE_MORN, SOURCE_AFTR]
for src in sources:
    if os.path.exists(src):
        with open(src, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if sent_new >= 100: break
                subject = f"Expand {row['Company']}'s 2026 catalog with high-margin Solar Insect Control"
                if send_via_json(row['Email'], subject, get_expert_v6_template(row['Name'], row['Company'], row['Category'], row['Country'])):
                    sent_new += 1
                    master_rows.append({
                        "Company Name": row['Company'], "Website": "", "Email": row['Email'], "Phone": "",
                        "Responsible Person": row['Name'], "Main Business": row['Category'], "Relevance": row['Country'],
                        "Status": "Sent Expert V6", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                    })
                time.sleep(3)

# 2. SEND FOLLOW-UPS
# Logic: Follow up on those sent 5+ days ago and no reply
# (Simplified target list for this turn)
fup_targets = ["rrh228@verizon.net", "mhousman@flowtron.com", "zoconnell@helenoftroy.com"]
for row in master_rows:
    if row['Email'].lower() in fup_targets and "V6" in row['Status']:
        if send_via_json(row['Email'], f"Follow-up: 2026 Solar Performance for {row['Company Name']}", get_followup_template(row['Responsible Person'], row['Company Name'])):
            row['Status'] = "Follow-up Sent"
            row['Last Contacted'] = datetime.now().strftime("%Y-%m-%d")
            sent_follow += 1
        time.sleep(3)

# 3. SAVE & SYNC
with open(MASTER_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(master_rows)

os.chdir(REPO_PATH)
subprocess.run(["git", "add", "."], shell=True)
subprocess.run(["git", "commit", "-m", f"July 03 Full Execution: {sent_new} New, {sent_follow} Followups"], shell=True)
subprocess.run(["git", "push", "origin", "main"], shell=True)

print(f"COMPLETE: {sent_new} New, {sent_follow} Followups.")
