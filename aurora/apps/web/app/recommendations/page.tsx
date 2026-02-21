"use client";
import { useState, useEffect } from "react";
import { Lightbulb, ArrowRight, ShieldCheck, Zap, AlertCircle } from "lucide-react";

export default function RecommendationsPage() {
  const [recs, setRecs] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/recommendations")
      .then(res => res.json())
      .then(data => {
        setRecs(data.recommendations);
        setLoading(false);
      });
  }, []);

  if (loading) return <div className="p-10 text-center">Analyzing portfolio & macro signals...</div>;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Actionable Guidance</h1>
        <p className="text-gray-500">Portfolio-aware suggestions based on current macro regime</p>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {recs.map((r, i) => (
          <div key={i} className="bg-white dark:bg-zinc-900 border rounded-2xl overflow-hidden flex flex-col md:flex-row">
            <div className={`p-6 md:w-1/3 flex flex-col justify-between ${r.action === 'Reduce Risk' ? 'bg-red-50 dark:bg-red-900/10' : r.action === 'Increase Exposure' ? 'bg-green-50 dark:bg-green-900/10' : 'bg-blue-50 dark:bg-blue-900/10'}`}>
              <div>
                <span className="text-xs font-bold uppercase tracking-widest text-gray-500">{r.type}</span>
                <h2 className="text-xl font-bold mt-1">{r.title}</h2>
              </div>
              <div className="mt-6">
                <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full text-xs font-bold ${r.action === 'Reduce Risk' ? 'bg-red-200 text-red-800' : 'bg-blue-200 text-blue-800'}`}>
                  {r.action}
                </div>
              </div>
            </div>

            <div className="p-8 md:w-2/3 space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-gray-500 flex items-center gap-2 mb-2">
                  <AlertCircle size={14} /> THE REASONING
                </h3>
                <p className="text-lg">{r.reason}</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {Object.entries(r.options).map(([key, val]: [string, any]) => (
                  <div key={key} className="border rounded-xl p-4 bg-zinc-50 dark:bg-zinc-800/50">
                    <div className="text-[10px] font-bold uppercase text-gray-400 mb-1">{key}</div>
                    <div className="text-sm leading-relaxed">{val}</div>
                  </div>
                ))}
              </div>

              <div className="pt-4 border-t grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                  <h4 className="text-xs font-bold text-gray-500 mb-1 flex items-center gap-1">
                    <Zap size={12} className="text-yellow-500" /> EXPECTED IMPACT
                  </h4>
                  <p className="text-sm text-gray-400">{r.impact}</p>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-gray-500 mb-1 flex items-center gap-1">
                    <ShieldCheck size={12} className="text-blue-500" /> KEY RISKS
                  </h4>
                  <p className="text-sm text-gray-400">{r.risks}</p>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="bg-zinc-100 dark:bg-zinc-800/30 rounded-xl p-6 border border-dashed border-zinc-700">
        <h4 className="text-sm font-semibold mb-2">Disclaimer & Safety Guardrails</h4>
        <p className="text-xs text-gray-500 leading-relaxed">
          AURORA provides decision support, not financial advice. Recommendations are generated based on historical correlations which may not persist in the future.
          The Macro Stress Score is a composite index and does not guarantee market direction.
          No individual tickers are guaranteed to perform. Always consult with a certified financial advisor before making large allocation shifts.
          Data citations: FRED (Labor), yfinance (Market), Google Trends (Behavioral).
        </p>
      </div>
    </div>
  );
}
