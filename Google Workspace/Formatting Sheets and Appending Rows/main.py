import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = "your-spreadsheet-id-here"
SHEET_ID = 0

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
service = build("sheets", "v4", credentials=creds)

# Step 1: append the new row
new_row = [["Jordan", 95]]

result = service.spreadsheets().values().append(
    spreadsheetId=SPREADSHEET_ID,
    range="Sheet1!A1",
    valueInputOption="USER_ENTERED",
    insertDataOption="INSERT_ROWS",
    body={"values": new_row}
).execute()

updated_range = result["updates"]["updatedRange"]
print("Data landed at:", updated_range)  # e.g. "Sheet1!A4:B4"

# Step 2: convert that A1 range into the zero-based row index batchUpdate needs
# "Sheet1!A4:B4" -> row 4 in A1 notation -> index 3 in GridRange terms
row_number = int(updated_range.split("!")[1].split(":")[0][1:])
row_index = row_number - 1

# Step 3: highlight exactly that row
highlight_request = {
    "requests": [
        {
            "repeatCell": {
                "range": {
                    "sheetId": SHEET_ID,
                    "startRowIndex": row_index,
                    "endRowIndex": row_index + 1
                },
                "cell": {
                    "userEnteredFormat": {
                        "backgroundColor": {"red": 0.85, "green": 0.93, "blue": 0.83}
                    }
                },
                "fields": "userEnteredFormat.backgroundColor"
            }
        }
    ]
}

service.spreadsheets().batchUpdate(spreadsheetId=SPREADSHEET_ID, body=highlight_request).execute()
print(f"Row {row_number} highlighted.")