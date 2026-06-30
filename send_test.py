import subprocess
import json

r = {"name": "Tahlie Hodson", "email": "tahlie.hodson@kmart.com.au", "company": "Kmart Australia"}
user_email = "miguelyang42@gmail.com"

subject = f"[Innovation] 4500V Solar Mosquito Technology for {r['company']}"
body = f"""<html><body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
<p>Hi {r['name']},</p>
<p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p>
<p>As a pioneer in Solar Mosquito Killer Lamps since 2020, we've released our 2026 4500V model with Zero Electricity Cost.</p>
<p>Highlights: <b>4500V Grid</b>, <b>3-Day Battery</b>, <b>IP65 Waterproof</b>.</p>
<p>Would you be open to our 2026 Catalog? Just reply "YES".</p>
<br>
<p>Best regards,<br>
<b>Miguel Yang</b><br>
Business Development Manager<br>
<b>Guangdong Xingpu Energy Saving Light</b></p>
</body></html>"""

# Call without shell=True to avoid cmd.exe parsing <
result = subprocess.run(['accio-mcp-cli', 'call', 'send_gmail_message', 
                        '--key', 'to', '--val', r['email'],
                        '--key', 'subject', '--val', subject,
                        '--key', 'body', '--val', body,
                        '--key', 'user_google_email', '--val', user_email,
                        '--key', 'body_format', '--val', 'html'], 
                        capture_output=True, text=True)

if result.returncode == 0:
    print(f"SUCCESS: {r['email']} - {result.stdout.strip()}")
else:
    print(f"FAILED: {r['email']} - {result.stderr.strip()}")
    # Try with shell=True but escaped
    print("Retrying with shell=True and simplified body...")
    simple_body = body.replace("<", "&lt;").replace(">", "&gt;") # This won't work for HTML rendering but tests connectivity
