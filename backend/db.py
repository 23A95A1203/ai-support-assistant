import sqlite3

DB_PATH = "emails.db"


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender TEXT,
        subject TEXT,
        body TEXT,
        received_at TEXT,
        sentiment TEXT,
        priority TEXT,
        phone TEXT,
        alt_email TEXT,
        draft_reply TEXT,
        processed INTEGER DEFAULT 0
    )
    """)
    conn.commit()
    conn.close()
    print("✅ Database initialized (emails table ready).")


def insert_email(sender, subject, body, received_at):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    INSERT INTO emails (sender, subject, body, received_at) VALUES (?, ?, ?, ?)
    """, (sender, subject, body, received_at))
    conn.commit()
    conn.close()
    print(f"📩 Inserted email from '{sender}' with subject '{subject}' at {received_at}")


def update_email(id, **kwargs):
    if not kwargs:
        print("⚠️ update_email called with no fields to update")
        return

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    fields = ", ".join([f"{k}=?" for k in kwargs.keys()])
    values = list(kwargs.values())
    values.append(id)

    c.execute(f"UPDATE emails SET {fields} WHERE id=?", values)
    conn.commit()
    conn.close()
    print(f"✏️ Updated email id={id} with fields {list(kwargs.keys())}")


def get_all_emails():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT * FROM emails
        ORDER BY CASE WHEN priority='Urgent' THEN 0 ELSE 1 END, received_at DESC
    """)
    rows = c.fetchall()
    conn.close()

    cols = ["id", "sender", "subject", "body", "received_at",
            "sentiment", "priority", "phone", "alt_email",
            "draft_reply", "processed"]

    emails = [dict(zip(cols, r)) for r in rows]
    print(f"📊 Retrieved {len(emails)} emails from database.")
    return emails


def get_email(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM emails WHERE id=?", (id,))
    r = c.fetchone()
    conn.close()

    if not r:
        print(f"⚠️ No email found with id={id}")
        return None

    cols = ["id", "sender", "subject", "body", "received_at",
            "sentiment", "priority", "phone", "alt_email",
            "draft_reply", "processed"]

    email_data = dict(zip(cols, r))
    print(f"📬 Retrieved email id={id}, subject='{email_data['subject']}'")
    return email_data
