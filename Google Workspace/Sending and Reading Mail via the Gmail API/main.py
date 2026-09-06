import os
import base64
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def get_credentials():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token_file:
            token_file.write(creds.to_json())
    return creds

creds = get_credentials()
service = build("gmail", "v1", credentials=creds)

MESSAGE_ID = "your-message-id-here"

message = service.users().messages().get(
    userId="me",
    id=MESSAGE_ID,
    format="full"
).execute()

def find_plain_text(payload):
    if payload.get("mimeType") == "text/plain":
        data = payload.get("body", {}).get("data")
        if data:
            return base64.urlsafe_b64decode(data).decode("utf-8")
    for part in payload.get("parts", []):
        result = find_plain_text(part)
        if result:
            return result
    return None

body_text = find_plain_text(message["payload"])
print(body_text)