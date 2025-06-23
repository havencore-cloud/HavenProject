import React, { useState } from 'react';
import ResultCard from './ResultCard';

export default function Scanner() {
  const [mint, setMint] = useState('');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [forceScan, setForceScan] = useState(false);

  const handleScan = async () => {
    if (!mint) return;
    setLoading(true);
    try {
      const res = await fetch(`http://localhost:8000/scan/${mint}?force=${forceScan}`);
      const json = await res.json();
      console.log("[DEBUG] Received:", json);
      setData(json);
    } catch (e) {
      console.error("Scan failed:", e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row gap-4 items-start sm:items-end">
        <input
          type="text"
          placeholder="Enter token mint address"
          value={mint}
          onChange={(e) => setMint(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleScan();
          }}
          className="w-full sm:w-96 px-4 py-2 rounded-lg bg-gray-800 text-white border border-gray-700"
        />

        <div className="flex flex-col sm:flex-row sm:items-center gap-2 text-sm">
          <label className="inline-flex items-center text-gray-300">
            <input
              type="checkbox"
              checked={forceScan}
              onChange={(e) => setForceScan(e.target.checked)}
              className="accent-blue-500 mr-2"
            />
            Force Live Scan
          </label>
          <span className="text-gray-400 text-xs">
            (Slower but uses fresh data. Raydium cache updates every few hours.)
          </span>
        </div>

        <button
          onClick={handleScan}
          className="px-6 py-2 bg-blue-600 hover:bg-blue-700 rounded-lg text-white"
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
