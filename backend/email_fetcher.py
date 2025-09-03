# backend/email_fetcher.py
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from db import insert_email

# Gmail credentials (use environment variables for security)
EMAIL_USER = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"  # use App Password for Gmail

IMAP_SERVER = "imap.gmail.com"

def clean_text(text):
    # Clean up email text
    return text.replace("\r", "").replace("\n", " ").strip()

def fetch_emails(mailbox="INBOX", limit=10):
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select(mailbox)

        # Search for all emails
        status, messages = mail.search(None, "ALL")
        mail_ids = messages[0].split()
        mail_ids = mail_ids[-limit:]  # fetch latest `limit` emails

        for mid in mail_ids:
            status, msg_data = mail.fetch(mid, "(RFC822)")
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    sender = msg.get("From")
                    date_raw = msg.get("Date")
                    received_at = datetime.strptime(date_raw[:25], "%a, %d %b %Y %H:%M:%S")
                    
                    # Get email body
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type = part.get_content_type()
                            content_dispo = str(part.get("Content-Disposition"))
                            if content_type == "text/plain" and "attachment" not in content_dispo:
                                body = part.get_payload(decode=True).decode()
                                break
                    else:
                        body = msg.get_payload(decode=True).decode()

                    body = clean_text(body)

                    # Filter emails by keywords
                    keywords = ["support", "query", "request", "help"]
                    if any(k.lower() in subject.lower() or k.lower() in body.lower() for k in keywords):
                        insert_email(sender, subject, body, received_at)

        mail.logout()
        print("✅ Email fetch completed.")
    except Exception as e:
        print("❌ Error fetching emails:", e)

if __name__ == "__main__":
    fetch_emails(limit=20)
