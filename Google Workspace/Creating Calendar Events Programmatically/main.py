import os
import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/calendar"]

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
service = build("calendar", "v3", credentials=creds)

now = datetime.datetime.utcnow().isoformat() + "Z"

results = service.events().list(
    calendarId="primary",
    timeMin=now,
    maxResults=10,
    singleEvents=True,
    orderBy="startTime"
).execute()

events = results.get("items", [])
for event in events:
    start = event["start"].get("dateTime", event["start"].get("date"))
    print(start, "-", event["summary"])