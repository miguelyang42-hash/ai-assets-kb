import subprocess
import json
import os
import time

# GOLD STANDARD PAYLOAD CONFIG
USER_EMAIL = "miguelyang42@gmail.com"
GOLDEN_IMAGE = "https://sc02.alicdn.com/kf/H8e7cedfb014d48649ed8a741c41c47daZ.jpg"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

# TARGETS (VERIFIED RESPONSIBLE PERSONS)
REMEDIAL_LEADS = [
    {"to": "tahlie.hodson@kmart.com.au", "name": "Tahlie Hodson", "company": "Kmart Australia", "business": "General Merchandise"},
    {"to": "sydney.goh@bunnings.com.au", "name": "Sydney Goh", "company": "Bunnings", "business": "Retailer Private Label"},
    {"to": "m-keremu@komeri.bit.or.jp", "name": "Maihemuti Keremu", "company": "KOMERI Japan", "business": "Home Center/DIY"},
    {"to": "tony.lee@emart.com", "name": "Tony Lee", "company": "EMART South Korea", "business": "Sourcing/Buying"},
    {"to": "freddie.lim@fairprice.com.sg", "name": "Freddie Lim", "company": "NTUC Fairprice Singapore", "business": "International Sourcing"}
]

def send_perfect_remedial_email(to, name, company, business):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company}"
    
    # EXACT TEMPLATE FROM USER FEEDBACK
    body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>I am writing to you regarding {company}'s leadership in {business}.</p>

<p>We are a <b>pioneer factory in Solar Mosquito Killer Lamps since 2020</b>. I want to share our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>

<p><b>Performance Highlights:</b></p>
<ul>
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for outdoor durability.</li>
</ul>

<p>Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.</p>

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
    
    # Avoid filename conflicts
    fn = f"remedy_{to.replace('@','_').replace('.','_')}.json"
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    # Use direct flag-based call to ensure absolute visibility in SENT folder
    # We use --json-file to prevent shell mangling
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", fn]
    
    print(f"Force-sending to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if os.path.exists(fn): os.remove(fn)
    
    return result.returncode == 0

# EXECUTE
count = 0
for lead in REMEDIAL_LEADS:
    if send_perfect_remedial_email(lead['to'], lead['name'], lead['company'], lead['business']):
        print(f"VERIFIED SENT: {lead['to']}")
        count += 1
    else:
        print(f"SEND FAILED: {lead['to']}")
    time.sleep(5)

print(f"--- TOTAL REMEDIATED: {count} ---")
