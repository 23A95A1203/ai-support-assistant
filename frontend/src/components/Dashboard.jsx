import React, { useEffect, useState } from 'react';
import EmailCard from './EmailCard';
import Analytics from './Analytics';

export default function Dashboard({ statusMessage }) {
  const [emails, setEmails] = useState([]);

  // Fetch emails from backend
  const fetchEmails = async () => {
    try {
      const res = await fetch("http://localhost:8000/emails");
      const data = await res.json();

      // Generate AI draft for any email that doesn't have one
      const updatedEmails = await Promise.all(
        data.map(async (email) => {
          if (!email.draft_reply) {
            try {
              const draftRes = await fetch(`http://localhost:8000/email/${email.id}/generate-draft`);
              if (draftRes.ok) {
                const draftData = await draftRes.json();
                email.draft_reply = draftData.draft_reply;
              } else {
                email.draft_reply = "Hi, thanks for contacting support. We received your request and will update you shortly.";
              }
            } catch (err) {
              console.error("Error generating draft:", err);
              email.draft_reply = "Hi, thanks for contacting support. We received your request and will update you shortly.";
            }
          }
          return email;
        })
      );

      setEmails(updatedEmails);
    } catch (err) {
      console.error(err);
      alert("Failed to fetch emails");
    }
  };

  // Save draft to backend
  const onSaveDraft = async (id, draft) => {
    try {
      const res = await fetch(`http://localhost:8000/email/${id}/update-draft`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ draft_reply: draft }),
      });
      if (!res.ok) throw new Error("Failed to save draft");
      fetchEmails(); // refresh after saving
    } catch (err) {
      console.error(err);
      alert("Error saving draft");
    }
  };

  useEffect(() => {
    fetchEmails();
    const interval = setInterval(fetchEmails, 60000); // auto-refresh every 60s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <h1>AI Support Assistant Dashboard</h1>

      {statusMessage && (
        <div style={{ marginBottom: '15px', color: '#333', fontWeight: 'bold' }}>
          {statusMessage}
        </div>
      )}

      <Analytics emails={emails} />

      <div className="email-list">
        {emails.length === 0 && <div className="no-emails">No emails yet.</div>}
        {emails.map(e => (
          <EmailCard key={e.id} email={e} onSave={draft => onSaveDraft(e.id, draft)} />
        ))}
      </div>
    </div>
  );
}
