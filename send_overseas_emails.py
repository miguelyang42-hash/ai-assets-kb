import subprocess
import json
import time

recipients = [
    {"to": "angela.adams@homedepot.com", "name": "Angela"},
    {"to": "melissa.major@homedepot.com", "name": "Melissa"},
    {"to": "Arely.Guzman0@walmart.com", "name": "Arely"}
]

html_template = """
<html><body>
<p>Hi {name},</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>As a pioneer in Solar Mosquito Killer Lamps since 2020, we've just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>
<p>Key Innovations: <b>4500V High-Voltage Grid</b>, <b>3-Day Battery</b>.</p>
<p><img src="https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174" width="300"></p>
<p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES".</p>
<p>Best regards,<br><b>Miguel Yang</b></p>
</body></html>
"""

node_bin = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\node\node.exe"
mcp_script = r"G:\文件安装\Accio\resources\accio-mcp-cli\accio-mcp.mjs"

for r in recipients:
    print(f"Sending to {r['to']}...")
    body = html_template.format(name=r['name'])
    payload = {
        "to": r['to'],
        "subject": "Industrial Solar Mosquito Killer Innovation - Zero Electricity Cost",
        "body": body,
        "user_google_email": "miguelyang42@gmail.com",
        "body_format": "html"
    }
    cmd = [node_bin, mcp_script, "call", "send_gmail_message", "--json", json.dumps(payload)]
    
    # shell=False ensures we don't use cmd.exe, so no redirection issues with < >
    result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
    
    if result.returncode == 0:
        print(f"  Success: {r['to']}")
        print(result.stdout)
    else:
        print(f"  Failed: {r['to']}")
        print(f"  STDOUT: {result.stdout}")
        print(f"  STDERR: {result.stderr}")
    time.sleep(1)

