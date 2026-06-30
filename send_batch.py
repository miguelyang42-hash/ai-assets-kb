import subprocess
import json

payloads = [
    {
        "to": "scott.h@charleskendall.com",
        "name": "Scott H.",
        "company": "Charles Kendall Australia",
        "business": "Retailer Private Label",
        "country": "Australia"
    },
    {
        "to": "n.halket@davidjones.com.au",
        "name": "Natasha Halket",
        "company": "David Jones",
        "business": "Retailer Private Label",
        "country": "Australia"
    },
    {
        "to": "v.wong@davidjones.com.au",
        "name": "Vanessa Wong",
        "company": "David Jones",
        "business": "Retailer Private Label",
        "country": "Australia"
    },
    {
        "to": "james.kearney@bcf.com.au",
        "name": "James Kearney",
        "company": "BCF (Super Retail Group)",
        "business": "Camping/Outdoor Gear Brand",
        "country": "Australia"
    },
    {
        "to": "monique.holmes@bcf.com.au",
        "name": "Monique Holmes",
        "company": "BCF (Super Retail Group)",
        "business": "Camping/Outdoor Gear Brand",
        "country": "Australia"
    }
]

template = """<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
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
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body>
</html>"""

def send_email(p):
    body = template.format(name=p['name'], company=p['company'], business=p['business'], country=p['country'])
    subject = f"[Innovation] 4500V Solar Mosquito Technology for {p['company']} ({p['country']})"
    
    call_payload = {
        "to": p['to'],
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": "miguelyang42@gmail.com"
    }
    
    with open('temp_payload.json', 'w', encoding='utf-8') as f:
        json.dump(call_payload, f)
    
    result = subprocess.run(['accio-mcp-cli', 'call', 'send_gmail_message', '--json-file', 'temp_payload.json'], capture_output=True, text=True)
    print(f"Sent to {p['to']}: {result.returncode} {result.stdout} {result.stderr}")

for p in payloads:
    send_email(p)
