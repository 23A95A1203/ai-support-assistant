# 🌟 AI-Powered Communication Assistant  
*Smart Email Management for Modern Support Teams*  

![License](https://img.shields.io/badge/License-MIT-green.svg)  
![React](https://img.shields.io/badge/Frontend-React-blue)  
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-yellow)  
![OpenAI](https://img.shields.io/badge/AI-Powered-OpenAI-purple)  
![Database](https://img.shields.io/badge/DB-SQLite-lightgrey)  

---

## 🚀 Project Overview
Modern organizations receive **hundreds of support-related emails daily** — manually prioritizing, analyzing, and replying is time-consuming ⚡.  

The **AI-Powered Communication Assistant** intelligently manages these emails **end-to-end**:  
- 📩 Fetches & filters incoming emails (support, query, help, request).  
- 🧠 Categorizes them with **sentiment analysis** & **priority detection**.  
- 🤖 Generates **context-aware draft replies** using LLMs (OpenAI GPT).  
- 📊 Displays everything on a **user-friendly dashboard** with analytics.  

✨ Result: Faster responses, reduced manual work, improved customer satisfaction.  

---

## 🛠️ Tech Stack
- **Frontend:** React (CRA), Axios, Chart.js  
- **Backend:** FastAPI (Python), Uvicorn  
- **Database:** SQLite (lightweight, easy setup)  
- **AI Models:** OpenAI GPT APIs (can extend with Hugging Face models)  
- **Email Retrieval:** Gmail IMAP (secure app password)  

---

## ⚙️ Features
✅ Fetch emails from Gmail/Outlook/IMAP  
✅ Filter for support-related queries  
✅ Extract metadata (phone, alt email, keywords)  
✅ Sentiment analysis (Positive / Neutral / Negative)  
✅ Urgency detection with **priority queue**  
✅ Auto-draft professional & empathetic replies  
✅ Dashboard with:  
   - 📈 Email analytics (total, pending, resolved)  
   - 🥧 Sentiment breakdown  
   - 📊 Urgent vs Non-Urgent chart  
✅ Edit AI-generated drafts before sending  

---

## 📂 Project Structure
```
ai-support-assistant/
│
├── backend/           # FastAPI backend
│   ├── app.py         # Main FastAPI app
│   ├── models/        # DB models
│   ├── services/      # Email + AI services
│   ├── requirements.txt
│   └── .env           # Env vars (API keys, email creds)
│
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/ # UI components
│   │   ├── pages/      # Dashboard pages
│   │   └── App.js
│   ├── public/
│   └── package.json
│
└── README.md
```

---

## 🔑 Setup Instructions

### 1️⃣ Clone Repository
```bash
git clone https://github.com/<your-username>/ai-support-assistant.git
cd ai-support-assistant
```

### 2️⃣ Backend Setup (FastAPI)
```bash
cd backend
python -m venv venv
.env\Scripts\activate   # (Windows)
# source venv/bin/activate (Linux/Mac)

pip install -r requirements.txt
```

**Configure `.env`** in `backend/`:
```ini
OPENAI_API_KEY=sk-xxxxxx
EMAIL_USER=yourmail@gmail.com
EMAIL_PASS=your_app_password
IMAP_SERVER=imap.gmail.com
IMAP_PORT=993
USE_IMAP=true
```

Run backend:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

API docs available at 👉 [http://localhost:8000/docs](http://localhost:8000/docs)

---

### 3️⃣ Frontend Setup (React)
```bash
cd ../frontend
npm install
```

**Configure `.env`** in `frontend/`:
```ini
REACT_APP_API_URL=http://localhost:8000
```

Run frontend:
```bash
npm start
```

Dashboard 👉 [http://localhost:3000](http://localhost:3000)

---

## 🎮 How It Works (Workflow)
1. **Fetch Emails** → Pulls support-related emails from Gmail IMAP.  
2. **Process All** → Classifies sentiment, detects urgency, and generates draft reply.  
3. **View Dashboard** → Emails listed with extracted metadata + AI responses.  
4. **Update Draft** → Edit AI reply and save.  
5. **Analytics** → See real-time email insights & stats.  

---
<img width="1366" height="768" alt="Screenshot (174)" src="https://github.com/user-attachments/assets/89822406-64df-47e6-8a4e-9e84bb5bf80c" />
<img width="1366" height="768" alt="Screenshot (175)" src="https://github.com/user-attachments/assets/89822406-64df-47e6-8a4e-9e84bb5bf80c" />

## 📊 Demo Screens (placeholders)
- Email List View  
- Draft Reply Panel  
- Analytics Dashboard (Pie/Bar charts)  

 

---

## 🏆 Evaluation Criteria (Hackathon)
- **Functionality:** Accurate filtering, prioritization, contextual AI replies  
- **User Experience:** Simple, clean dashboard with insights  
- **Response Quality:** Empathetic, professional auto-replies with context  
- **Impact:** Faster support, reduced workload, better customer satisfaction  

---

## 🤝 Contributors
👤 **Katraju Raviteja**  
📧 ravitejakatraju73@gmail.com  

---

## 📜 License
This project is licensed under the MIT License.  

---

✨ *“Transforming customer support with the power of AI.”*  
