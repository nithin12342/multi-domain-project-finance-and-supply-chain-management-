import React, { useState, useEffect } from 'react';
import { Bar, Line, Pie, Doughnut } from 'react-chartjs-2';
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

const Analytics = () => {
  const [timeRange, setTimeRange] = useState('monthly');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API call to fetch analytics data
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  }, [timeRange]);

  const shipmentStatusData = {
    labels: ['Created', 'In Transit', 'Delivered', 'Delayed', 'Cancelled'],
    datasets: [
      {
        label: 'Shipments by Status',
        data: [120, 340, 420, 45, 15],
        backgroundColor: [
          'rgba(54, 162, 235, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 99, 132, 0.6)',
          'rgba(153, 102, 255, 0.6)'
        ],
      },
    ],
  };

  const revenueData = {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      {
        label: 'Revenue ($)',
        data: [120000, 190000, 150000, 220000, 180000, 250000],
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        tension: 0.1
      },
    ],
  };

  const supplierPerformanceData = {
    labels: ['Supplier A', 'Supplier B', 'Supplier C', 'Supplier D', 'Supplier E'],
    datasets: [
      {
        label: 'On-time Delivery %',
        data: [95, 87, 92, 78, 88],
        backgroundColor: 'rgba(153, 102, 255, 0.6)',
      },
    ],
  };

  const financierRiskData = {
    labels: ['Low Risk', 'Medium Risk', 'High Risk'],
    datasets: [
      {
        data: [70, 25, 5],
        backgroundColor: [
          'rgba(75, 192, 192, 0.6)',
          'rgba(255, 206, 86, 0.6)',
          'rgba(255, 99, 132, 0.6)'
        ],
      },
    ],
  };

  const inventoryTurnoverData = {
    labels: ['Product A', 'Product B', 'Product C', 'Product D', 'Product E'],
    datasets: [
      {
        label: 'Turnover Rate',
        data: [8.2, 6.5, 9.1, 7.3, 5.8],
        backgroundColor: 'rgba(255, 159, 64, 0.6)',
      },
    ],
  };

  if (loading) {
    return <div className="analytics">Loading analytics data...</div>;
  }

  return (
    <div className="analytics">
      <div className="page-header">
        <h1>Advanced Analytics</h1>
        <div className="time-range-selector">
          <select value={timeRange} onChange={(e) => setTimeRange(e.target.value)}>
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
            <option value="yearly">Yearly</option>
          </select>
        </div>
      </div>
      
      <div className="analytics-grid">
        <div className="chart-card">
          <h2>Shipment Status Distribution</h2>
          <Pie data={shipmentStatusData} />
        </div>
        
        <div className="chart-card">
          <h2>Monthly Revenue Trend</h2>
          <Line data={revenueData} />
        </div>
        
        <div className="chart-card">
          <h2>Supplier Performance</h2>
          <Bar data={supplierPerformanceData} />
        </div>
        
        <div className="chart-card">
          <h2>Financier Risk Distribution</h2>
          <Doughnut data={financierRiskData} />
        </div>
        
        <div className="chart-card">
          <h2>Inventory Turnover Rate</h2>
          <Bar data={inventoryTurnoverData} />
        </div>
        
        <div className="chart-card">
          <h2>Geographic Distribution</h2>
          <div className="map-placeholder">
            <p>Interactive Map Visualization</p>
            <div className="map-container">
              {/* This would be replaced with an actual map component like react-leaflet */}
              <div className="map-grid">
                <div className="map-region" style={{backgroundColor: 'rgba(54, 162, 235, 0.6)'}}>North America</div>
                <div className="map-region" style={{backgroundColor: 'rgba(255, 99, 132, 0.6)'}}>Europe</div>
                <div className="map-region" style={{backgroundColor: 'rgba(255, 206, 86, 0.6)'}}>Asia</div>
                <div className="map-region" style={{backgroundColor: 'rgba(75, 192, 192, 0.6)'}}>South America</div>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div className="kpi-section">
        <h2>Key Performance Indicators</h2>
        <div className="kpi-grid">
          <div className="kpi-card">
            <h3>On-time Delivery Rate</h3>
            <p className="kpi-value">92.4%</p>
            <div className="kpi-trend positive">↑ 3.2% from last period</div>
          </div>
          
          <div className="kpi-card">
            <h3>Average Shipment Time</h3>
            <p className="kpi-value">4.2 days</p>
            <div className="kpi-trend negative">↑ 0.3 days from last period</div>
          </div>
          
          <div className="kpi-card">
            <h3>Inventory Accuracy</h3>
            <p className="kpi-value">98.7%</p>
            <div className="kpi-trend positive">↑ 1.1% from last period</div>
          </div>
          
          <div className="kpi-card">
            <h3>Customer Satisfaction</h3>
            <p className="kpi-value">4.7/5.0</p>
            <div className="kpi-trend positive">↑ 0.2 from last period</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;