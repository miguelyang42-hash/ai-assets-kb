import csv
import subprocess
import json
import time
import os

# Configuration
USER_EMAIL = "xpesuvc.miguel@gmail.com"
LEADS_FILE = "XPES_Leads_2026-06-16.csv"
DRAFTS_FILE = "XPES_Email_Drafts_2026-06-16.md"
LOG_FILE = "Email_Send_Log.txt"

def log_message(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {msg}\n")
    print(msg)

def get_draft(company_name):
    try:
        with open(DRAFTS_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        
        sections = content.split("---")
        for section in sections:
            if company_name.lower() in section.lower() and "**Subject:**" in section:
                lines = section.strip().split("\n")
                subject = ""
                body = []
                body_started = False
                for line in lines:
                    if line.startswith("**Subject:**"):
                        subject = line.replace("**Subject:**", "").strip()
                        body_started = True
                    elif body_started:
                        if not line.startswith("##"): # Skip headers
                            body.append(line)
                
                return subject, "\n".join(body).strip()
    except Exception as e:
        log_message(f"Error reading draft for {company_name}: {e}")
    return None, None

def send_email(to_email, subject, body):
    payload = {
        "user_google_email": USER_EMAIL,
        "to": to_email,
        "subject": subject,
        "body": body,
        "body_format": "plain"
    }
    
    cmd = [
        "accio-mcp-cli", "call", "send_gmail_message",
        "--json", json.dumps(payload)
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        log_message(f"Successfully sent email to {to_email}")
        return True
    except Exception as e:
        log_message(f"Failed to send email to {to_email}: {e}")
        return False

def main():
    log_message("Starting batch email send...")
    
    leads = []
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    updated_leads = []
    sent_count = 0
    
    for lead in leads:
        company = lead["Company"]
        email = lead["Email"]
        status = lead["Status"]
        
        if email and email != "TBD" and status == "Developing":
            subject, body = get_draft(company)
            if subject and body:
                log_message(f"Found draft for {company}. Sending to {email}...")
                if send_email(email, subject, body):
                    lead["Status"] = "Sent"
                    lead["Sent_Date"] = time.strftime("%Y-%m-%d")
                    sent_count += 1
                else:
                    lead["Status"] = "Failed"
            else:
                log_message(f"No draft found for {company}. Skipping.")
        
        updated_leads.append(lead)
    
    # Write back updated leads
    if leads:
        keys = updated_leads[0].keys()
        with open(LEADS_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(updated_leads)
    
    log_message(f"Batch send finished. Total sent: {sent_count}")

if __name__ == "__main__":
    main()
