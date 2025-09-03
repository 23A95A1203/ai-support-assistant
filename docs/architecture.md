# Architecture (AI-Powered Communication Assistant)

**Pipeline**: IMAP Fetch → Filter → NLP (Sentiment/Urgency/Extraction) → LLM Draft → SQLite → React Dashboard

- **Email Retrieval**: IMAP (imaplib). Filters by keywords in subject/body.
- **Categorization**: Sentiment (HF pipeline), Priority (keyword-based), priority queue ordering in DB query.
- **Information Extraction**: Regex for phone & alt email.
- **LLM Draft**: OpenAI ChatCompletion with context (sentiment, priority, extracted info).
- **Storage**: SQLite (`emails.db`).
- **UI**: React dashboard; list emails and show analytics (Chart.js doughnut). Draft editable & saved via API.
