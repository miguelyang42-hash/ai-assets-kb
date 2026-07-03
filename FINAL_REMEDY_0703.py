import subprocess
import csv
import time
import os

# CONFIGURATION
USER_EMAIL = "miguelyang42@gmail.com"
CLI_PATH = r"C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd"
CSV_PATH = r"G:\XPES_Customer_Assets\leads_afternoon_0703\leads_verified_50.csv"

def send_robust_email(to, name, company, business, country):
    subject = f"Expand {company}'s 2026 catalog with high-margin Solar Insect Control"
    body = f"Hi {name}, I am Miguel Yang from Guangdong Xingpu Energy Saving Light. We just released our 2026 4500V Industrial-Grade Solar Model. It matches grid power with Zero Electricity Cost. Would you be open to our 2026 Catalog? Regards, Miguel Yang"

    # Use individual flags and shell=False (MANDATORY FOR WINDOWS)
    cmd = [
        CLI_PATH, "call", "send_gmail_message",
        "--to", to,
        "--subject", subject,
        "--body", body,
        "--user_google_email", USER_EMAIL
    ]
    
    try:
        # shell=False prevents CMD from interpreting special characters
        result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
        return result.returncode == 0 and "Email sent!" in result.stdout
    except:
        return False

if os.path.exists(CSV_PATH):
    with open(CSV_PATH, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            # Skip first 3 (already sent)
            count += 1
            if count <= 3: continue
            
            if send_robust_email(row['Email'], row['Name'], row['Company'], row['Category'], row['Country']):
                print(f"SENT: {row['Email']}")
            else:
                print(f"FAILED: {row['Email']}")
            time.sleep(2)
    print("FINISHED")
else:
    print("CSV NOT FOUND")
