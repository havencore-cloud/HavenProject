import React from 'react';

export default function Navbar() {
  return (
    <nav className="bg-gray-800 shadow-md py-4 px-6 text-lg font-semibold">
      <div className="container mx-auto flex justify-between items-center">
        <span className="text-white">Ember Trust Scanner</span>
      </div>
    </nav>
  );
}