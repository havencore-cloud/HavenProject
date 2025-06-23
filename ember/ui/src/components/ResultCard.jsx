import React from 'react';

export default function ResultCard({ data }) {
  const {
    mint = "Unknown",
    update_authority = {},
    badges = [],
    flags = [],
    token_metadata = {},
    liquidity = {},
    jupiter_tradable = false,
  } = data || {};

  const {
    pair: pool_pair = "None found",
    liquidity_usd = 0,
    found: liquidity_found = false,
  } = liquidity;

  const clean = (str) => typeof str === "string" ? str.replace(/\x00/g, "").trim() : str;

  return (
    <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 shadow-lg space-y-4">
      <h2 className="text-2xl font-bold text-white">
  🪙 {clean(token_metadata?.name) || "Unknown Token"}
      </h2>



      <p className="text-sm text-gray-400">📋 Copy Mint</p>
      <p className="break-all text-blue-400 underline">{mint}</p>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm mt-4">
        <div>
          <p className="text-gray-300 font-medium">On-Chain Authority:</p>
          <p className="text-gray-400">{update_authority.on_chain || "Unknown"}</p>
        </div>
        <div>
          <p className="text-gray-300 font-medium">Declared in Metadata:</p>
          <p className="text-gray-400">{update_authority.declared || "Unknown"}</p>
        </div>
        <div>
          <p className="text-gray-300 font-medium">💧 Pool Pair:</p>
          <p className="text-gray-400">{pool_pair}</p>
        </div>
        <div>
          <p className="text-gray-300 font-medium">📊 Total Liquidity:</p>
          <p className="text-gray-400">
            {liquidity_found && liquidity_usd > 0
              ? `$${liquidity_usd.toFixed(2)}`
              : "$0.00"}
          </p>
        </div>
        <div>
          <p className="text-gray-300 font-medium">🌐 Jupiter Tradable:</p>
          <p className="text-gray-400">{jupiter_tradable ? "Yes" : "No"}</p>
        </div>
      </div>

      <div className="mt-6">
        <h3 className="text-lg text-green-400 font-semibold">✅ Badges</h3>
        <ul className="list-disc ml-6 text-sm text-green-300 space-y-1">
          {badges.length > 0 ? badges.map((b, i) => <li key={i}>{b}</li>) : (
            <li>No badges found.</li>
          )}
        </ul>
      </div>

      <div className="mt-4">
        <h3 className="text-lg text-red-400 font-semibold">⚠️ Flags</h3>
        <ul className="list-disc ml-6 text-sm text-red-300 space-y-1">
          {flags.length > 0 ? flags.map((f, i) => <li key={i}>{f}</li>) : (
            <li>No flags raised.</li>
          )}
        </ul>
      </div>

      {token_metadata?.symbol && (
        <div className="mt-4 text-sm text-gray-400">
          <strong>Symbol:</strong> {clean(token_metadata.symbol)}
        </div>
      )}
    </div>
  );
}
