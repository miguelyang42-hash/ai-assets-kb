import subprocess

CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
USER_EMAIL = "miguelyang42@gmail.com"

# Single line body to be safe
body = "<html><body><p>Hi Miguel,</p><p>I am <b>Miguel Yang</b>, Business Development Manager at <b>Guangdong Xingpu Energy Saving Light</b>.</p><p>Core selling point: <b>4500V High Voltage</b>.</p><p><img src='https://gootopshop.com/cdn/shop/files/1_3a59d9c2-5558-485a-8d77-62804b4d7990.jpg?v=1712716174' width='200'></p><p>Best regards,<br><b>Miguel Yang</b></p></body></html>"

cmd = [
    CLI_PATH, "call", "send_gmail_message",
    "--user_google_email", USER_EMAIL,
    "--to", USER_EMAIL,
    "--subject", "[FINAL TEST] Gold Standard - Miguel Yang",
    "--body", body,
    "--body_format", "html"
]

print("Executing definitive send...")
result = subprocess.run(cmd, capture_output=True, text=True, shell=False)

if result.returncode == 0:
    print(f"SUCCESS: {result.stdout}")
else:
    print(f"FAILED: {result.stdout} {result.stderr}")
