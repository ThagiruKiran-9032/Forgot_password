import React, { useState } from 'react';
import { useSearchParams, Link, useNavigate } from 'react-router-dom';
import API from '../services/api';

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  const token = searchParams.get('token');
  const navigate = useNavigate();

  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [otp, setOtp] = useState('');

  const [loading, setLoading] = useState(false);
  const [passwordStaged, setPasswordStaged] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // Step 1: Submit New Password -> Backend sends Confirmation OTP to registered email
  const handleStagePassword = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    if (newPassword !== confirmPassword) {
      setError('New password and confirm password do not match.');
      return;
    }

    if (newPassword.length < 8) {
      setError('Password must be at least 8 characters long.');
      return;
    }

    setLoading(true);

    try {
      const response = await API.post('/auth/stage-password', {
        reset_token: token,
        new_password: newPassword,
      });

      setPasswordStaged(true);
      setSuccessMessage(response.data.message || 'Confirmation OTP sent to your registered email.');
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'Failed to submit new password.');
      } else {
        setError('Network error submitting new password.');
      }
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Enter Confirmation OTP -> Backend verifies OTP & updates PostgreSQL password
  const handleVerifyOtpAndFinalize = async (e) => {
    e.preventDefault();
    setError('');
    setSuccessMessage('');

    if (otp.length !== 6) {
      setError('Confirmation OTP must be exactly 6 digits.');
      return;
    }

    setLoading(true);

    try {
      const response = await API.post('/auth/verify-otp', {
        reset_token: token,
        otp: otp.trim(),
      });

      setSuccessMessage(response.data.message || 'Password reset confirmed and completed successfully!');
      setTimeout(() => {
        navigate('/login');
      }, 2500);
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.detail || 'OTP verification failed.');
      } else {
        setError('Network error verifying OTP.');
      }
    } finally {
      setLoading(false);
    }
  };

  if (!token) {
    return (
      <div className="container">
        <h2>Invalid Reset Link</h2>
        <div className="alert alert-error">
          No password reset token found in the URL query parameters.
        </div>
        <p>Please enter your registered email on the Forgot Password page to receive a reset link.</p>
        <div className="nav-links">
          <Link to="/forgot-password">Go to Forgot Password →</Link>
          <Link to="/login">Go to Login →</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>Reset Password</h2>

      {error && <div className="alert alert-error">{error}</div>}
      {successMessage && <div className="alert alert-success">{successMessage}</div>}

      {!passwordStaged ? (
        /* Step 1: Set New Password Form */
        <form onSubmit={handleStagePassword}>
          <p>Set up your new password below. A 6-digit confirmation OTP will be sent to your registered email.</p>

          <div className="form-group">
            <label>New Password</label>
            <div style={{ position: 'relative' }}>
              <input
                type={showPassword ? 'text' : 'password'}
                placeholder="e.g. NewPassword@123"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
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
                  userSelect: 'none'
                }}
              >
                {showPassword ? '🙈' : '👁️'}
              </button>
            </div>
            <small style={{ color: '#718096', display: 'block', marginTop: '4px' }}>
              Must be at least 8 characters long, containing uppercase, lowercase, digit, and special character.
            </small>
          </div>

          <div className="form-group">
            <label>Confirm New Password</label>
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Re-enter new password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Submitting Password...' : '🔒 Submit New Password & Send OTP'}
          </button>
        </form>
      ) : (
        /* Step 2: Enter Confirmation OTP Form */
        <form onSubmit={handleVerifyOtpAndFinalize}>
          <div className="form-group">
            <label>6-Digit Confirmation OTP</label>
            <input
              type="text"
              maxLength="6"
              placeholder="e.g. 123456"
              value={otp}
              onChange={(e) => setOtp(e.target.value.replace(/\D/g, ''))}
              required
            />
            <small style={{ color: '#718096', display: 'block', marginTop: '4px' }}>
              Enter the 6-digit confirmation code sent to your registered email to complete password update.
            </small>
          </div>

          <button type="submit" className="btn" disabled={loading}>
            {loading ? 'Verifying OTP...' : '✅ Verify OTP & Complete Reset'}
          </button>
        </form>
      )}

      <div className="nav-links" style={{ marginTop: '20px' }}>
        <Link to="/login">← Back to Login</Link>
      </div>
    </div>
  );
}
