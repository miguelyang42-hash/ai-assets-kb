import subprocess
import json
import time

TO = "miguelyang42@gmail.com"
SUBJECT = "[Expert Audit] 4500V Solar Technology - HTML Verification"
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

body = f"""<html>
<body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi Miguel Yang,</p>
<p>I am <b>Miguel Yang</b> from Guangdong Xingpu Energy Saving Light.</p>
<p>Key Highlights:</p>
<ul>
    <li><b>4500V Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>Zero Electricity Cost</b>: 100% sustainable.</li>
</ul>
<p>Best regards,<br><b>Miguel Yang</b></p>
</body>
</html>"""

payload = {"to": TO, "subject": SUBJECT, "body": body, "body_format": "html", "user_google_email": USER_EMAIL}
with open('C:\\Users\\Lenovo\\AccioWork\\2026-06-16-14-18-24\\perfect_audit.json', 'w', encoding='utf-8') as f:
    json.dump(payload, f, ensure_ascii=False)

cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", "C:\\Users\Lenovo\\AccioWork\\2026-06-16-14-18-24\\perfect_audit.json"]
result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
print(result.stdout)
