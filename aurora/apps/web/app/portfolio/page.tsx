"use client";
import React, { useState, useEffect } from "react";
import { PieChart, ShieldAlert, TrendingDown } from "lucide-react";
import PortfolioUpload from "@/components/PortfolioUpload";

export default function PortfolioPage() {
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const fetchSummary = () => {
    setLoading(true);
    fetch("http://localhost:8000/api/portfolio/summary")
      .then(res => res.json())
      .then(data => {
        setSummary(data);
        setLoading(false);
      });
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  if (loading) return <div className="p-10 text-center">Loading portfolio...</div>;

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">{summary.name}</h1>
          <p className="text-gray-500">Risk Profile: Balanced | Fragility Score: {summary.fragility}</p>
        </div>
        <PortfolioUpload onUploadSuccess={fetchSummary} />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Holdings */}
        <div className="md:col-span-2 bg-white dark:bg-zinc-900 border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <PieChart size={20} className="text-blue-500" /> Current Holdings
          </h2>
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-500 border-b">
                <th className="pb-2">Asset</th>
                <th className="pb-2">Weight</th>
                <th className="pb-2">Exposure</th>
              </tr>
            </thead>
            <tbody className="divide-y">
              {summary.holdings.map((h: any) => (
                <tr key={h.symbol}>
                  <td className="py-3 font-medium">{h.symbol}</td>
                  <td className="py-3">{(h.weight * 100).toFixed(0)}%</td>
                  <td className="py-3">
                    <span className="px-2 py-1 bg-gray-100 dark:bg-zinc-800 rounded text-xs">
                      {h.symbol === 'SPY' ? 'Equity' : h.symbol === 'TLT' ? 'Rates' : 'Commodity'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Risk Metrics */}
        <div className="space-y-6">
          <div className="bg-white dark:bg-zinc-900 border rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <ShieldAlert size={20} className="text-orange-500" /> Fragility
            </h2>
            <div className="text-4xl font-bold text-orange-500">{summary.fragility}</div>
            <p className="text-sm text-gray-500 mt-2">Score &gt; 70 indicates high concentration or beta sensitivity.</p>
          </div>

          <div className="bg-white dark:bg-zinc-900 border rounded-xl p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <TrendingDown size={20} className="text-red-500" /> Stress Tests
            </h2>
            <div className="space-y-4">
              {summary.stress_tests.map((st: any) => (
                <div key={st.scenario} className="flex justify-between items-center">
                  <span className="text-sm capitalize">{st.scenario.replace('_', ' ')}</span>
                  <span className={`font-mono ${st.expected_return < 0 ? 'text-red-500' : 'text-green-500'}`}>
                    {(st.expected_return * 100).toFixed(1)}%
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
