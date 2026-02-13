import Link from "next/link";
import { ArrowRight, BarChart3, Shield, Zap } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[80vh] text-center space-y-12">
      <div className="space-y-4 max-w-3xl">
        <h1 className="text-6xl font-black tracking-tighter">
          Navigate Markets with <span className="text-blue-600">Clarity.</span>
        </h1>
        <p className="text-xl text-gray-500">
          AURORA turns messy macro and behavioral data into clear, actionable investment guidance.
          Portfolio-aware, transparent, and built for the modern investor.
        </p>
      </div>

      <div className="flex gap-4">
        <Link href="/dashboard" className="bg-blue-600 text-white px-8 py-3 rounded-full font-bold hover:bg-blue-700 transition flex items-center gap-2">
          Get Started <ArrowRight size={20} />
        </Link>
        <Link href="/portfolio" className="border px-8 py-3 rounded-full font-bold hover:bg-gray-50 dark:hover:bg-zinc-800 transition">
          View Demo Portfolio
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 w-full max-w-5xl pt-12">
        <div className="p-6 border rounded-2xl text-left space-y-3">
          <BarChart3 className="text-blue-500" />
          <h3 className="font-bold">Macro Stress Engine</h3>
          <p className="text-sm text-gray-500">Quantify market stress using labor, credit, and behavioral signals.</p>
        </div>
        <div className="p-6 border rounded-2xl text-left space-y-3">
          <Shield className="text-green-500" />
          <h3 className="font-bold">Portfolio Risk Intel</h3>
          <p className="text-sm text-gray-500">Stress test your holdings against rates, inflation, and volatility shocks.</p>
        </div>
        <div className="p-6 border rounded-2xl text-left space-y-3">
          <Zap className="text-yellow-500" />
          <h3 className="font-bold">Actionable Guidance</h3>
          <p className="text-sm text-gray-500">Get "why-first" recommendations tailored to your unique exposures.</p>
        </div>
      </div>
    </div>
  );
}
