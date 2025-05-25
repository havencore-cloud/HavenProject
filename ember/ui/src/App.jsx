import React from 'react';
import Navbar from './components/Navbar';
import Scanner from './components/Scanner';
import Footer from './components/Footer';

export default function App() {
  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      <Navbar />
      <main className="flex-grow container mx-auto px-4 py-8">
        <Scanner />
      </main>
      <Footer />
    </div>
  );
}
