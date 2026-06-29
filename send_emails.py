import csv

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

for i, lead in enumerate(leads):
    name = lead['Name']
    company = lead['Company']
    category = lead['Category']
    email = lead['Email']
    body = template.format(name=name, company=company, category=category).replace('\n', '')
    subject = f"Industrial-Grade Solar Mosquito Killer Lamp for {company}"
    # Escape quotes for CLI
    body_escaped = body.replace('"', '\\"')
    print(f'accio-mcp-cli call send_gmail_message --json \'{{"to": "{email}", "subject": "{subject}", "body": "{body_escaped}", "user_google_email": "miguelyang42@gmail.com", "body_format": "html"}}\'')
