import React from 'react';
import './globals.css';
import Sidebar from '../components/Sidebar';

export const metadata = {
  title: 'Supply Chain Finance Platform',
  description: 'Enterprise-grade multi-domain supply chain finance platform with AI/ML, Blockchain, IoT, and DeFi',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="bg-slate-950 text-slate-100 antialiased">
        <Sidebar />
        <main className="ml-64 min-h-screen p-8 page-enter">
          {children}
        </main>
      </body>
    </html>
  );
}