import React, { useState, useEffect } from 'react';
import { Bar, Line, Pie } from 'react-chartjs-2';
import SupplyService from '../services/supplyService';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  LineElement,
  PointElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

const Dashboard = () => {
  const [metrics, setMetrics] = useState({
    totalUsers: 0,
    totalSuppliers: 0,
    totalFinanciers: 0,
    totalShipments: 0,
    pendingApprovals: 0,
    monthlyRevenue: 0
  });

  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch suppliers data
        const suppliersResponse = await SupplyService.getSuppliers();
        const suppliers = suppliersResponse.data || [];
        
        // Fetch inventory analytics
        const analyticsResponse = await SupplyService.getInventoryAnalytics();
        const analytics = analyticsResponse.data || {};
        
        // Update state with fetched data
        setMetrics(prev => ({
          ...prev,
          totalSuppliers: suppliers.length,
          // In a real implementation, we would get these from actual API calls
        }));
        
        // Simulate recent activity for now
        setRecentActivity([
          { id: 1, user: 'John Supplier', action: 'New shipment created', time: '2 mins ago' },
          { id: 2, user: 'Finance Corp', action: 'Invoice approved', time: '15 mins ago' },
          { id: 3, user: 'Admin User', action: 'New user registered', time: '1 hour ago' },
          { id: 4, user: 'Global Logistics', action: 'Shipment delivered', time: '2 hours ago' },
          { id: 5, user: 'Bank of Finance', action: 'Payment processed', time: '3 hours ago' }
        ]);
      } catch (err) {
        setError('Failed to load dashboard data');
        console.error('Dashboard data fetch error:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const barChartData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Shipments',
        data: [1200, 1900, 1500, 2200, 1800, 2500],
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
    ],
  };

  const lineChartData = {
    labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
    datasets: [
      {
        label: 'Revenue',
        data: [12000, 19000, 15000, 22000, 18000, 25000, 21000],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1
      },
    ],
  };

  const pieChartData = {
    labels: ['Suppliers', 'Financiers', 'Customers'],
    datasets: [
      {
        data: [87, 23, 1242],
        backgroundColor: [
          'rgba(255, 99, 132, 0.6)',
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 205, 86, 0.6)',
        ],
      },
    ],
  };

  if (loading) {
    return <div className="dashboard">Loading dashboard data...</div>;
  }

  if (error) {
    return <div className="dashboard error">Error: {error}</div>;
  }

  return (
    <div className="dashboard">
      <h1>Admin Dashboard</h1>
      
      <div className="metrics-grid">
        <div className="metric-card">
          <h3>Total Users</h3>
          <p className="metric-value">{metrics.totalUsers.toLocaleString()}</p>
          <div className="metric-trend positive">+12% from last month</div>
        </div>
        
        <div className="metric-card">
          <h3>Total Suppliers</h3>
          <p className="metric-value">{metrics.totalSuppliers}</p>
          <div className="metric-trend positive">+5% from last month</div>
        </div>
        
        <div className="metric-card">
          <h3>Total Financiers</h3>
          <p className="metric-value">{metrics.totalFinanciers}</p>
          <div className="metric-trend negative">-2% from last month</div>
        </div>
        
        <div className="metric-card">
          <h3>Total Shipments</h3>
          <p className="metric-value">{metrics.totalShipments.toLocaleString()}</p>
          <div className="metric-trend positive">+18% from last month</div>
        </div>
        
        <div className="metric-card">
          <h3>Pending Approvals</h3>
          <p className="metric-value">{metrics.pendingApprovals}</p>
          <div className="metric-trend neutral">No change</div>
        </div>
        
        <div className="metric-card">
          <h3>Monthly Revenue</h3>
          <p className="metric-value">${metrics.monthlyRevenue.toLocaleString()}</p>
          <div className="metric-trend positive">+22% from last month</div>
        </div>
      </div>
      
      <div className="charts-grid">
        <div className="chart-container">
          <h2>Monthly Shipments</h2>
          <Bar data={barChartData} />
        </div>
        
        <div className="chart-container">
          <h2>Weekly Revenue</h2>
          <Line data={lineChartData} />
        </div>
        
        <div className="chart-container">
          <h2>User Distribution</h2>
          <Pie data={pieChartData} />
        </div>
      </div>
      
      <div className="recent-activity">
        <h2>Recent Activity</h2>
        <table>
          <thead>
            <tr>
              <th>User</th>
              <th>Action</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {recentActivity.map(activity => (
              <tr key={activity.id}>
                <td>{activity.user}</td>
                <td>{activity.action}</td>
                <td>{activity.time}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;