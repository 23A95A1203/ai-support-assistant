// frontend/src/api.js
import axios from 'axios';
const BASE = process.env.REACT_APP_BACKEND || "http://localhost:8000";
export const fetchEmails = () => axios.get(`${BASE}/emails`).then(r=>r.data);
export const fetchHealth = () => axios.get(`${BASE}/health`).then(r=>r.data);
export const triggerFetch = () => axios.post(`${BASE}/fetch-emails`).then(r=>r.data);
export const triggerProcess = () => axios.get(`${BASE}/process-all`).then(r=>r.data);
export const updateDraft = (id, draft) => axios.post(`${BASE}/email/${id}/update-draft`, {draft_reply: draft}).then(r=>r.data);
