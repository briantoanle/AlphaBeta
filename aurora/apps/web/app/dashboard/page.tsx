"use client";
import { useState, useEffect } from "react";
import { Activity, AlertTriangle, CheckCircle2, Info } from "lucide-react";
import { API_BASE_URL } from "@/lib/config";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, AreaChart, Area } from 'recharts';

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [alerts, setAlerts] = useState<any[]>([]);
  const [freshness, setFreshness] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch(`${API_BASE_URL}/api/macro/score`).then(res => res.json()),
      fetch(`${API_BASE_URL}/api/alerts`).then(res => res.json()),
      fetch(`${API_BASE_URL}/api/data/freshness`).then(res => res.json())
    ]).then(([macro, alertList, fresh]) => {
      setData(macro);
      setAlerts(alertList);
      setFreshness(fresh);
      setLoading(false);
    });
  }, []);

  if (loading) return <div className="p-10 text-center">Loading macro data...</div>;

  // Mock historical data for the chart
  const historicalData = [
    { name: 'Mon', score: 45 },
    { name: 'Tue', score: 48 },
    { name: 'Wed', score: 42 },
    { name: 'Thu', score: 55 },
    { name: 'Fri', score: data.score },
  ];

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-3xl font-bold">Macro Stress Engine</h1>
          <p className="text-gray-500">Real-time regime detection and signal monitoring</p>
        </div>
        <div className="text-right">
          <div className="text-sm text-gray-400">Last Updated</div>
          <div className="text-sm font-medium">{new Date(data.timestamp).toLocaleString()}</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="md:col-span-1 bg-white dark:bg-zinc-900 border rounded-xl p-6 flex flex-col justify-center items-center">
          <div className="text-sm font-semibold uppercase tracking-wider text-gray-500 mb-2">Stress Score</div>
          <div className={`text-6xl font-black ${data.score > 70 ? 'text-red-500' : data.score < 40 ? 'text-green-500' : 'text-blue-500'}`}>
            {data.score}
          </div>
          <div className={`mt-4 px-3 py-1 rounded-full text-xs font-bold uppercase tracking-widest ${data.regime === 'Risk-off' ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'}`}>
            {data.regime}
          </div>
        </div>

        <div className="md:col-span-3 bg-white dark:bg-zinc-900 border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Activity size={20} className="text-blue-500" /> Stress Trajectory (5D)
          </h2>
          <div className="h-[200px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={historicalData}>
                <defs>
                  <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#333" />
                <XAxis dataKey="name" stroke="#666" fontSize={12} />
                <YAxis domain={[0, 100]} stroke="#666" fontSize={12} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#18181b', border: '1px solid #3f3f46', borderRadius: '8px' }}
                />
                <Area type="monotone" dataKey="score" stroke="#3b82f6" fillOpacity={1} fill="url(#colorScore)" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Alerts Panel */}
        <div className="md:col-span-1 bg-white dark:bg-zinc-900 border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2 text-red-500">
            <AlertTriangle size={20} /> Active Alerts
          </h2>
          <div className="space-y-4">
            {alerts.length > 0 ? alerts.map((a: any) => (
              <div key={a.id} className="p-3 bg-red-50 dark:bg-red-900/10 rounded-lg border border-red-100 dark:border-red-900/20">
                <div className="flex justify-between items-start mb-1">
                  <span className="text-[10px] font-bold uppercase text-red-600">{a.severity}</span>
                  <span className="text-[10px] text-gray-500">{new Date(a.timestamp).toLocaleTimeString()}</span>
                </div>
                <p className="text-xs font-medium">{a.message}</p>
              </div>
            )) : (
              <div className="text-center py-8 text-gray-500 italic text-sm">No critical alerts today.</div>
            )}
          </div>

          <div className="mt-8 pt-6 border-t">
             <h3 className="text-xs font-bold uppercase tracking-wider text-gray-400 mb-3">Data Freshness</h3>
             <div className="space-y-2">
               {freshness && Object.entries(freshness).map(([key, val]: [string, any]) => (
                 <div key={key} className="flex justify-between items-center text-[11px]">
                   <span className="capitalize text-gray-500">{key}</span>
                   <span className="font-mono text-green-500">Updated {new Date(val).toLocaleTimeString()}</span>
                 </div>
               ))}
             </div>
          </div>
        </div>

        <div className="md:col-span-1 bg-white dark:bg-zinc-900 border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <Info size={20} className="text-purple-500" /> Driver Attribution
          </h2>
          <div className="space-y-4">
            {data.drivers.length > 0 ? data.drivers.map((d: any) => (
              <div key={d.signal} className="flex justify-between items-center">
                <div>
                  <div className="font-medium">{d.signal}</div>
                  <div className="text-xs text-gray-500 capitalize">{d.category}</div>
                </div>
                <div className={`font-mono ${d.impact > 0 ? 'text-red-500' : 'text-green-500'}`}>
                  {d.impact > 0 ? '+' : ''}{d.impact}
                </div>
              </div>
            )) : (
              <p className="text-gray-500 text-sm">Insufficient signal data for attribution today.</p>
            )}
          </div>
        </div>

        <div className="bg-white dark:bg-zinc-900 border rounded-xl p-6">
          <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
            <AlertTriangle size={20} className="text-yellow-500" /> Market Context
          </h2>
          <div className="text-sm text-gray-400 space-y-3">
             <div className="p-3 bg-zinc-800/50 rounded-lg flex gap-3">
               <CheckCircle2 size={16} className="text-green-500 shrink-0 mt-0.5" />
               <p>Labor market signals remain stable despite rising volatility in energy proxies.</p>
             </div>
             <div className="p-3 bg-zinc-800/50 rounded-lg flex gap-3">
               <Info size={16} className="text-blue-500 shrink-0 mt-0.5" />
               <p>Google search trends for "recession" are 12% below their 90-day rolling average.</p>
             </div>
          </div>
        </div>
      </div>
    </div>
  );
}
