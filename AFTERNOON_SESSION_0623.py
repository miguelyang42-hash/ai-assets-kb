import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
MASTER_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\XPES_Master_Leads_Database.csv"
NEW_LEADS_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_afternoon_verified\leads_evidence_50.csv"

# Bounced emails to purge
BOUNCED = [
    "mike.alcock@diy.com", "mliu@miloenterprises.com", "sourcing@scotts.com.au",
    "m.thibaut@mr-bricolage.com", "monika.baesel@hornbach.com", "frank.feiertag@obi.de",
    "vadim.chernov@obi.de", "anton.bezbokov@castorama.fr", "ignacio.villares@leroymerlin.fr",
    "catalin.lene@leroymerlin.fr", "alain.ryckeboer@leroymerlin.fr", "francois.noel@castorama.fr",
    "elena.shatalova@leroymerlin.fr", "sjassal@bunnings.com.au", "jweinstein@woodstream.com",
    "cfowler@target-specialty.com", "matthew.henriksen@stvuk.com", "ykim@homeplus.co.kr",
    "aeo@homeplus.co.kr", "mahmood.obaid@saco-ksa.com", "frederique.mussat-broussard@leroymerlin.fr",
    "olga.ponadtsova@obi.de", "montaser.abdullah@saco-ksa.com", "m.nabaa@saco-ksa.com",
    "anna.hosszu@procurementservices.co.uk", "karen.fillingham@procurementservices.co.uk",
    "kristen.coenen@canadiantire.ca"
]

def send_via_json(to, subject, body):
    payload = {"to": to, "subject": subject, "body": body, "body_format": "html", "user_google_email": USER_EMAIL}
    fn = f"temp_send_{to.replace('@','_').replace('.','_')}.json"
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
    res = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    if os.path.exists(fn): os.remove(fn)
    return res.returncode == 0

def get_day1_body(name, company, business):
    return f"""<html><body style="font-family: Arial; line-height: 1.6;">
<p>Hi {name},</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>I noticed {company}'s leadership in {business} and wanted to share a breakthrough.</p>
<p>As a <b>pioneer in Solar Mosquito Killer Lamps since 2020</b>, our <b>2026 4500V Industrial Model</b> matches grid power with <b>Zero Electricity Cost</b>.</p>
<p><b>Highlights:</b> 4500V Grid, 3-Day Battery, IP65 Waterproof.</p>
<p>Would you be open to our 2026 Catalog? Just reply "YES".</p><br>
<p>Best regards,<br><b>Miguel Yang</b><br>Guangdong Xingpu Energy Saving Light</p></body></html>"""

def get_day5_body(name, company):
    return f"""<html><body style="font-family: Arial; line-height: 1.6;">
<p>Hi {name},</p>
<p>Following up on the <b>4500V Solar tech</b>. Skeptical about solar power?</p>
<p>Our 2026 model maintains <b>4500V discharge even after 3 cloudy days</b>, matching AC units while being 100% sustainable.</p>
<p><b>Data:</b> Constant 4500V DC, 365nm UV-LED, Auto-cleaning grid.</p>
<p>Useful for your sourcing team?</p><br>
<p>Best regards,<br><b>Miguel Yang</b><br>Guangdong Xingpu Energy Saving Light</p></body></html>"""

# 1. PURGE AND IDENTIFY FOLLOW-UPS
master_data = []
followups = [] # (email, name, company)
with open(MASTER_CSV, mode='r', encoding='utf-8-sig') as f:
    reader = csv.DictReader(f)
    headers = reader.fieldnames
    for row in reader:
        email = row['Email'].strip().lower()
        if email in [e.lower() for e in BOUNCED]:
            row['Status'] = "Invalid (Bounced)"
        
        # Identify June 18th batch for Day 5
        # For simplicity, we match the known emails
        if email in ["rrh228@verizon.net", "mhousman@flowtron.com", "zoconnell@helenoftroy.com", "yuriy@tbi-pro.com"]:
             if row['Status'] != "Sent Day 5":
                 followups.append((row['Email'], row['Responsible Person'], row['Company Name']))
        
        master_data.append(row)

# 2. SEND DAY 5 FOLLOW-UPS
print(f"Starting Day 5 Follow-ups ({len(followups)})...")
for e, n, c in followups:
    if send_via_json(e, f"[Data] Solar vs. AC Grid performance for {c}", get_day5_body(n, c)):
        print(f"FOLLOWUP SUCCESS: {e}")
        for row in master_data:
            if row['Email'].lower() == e.lower():
                row['Status'] = "Sent Day 5"
                row['Last Contacted'] = datetime.now().strftime("%Y-%m-%d")
    time.sleep(3)

# 3. SEND DAY 1 NEW LEADS
new_sent = 0
if os.path.exists(NEW_LEADS_CSV):
    with open(NEW_LEADS_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if new_sent >= 50: break
            if send_via_json(row['Email'], f"[Innovation] 4500V Solar Mosquito Tech for {row['Company']}", get_day1_body(row['Name'], row['Company'], row['Category'])):
                print(f"NEW SENT: {row['Email']}")
                new_sent += 1
                # Add to master or update if exists
                found = False
                for mrow in master_data:
                    if mrow['Email'].lower() == row['Email'].lower():
                        mrow['Status'] = "Sent Day 1"
                        mrow['Last Contacted'] = datetime.now().strftime("%Y-%m-%d")
                        found = True
                if not found:
                    master_data.append({
                        "Company Name": row['Company'], "Website": "", "Email": row['Email'], "Phone": "",
                        "Responsible Person": row['Name'], "Main Business": row['Category'], "Relevance": row['Country'],
                        "Status": "Sent Day 1", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                    })
            time.sleep(3)

# 4. SAVE MASTER DATABASE
with open(MASTER_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(master_data)

print(f"Final Count - New: {new_sent}, Followup: {len(followups)}")
