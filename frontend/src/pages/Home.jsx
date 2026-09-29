import React from 'react';
import { Link } from 'react-router-dom';

export default function Home({ currentUser }) {
  return (
    <div className="container" style={{ maxWidth: '560px' }}>
      <h2>Secure Authentication System</h2>
      <p className="subtitle">
        A production-grade Secure Password Reset and OTP Authentication platform built with FastAPI, PostgreSQL, and React.
      </p>

      <div style={{ display: 'flex', flexDirection: 'column', gap: '14px', marginTop: '10px' }}>
        {currentUser ? (
          <Link to="/login" className="btn-primary" style={{ textAlign: 'center', textDecoration: 'none' }}>
            Go to Your Account Dashboard ({currentUser.name}) →
          </Link>
        ) : (
          <div style={{ display: 'flex', gap: '12px' }}>
            <Link to="/login" className="btn-primary" style={{ flex: 1, textAlign: 'center', textDecoration: 'none' }}>
              Sign In →
            </Link>
            <Link to="/register" className="btn-secondary" style={{ flex: 1, textAlign: 'center' }}>
              Register Account
            </Link>
          </div>
        )}

        <Link to="/status" className="btn-secondary" style={{ textAlign: 'center', marginTop: '8px' }}>
          🔍 View System Connection Status (Backend & Database)
        </Link>
      </div>
    </div>
  );
}
