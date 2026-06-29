import subprocess
import json
import os
import time

USER_EMAIL = "miguelyang42@gmail.com"
IMAGE_URL = "https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174"

def send_perfect_email(to, name, company, business):
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {company}"
    
    # HTML content with proper formatting and signature
    # Note: Use <b> tags for highlighting as requested
    body = f"""
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
        .highlight {{ color: #d32f2f; font-weight: bold; }}
        .signature {{ margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }}
    </style>
    </head>
    <body>
    <p>Hi {name},</p>
    
    <p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
    
    <p>I noticed {company}'s commitment to quality in {business} and wanted to share a breakthrough.</p>
    
    <p>Since 2020, our factory has pioneered <b>Solar Mosquito Killer Lamps</b>. We've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
    
    <p><b>Key Innovations:</b></p>
    <ul>
        <li><b>4500V High-Voltage Grid</b>: Industrial grade power.</li>
        <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather.</li>
        <li><b>Self-Cleaning Feature</b>: Reducing maintenance complaints.</li>
    </ul>
    
    <p><img src="{IMAGE_URL}" width="300" alt="XPES 4500V Solar Mosquito Lamp" style="display: block; margin: 15px 0;"></p>
    
    <p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>
    
    <div class="signature">
    <p>Best regards,</p>
    <p><b>Miguel Yang</b><br>
    Business Development Manager<br>
    <b>Guangdong Xingpu Energy Saving Light</b></p>
    </div>
    </body>
    </html>
    """

    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    
    # Write to a temporary JSON file to ensure zero shell mangling
    with open('perfect_payload.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [
        r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd",
        "call", "send_gmail_message", "--json-file", "perfect_payload.json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

REFINED_TARGETS = [
    {"to": "alex@murphysnaturals.com", "name": "Alex Tomaras", "company": "Murphy's Naturals", "business": "Natural Mosquito Repellents"},
    {"to": "dlavender@globeaus.com.au", "name": "David Lavender", "company": "Globe Pest Solutions", "business": "Professional Pest Management"},
    {"to": "dwei@catchmasterpro.com", "name": "Davey Wei Tian", "company": "AP&G Co. (Catchmaster)", "business": "Pest Control Devices"},
    {"to": "mholley@paraclipse.com", "name": "Miranda Holley", "company": "Paraclipse", "business": "Automated Insect Control"},
    {"to": "mliu@miloenterprises.com", "name": "Michael Liu", "company": "Milo Enterprises", "business": "Home & Garden"},
    {"to": "yuriy@tbi-pro.com", "name": "Yuriy Chernyshov", "company": "TBI Pro", "business": "Tech-based Pest Control"},
    {"to": "mikem@raganandmassey.com", "name": "Mike Massey", "company": "Ragan & Massey LLC", "business": "Insect Control"},
    {"to": "gabriel.lelaidier@swissinno.com", "name": "Gabriel Le Laidier", "company": "Swissinno Solutions AG", "business": "Animal-respectful Pest Control"},
    {"to": "loic.cecillon@biogents.com", "name": "Loïc Cécillon", "company": "Biogents AG", "business": "Mosquito Specialist"},
    {"to": "bert.derycke@vellemangroup.eu", "name": "Bert De Rycke", "company": "Velleman Group nv", "business": "Electronics & Outdoor"},
    {"to": "john.laurijsen@nedis.com", "name": "John Laurijsen", "company": "Nedis BV", "business": "Consumer Electronics"},
    {"to": "larry.lam@kingfisher.com", "name": "Larry Lam", "company": "Kingfisher plc", "business": "Home Improvement"},
    {"to": "mhoffmann@bunnings.com.au", "name": "Matthew Hoffmann", "company": "Bunnings Group", "business": "Hardware & Garden Retailer"},
    {"to": "aguinvarch@leroymerlin.fr", "name": "Antony Guinvarch", "company": "Leroy Merlin", "business": "Home Improvement & Gardening"},
    {"to": "stefan.loewe@obi.de", "name": "Stefan Loewe", "company": "OBI Group", "business": "DIY & Home Improvement"},
    {"to": "corey.lok@hornbach.com", "name": "Corey Lok", "company": "HORNBACH", "business": "International DIY Retailer"},
    {"to": "sfisher@central.com", "name": "Scott Fisher", "company": "Central Garden & Pet", "business": "Lawn & Garden Pest Control"},
    {"to": "sourcing@scotts.com.au", "name": "Sourcing Manager", "company": "Scott's Australia", "business": "Lawn & Garden Care"},
    {"to": "products@rentokil-initial.com", "name": "Head of Sourcing", "company": "Rentokil Initial", "business": "Professional Pest Products"},
    {"to": "purchasing@hozelock.com", "name": "Purchasing Manager", "company": "Hozelock Ltd", "business": "Garden & Pest Control"}
]

count = 0
for lead in REFINED_TARGETS:
    print(f"Sending to {lead['to']}...")
    if send_perfect_email(lead['to'], lead['name'], lead['company'], lead['business']):
        count += 1
        print(f"SUCCESS: {lead['to']}")
    else:
        print(f"FAILED: {lead['to']}")
    time.sleep(2)

print(f"Finished! Total sent: {count}")
