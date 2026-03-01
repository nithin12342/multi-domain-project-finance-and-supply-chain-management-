import React from 'react';

interface DashboardCardProps {
  title: string;
  description: string;
  icon?: React.ReactNode;
}

export default function DashboardCard({ title, description, icon }: DashboardCardProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300">
      {icon && <div className="mb-4 text-blue-500">{icon}</div>}
      <h2 className="text-xl font-semibold mb-2">{title}</h2>
      <p className="text-gray-600">{description}</p>
    </div>
  );
}