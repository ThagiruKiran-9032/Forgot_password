import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';

export default function Navbar({ currentUser, onLogout }) {
  const navigate = useNavigate();
  const location = useLocation();

  const isActive = (path) => location.pathname === path;

  return (
    <header className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand">
          🔐 AuthSystem
        </Link>

        <nav className="navbar-links">
          <Link to="/" className={`nav-item ${isActive('/') ? 'active' : ''}`}>
            Home
          </Link>
          <Link to="/status" className={`nav-item ${isActive('/status') ? 'active' : ''}`}>
            System Status
          </Link>

          {currentUser ? (
            <>
              <Link to="/login" className={`nav-item ${isActive('/login') ? 'active' : ''}`}>
                Dashboard
              </Link>
              <button onClick={onLogout} className="btn-logout">
                Log Out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className={`nav-item ${isActive('/login') ? 'active' : ''}`}>
                Sign In
              </Link>
              <Link to="/register" className={`nav-item ${isActive('/register') ? 'active' : ''}`}>
                Register
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
