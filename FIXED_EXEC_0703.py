import subprocess
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

def send_via_subprocess(to, subject, body):
    cmd = [
        CLI_PATH, "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--body_format", "html",
        "--user_google_email", USER_EMAIL
    ]
    # shell=False is CRITICAL for Windows to pass arguments correctly without shell mangling
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    if result.returncode == 0 and "Email sent!" in result.stdout:
        return True
    else:
        print(f"FAILED TO SEND TO {to}: {result.stdout} {result.stderr}")
        return False

# --- EXECUTION ---
new_sent = 0
master_rows = []
if os.path.exists(MASTER_CSV):
    with open(MASTER_CSV, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader: master_rows.append(row)

# 1. SEND NEW LEADS
sources = [SOURCE_MORN, SOURCE_AFTR]
for src in sources:
    if os.path.exists(src):
        with open(src, mode='r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if new_sent >= 100: break
                subject = f"Expand {row['Company']}'s 2026 catalog with high-margin Solar Insect Control"
                body = get_expert_v6_template(row['Name'], row['Company'], row['Category'], row['Country'])
                if send_via_subprocess(row['Email'], subject, body):
                    new_sent += 1
                    print(f"SUCCESS [{new_sent}]: {row['Email']}")
                    master_rows.append({
                        "Company Name": row['Company'], "Website": "", "Email": row['Email'], "Phone": "",
                        "Responsible Person": row['Name'], "Main Business": row['Category'], "Relevance": row['Country'],
                        "Status": "Sent Expert V6", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                    })
                time.sleep(3)

# 2. SAVE MASTER DB
with open(MASTER_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(master_rows)

print(f"FINISHED: {new_sent} New emails sent.")
