import subprocess
import json
import os

# TRIPLE-VERIFIED STABLE IMAGE (Alibaba Official)
STABLE_IMAGE = "https://s.alicdn.com/@sc04/kf/H65db553ddabe48c280d3c4996799fb32x.jpg"
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"

def send_perfect_proof_v3(to, name):
    subject = "[FINAL PROOF] Gold Standard Format - XPES Factory"
    
    body = f"""<html>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #333; max-width: 600px;">
<p>Hi {name},</p>

<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>

<p>I noticed your leadership in the pest control market and wanted to share our latest innovation.</p>

<p>As a <b>pioneer in Solar Mosquito Killer Lamps since 2020</b>, we have just released our <b>2026 4500V Industrial-Grade Solar Model</b>. It provides the same killing power as traditional AC grid units with <b>Zero Electricity Cost</b>.</p>

<p><b>Key Technical Highlights:</b></p>
<ul style="color: #d32f2f;">
    <li><b>4500V High-Voltage Grid</b>: Consistent industrial-grade kill power.</li>
    <li><b>3-Day Battery Backup</b>: Optimized for cloudy weather performance.</li>
    <li><b>IP65 Waterproofing</b>: Perfect for extreme outdoor durability.</li>
</ul>

<div style="text-align: center; margin: 20px 0;">
    <img src="{STABLE_IMAGE}" width="400" alt="4500V Solar Mosquito Lamp" style="border: 1px solid #ddd; border-radius: 8px; padding: 5px;">
    <p style="font-size: 12px; color: #666;">Model XP711 - 4500V Industrial Solar Unit</p>
</div>

<p>Would you be open to a quick review of our 2026 Wholesale Catalog? Just reply "YES" and I'll send it over.</p>

<br>
<div style="border-top: 2px solid #eee; padding-top: 10px;">
<p>Best regards,</p>
<p><b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</div>
</body>
</html>"""

    payload = {
        "to": to,
        "subject": subject,
        "body": body,
        "body_format": "html",
        "user_google_email": USER_EMAIL
    }
    
    with open('final_proof_v3.json', 'w', encoding='utf-8') as f:
        json.dump(payload, f, ensure_ascii=False)
    
    cmd = [CLI_PATH, "call", "send_gmail_message", "--json-file", "final_proof_v3.json"]
    
    print(f"Sending definitive proof to {to}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

if send_perfect_proof_v3(USER_EMAIL, "Miguel"):
    print("SUCCESS: Final proof sent.")
else:
    print("FAILED")
