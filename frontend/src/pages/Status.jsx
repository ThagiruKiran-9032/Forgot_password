import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import API from '../services/api';

export default function Status() {
  const [backendStatus, setBackendStatus] = useState(null);
  const [dbStatus, setDbStatus] = useState(null);
  const [backendError, setBackendError] = useState(null);
  const [dbError, setDbError] = useState(null);
  const [loading, setLoading] = useState(true);

  const checkConnections = async () => {
    setLoading(true);
    setBackendError(null);
    setDbError(null);

    // 1. Check Backend API Root
    try {
      const resBackend = await API.get('/');
      setBackendStatus(resBackend.data);
    } catch (err) {
      setBackendError(err.message || 'Failed to connect to backend API');
    }

    // 2. Check PostgreSQL Database Connection
    try {
      const resDb = await API.get('/db-test');
      setDbStatus(resDb.data);
    } catch (err) {
      setDbError(err.message || 'Failed to connect to database');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    checkConnections();
  }, []);

  return (
    <div className="container" style={{ maxWidth: '600px' }}>
      <h2>System Connection Status</h2>
      <p>Live health monitoring for Backend API and PostgreSQL Database connection.</p>

      <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
        <button className="btn" onClick={checkConnections} disabled={loading} style={{ width: 'auto', padding: '8px 16px' }}>
          {loading ? 'Testing...' : '🔄 Re-test Connections'}
        </button>
      </div>

      {/* Backend API Connection Card */}
      <div style={{
        background: backendError ? '#fff5f5' : '#f0fff4',
        border: `1px solid ${backendError ? '#feb2b2' : '#9ae6b4'}`,
        borderRadius: '8px',
        padding: '16px',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '16px', color: backendError ? '#9b2c2c' : '#276749' }}>
            ⚡ FastAPI Backend API
          </h3>
          <span style={{
            padding: '4px 10px',
            borderRadius: '12px',
            fontSize: '12px',
            fontWeight: 'bold',
            background: backendError ? '#e53e3e' : '#38a169',
            color: '#ffffff'
          }}>
            {backendError ? 'DISCONNECTED' : 'ONLINE'}
          </span>
        </div>
        <p style={{ margin: '8px 0 0 0', fontSize: '13px', color: '#4a5568' }}>
          Endpoint: <code>GET http://localhost:8000/</code>
        </p>
        {backendError ? (
          <div className="alert alert-error" style={{ marginTop: '10px', marginBottom: 0 }}>
            {backendError}
          </div>
        ) : (
          <pre>{JSON.stringify(backendStatus, null, 2)}</pre>
        )}
      </div>

      {/* PostgreSQL Database Connection Card */}
      <div style={{
        background: dbError ? '#fff5f5' : '#f0fff4',
        border: `1px solid ${dbError ? '#feb2b2' : '#9ae6b4'}`,
        borderRadius: '8px',
        padding: '16px',
        marginBottom: '16px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <h3 style={{ fontSize: '16px', color: dbError ? '#9b2c2c' : '#276749' }}>
            🐘 PostgreSQL Database
          </h3>
          <span style={{
            padding: '4px 10px',
            borderRadius: '12px',
            fontSize: '12px',
            fontWeight: 'bold',
            background: dbError ? '#e53e3e' : '#38a169',
            color: '#ffffff'
          }}>
            {dbError ? 'DISCONNECTED' : 'CONNECTED'}
          </span>
        </div>
        <p style={{ margin: '8px 0 0 0', fontSize: '13px', color: '#4a5568' }}>
          Endpoint: <code>GET http://localhost:8000/db-test</code>
        </p>
        {dbError ? (
          <div className="alert alert-error" style={{ marginTop: '10px', marginBottom: 0 }}>
            {dbError}
          </div>
        ) : (
          <pre>{JSON.stringify(dbStatus, null, 2)}</pre>
        )}
      </div>

      <div className="nav-links">
        <Link to="/">← Home</Link>
        <Link to="/register">Register Page →</Link>
      </div>
    </div>
  );
}
