import subprocess
import json
import time
import os

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"
IMAGE_URL = "https://sc02.alicdn.com/kf/H8e7cedfb014d48649ed8a741c41c47daZ.jpg"

def send_validated_gold_standard(to, name, company, business):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company}"
    
    # THE PERFECT TEMPLATE
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

<div style="margin: 20px 0;">
    <img src="{IMAGE_URL}" width="600" alt="Solar Mosquito Killer Lamp">
</div>

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
    
    # Save to a unique file
    filename = f"payload_gold_{to.replace('@','_').replace('.','_')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    # CALL CLI with NO shell redirection
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", filename]
    
    print(f"Sending perfect copy to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if os.path.exists(filename):
        os.remove(filename)
        
    return result.returncode == 0

# TARGETS
LEADS = [
    {"to": "sydney.goh@bunnings.com.au", "name": "Sydney Goh", "company": "Bunnings", "business": "Retailer Private Label"},
    {"to": "tahlie.hodson@kmart.com.au", "name": "Tahlie Hodson", "company": "Kmart Australia", "business": "General Merchandise"},
    {"to": "m-keremu@komeri.bit.or.jp", "name": "Maihemuti Keremu", "company": "KOMERI", "business": "Home Center/DIY"},
    {"to": "keisuke.tanaka@aeon.jp", "name": "Keisuke Tanaka", "company": "AEON", "business": "Retail"},
    {"to": "freddie.lim@fairprice.com.sg", "name": "Freddie Lim", "company": "NTUC Fairprice", "business": "International Sourcing"},
    {"to": "natalia.hana@mrdiy.com", "name": "Natalia Hana", "company": "MR.DIY", "business": "Hardware Retail"},
    {"to": "suthinee.a@homepro.co.th", "name": "Suthinee Ambudha", "company": "HomePro", "business": "Home Improvement"}
]

for lead in LEADS:
    if send_validated_gold_standard(lead['to'], lead['name'], lead['company'], lead['business']):
        print(f"DONE: {lead['to']}")
    else:
        print(f"FAIL: {lead['to']}")
    time.sleep(5)
