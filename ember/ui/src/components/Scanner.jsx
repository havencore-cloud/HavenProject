import React, { useState } from 'react';
import ResultCard from './ResultCard';


export default function Scanner() {
  const [mint, setMint] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [forceScan, setForceScan] = useState(false);


  const handleScan = async () => {
  setLoading(true);
  try {
    const res = await fetch(`http://localhost:8000/scan/${mint}?force=${forceScan}`);
    const json = await res.json();
    console.log("[DEBUG] Received:", json);
    setData(json);
  } catch (e) {
    console.error(e);
  } finally {
    setLoading(false);
  }
};
return (
  <div className="space-y-6">
    <div className="flex gap-4">
      <input
        type="text"
        placeholder="Enter token mint address"
        value={mint}
        onChange={(e) => setMint(e.target.value)}
        onKeyDown={(e) => {
    if (e.key === "Enter") handleScan();
  }}
        className="w-full px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700"
      />
      <div className="flex items-center gap-2 mt-2">
  <input
    type="checkbox"
    id="force-scan"
    checked={forceScan}
    onChange={(e) => setForceScan(e.target.checked)}
    className="accent-blue-500"
  />
  <label htmlFor="force-scan" className="text-sm text-gray-300">
    Force Live Scan (slower but more accurate)
  </label>
  </div>
  <small className="text-xs text-gray-400 ml-1">
    
  Cached Raydium data updates every few hours.
  </small>


      <button
        onClick={handleScan}
        className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg"
      >
        Scan
      </button>
    </div>

    {/* Loading Spinner */}
    {loading && (
      <div className="flex justify-center mt-4">
        <div className="h-8 w-8 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
      </div>
    )}

    {data && <ResultCard data={data} />}
  </div>
);
}