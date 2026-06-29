import subprocess
import json

query = 'subject:"2026 Solar 4500V Technology"'
user_email = "miguelyang42@gmail.com"

cmd = [
    "accio-mcp-cli", "call", "search_gmail_messages",
    "--query", query,
    "--user_google_email", user_email
]

print(f"Searching for sent emails with query: {query}")
result = subprocess.run(cmd, capture_output=True, text=True, shell=True)

if result.returncode == 0:
    print("Search Result:")
    print(result.stdout)
else:
    print("Search Failed:")
    print(result.stderr)
