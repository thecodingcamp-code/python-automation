from pydantic import BaseModel, ValidationError
import imaplib
import email as email_module
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


class EmailClassification(BaseModel):
    category: Literal["urgent", "complaint", "billing", "general_inquiry", "spam"]
    reasoning: str
    
bad_response = '{"category": "annoyed", "reasoning": "Customer seems upset."}'

try:
    EmailClassification.model_validate_json(bad_response)
except ValidationError as e:
    print("Validation failed:")
    print(e)
    
imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login("your-email", "your-app-password")
imap.select("inbox")

status, message_ids = imap.search(None, "UNSEEN")
id_list = message_ids[0].split()

fetched_emails = []
for msg_id in id_list:
    status, msg_data = imap.fetch(msg_id, "(RFC822)")
    raw_email = msg_data[0][1]
    parsed = email_module.message_from_bytes(raw_email)

    subject = parsed["Subject"]
    body = ""
    for part in parsed.walk():
        if part.get_content_type() == "text/plain":
            body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
            break

    fetched_emails.append({"id": msg_id, "subject": subject, "body": body})

print(f"Fetched {len(fetched_emails)} unread messages")



load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def classify_email(subject, body):
    prompt = f"Classify this customer email.\n\nSubject: {subject}\n\nBody: {body}"
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=EmailClassification
        )
    )
    return response.parsed

def route_email(imap, msg_id, classification):
    if classification.category == "urgent":
        imap.store(msg_id, "+FLAGS", "\\Flagged")
        print(f"Flagged message {msg_id} as urgent")

    elif classification.category == "spam":
        imap.store(msg_id, "+FLAGS", "\\Deleted")
        print(f"Marked message {msg_id} for deletion")

    else:
        folder_map = {
            "complaint": "Complaints",
            "billing": "Billing",
            "general_inquiry": "General"
        }
        destination = folder_map[classification.category]
        imap.copy(msg_id, destination)
        imap.store(msg_id, "+FLAGS", "\\Deleted")
        print(f"Moved message {msg_id} to {destination}")
        

for email_data in fetched_emails:
    try:
        classification = classify_email(email_data["subject"], email_data["body"])
        route_email(imap, email_data["id"], classification)
    except Exception as e:
        print(f"Could not classify message {email_data['id']}: {e}")
        # left untouched in the inbox for manual review

imap.expunge()
imap.close()
imap.logout()