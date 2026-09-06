from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import os

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
creds = flow.run_local_server(port=0)

with open("token.json", "w") as token_file:
    token_file.write(creds.to_json())
    
    


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

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
        

service = build("sheets", "v4", credentials=creds)
SPREADSHEET_ID = "your-spreadsheet-id-here"
RANGE = "Sheet1!A1:C10"

result = service.spreadsheets().values().get(
    spreadsheetId=SPREADSHEET_ID,
    range=RANGE
).execute()

rows = result.get("values", [])
for row in rows:
    print(row)
    
header, *data_rows = rows
df = pd.DataFrame(data_rows, columns=header)
print(df)

new_data = [
    ["Name", "Score"],
    ["Alex", 92],
    ["Priya", 88],
]

service.spreadsheets().values().update(
    spreadsheetId=SPREADSHEET_ID,
    range="Sheet1!A1:B3",
    valueInputOption="USER_ENTERED",
    body={"values": new_data}
).execute()

service.spreadsheets().values().append(
    spreadsheetId=SPREADSHEET_ID,
    range="Sheet1!A1",
    valueInputOption="USER_ENTERED",
    insertDataOption="INSERT_ROWS",
    body={"values": [["Jordan", 95]]}
).execute()