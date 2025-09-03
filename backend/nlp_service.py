# backend/nlp_service.py
import re
from transformers import pipeline

# Sentiment via Hugging Face
sentiment_pipeline = pipeline("sentiment-analysis")

URGENCY_KEYWORDS = ["immediately","urgent","asap","cannot","can't","unable","critical","soon","right away","now","down","cannot access","can't access"]

PHONE_REGEX = re.compile(r'(?:\+?\d{1,4}[-.\s]?)?(\d{10,12})')
EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+')

def analyze_sentiment(text):
    try:
        out = sentiment_pipeline(text[:1000])[0]
        label = out['label']
        if label.upper().startswith("POS"):
            return "Positive"
        elif label.upper().startswith("NEG"):
            return "Negative"
        else:
            return "Neutral"
    except Exception:
        return "Neutral"

def detect_priority(text):
    text_l = text.lower()
    for kw in URGENCY_KEYWORDS:
        if kw in text_l:
            return "Urgent"
    return "Not urgent"

def extract_contact_details(text):
    phone = None
    m = PHONE_REGEX.search(text)
    if m:
        phone = m.group(1)
    emails = EMAIL_REGEX.findall(text)
    alt_email = emails[0] if emails else None
    return phone, alt_email
