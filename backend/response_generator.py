# backend/response_generator.py
import os
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """You are a professional customer support assistant.
Given the email body and metadata, generate a short professional reply.
Be empathetic if sentiment is negative, mention product if present, and include next steps."""

def generate_draft_reply(sender, subject, body, sentiment, priority, extracted):
    user_prompt = f"""Sender: {sender}
Subject: {subject}
Priority: {priority}
Sentiment: {sentiment}
Extracted info: {extracted}

Email body:
{body}

Write an appropriate concise reply (2-6 sentences)."""
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role":"system","content":SYSTEM_PROMPT},
                {"role":"user","content":user_prompt}
            ],
            max_tokens=220,
            temperature=0.2
        )
        return resp['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("OpenAI error:", e)
        return "Hi, thanks for contacting support. We received your request and are on it. We'll update you shortly. — Support Team"
