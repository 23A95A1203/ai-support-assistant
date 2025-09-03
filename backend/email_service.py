import imaplib
import email
from email.header import decode_header
from db import insert_email

IMAP_HOST = "imap.gmail.com"
IMAP_USER = "your_email@gmail.com"
IMAP_PASS = "your_password"

def fetch_and_store_imap():
    """Fetch unread emails via IMAP and store them in DB."""
    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(IMAP_USER, IMAP_PASS)
        mail.select("inbox")

        status, messages = mail.search(None, "UNSEEN")
        email_ids = messages[0].split()

        for e_id in email_ids:
            res, msg_data = mail.fetch(e_id, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding or "utf-8")
                    sender = msg.get("From")
                    body = ""

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))

                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    insert_email(
                        sender=sender,
                        subject=subject,
                        body=body,
                        processed=0
                    )
        mail.logout()
        print(f"✅ Fetched {len(email_ids)} new emails.")
    except Exception as e:
        print("Error fetching emails:", e)
