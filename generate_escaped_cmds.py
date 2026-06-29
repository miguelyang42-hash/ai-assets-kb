import json

def escape_string(s):
    return "".join(f"\\u{ord(c):04x}" for c in s)

recipients = [
    {"to": "angela.adams@homedepot.com", "name": "Angela"},
    {"to": "melissa.major@homedepot.com", "name": "Melissa"},
    {"to": "Arely.Guzman0@walmart.com", "name": "Arely"}
]

html_template = """<html><body><p>Hi {name},</p><p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p><p>As a pioneer in Solar Mosquito Killer Lamps since 2020, we've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p><p>Key Innovations: <b>4500V High-Voltage Grid</b>, <b>3-Day Battery</b>.</p><p><img src="https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174" width="300"></p><p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES".</p><p>Best regards,<br><b>Miguel Yang</b></p></body></html>"""

for r in recipients:
    body = html_template.replace("{name}", r['name'])
    payload = {
        "to": r['to'],
        "subject": "Solar Innovation",
        "body": body,
        "user_google_email": "miguelyang42@gmail.com",
        "body_format": "html"
    }
    # Manually build the JSON with full unicode escapes for everything
    # This ensures no special chars are left to confuse the shell
    json_parts = []
    for k, v in payload.items():
        json_parts.append(f'"{k}":"{escape_string(v)}"')
    json_str = "{" + ",".join(json_parts) + "}"
    print(f"accio-mcp-cli call send_gmail_message --json '{json_str}'")
