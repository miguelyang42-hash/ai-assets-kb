import subprocess
import json

cli_path = r'C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd'

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
    body = f"""Hi {r['name']},

I am **Miguel Yang**, Business Development Manager at **Guangdong Xingpu Energy Saving Light**.

As a pioneer in Solar Mosquito Killer Lamps since 2020, we've released our 2026 4500V model with Zero Electricity Cost.

Highlights: 4500V Grid, 3-Day Battery, IP65 Waterproof.

Would you be open to our 2026 Catalog? Just reply "YES".

Best regards,
**Miguel Yang**
Business Development Manager
**Guangdong Xingpu Energy Saving Light**"""

    payload = {
        "to": r['email'],
        "subject": subject,
        "body": body,
        "user_google_email": user_email,
        "body_format": "plain"
    }
    
    print(f"Sending to {r['email']}...")
    
    result = subprocess.run([cli_path, 'call', 'send_gmail_message', '--json', json.dumps(payload)], 
                            capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"SUCCESS: {r['email']}")
    else:
        print(f"FAILED: {r['email']} - {result.stderr.strip()}")
