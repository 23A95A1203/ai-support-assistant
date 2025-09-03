# backend/response_generator.py
import os
import openai

# Load API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = """
You are a professional customer support assistant.
Given an email body and metadata, generate a short, professional reply.
- Be empathetic if sentiment is negative.
- Mention the product if present in the email.
- Provide clear next steps or solution suggestions.
- Keep it concise (2-6 sentences) and natural.
"""

def generate_draft_reply(sender, subject, body, sentiment, priority, extracted):
    """
    Generates a context-aware, professional draft reply for an email.

    Args:
        sender (str): Sender's email address
        subject (str): Email subject line
        body (str): Email body text
        sentiment (str): Sentiment analysis of the email (Positive/Negative/Neutral)
        priority (str): Priority level (Urgent/Not urgent)
        extracted (dict): Extracted metadata or key info from the email

    Returns:
        str: Generated draft reply
    """
    user_prompt = f"""
Sender: {sender}
Subject: {subject}
Priority: {priority}
Sentiment: {sentiment}
Extracted info: {extracted}

Email body:
{body}

Write a concise, professional reply based on this context.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=220,
            temperature=0.5  # Slight randomness for unique responses
        )

        # Extract content safely
        draft_reply = response['choices'][0]['message']['content'].strip()
        if not draft_reply:
            # Fallback if response is empty
            draft_reply = "Hi, thanks for contacting support. We received your request and will update you shortly. — Support Team"
        return draft_reply

    except Exception as e:
        # Print error to debug issues like invalid API key
        print("OpenAI API error:", e)
        return "Hi, thanks for contacting support. We received your request and will update you shortly. — Support Team"
