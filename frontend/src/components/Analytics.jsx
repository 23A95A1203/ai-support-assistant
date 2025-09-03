import React, { useEffect, useRef } from 'react';
import Chart from 'chart.js/auto';

export default function Analytics({ emails }) {
  const total = emails.length;
  const urgent = emails.filter(e => e.priority === "Urgent").length;
  const neg = emails.filter(e => e.sentiment === 'Negative').length;
  const pending = emails.filter(e => e.processed === 0).length;

  const canvasRef = useRef(null);

  useEffect(() => {
    if (!canvasRef.current) return;
    const ctx = canvasRef.current.getContext('2d');
    const chart = new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: ['Urgent', 'Negative', 'Pending'],
        datasets: [{
          data: [urgent, neg, pending],
          backgroundColor: ['#ff6b6b', '#ffa94d', '#4dabf7'],
          borderWidth: 1
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { position: 'bottom' } }
      }
    });
    return () => chart.destroy();
  }, [urgent, neg, pending]);

  return (
    <div className="analytics-container" style={{ display: 'flex', marginBottom: '20px' }}>
      <div className="analytics-stats" style={{ marginRight: '20px' }}>
        <div>Total: {total}</div>
        <div style={{ color: '#ff6b6b' }}>Urgent: {urgent}</div>
        <div style={{ color: '#ffa94d' }}>Negative: {neg}</div>
        <div style={{ color: '#4dabf7' }}>Pending: {pending}</div>
      </div>
      <div className="analytics-chart" style={{ width: '200px', height: '200px' }}>
        <canvas ref={canvasRef}></canvas>
      </div>
    </div>
  );
}
