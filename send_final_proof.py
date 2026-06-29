import subprocess
import json

def send_final_txt(to, subject, body):
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "user_google_email": "miguelyang42@gmail.com"
    }
    with open('final_txt.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f)
    
    cmd = [
        r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd",
        "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--user_google_email", "miguelyang42@gmail.com"
    ]
    subprocess.run(cmd)

body = """Hi Miguel,

I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light.

Since 2020, our factory has pioneered Solar Mosquito Killer Lamps. We've just released our 2026 4500V Industrial-Grade Solar Model.

Key Innovations:
- 4500V High-Voltage Grid: Consistent industrial-grade power.
- 3-Day Battery: Optimized for cloudy weather.

Product Preview: https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174

Best regards,

Miguel Yang
Business Development Manager
Guangdong Xingpu Energy Saving Light"""

send_final_txt("miguelyang42@gmail.com", "[FINAL PROOF] 2026 Solar Technology", body)
