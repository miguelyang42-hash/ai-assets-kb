import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR EXPERT LEVEL REDO (06/30)
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"G:\XPES_Customer_Assets\leads_morning_0630\leads_evidence_50.csv"
MASTER_CSV = r"G:\XPES_Customer_Assets\XPES_Master_Leads_Database_Updated.csv"

def send_expert_email(to, name, company, business, country):
    subject = f"Expand {company}'s 2026 catalog with high-margin Solar Insect Control"
    
    # Gold Standard Template V6 - Professional Foreign Trade Expert Style
    body = f"""<html>
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

    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    
    fn = f"payload_expert_{to.replace('@','_').replace('.','_')}.json"
    try:
        with open(fn, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        
        if os.path.exists(fn): os.remove(fn)
        return result.returncode == 0 and "Email sent!" in result.stdout
    except:
        return False

# EXECUTION
sent_count = 0
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
            
            print(f"Sending expert pitch to {to}...")
            if send_expert_email(to, name, company, biz, country):
                sent_count += 1
                print(f"SUCCESS [{sent_count}]: {to}")
            else:
                print(f"FAILED: {to}")
            time.sleep(3)
    print(f"--- EXPERT REDO COMPLETE: {sent_count} SENT ---")
else:
    print(f"CSV not found")
