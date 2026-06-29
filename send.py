import os
import subprocess
import json

payload = {
    "to": "Arely.Guzman0@walmart.com",
    "subject": "Industrial Solar Mosquito Killer Innovation - Zero Electricity Cost",
    "body": \"\"\"<html><body>
<p>Hi Arely,</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>As a pioneer in Solar Mosquito Killer Lamps since 2020, we've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
<p>Key Innovations: <b>4500V High-Voltage Grid</b>, <b>3-Day Battery</b>.</p>
<p><img src='https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174' width='300'></p>
<p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply 'YES'.</p>
<p>Best regards,<br><b>Miguel Yang</b></p>
</body></html>\"\"\",
    "user_google_email": "miguelyang42@gmail.com",
    "body_format": "html"
}

# Find accio-mcp-cli path
# On windows it might be in the scripts folder or a shim
cmd = ["accio-mcp-cli", "call", "send_gmail_message", "--json", json.dumps(payload)]
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
stdout, stderr = process.communicate()
print(f"To: {payload['to']}")
print(f"STDOUT: {stdout}")
print(f"STDERR: {stderr}")
