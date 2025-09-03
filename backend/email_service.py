import imaplib, email
from email.header import decode_header
import datetime
import os
from db import insert_email

FILTER_KEYWORDS = ["support", "query", "request", "help"]


def decode_str(s):
    try:
        parts = decode_header(s)
        text = ''
        for t, enc in parts:
            if isinstance(t, bytes):
                text += t.decode(enc or 'utf-8', errors='ignore')
            else:
                text += t
        return text
    except Exception:
        return s


def fetch_and_store_imap(limit=50):
    """Fetch recent emails via IMAP and store filtered ones into DB"""

    # ✅ Read environment variables at runtime
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASS = os.getenv("EMAIL_PASS")
    IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
    IMAP_PORT = int(os.getenv("IMAP_PORT", 993))

    if not EMAIL_USER or not EMAIL_PASS:
        print("Email credentials not set; skipping IMAP fetch.")
        return

    try:
        imap = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        imap.login(EMAIL_USER, EMAIL_PASS)
        imap.select("INBOX")

        status, messages = imap.search(None, "ALL")
        if status != "OK":
            print("IMAP search failed")
            imap.logout()
            return

        mail_ids = messages[0].split()

        # Fetch latest N emails
        for num in mail_ids[-limit:]:
            res, msg = imap.fetch(num, "(RFC822)")
            if res != 'OK':
                continue

            msg_obj = email.message_from_bytes(msg[0][1])
            subject = decode_str(msg_obj.get("Subject", ""))
            from_ = decode_str(msg_obj.get("From", ""))
            date_ = msg_obj.get("Date", "")

            # Extract body
            body = ""
            if msg_obj.is_multipart():
                for part in msg_obj.walk():
                    content_type = part.get_content_type()
                    disp = str(part.get("Content-Disposition"))
                    if content_type == "text/plain" and "attachment" not in disp:
                        try:
                            body = part.get_payload(decode=True).decode(errors='ignore')
                            break
                        except Exception:
                            continue
            else:
                try:
                    body = msg_obj.get_payload(decode=True).decode(errors='ignore')
                except Exception:
                    body = str(msg_obj.get_payload())

            # Filter and insert
            if any(k.lower() in (subject + body).lower() for k in FILTER_KEYWORDS):
                insert_email(
                    from_,
                    subject,
                    body,
                    date_ or datetime.datetime.now().isoformat()
                )

        imap.logout()

    except Exception as e:
        print("IMAP fetch error:", e)
