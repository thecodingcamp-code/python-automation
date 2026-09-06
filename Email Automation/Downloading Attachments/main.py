import imaplib
import email
import os

imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login("thecodingcamp.contact@gmail.com", "your-app-password")
imap.select("inbox")

target_subject = "Your Invoice from The Coding Camp"
status, message_ids = imap.search(None, f'(SUBJECT "{target_subject}")')
id_list = message_ids[0].split()

download_folder = "downloaded_attachments"
os.makedirs(download_folder, exist_ok=True)

for msg_id in id_list:
    status, msg_data = imap.fetch(msg_id, "(RFC822)")
    raw_email_bytes = msg_data[0][1]
    msg = email.message_from_bytes(raw_email_bytes)

    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue  # container parts aren't attachments themselves
        if part.get("Content-Disposition") is None:
            continue  # skip the plain text and HTML body parts

        filename = part.get_filename()
        if filename:
            filename = os.path.basename(filename)
            filepath = os.path.join(download_folder, filename)
            with open(filepath, "wb") as f:
                f.write(part.get_payload(decode=True))
            print(f"Saved '{filename}' from message: {msg['Subject']}")

imap.close()
imap.logout()