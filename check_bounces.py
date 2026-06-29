import subprocess
import json
import time

query = 'from:mailer-daemon@googlemail.com (subject:"Delivery Status Notification" OR subject:"Address not found") newer_than:1h'
cmd = [
    "accio-mcp-cli", "call", "search_gmail_messages",
    "--query", query,
    "--user_google_email", "miguelyang42@gmail.com"
]

print(f"Searching for bounces with query: {query}")
result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

if result.returncode == 0:
    print("Search Result:")
    print(result.stdout)
else:
    print("Search Failed:")
    print(result.stderr)
