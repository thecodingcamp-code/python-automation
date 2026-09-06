from email.message import EmailMessage
import mimetypes
import email
import smtplib

msg = EmailMessage()
msg["Subject"] = "Your Invoice from The Coding Camp"
msg["From"] = "thecodingcamp.contact@gmail.com"
msg["To"] = "student@example.com"
msg.set_content("Hi there,\n\nPlease find your invoice attached.\n\nThanks")


filepath = "invoice_2024_03.pdf"

mime_type, _ = mimetypes.guess_type(filepath)
maintype, subtype = mime_type.split("/")

with open(filepath, "rb") as f:
    file_data = f.read()

msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename="invoice_2024_03.pdf")

raw = msg.as_bytes()
parsed = email.message_from_bytes(raw)

for part in parsed.walk():
    if part.get_filename():
        extracted = part.get_payload(decode=True)
        print("Attached file:", part.get_filename())
        print("Extracted size:", len(extracted), "bytes")
        
msg2 = EmailMessage()
msg2["Subject"] = "Your Course Materials"
msg2["From"] = "thecodingcamp.contact@gmail.com"
msg2["To"] = "student@example.com"
msg2.set_content("Attached are both files for this module.")

filepaths = ["invoice_2024_03.pdf", "inventory.xlsx"]

for filepath in filepaths:
    mime_type, _ = mimetypes.guess_type(filepath)
    if mime_type is None:
        mime_type = "application/octet-stream"  # fallback for file types Python can't identify
    maintype, subtype = mime_type.split("/")

    with open(filepath, "rb") as f:
        file_data = f.read()

    msg2.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filepath)

with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()
    server.login("thecodingcamp.contact@gmail.com", "your-app-password")
    server.send_message(msg)