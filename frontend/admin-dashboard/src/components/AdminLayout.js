import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import './AdminLayout.css';

const AdminLayout = () => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path || location.pathname.startsWith(path);
  };

  return (
    <div className="admin-layout">
      <nav className="sidebar">
        <div className="logo">
          <h2>SCF Platform</h2>
          <p>Admin Dashboard</p>
        </div>
        <ul className="nav-links">
          <li className={isActive('/dashboard') ? 'active' : ''}>
            <Link to="/dashboard">
              <i className="fas fa-tachometer-alt"></i>
              <span>Dashboard</span>
            </Link>
          </li>
          <li className={isActive('/users') ? 'active' : ''}>
            <Link to="/users">
              <i className="fas fa-users"></i>
              <span>Users</span>
            </Link>
          </li>
          <li className={isActive('/suppliers') ? 'active' : ''}>
            <Link to="/suppliers">
              <i className="fas fa-truck"></i>
              <span>Suppliers</span>
            </Link>
          </li>
          <li className={isActive('/financiers') ? 'active' : ''}>
            <Link to="/financiers">
              <i className="fas fa-money-bill-wave"></i>
              <span>Financiers</span>
            </Link>
          </li>
          <li className={isActive('/shipments') ? 'active' : ''}>
            <Link to="/shipments">
              <i className="fas fa-shipping-fast"></i>
              <span>Shipments</span>
            </Link>
          </li>
          <li className={isActive('/analytics') ? 'active' : ''}>
            <Link to="/analytics">
              <i className="fas fa-chart-line"></i>
              <span>Analytics</span>
            </Link>
          </li>
          <li className={isActive('/settings') ? 'active' : ''}>
            <Link to="/settings">
              <i className="fas fa-cog"></i>
              <span>Settings</span>
            </Link>
          </li>
        </ul>
        <div className="logout">
          <Link to="/logout">
            <i className="fas fa-sign-out-alt"></i>
            <span>Logout</span>
          </Link>
        </div>
      </nav>
      <main className="main-content">
        <header className="topbar">
          <div className="user-info">
            <span>Admin User</span>
            <div className="user-avatar">
              <i className="fas fa-user"></i>
            </div>
          </div>
        </header>
        <div className="content">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default AdminLayout;