import re
import os.path
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def getCodeFromGmail():
    """
    Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    verification_code_list = []
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    # Call the Gmail API
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="subject:Verify your email from:noreply@frontdesksuite.com ", maxResults=5).execute()
    messages = results.get('messages', [])
    for msg in messages:
        # Get the message from its id
        response = service.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            # Get value of 'payload' from dictionary 'txt'
            payload = response['payload']
            data = payload['body']['data']
            decoded_data = base64.b64decode(data)
            emailBody = decoded_data.decode("utf-8")
            match = re.search(r"(\d{4})", emailBody)
            if match:
                verification_code_list.append(match.group(1))
        except Exception as e:
            pass
    return verification_code_list


if __name__ == '__main__':
    print(getCodeFromGmail())

