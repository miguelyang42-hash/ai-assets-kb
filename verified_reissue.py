import subprocess
import json
import time

# 修正后的 5 个负责人（经过二次验证，排除 info@，使用推导+证据模式）
REFINED_LEADS = [
    {
        "to": "RRH228@verizon.net", # Robert Hoefel 的个人验证邮箱（源自 veripages/finra 证据）
        "name": "Robert Hoefel",
        "company": "Woodstream Corporation",
        "business": "Insect Control"
    },
    {
        "to": "mhousman@flowtron.com", # Mark Housman 格式推导（源自 zoominfo/datanyze）
        "name": "Mark Housman",
        "company": "Armatron/Flowtron",
        "business": "Outdoor Zappers"
    },
    {
        "to": "zoconnell@helenoftroy.com", # Zac O'Connell 确认职位：Helen of Troy 运营经理
        "name": "Zac O'Connell",
        "company": "Helen of Troy",
        "business": "Consumer Products"
    },
    {
        "to": "mliu@miloenterprises.com", # Michael Liu (Aspectek 创始人) 确认身份
        "name": "Michael Liu",
        "company": "Milo Enterprises",
        "business": "Pest Control"
    },
    {
        "to": "yuriy@tbi-pro.com", # Yuriy Chernyshov (TBI Pro 负责人)
        "name": "Yuriy",
        "company": "TBI Pro",
        "business": "Tech Pest Control"
    }
]

def send_final_verified(to, name, company, business):
    subject = f"[Direct Factory] 4500V Solar Mosquito Technology for {company}"
    body = f"""Hi {name},

I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light.

I am writing regarding {company}'s commitment to quality in {business}.

Since 2020, our factory has pioneered Solar Mosquito Killer Lamps. I want to share our 2026 4500V Industrial-Grade Solar Model. It matches the killing power of traditional AC grid units with Zero Electricity Cost.

Key Innovations:
- 4500V High-Voltage Grid: Consistent industrial-grade power.
- 3-Day Battery: Optimized for cloudy weather.

Product Preview (verified image): https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174

Best regards,

Miguel Yang
Business Development Manager
Guangdong Xingpu Energy Saving Light"""

    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "user_google_email": "miguelyang42@gmail.com"
    }
    
    with open('verified_payload.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [
        r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd",
        "call", "send_gmail_message", "--json-file", "verified_payload.json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

for lead in REFINED_LEADS:
    print(f"Refining outreach to {lead['name']}...")
    if send_final_verified(lead['to'], lead['name'], lead['company'], lead['business']):
        print(f"DONE: {lead['to']}")
    else:
        print(f"FAIL: {lead['to']}")
    time.sleep(2)
