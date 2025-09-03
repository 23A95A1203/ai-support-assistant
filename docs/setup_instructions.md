# Setup Instructions

## Prereqs
- Python 3.10+
- Node.js 18+ and npm
- (Optional) OpenAI API key for better replies
- (Optional) IMAP account + app password

## 1) Backend
```bash
cd backend
python -m venv venv
# Linux/Mac:
source venv/bin/activate
# Windows (PowerShell):
# .\\venv\\Scripts\\Activate.ps1

pip install -r requirements.txt

# Create .env from example and fill values
cp .env.example .env
# EDIT .env with your keys and email creds

# Seed demo emails (optional)
python seed_dummy_emails.py

# Run API
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

## 2) Frontend
```bash
cd frontend
npm install
# Optionally create .env and set:
# REACT_APP_BACKEND=http://localhost:8000
npm start
```

Open http://localhost:3000

## 3) Using the app
- Click **Process (Sentiment & Drafts)** to analyze emails & generate drafts.
- Click **Fetch Emails** to pull real IMAP emails (if .env is configured).
- Edit any draft → **Save Draft**.
```

