# backend/seed_dummy_emails.py
from db import init_db, insert_email
from datetime import datetime, timedelta

def seed():
    init_db()
    now = datetime.now()
    insert_email("alice@example.com", "Support: Cannot access account", "Hi team, I cannot access my account since yesterday. It's urgent!", (now - timedelta(hours=2)).isoformat())
    insert_email("bob@example.com", "Request: Refund for Order #1234", "I want a refund. The product seems defective. Please process ASAP.", (now - timedelta(hours=3)).isoformat())
    insert_email("carol@example.com", "Query: Premium plan features", "Could you share more details about the premium plan and pricing?", (now - timedelta(days=1)).isoformat())
    print("Seeded dummy emails.")

if __name__ == "__main__":
    seed()
