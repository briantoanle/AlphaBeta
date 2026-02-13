import type { Metadata } from "next";
import "./globals.css";
import Link from "next/link";
import { Providers } from "@/components/Providers";

export const metadata: Metadata = {
  title: "AURORA | Investment Helper",
  description: "Next-Gen Investment Guidance",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased">
        <Providers>
          <nav className="border-b px-6 py-4 flex items-center justify-between bg-white dark:bg-black sticky top-0 z-50">
            <div className="flex items-center gap-8">
              <Link href="/" className="text-xl font-bold tracking-tighter text-black dark:text-white">AURORA</Link>
              <div className="flex gap-4 text-sm font-medium">
                <Link href="/dashboard" className="hover:text-blue-500">Dashboard</Link>
                <Link href="/portfolio" className="hover:text-blue-500">Portfolio</Link>
                <Link href="/recommendations" className="hover:text-blue-500">Insights</Link>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-xs text-gray-500 hidden md:block">System: Healthy</div>
              <div className="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold">
                DU
              </div>
            </div>
          </nav>
          <main className="max-w-7xl mx-auto p-6">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
