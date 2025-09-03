# backend/email_processor.py
import re
from db import get_all_emails, update_email
from response_generator import generate_draft_reply

# Simple sentiment keywords (expand as needed)
NEGATIVE_WORDS = ["not working", "problem", "issue", "frustrated", "angry", "fail"]
POSITIVE_WORDS = ["thank", "great", "good", "happy", "awesome"]

# Priority keywords
URGENT_WORDS = ["immediately", "urgent", "critical", "cannot access", "asap"]

def extract_contact_info(text):
    phone_match = re.search(r"\+?\d[\d -]{8,12}\d", text)
    email_match = re.search(r"[\w\.-]+@[\w\.-]+", text)
    return {
        "phone": phone_match.group() if phone_match else None,
        "alt_email": email_match.group() if email_match else None
    }

def detect_sentiment(text):
    text_lower = text.lower()
    if any(word in text_lower for word in NEGATIVE_WORDS):
        return "Negative"
    if any(word in text_lower for word in POSITIVE_WORDS):
        return "Positive"
    return "Neutral"

def assign_priority(text):
    text_lower = text.lower()
    if any(word in text_lower for word in URGENT_WORDS):
        return "Urgent"
    return "Not Urgent"

def process_emails():
    emails = get_all_emails()
    for email_data in emails:
        if email_data["processed"]:
            continue

        extracted = extract_contact_info(email_data["body"])
        sentiment = detect_sentiment(email_data["body"])
        priority = assign_priority(email_data["body"])
        draft = generate_draft_reply(
            sender=email_data["sender"],
            subject=email_data["subject"],
            body=email_data["body"],
            sentiment=sentiment,
            priority=priority,
            extracted=extracted
        )

        update_email(
            email_data["id"],
            phone=extracted["phone"],
            alt_email=extracted["alt_email"],
            sentiment=sentiment,
            priority=priority,
            draft_reply=draft,
            processed=1
        )
        print(f"✏️ Processed email id={email_data['id']}")

if __name__ == "__main__":
    process_emails()
