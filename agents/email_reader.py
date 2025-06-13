from utils.gmail_auth import get_gmail_service
from datetime import datetime, timedelta
import base64
import email


def get_today_date_query():
    today = datetime.today()
    tomorrow = today.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return f"after:{today.strftime('%Y/%m/%d')} before:{tomorrow.strftime('%Y/%m/%d')}"

def fetch_today_emails(max_results=150):
    service = get_gmail_service()
    query = get_today_date_query()

    results = service.users().messages().list(userId='me', maxResults=max_results).execute()
    print(results, "-----results-----")
    messages = results.get('messages', [])
    print(len(messages), "-----messages-----")
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='full').execute()

        print(msg_data, "-----msg_data-----")
        headers = msg_data['payload']['headers']

        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '')
        sender = next((h['value'] for h in headers if h['name'] == 'From'), '')
        date = next((h['value'] for h in headers if h['name'] == "Date"), '')

        body = ''

        payload = msg_data['payload']
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data')
                    if data:
                        body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        else:
            data = payload['body'].get('data')
            if data:
                body = base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        emails.append({
            'subject': subject,
            'sender': sender,
            'date': date,
            'body': body
        })

    return emails