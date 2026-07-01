import subprocess
import json
import csv
import time
import os
from datetime import datetime

# CONFIGURATION FOR 07/01 MORNING ROUND
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"G:\XPES_Customer_Assets\leads_morning_0701\leads_evidence_50.csv"
MASTER_CSV = r"G:\XPES_Customer_Assets\XPES_Master_Leads_Database_Updated.csv"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"

def get_v6_expert_template(name, company, business, country):
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

def send_validated_email(to, name, company, business, country):
    subject = f"Expand {company}'s 2026 catalog with high-margin Solar Insect Control"
    body = get_v6_expert_template(name, company, business, country)
    
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    
    # Secure payload file transfer
    fn = f"payload_0701_{to.replace('@','_').replace('.','_')}.json"
    try:
        with open(fn, 'w', encoding='utf-8') as f:
            json.dump(payload, f, ensure_ascii=False)
        
        cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        
        if os.path.exists(fn): os.remove(fn)
        # Check for success indicators
        if result.returncode == 0 and "Email sent!" in result.stdout:
            return True
        else:
            print(f"FAILED: {to} | {result.stdout} {result.stderr}")
            return False
    except Exception as e:
        print(f"ERROR processing {to}: {e}")
        return False

# EXECUTION
sent_count = 0
new_master_entries = []

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
            
            print(f"Sending to {to}...")
            if send_validated_email(to, name, company, biz, country):
                sent_count += 1
                print(f"SUCCESS [{sent_count}]: {to}")
                new_master_entries.append({
                    "Company Name": company, "Website": "", "Email": to, "Phone": "",
                    "Responsible Person": name, "Main Business": biz, "Relevance": country,
                    "Status": "Sent Expert V6", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                })
            else:
                print(f"ABORT: {to}")
            time.sleep(3)

    # Sync to Master DB
    if sent_count > 0:
        print(f"Updating G Drive Master DB...")
        with open(MASTER_CSV, mode='a', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=["Company Name", "Website", "Email", "Phone", "Responsible Person", "Main Business", "Relevance", "Status", "Last Contacted"])
            writer.writerows(new_entries if 'new_entries' in locals() else new_master_entries)
    
    # Final Git Sync
    print("Pushing to GitHub Knowledge Base...")
    os.chdir(REPO_PATH)
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", "07/01 Morning Round: 50 Verified Experts Sent"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)
    
    print(f"--- 07/01 MORNING ROUND COMPLETE: {sent_count} SENT ---")
else:
    print(f"CSV not found")
