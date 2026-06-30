import subprocess
import json

cli_path = r'C:\Users\Lenovo\AppData\Roaming\Accio\pre-install\e6550f7e00ff\accio-mcp-cli.cmd'
user_email = "miguelyang42@gmail.com"

# Search for the message
search_payload = {
    "query": "label:sent",
    "user_google_email": user_email,
    "page_size": 1
}

search_result = subprocess.run([cli_path, 'call', 'search_gmail_messages', '--json', json.dumps(search_payload)], 
                                capture_output=True, text=True, encoding='utf-8')

if search_result.returncode == 0:
    # Strip non-JSON parts if any
    try:
        raw_json = search_result.stdout.strip()
        messages = json.loads(raw_json)
    except Exception as e:
        messages = []
    if messages and len(messages) > 0:
        msg_id = messages[0]['id']
        print(f"Found Message ID: {msg_id}")
        
        # Get content
        content_payload = {
            "message_id": msg_id,
            "user_google_email": user_email
        }
        content_result = subprocess.run([cli_path, 'call', 'get_gmail_message_content', '--json', json.dumps(content_payload)], 
                                         capture_output=True, text=True, encoding='utf-8')
        if content_result.returncode == 0:
            print("--- MESSAGE CONTENT ---")
            print(content_result.stdout)
        else:
            print(f"Failed to get content: {content_result.stderr}")
    else:
        print("No messages found.")
else:
    print(f"Search failed: {search_result.stderr}")
