import subprocess

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"

# PERFECT BODY - Single Line to avoid all redirection/parsing issues
body = "Hi Miguel, I am Miguel Yang, Business Development Manager at Guangdong Xingpu Energy Saving Light. We have released our 2026 4500V Industrial-Grade Solar Model. Zero Electricity Cost. Key: 4500V Grid, 3-Day Battery. Preview: https://s.alicdn.com/@sc04/kf/H65db553ddabe48c280d3c4996799fb32x.jpg. Best, Miguel Yang"

cmd = [
    CLI_PATH, "call", "send_gmail_message",
    "--user_google_email", USER_EMAIL,
    "--to", USER_EMAIL,
    "--subject", "[VERIFIED SUCCESS] Gold Standard - Miguel Yang",
    "--body", body
]

print("Executing definitive send v4...")
result = subprocess.run(cmd, capture_output=True, text=True, shell=False)

if result.returncode == 0:
    print(f"SUCCESS: {result.stdout}")
else:
    print(f"FAILED: {result.stdout} {result.stderr}")
