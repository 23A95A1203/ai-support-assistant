import os
from dotenv import load_dotenv

# ✅ Load environment variables before importing services
load_dotenv()

from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from db import init_db, get_all_emails, update_email, get_email
from email_service import fetch_and_store_imap
from nlp_service import analyze_sentiment, detect_priority, extract_contact_details
from response_generator import generate_draft_reply

app = FastAPI(title="AI Support Assistant API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/fetch-emails")
def fetch_emails(bg: BackgroundTasks):
    use_imap = os.getenv("USE_IMAP", "true").lower() == "true"
    if use_imap:
        bg.add_task(fetch_and_store_imap)
    return {"status": "started"}


@app.get("/process-all")
def process_all():
    emails = get_all_emails()
    for e in emails:
        if e["processed"]:
            continue
        text = f"{e.get('subject', '')}\n{e.get('body', '')}"
        sentiment = analyze_sentiment(text)
        priority = detect_priority(text)
        phone, alt_email = extract_contact_details(text)
        draft = generate_draft_reply(
            e['sender'],
            e['subject'],
            e['body'],
            sentiment,
            priority,
            {"phone": phone, "alt_email": alt_email}
        )
        update_email(
            e['id'],
            sentiment=sentiment,
            priority=priority,
            phone=phone,
            alt_email=alt_email,
            draft_reply=draft,
            processed=1
        )
    return {"status": "processed"}


@app.get("/emails")
def list_emails():
    return get_all_emails()


@app.get("/email/{id}")
def get_single(id: int):
    return get_email(id)


@app.post("/email/{id}/update-draft")
def update_draft(id: int, payload: dict):
    draft = payload.get("draft_reply")
    update_email(id, draft_reply=draft)
    return {"status": "ok"}


# ✅ New endpoint to generate draft for a single email
@app.get("/email/{id}/generate-draft")
def generate_single_draft(id: int):
    email = get_email(id)
    if not email:
        return {"error": "Email not found"}, 404

    text = f"{email.get('subject', '')}\n{email.get('body', '')}"
    sentiment = analyze_sentiment(text)
    priority = detect_priority(text)
    phone, alt_email = extract_contact_details(text)
    draft = generate_draft_reply(
        email['sender'],
        email['subject'],
        email['body'],
        sentiment,
        priority,
        {"phone": phone, "alt_email": alt_email}
    )
    
    # Update the email with this draft
    update_email(
        email['id'],
        draft_reply=draft,
        sentiment=sentiment,
        priority=priority,
        phone=phone,
        alt_email=alt_email
    )

    return {"draft_reply": draft}
