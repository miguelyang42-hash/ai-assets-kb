import subprocess
import json
import csv
import time
import os

# AFTERNOON CONFIGURATION
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

# TARGETS
NEW_LEADS_CSV = r"C:\Users\Lenovo\AccioWork\2026-06-16-14-18-24\XPES_Customer_Assets\leads_afternoon\leads_verified_50.csv"
FOLLOWUP_TARGETS = [
    {"to": "RRH228@verizon.net", "name": "Robert Hoefel", "company": "Woodstream Corporation", "business": "Insect Control"},
    {"to": "mhousman@flowtron.com", "name": "Mark Housman", "company": "Armatron/Flowtron", "business": "Outdoor Zappers"},
    {"to": "zoconnell@helenoftroy.com", "name": "Zac O'Connell", "company": "Helen of Troy", "business": "Consumer Products"},
    {"to": "mliu@miloenterprises.com", "name": "Michael Liu", "company": "Milo Enterprises", "business": "Home & Garden"},
    {"to": "yuriy@tbi-pro.com", "name": "Yuriy Chernyshov", "company": "TBI Pro", "business": "Tech-based Pest Control"}
]

def send_email_via_json(to, subject, body):
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    
    # Use a per-recipient file to ensure isolation
    safe_to = to.replace("@","_").replace(".","_")
    filename = f"payload_af_{safe_to}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if os.path.exists(filename):
        os.remove(filename)
        
    return result.returncode == 0

# --- PART 1: DAY 1 NEW OUTREACH ---
def send_day1(to, name, company, business):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company}"
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>I noticed {company}'s leadership in {business} and wanted to share a breakthrough for your 2026 lineup.</p>
<p>As a <b>pioneer in Solar Mosquito Killer Lamps since 2020</b>, we've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
<p><b>Performance Highlights:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for extreme outdoor durability.</li>
</ul>
<p>Did you do the market survey for your local market selling? I would like to share our quotation with you.</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""
    return send_email_via_json(to, subject, body)

# --- PART 2: DAY 5 FOLLOW-UP (Performance Proof) ---
def send_day5(to, name, company):
    subject = f"[Data] Solar vs. AC Grid performance comparison for {company}"
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>
<p>Just checking if you saw my note on our <b>4500V Solar tech</b>. A common question we get is: "Does solar really have enough power?"</p>
<p>I've attached our internal performance audit showing our 2026 model maintains a <b>4500V discharge even after 3 cloudy days</b>. This matches traditional industrial AC units while being 100% sustainable.</p>
<p><b>Key Tech Specs:</b></p>
<ul>
    <li><b>Grid Output</b>: Constant 4500V DC.</li>
    <li><b>Wavelength</b>: 365nm UV-LED (Highest attraction rate).</li>
    <li><b>Maintenance</b>: Auto-cleaning grid design.</li>
</ul>
<p>Would this data be useful for your engineering or sourcing team?</p>
<br>
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""
    return send_email_via_json(to, subject, body)

# --- EXECUTION ---
sent_new = 0
if os.path.exists(NEW_LEADS_CSV):
    with open(NEW_LEADS_CSV, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if sent_new >= 50: break
            if send_day1(row['Email'], row['Name'], row['Company'], row['Category']):
                print(f"NEW SENT: {row['Email']}")
                sent_new += 1
            time.sleep(4)

sent_follow = 0
for lead in FOLLOWUP_TARGETS:
    if send_day5(lead['to'], lead['name'], lead['company']):
        print(f"FOLLOWUP SENT: {lead['to']}")
        sent_follow += 1
    time.sleep(4)

print(f"--- AFTERNOON ROUND FINISHED ---")
print(f"New Leads Sent: {sent_new}")
print(f"Followups Sent: {sent_follow}")
