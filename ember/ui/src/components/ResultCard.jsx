export default function ResultCard({ data }) {
  const { mint, update_authority, badges, flags, token_metadata } = data;
  const name = token_metadata?.name || "Unknown";
  const symbol = token_metadata?.symbol || "N/A";

  return (
    <div className="bg-gray-900 p-6 rounded-xl shadow-lg space-y-4 border border-gray-700">
      <div className="text-xl font-semibold text-white flex items-center justify-between">
        <div>
          🪙 {name} <span className="text-gray-400">({symbol})</span>
        </div>
        <button
          onClick={() => navigator.clipboard.writeText(mint)}
          className="text-sm text-blue-400 hover:underline"
        >
          📋 Copy Mint
        </button>
      </div>

      <div className="text-sm text-gray-400 break-all">🔗 {mint}</div>

      <div className="text-xs text-gray-500 space-y-1">
        <div>
          On-Chain Authority:{" "}
          <span className="text-white">
            {update_authority?.on_chain || "Unknown"}
          </span>
        </div>
        <div>
          Declared in Metadata:{" "}
          <span className="text-white">
            {update_authority?.declared || "Unknown"}
          </span>
        </div>
        {update_authority?.on_chain &&
          update_authority?.declared &&
          update_authority.on_chain !== update_authority.declared && (
            <div className="text-yellow-400">
              ⚠️ Mismatch between declared and on-chain update authority!
            </div>
        )}
      </div>

      <div className="flex flex-wrap gap-2 mt-2">
        {badges.map((badge, idx) => (
          <span
            key={idx}
            className="bg-green-700 text-white text-xs px-2 py-1 rounded-full"
          >
            {badge}
          </span>
        ))}
      </div>

      <div className="mt-2 space-y-1">
        {flags.map((flag, idx) => (
          <div key={idx} className="text-sm text-red-400">
            {flag}
          </div>
        ))}
      </div>
    </div>
  );
}
