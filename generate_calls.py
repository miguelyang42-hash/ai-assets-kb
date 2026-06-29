import csv
import json

with open('XPES_Customer_Assets/leads_morning/leads_morning_50.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    leads = list(reader)

template = """<p>Hi {name},</p>
<p>I am <strong>Miguel Yang</strong>, Business Development Manager at <strong>Guangdong Xingpu Energy Saving Light</strong>.</p>
<p>I am writing to you regarding {company}'s leadership in {category}.</p>
<p>We are a <strong>pioneer factory in Solar Mosquito Killer Lamps since 2020</strong>. I want to share our <strong>2026 4500V Industrial-Grade Solar Model</strong>. It provides the same killing power as traditional AC grid units with <strong>Zero Electricity Cost</strong>.</p>
<p><strong>Performance Highlights:</strong></p>
<ul>
<li><strong>4500V High-Voltage Grid</strong>: Consistent industrial-grade kill power.</li>
<li><strong>3-Day Battery Backup</strong>: Optimized for cloudy weather performance.</li>
<li><strong>IP65 Waterproofing</strong>: Perfect for outdoor durability.</li>
</ul>
<p>Did you do the market survey for your local market selling? I would like to share our quotation and you local hotsale model with you.</p>
<p><img src="https://sc02.alicdn.com/kf/H8e7cedfb014d48649ed8a741c41c47daZ.jpg" width="600"></p>
<p>Best regards,<br>
<strong>Miguel Yang</strong><br>
Business Development Manager<br>
<strong>Guangdong Xingpu Energy Saving Light</strong></p>"""

calls = []
for lead in leads:
    body = template.format(name=lead['Name'], company=lead['Company'], category=lead['Category']).replace('\n', '')
    calls.append({
        "to": lead['Email'],
        "subject": f"Collaboration: Industrial-Grade Solar Mosquito Killer Lamp for {lead['Company']}",
        "body": body,
        "user_google_email": "miguelyang42@gmail.com",
        "body_format": "html"
    })

with open('tool_calls.json', 'w', encoding='utf-8') as f:
    json.dump(calls, f, indent=2)
