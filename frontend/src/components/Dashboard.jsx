import React, { useEffect, useState } from 'react';
import EmailCard from './EmailCard';
import Analytics from './Analytics';

export default function Dashboard({ fetchEmailsFunc, processAllFunc, refreshEmailsFunc, statusMessage }) {
  const [emails, setEmails] = useState([]);

  // Fetch emails from backend
  const fetchEmails = async () => {
    try {
      const res = await fetch("http://localhost:8000/emails");
      const data = await res.json();
      setEmails(data);
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
      alert("Draft saved!");
      fetchEmails(); // refresh email list after save
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

      {/* Display current status from top buttons */}
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
