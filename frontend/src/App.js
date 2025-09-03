import React, { useEffect, useState } from 'react';
import { fetchEmails, triggerFetch, triggerProcess, updateDraft } from './api';
import Dashboard from './components/Dashboard';
import './styles.css';

function App() {
  const [emails, setEmails] = useState([]);
  const [loadingFetch, setLoadingFetch] = useState(false);
  const [loadingProcess, setLoadingProcess] = useState(false);
  const [loadingRefresh, setLoadingRefresh] = useState(false);

  useEffect(() => {
    load();
  }, []);

  function load() {
    setLoadingRefresh(true);
    fetchEmails()
      .then(setEmails)
      .finally(() => setLoadingRefresh(false));
  }

  const handleFetch = () => {
    setLoadingFetch(true);
    triggerFetch()
      .then(() => alert('Fetch started (backend)'))
      .finally(() => setLoadingFetch(false));
  };

  const handleProcess = () => {
    setLoadingProcess(true);
    triggerProcess()
      .then(() => load())
      .finally(() => setLoadingProcess(false));
  };

  const handleSaveDraft = (id, draft) => {
    updateDraft(id, draft).then(() => load());
  };

  return (
    <div className="app">
      <header className="topbar">
        <h1>AI Support Assistant — Linkenite</h1>
        <div className="topbar-actions">
          <button className="action-btn" onClick={handleFetch} disabled={loadingFetch}>
            {loadingFetch ? 'Fetching...' : 'Fetch Emails'}
          </button>
          <button className="action-btn" onClick={handleProcess} disabled={loadingProcess}>
            {loadingProcess ? 'Processing...' : 'Process (Sentiment & Drafts)'}
          </button>
          <button className="action-btn" onClick={load} disabled={loadingRefresh}>
            {loadingRefresh ? 'Refreshing...' : 'Refresh'}
          </button>
        </div>
      </header>
      <main>
        <Dashboard emails={emails} onSaveDraft={handleSaveDraft} />
      </main>
    </div>
  );
}

export default App;
