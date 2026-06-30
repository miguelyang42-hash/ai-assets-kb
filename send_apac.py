import subprocess
import json

recipients = [
    {"name": "Tahlie Hodson", "email": "tahlie.hodson@kmart.com.au", "company": "Kmart Australia"},
    {"name": "Maihemuti Keremu", "email": "m-keremu@komeri.bit.or.jp", "company": "KOMERI Japan"},
    {"name": "Tony Lee", "email": "tony.lee@emart.com", "company": "EMART South Korea"},
    {"name": "Freddie Lim", "email": "freddie.lim@fairprice.com.sg", "company": "NTUC Fairprice"},
    {"name": "Adam Baker", "email": "adam.baker@superretailgroup.com.au", "company": "BCF Australia"},
    {"name": "Joshua Strickland", "email": "joshua.strickland@superretailgroup.com.au", "company": "BCF Australia"},
    {"name": "Henry Murning", "email": "henry.murning@superretailgroup.com.au", "company": "BCF Australia"},
    {"name": "Jonny Wears", "email": "jonny.wears@superretailgroup.com.au", "company": "BCF Australia"},
    {"name": "Matt Behan", "email": "matt.behan@bcf.com.au", "company": "BCF Australia"}
]

user_email = "miguelyang42@gmail.com"

for r in recipients:
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {r['company']}"
    body = f"""
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
    <p>Hi {r['name']},</p>
    <p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
    <p>As a pioneer in Solar Mosquito Killer Lamps since 2020, we've released our 2026 4500V model with Zero Electricity Cost.</p>
    <p>Highlights: <b>4500V Grid</b>, <b>3-Day Battery</b>, <b>IP65 Waterproof</b>.</p>
    <p>Would you be open to our 2026 Catalog? Just reply "YES".</p>
    <br>
    <p>Best regards,<br>
    <b>Miguel Yang</b><br>
    Business Development Manager<br>
    <b>Guangdong Xingpu Energy Saving Light</b></p>
    </body>
    </html>
    """
    
    payload = {
        "to": r['email'],
        "subject": subject,
        "body": body,
        "user_google_email": user_email,
        "body_format": "html"
    }
    
    with open('payload.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f)
    
    print(f"Sending to {r['email']}...")
    
    # Use powershell to read the file and pass it to the cli
    ps_cmd = f'accio-mcp-cli call send_gmail_message --json (Get-Content payload.json -Raw)'
    result = subprocess.run(['powershell', '-Command', ps_cmd], 
                            capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {r['email']} - {result.stdout.strip()}")
    else:
        print(f"FAILED: {r['email']} - {result.stderr.strip()}")
