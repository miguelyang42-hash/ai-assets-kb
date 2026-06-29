import subprocess
import json
import time

def send_validated_email(to, name, company, business):
    # 彻底隔离 Shell 转义，使用 JSON 文件中转
    subject = f"[Direct Factory] 4500V Solar Mosquito Technology for {company}"
    
    # 严格按照阿D要求的签名格式
    body = f"""Hi {name},

I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light.

Since 2020, our factory has pioneered Solar Mosquito Killer Lamps. I want to share our 2026 4500V Industrial-Grade Solar Model. It provides the same killing power as traditional AC grid units with Zero Electricity Cost.

Key Innovations:
- 4500V High-Voltage Grid: Consistent industrial-grade power.
- 3-Day Battery: Optimized for cloudy weather.

Product Preview: https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174

Best regards,

Miguel Yang
Business Development Manager
Guangdong Xingpu Energy Saving Light"""

    # 使用纯文本 + 链接方式确保 100% 可见性，不冒 HTML 乱码风险
    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "user_google_email": "miguelyang42@gmail.com"
    }
    
    with open('temp_email.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [
        r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd",
        "call", "send_gmail_message", "--json-file", "temp_email.json"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

# 1. 自测：先发给自己
print("Testing self-send...")
if send_validated_email("miguelyang42@gmail.com", "Miguel", "Self-Test", "Quality Control"):
    print("Self-test SUCCESS. Check your inbox now.")
else:
    print("Self-test FAILED.")
