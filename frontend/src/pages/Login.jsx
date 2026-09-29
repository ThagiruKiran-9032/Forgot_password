import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function Login({ currentUser, setCurrentUser }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  // On mount, if token exists, fetch logged-in user profile
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token && !currentUser) {
      API.get('/auth/me')
        .then((res) => setCurrentUser(res.data))
        .catch(() => {
          localStorage.removeItem('token');
          setCurrentUser(null);
        });
    }
  }, [currentUser, setCurrentUser]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await API.post('/auth/login', {
        email: email.trim(),
        password,
      });

      const { access_token } = response.data;
      localStorage.setItem('token', access_token);

      // Fetch formal user profile
      const profileRes = await API.get('/auth/me');
      setCurrentUser(profileRes.data);
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'Invalid email or password.');
      } else {
        setError('Network error. Is backend server running on port 8000?');
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setCurrentUser(null);
    setEmail('');
    setPassword('');
  };

  const formatDate = (isoString) => {
    if (!isoString) return 'N/A';
    return new Date(isoString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  return (
    <div className="container">
      {currentUser ? (
        /* Formal Post-Login User Dashboard */
        <div>
          <h2>Welcome, {currentUser.name}!</h2>
          <p className="subtitle">You have successfully logged in to your account.</p>

          <div className="dashboard-card">
            <div className="detail-row">
              <span className="detail-label">Full Name</span>
              <span className="detail-value">{currentUser.name}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Email Address</span>
              <span className="detail-value">{currentUser.email}</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Account Status</span>
              <span className="badge-active">Active</span>
            </div>
            <div className="detail-row">
              <span className="detail-label">Member Since</span>
              <span className="detail-value">{formatDate(currentUser.created_at)}</span>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <button
              className="btn-primary"
              onClick={() => navigate('/forgot-password')}
            >
              🔒 Change Password
            </button>

            <button
              className="btn-secondary"
              onClick={handleLogout}
              style={{ color: '#e53e3e', borderColor: '#feb2b2' }}
            >
              🚪 Log Out
            </button>
          </div>
        </div>
      ) : (
        /* Formal Login Form */
        <div>
          <h2>Sign In to Your Account</h2>
          <p className="subtitle">Enter your email and password below to log in.</p>

          {error && <div className="alert alert-error">{error}</div>}

          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label>Password</label>
              <div style={{ position: 'relative' }}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  style={{ paddingRight: '40px' }}
                  required
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    position: 'absolute',
                    right: '10px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    background: 'none',
                    border: 'none',
                    cursor: 'pointer',
                    fontSize: '18px',
                    padding: '4px',
                  }}
                  title={showPassword ? 'Hide password' : 'Show password'}
                >
                  {showPassword ? '🙈' : '👁️'}
                </button>
              </div>
            </div>

            <button type="submit" className="btn-primary" disabled={loading}>
              {loading ? 'Signing In...' : 'Sign In'}
            </button>

            <div className="form-footer">
              <Link to="/register">Create an Account</Link>
              <Link to="/forgot-password" style={{ color: '#e53e3e' }}>
                Forgot Password?
              </Link>
            </div>
          </form>
        </div>
      )}
    </div>
  );
}
