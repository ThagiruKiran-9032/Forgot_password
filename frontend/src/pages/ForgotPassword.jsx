import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import API from '../services/api';

export default function ForgotPassword() {
  const [email, setEmail] = useState('');
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleRequestReset = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await API.post('/auth/forgot-password', {
        email: email.trim(),
      });
      setMessage(response.data.message);
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'Failed to request password reset.');
      } else {
        setError('Network error calling /auth/forgot-password.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Forgot Password</h2>
      <p className="subtitle">Enter your registered email address to receive a secure password reset link.</p>

      {error && <div className="alert alert-error">{error}</div>}
      {message && <div className="alert alert-success">{message}</div>}

      <form onSubmit={handleRequestReset}>
        <div className="form-group">
          <label>Registered Email Address</label>
          <input
            type="email"
            placeholder="Enter your registered email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn-primary" disabled={loading}>
          {loading ? 'Sending Reset Link...' : '📧 Send Reset Link'}
        </button>

        <div className="form-footer">
          <Link to="/login">← Back to Sign In</Link>
        </div>
      </form>
    </div>
  );
}
