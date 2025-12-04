'use client';

import { useState } from 'react';
import axios from 'axios';
import { 
  Activity, 
  AlertCircle, 
  CheckCircle2, 
  BarChart2, 
  Zap,
  Play,
  Github,
  Command
} from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts';


interface PredictionResponse {
  is_drop_off: number; 
  confidence_score: number;
  message: string;
}

interface ChartMetric {
  name: string;
  score: number;
  color: string;
}


const API_URL = 'http://127.0.0.1:8000/predict'; 

export default function Dashboard() {
  const [text, setText] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [data, setData] = useState<PredictionResponse | null>(null);
  const [error, setError] = useState<string>('');

  const handleAnalyze = async () => {
    if (!text.trim()) return;
    
    setLoading(true);
    setError('');
    
    try {
      const res = await axios.post<PredictionResponse>(API_URL, { text });
      setData(res.data);
    } catch (err) {
      console.error(err); 
      setError('Connection failed. Ensure the backend server is running.');
    } finally {
      setLoading(false);
    }
  };

 
  const getMetrics = (result: PredictionResponse | null): ChartMetric[] => {
    if (!result) return [];
    
    
    const isGood = result.is_drop_off === 0;
    
    return [
      { 
        name: 'Sentiment', 
        score: isGood ? 85 : 25, 
        color: '#34d399'
      },
      { 
        name: 'Hooks', 
        score: isGood ? 70 : 10, 
        color: '#60a5fa' 
      },
      { 
        name: 'Complexity', 
        score: isGood ? 30 : 95, 
        color: '#f87171'
      },
    ];
  };

  const metrics = getMetrics(data);

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-white/20">
      
      {/* Navbar */}
      <nav className="border-b border-white/10 bg-zinc-950/50 backdrop-blur-xl sticky top-0 z-50">
        <div className="max-w-5xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-2 font-semibold tracking-tight">
            <div className="w-8 h-8 bg-white rounded-lg flex items-center justify-center">
              <Activity size={18} className="text-black" />
            </div>
            <span>PodPulse</span>
          </div>
          <div className="flex items-center gap-4 text-sm text-zinc-400">
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noopener noreferrer"
              className="flex items-center gap-1 hover:text-white cursor-pointer transition-colors"
            >
              <Github size={16} /> GitHub
            </a>
            <span className="px-3 py-1 rounded-full bg-white/10 text-white text-xs font-medium">v1.0.0</span>
          </div>
        </div>
      </nav>

      <main className="max-w-5xl mx-auto px-6 py-12 space-y-8">
        
        {/* Hero Section */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">Content Analytics</h1>
          <p className="text-zinc-400 max-w-2xl">
            Optimize your podcast scripts for maximum retention using our hybrid Random Forest model trained on 5,000+ viral segments.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-6">
          
          {/* Input Area */}
          <div className="md:col-span-2 space-y-4">
            <div className="bg-zinc-900/50 border border-white/10 rounded-xl overflow-hidden focus-within:ring-2 focus-within:ring-white/20 transition-all">
              <div className="flex items-center justify-between px-4 py-3 border-b border-white/5 bg-white/5">
                <div className="flex items-center gap-2 text-xs font-medium text-zinc-400">
                  <Command size={12} />
                  <span>SCRIPT INPUT</span>
                </div>
                <div className="text-xs text-zinc-500 font-mono">
                  {text.length} chars
                </div>
              </div>
              <textarea
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Paste your transcript segment here..."
                aria-label="Script Input"
                className="w-full h-64 bg-transparent p-4 text-sm leading-relaxed resize-none focus:outline-none placeholder:text-zinc-700"
                spellCheck={false}
              />
            </div>

            <div className="flex justify-end">
              <button
                onClick={handleAnalyze}
                disabled={loading || !text}
                className="group relative inline-flex items-center gap-2 px-6 py-2.5 bg-white text-black text-sm font-semibold rounded-lg hover:bg-zinc-200 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {loading ? (
                  <span className="w-4 h-4 border-2 border-black/30 border-t-black rounded-full animate-spin" />
                ) : (
                  <Play size={16} className="fill-current" />
                )}
                <span>{loading ? 'Processing...' : 'Run Analysis'}</span>
              </button>
            </div>
          </div>

          {/* Results Sidebar */}
          <div className="space-y-4">
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg text-red-400 text-sm flex items-center gap-2">
                <AlertCircle size={16} />
                {error}
              </div>
            )}

            {!data ? (
              <div className="h-full border border-white/5 border-dashed rounded-xl flex flex-col items-center justify-center text-zinc-600 space-y-2 min-h-[300px]">
                <BarChart2 size={32} className="opacity-20" />
                <p className="text-sm">Awaiting input data...</p>
              </div>
            ) : (
              <div className="space-y-4 animate-in fade-in slide-in-from-right-4 duration-500">
                
                {/* Verdict Card */}
                <div className={`p-5 rounded-xl border ${
                  data.is_drop_off === 1 
                    ? 'bg-red-500/10 border-red-500/20' 
                    : 'bg-emerald-500/10 border-emerald-500/20'
                }`}>
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <p className="text-xs font-medium uppercase tracking-wider opacity-70 mb-1">
                        Prediction
                      </p>
                      <h3 className={`text-xl font-bold ${
                        data.is_drop_off === 1 ? 'text-red-400' : 'text-emerald-400'
                      }`}>
                        {data.message}
                      </h3>
                    </div>
                    {data.is_drop_off === 1 
                      ? <AlertCircle className="text-red-500" /> 
                      : <CheckCircle2 className="text-emerald-500" />
                    }
                  </div>
                  
                  <div className="flex items-center gap-2 text-sm">
                    <div className="flex-1 h-1.5 bg-black/20 rounded-full overflow-hidden">
                      <div 
                        className={`h-full rounded-full ${
                          data.is_drop_off === 1 ? 'bg-red-500' : 'bg-emerald-500'
                        }`}
                        style={{ width: `${data.confidence_score}%` }}
                      />
                    </div>
                    <span className="font-mono text-xs opacity-70">{data.confidence_score}%</span>
                  </div>
                </div>

                {/* Feature Graph */}
                <div className="p-5 bg-zinc-900/50 border border-white/10 rounded-xl">
                  <div className="flex items-center justify-between mb-6">
                    <h4 className="text-sm font-medium text-zinc-300">Signal Analysis</h4>
                    <Zap size={14} className="text-yellow-500" />
                  </div>
                  <div className="h-40">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart data={metrics} layout="vertical" margin={{ left: 0, right: 0 }}>
                        <XAxis type="number" hide />
                        <YAxis 
                          dataKey="name" 
                          type="category" 
                          width={70} 
                          tick={{fill: '#71717a', fontSize: 11}} 
                          axisLine={false} 
                          tickLine={false} 
                        />
                        <Tooltip 
                          cursor={{fill: 'transparent'}}
                          contentStyle={{
                            backgroundColor: '#18181b', 
                            border: '1px solid #27272a',
                            fontSize: '12px',
                            borderRadius: '6px'
                          }} 
                        />
                        <Bar dataKey="score" barSize={16} radius={[0, 4, 4, 0]}>
                          {metrics.map((entry: any, index: number) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                          ))}
                        </Bar>
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>

              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}