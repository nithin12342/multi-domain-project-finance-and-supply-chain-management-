import React, { useState, useEffect } from 'react';

const Users = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Simulate API call to fetch users
    setTimeout(() => {
      setUsers([
        { id: 1, name: 'John Supplier', email: 'john@supplier.com', role: 'Supplier', status: 'Active', lastLogin: '2023-06-15' },
        { id: 2, name: 'Finance Corp', email: 'contact@financecorp.com', role: 'Financier', status: 'Active', lastLogin: '2023-06-14' },
        { id: 3, name: 'Global Logistics', email: 'info@globallogistics.com', role: 'Supplier', status: 'Pending', lastLogin: '2023-06-10' },
        { id: 4, name: 'Bank of Finance', email: 'support@bankoffinance.com', role: 'Financier', status: 'Active', lastLogin: '2023-06-12' },
        { id: 5, name: 'Admin User', email: 'admin@scfplatform.com', role: 'Admin', status: 'Active', lastLogin: '2023-06-15' },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const filteredUsers = users.filter(user => 
    user.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
    user.role.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleStatusChange = (userId, newStatus) => {
    setUsers(users.map(user => 
      user.id === userId ? { ...user, status: newStatus } : user
    ));
  };

  if (loading) {
    return <div className="users">Loading...</div>;
  }

  return (
    <div className="users">
      <div className="page-header">
        <h1>Users Management</h1>
        <button className="btn btn-primary">Add New User</button>
      </div>
      
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search users..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>
      
      <div className="users-table">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Email</th>
              <th>Role</th>
              <th>Status</th>
              <th>Last Login</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map(user => (
              <tr key={user.id}>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.role}</td>
                <td>
                  <span className={`status-badge ${user.status.toLowerCase()}`}>
                    {user.status}
                  </span>
                </td>
                <td>{user.lastLogin}</td>
                <td>
                  <button className="btn btn-sm btn-outline">Edit</button>
                  {user.status === 'Pending' && (
                    <button 
                      className="btn btn-sm btn-success"
                      onClick={() => handleStatusChange(user.id, 'Active')}
                    >
                      Approve
                    </button>
                  )}
                  <button className="btn btn-sm btn-danger">Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Users;