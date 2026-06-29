import subprocess
import json
import csv
import time

# Configuration
USER_EMAIL = "xpesuvc.miguel@gmail.com"
LEADS_FILE = "XPES_Leads_2026-06-16.csv"
REPLY_LOG = "Reply_Analysis_Log.md"

def log_analysis(msg):
    with open(REPLY_LOG, "a", encoding="utf-8") as f:
        f.write(msg + "\n")
    print(msg)

def get_unread_messages():
    query = "is:unread newer_than:1d"
    cmd = [
        "accio-mcp-cli", "call", "search_gmail_messages",
        "--user_google_email", USER_EMAIL,
        "--query", query,
        "--page_size", "50"
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        data = json.loads(result.stdout)
        return data.get("messages", [])
    except Exception as e:
        print(f"Error searching messages: {e}")
        return []

def get_message_content(msg_id):
    cmd = [
        "accio-mcp-cli", "call", "get_gmail_message_content",
        "--user_google_email", USER_EMAIL,
        "--message_id", msg_id
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return json.loads(result.stdout)
    except Exception as e:
        print(f"Error reading message {msg_id}: {e}")
        return {}

def main():
    log_analysis(f"## Reply Analysis Report - {time.strftime('%Y-%m-%d')}")
    
    messages = get_unread_messages()
    if not messages:
        log_analysis("No new unread messages found today.")
        return

    replies_found = []
    
    # Load leads to check against
    with open(LEADS_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        leads = list(reader)
    
    for msg_info in messages:
        msg_id = msg_info["id"]
        content = get_message_content(msg_id)
        sender = content.get("from", "")
        subject = content.get("subject", "")
        snippet = content.get("snippet", "")
        
        # Check if sender matches any lead email
        for lead in leads:
            if lead["Email"].lower() in sender.lower():
                log_analysis(f"### New Reply from {lead['Company']} ({sender})")
                log_analysis(f"**Subject:** {subject}")
                log_analysis(f"**Snippet:** {snippet}")
                log_analysis("---")
                lead["Status"] = "Replied"
                replies_found.append(lead["Company"])
    
    # Calculate stats
    total_sent = sum(1 for l in leads if l["Status"] in ["Sent", "Replied", "Failed"])
    total_replied = sum(1 for l in leads if l["Status"] == "Replied")
    rate = (total_replied / total_sent * 100) if total_sent > 0 else 0
    
    log_analysis(f"**Stats:** Sent: {total_sent} | Replied: {total_replied} | Rate: {rate:.2f}%")
    
    # Save leads
    if leads:
        keys = leads[0].keys()
        with open(LEADS_FILE, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(leads)

if __name__ == "__main__":
    main()
