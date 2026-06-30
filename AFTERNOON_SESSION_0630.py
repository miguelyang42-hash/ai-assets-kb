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
NEW_LEADS_CSV = r"G:\XPES_Customer_Assets\leads_afternoon_0630\leads_verified_50.csv"
REPO_PATH = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24"

# RECIPIENTS TO EXCLUDE (Manual list based on replies or blocks)
REPLIED_EMAILS = ["sydney.goh@bunnings.com.au"]

def send_via_json(to, subject, body):
    payload = {"to": to, "subject": subject, "body": body, "body_format": "html", "user_google_email": USER_EMAIL}
    # Unique temp file
    safe_to = to.replace("@","_").replace(".","_")
    filename = f"payload_af_{safe_to}.json"
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

def get_day1_body(name, company, business, country):
    return f"""<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
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
<b>Guangdong Xingpu Energy Saving Light</b></p></body></html>"""

def get_day5_body(name, company):
    return f"""<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>
<p>Just checking if you saw my previous note on the <b>4500V Solar tech</b>. A common question we get is: "Does solar really have enough power for industrial use?"</p>
<p>Our internal performance audit shows our 2026 model maintains a <b>4500V discharge even after 3 cloudy days</b>. This matches traditional AC units while being 100% sustainable.</p>
<p><b>Key Tech Specs:</b></p>
<ul>
    <li><b>Grid Output</b>: Constant 4500V DC.</li>
    <li><b>Wavelength</b>: 365nm UV-LED (Highest attraction rate).</li>
    <li><b>Maintenance</b>: Auto-cleaning grid design.</li>
</ul>
<p>Would this data be useful for your engineering or sourcing team? I'd be happy to share the full report.</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p></body></html>"""

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
# Targeted follow-ups for those sent on June 18th/21st (verified)
targets_for_fup = ["rrh228@verizon.net", "mhousman@flowtron.com", "zoconnell@helenoftroy.com", "mliu@miloenterprises.com", "yuriy@tbi-pro.com"]
for row in master_rows:
    email = row['Email'].strip().lower()
    if email in targets_for_fup and row['Status'] == "Sent Day 1" and email not in REPLIED_EMAILS:
        print(f"Sending Follow-up to {email}...")
        if send_via_json(email, f"[Data] Solar vs. AC Grid performance comparison for {row['Company Name']}", get_day5_body(row['Responsible Person'], row['Company Name'])):
            row['Status'] = "Sent Day 5"
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
            if send_via_json(to, f"[Innovation] 4500V Solar Mosquito Technology for {company} ({country})", get_day1_body(name, company, biz, country)):
                new_sent += 1
                # Add to master
                master_rows.append({
                    "Company Name": company, "Website": "", "Email": to, "Phone": "",
                    "Responsible Person": name, "Main Business": biz, "Relevance": country,
                    "Status": "Sent Day 1", "Last Contacted": datetime.now().strftime("%Y-%m-%d")
                })
            time.sleep(3)

# 4. SAVE UPDATED MASTER DB
with open(MASTER_CSV, mode='w', encoding='utf-8-sig', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=headers)
    writer.writeheader()
    writer.writerows(master_rows)

# 5. GIT SYNC
print("Syncing to GitHub...")
os.chdir(REPO_PATH)
try:
    subprocess.run(["git", "add", "."], shell=True)
    subprocess.run(["git", "commit", "-m", f"Afternoon Round 06/30: {new_sent} New, {followup_sent} Followups"], shell=True)
    subprocess.run(["git", "push", "origin", "main"], shell=True)
    print("GitHub Sync Done.")
except Exception as e:
    print(f"Git Error: {e}")

print(f"FINISHED: {new_sent} New, {followup_sent} Followups.")
