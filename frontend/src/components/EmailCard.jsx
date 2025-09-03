import React, { useState } from 'react';

export default function EmailCard({ email, onSave }) {
  const [draft, setDraft] = useState(email.draft_reply || "");

  return (
    <div className={`card ${email.priority === "Urgent" ? 'urgent' : ''}`} style={{ border: '1px solid #ccc', marginBottom: '10px', padding: '15px', borderRadius: '8px' }}>
      <div className="meta" style={{ marginBottom: '10px' }}>
        <div className="subject"><strong>{email.subject}</strong></div>
        <div className="sender">{email.sender} • {new Date(email.received_at).toLocaleString()}</div>
        <div className="sentiment">Sentiment: {email.sentiment || 'N/A'} • Priority: {email.priority || 'N/A'}</div>
        <div className="contact">Phone: {email.phone || '—'} • Alt Email: {email.alt_email || '—'}</div>
      </div>

      <div className="body" style={{ marginBottom: '10px' }}>{email.body}</div>

      <textarea
        value={draft}
        onChange={e => setDraft(e.target.value)}
        rows={4}
        style={{ width: '100%', marginBottom: '10px', borderRadius: '5px', padding: '5px' }}
      />

      <button onClick={() => onSave(draft)} style={{ padding: '5px 10px', borderRadius: '5px', cursor: 'pointer' }}>
        Save Draft
      </button>
    </div>
  );
}
