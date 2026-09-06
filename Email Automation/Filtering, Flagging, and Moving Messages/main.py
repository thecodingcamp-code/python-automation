import imaplib

imap = imaplib.IMAP4_SSL("imap.gmail.com", 993)
imap.login("thecodingcamp.contact@gmail.com", "your-app-password")
imap.select("inbox")

target_subject = "Your Invoice from The Coding Camp"
status, message_ids = imap.search(None, f'(SUBJECT "{target_subject}")')
id_list = message_ids[0].split()

for msg_id in id_list:
    imap.store(msg_id, "+FLAGS", "\\Seen")
    imap.store(msg_id, "+FLAGS", "\\Flagged")
    imap.copy(msg_id, "Processed")
    imap.store(msg_id, "+FLAGS", "\\Deleted")

imap.expunge()  # commit all the deletions from this batch in one pass
imap.close()
imap.logout()