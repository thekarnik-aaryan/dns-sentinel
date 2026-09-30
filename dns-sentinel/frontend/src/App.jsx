import React, { useState, useEffect } from 'react'
import { Shield, AlertTriangle } from 'lucide-react'

export default function App() {
  const [summary, setSummary] = useState({ total_queries: 0, active_alerts: 0, critical_alerts: 0 })
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    fetch('/api/dashboard/summary').then(r => r.json()).then(setSummary).catch(console.error)
    fetch('/api/alerts').then(r => r.json()).then(setAlerts).catch(console.error)
  }, [])

  return (
    <div className="min-h-screen bg-[#0B0F19] p-6 text-white font-sans">
      <header className="border-b border-gray-800 pb-4 mb-6 flex items-center gap-3">
        <Shield className="w-8 h-8 text-blue-500" />
        <h1 className="text-2xl font-bold tracking-wider">DNS SENTINEL SOC</h1>
      </header>
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-[#111827] p-4 rounded border border-gray-800">Total Queries: {summary.total_queries}</div>
        <div className="bg-[#111827] p-4 rounded border border-gray-800 text-yellow-400">Active Alerts: {summary.active_alerts}</div>
        <div className="bg-[#111827] p-4 rounded border border-gray-800 text-red-500">Critical Threats: {summary.critical_alerts}</div>
      </div>
      <div className="bg-[#111827] p-4 rounded border border-gray-800">
        <h2 className="text-lg font-semibold mb-3 flex items-center gap-2"><AlertTriangle className="text-red-400"/> Active Threats</h2>
        {alerts.map(a => (
          <div key={a.id} className="p-3 bg-gray-900 border border-gray-800 mb-2 rounded flex justify-between">
            <span>[{a.severity}] {a.title}</span>
            <span className="text-blue-400">{a.mitre_technique}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
