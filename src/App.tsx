import React, { useState, useEffect, useMemo, useRef } from 'react';
import { 
  Search, 
  Inbox, 
  AlertCircle, 
  CheckCircle2, 
  Clock, 
  Send, 
  User, 
  Headset, 
  TrendingUp, 
  BarChart3,
  RefreshCw,
  MessageSquare,
  ArrowRight,
  Zap,
  HelpCircle,
  Info,
  ShieldCheck,
  Cpu,
  Activity,
  PieChart as PieChartIcon,
  Layers,
  Terminal,
  Network,
  Share2,
  ChevronRight,
  AlertTriangle,
  Package,
  Truck,
  Factory,
  Store,
  Play,
  Pause,
  RotateCcw,
  Settings2,
  Database,
  Globe
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';
import { cn } from './lib/utils';
import { LogisticsFlowEnv, EnvState, EnvAction } from './lib/OpenEnv';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Cell,
  PieChart,
  Pie,
  AreaChart,
  Area,
  LineChart,
  Line,
  Legend
} from 'recharts';

export default function App() {
  const [view, setView] = useState<'landing' | 'workspace'>('landing');
  const [env] = useState(() => new LogisticsFlowEnv());
  const [state, setState] = useState<EnvState>(env.reset());
  const [history, setHistory] = useState<EnvState[]>([]);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackSpeed, setPlaybackSpeed] = useState(500);
  const [logs, setLogs] = useState<{ id: string; msg: string; time: string }[]>([]);
  const [autoAgent, setAutoAgent] = useState(false);
  const [manualActions, setManualActions] = useState<EnvAction>({ factoryToWH: 20, whToRetail: 15 });

  const addLog = (msg: string) => {
    setLogs(prev => [{ id: Math.random().toString(36).substr(2, 9), msg, time: new Date().toLocaleTimeString() }, ...prev].slice(0, 20));
  };

  const handleReset = () => {
    const newState = env.reset();
    setState(newState);
    setHistory([newState]);
    setLogs([]);
    addLog("Environment reset to initial state.");
  };

  const handleStep = (action: EnvAction) => {
    const result = env.step(action);
    setState(result.state);
    setHistory(prev => [...prev, result.state]);
    addLog(`Week ${result.state.week}: Action [F:${action.factoryToWH}, W:${action.whToRetail}] -> Reward: ${result.reward.toFixed(2)}`);
    if (result.done) {
      setIsPlaying(false);
      addLog("Simulation complete (52 weeks).");
    }
  };

  // Simple Heuristic Agent
  useEffect(() => {
    if (isPlaying && !state.done) {
      const timer = setTimeout(() => {
        const action: EnvAction = autoAgent ? {
          factoryToWH: Math.max(0, 100 - state.inventory.warehouse + state.backlog.warehouse),
          whToRetail: Math.max(0, 50 - state.inventory.retail + state.backlog.retail)
        } : manualActions;
        handleStep(action);
      }, playbackSpeed);
      return () => clearTimeout(timer);
    }
  }, [isPlaying, state, autoAgent, manualActions, playbackSpeed]);

  if (view === 'landing') {
    return (
      <div className="min-h-screen bg-[#0a0a0c] text-slate-200 font-sans selection:bg-indigo-500/30 overflow-x-hidden">
        {/* Background Glows */}
        <div className="fixed inset-0 overflow-hidden pointer-events-none">
          <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-indigo-600/10 blur-[120px] rounded-full" />
          <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-violet-600/10 blur-[120px] rounded-full" />
        </div>

        {/* Nav */}
        <nav className="max-w-[1200px] mx-auto px-6 h-14 flex items-center justify-between relative z-10">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 bg-indigo-600 rounded-xl flex items-center justify-center shadow-xl shadow-indigo-500/20">
              <Globe className="w-4 h-4 text-white" />
            </div>
            <span className="text-base font-bold tracking-tight text-white">OpenEnv<span className="text-indigo-400">Flow</span></span>
          </div>
          <div className="hidden md:flex items-center gap-6">
            <a href="#features" className="text-[10px] font-bold text-slate-400 hover:text-white transition-colors">Features</a>
            <a href="#tasks" className="text-[10px] font-bold text-slate-400 hover:text-white transition-colors">Tasks</a>
          </div>
          <button 
            onClick={() => setView('workspace')}
            className="px-4 py-1.5 bg-slate-900 border border-slate-800 rounded-full text-[10px] font-semibold hover:bg-slate-800 transition-all"
          >
            Launch Workspace
          </button>
        </nav>

        {/* Hero Section */}
        <section className="max-w-[1200px] mx-auto px-6 pt-12 pb-12 relative z-10">
          <div className="max-w-3xl">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 text-[8px] font-bold uppercase tracking-widest mb-3">
                <Zap className="w-3 h-3" /> OpenEnv Logistics v1.0
              </div>
              <h1 className="text-4xl md:text-5xl font-bold text-white tracking-tight leading-[1.1] mb-4">
                Train RL Agents <br />
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-violet-400">In Real-World Logistics.</span>
              </h1>
              <p className="text-sm text-slate-400 leading-relaxed mb-5 max-w-lg">
                LogisticsFlow-v1 is a high-fidelity supply chain simulation environment. 
                Implement the full OpenEnv spec with typed models, standardized step/reset API, and automated graders.
              </p>
              <div className="flex flex-col sm:flex-row items-center gap-3">
                <button 
                  onClick={() => setView('workspace')}
                  className="w-full sm:w-auto px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white rounded-xl font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-2xl shadow-indigo-500/40 group"
                >
                  Enter Workspace <ArrowRight className="w-3 h-3 group-hover:translate-x-1 transition-transform" />
                </button>
              </div>
            </motion.div>
          </div>
        </section>

        {/* Features Grid */}
        <section id="features" className="max-w-[1200px] mx-auto px-6 py-12 border-t border-slate-800/50 relative z-10">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <motion.div 
              whileHover={{ y: -5 }}
              className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-indigo-500/50 transition-all"
            >
              <div className="w-10 h-10 bg-emerald-500/10 rounded-xl flex items-center justify-center mb-4">
                <ShieldCheck className="w-5 h-5 text-emerald-500" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">OpenEnv Spec</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Full compliance with typed models, openenv.yaml, and standard step/reset/state API.
              </p>
            </motion.div>

            <motion.div 
              whileHover={{ y: -5 }}
              className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-indigo-500/50 transition-all"
            >
              <div className="w-10 h-10 bg-indigo-500/10 rounded-xl flex items-center justify-center mb-4">
                <BarChart3 className="w-5 h-5 text-indigo-500" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Automated Graders</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Three distinct tasks (Easy, Medium, Hard) with automated agent evaluation and scoring.
              </p>
            </motion.div>

            <motion.div 
              whileHover={{ y: -5 }}
              className="p-6 rounded-2xl bg-slate-900/40 border border-slate-800 hover:border-indigo-500/50 transition-all"
            >
              <div className="w-10 h-10 bg-violet-500/10 rounded-xl flex items-center justify-center mb-4">
                <Terminal className="w-5 h-5 text-violet-500" />
              </div>
              <h3 className="text-lg font-bold text-white mb-2">Baseline Script</h3>
              <p className="text-xs text-slate-400 leading-relaxed">
                Reproducible inference.py script with structured logging for easy evaluation.
              </p>
            </motion.div>
          </div>
        </section>

        {/* Footer */}
        <footer className="max-w-[1200px] mx-auto px-6 py-8 border-t border-slate-800/50 flex flex-col md:flex-row items-center justify-between gap-4 relative z-10">
          <div className="flex items-center gap-3">
            <Globe className="w-5 h-5 text-indigo-500" />
            <span className="text-xs font-bold text-white">OpenEnv Flow</span>
          </div>
          <p className="text-[10px] text-slate-500">© 2026 OpenEnv Logistics. All rights reserved.</p>
        </footer>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0a0a0c] text-slate-200 font-sans selection:bg-indigo-500/30">
      {/* Header */}
      <header className="border-b border-slate-800/50 bg-[#0a0a0c]/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-[1200px] mx-auto px-6 h-14 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <button 
              onClick={() => setView('landing')}
              className="w-7 h-7 bg-indigo-600 rounded-lg flex items-center justify-center shadow-lg shadow-indigo-500/20 hover:scale-105 transition-transform"
            >
              <Globe className="w-4 h-4 text-white" />
            </button>
            <h1 className="text-base font-semibold tracking-tight text-white">OpenEnv<span className="text-indigo-400">Flow</span></h1>
            <div className="ml-3 px-2 py-0.5 rounded-full bg-slate-800 border border-slate-700 text-[9px] font-bold uppercase tracking-wider text-slate-400">
              WORKSPACE
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 px-2.5 py-1 rounded-lg bg-slate-900 border border-slate-800">
              <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
              <span className="text-[10px] font-medium text-slate-400">Simulation Active</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content: Vertical Scrolling Layout */}
      <main className="max-w-[1000px] mx-auto py-12 px-6 space-y-16">
        
        {/* Section 1: Control Panel */}
        <section className="space-y-8">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center shadow-xl shadow-indigo-600/20">
                <Cpu className="w-6 h-6 text-white" />
              </div>
              <div>
                <h2 className="text-2xl font-bold text-white">Simulation Core</h2>
                <p className="text-xs text-slate-500">Manage environment state and agent configuration</p>
              </div>
            </div>
            <div className="flex items-center gap-3">
              <button 
                onClick={handleReset}
                className="p-3 rounded-xl bg-slate-800 border border-slate-700 text-slate-400 hover:text-white transition-colors"
                title="Reset Env"
              >
                <RotateCcw className="w-5 h-5" />
              </button>
              <button 
                onClick={() => setIsPlaying(!isPlaying)}
                className={cn(
                  "px-6 py-3 rounded-xl font-bold text-sm flex items-center gap-2 transition-all shadow-lg",
                  isPlaying 
                    ? "bg-rose-600 text-white shadow-rose-600/20 hover:bg-rose-500" 
                    : "bg-emerald-600 text-white shadow-emerald-600/20 hover:bg-emerald-500"
                )}
              >
                {isPlaying ? <><Pause className="w-5 h-5" /> Pause</> : <><Play className="w-5 h-5" /> Start</>}
              </button>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="p-6 rounded-3xl bg-slate-900/40 border border-slate-800">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block mb-1">Total Reward</span>
              <div className="text-3xl font-bold text-white">{state.totalReward.toFixed(1)}</div>
            </div>
            <div className="p-6 rounded-3xl bg-slate-900/40 border border-slate-800">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block mb-1">Last Reward</span>
              <div className={cn("text-3xl font-bold", state.lastReward >= 0 ? "text-emerald-400" : "text-rose-400")}>
                {state.lastReward.toFixed(1)}
              </div>
            </div>
            <div className="p-6 rounded-3xl bg-slate-900/40 border border-slate-800">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block mb-1">Current Demand</span>
              <div className="text-3xl font-bold text-indigo-400">{state.demand}</div>
            </div>
            <div className="p-6 rounded-3xl bg-indigo-500/10 border border-indigo-500/20">
              <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest block mb-1">Week</span>
              <div className="text-3xl font-bold text-white">{state.week}/52</div>
            </div>
          </div>
        </section>

        {/* Section 2: Environment Visualization */}
        <section className="space-y-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-violet-600/10 border border-violet-500/20 flex items-center justify-center">
              <Layers className="w-6 h-6 text-violet-500" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">Network State</h2>
              <p className="text-xs text-slate-500">Real-time inventory and logistics flow</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Factory */}
            <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Factory className="w-16 h-16 text-white" />
              </div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Factory</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-[10px] mb-1">
                    <span className="text-slate-400">Inventory</span>
                    <span className="text-white font-mono">{state.inventory.factory}</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-indigo-500" style={{ width: `${(state.inventory.factory / 200) * 100}%` }} />
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                  <span className="text-[9px] text-slate-500 uppercase block mb-1">Backlog</span>
                  <span className="text-sm font-bold text-rose-400">{state.backlog.factory}</span>
                </div>
              </div>
            </div>

            {/* Warehouse */}
            <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Package className="w-16 h-16 text-white" />
              </div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Warehouse</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-[10px] mb-1">
                    <span className="text-slate-400">Inventory</span>
                    <span className="text-white font-mono">{state.inventory.warehouse}</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-violet-500" style={{ width: `${(state.inventory.warehouse / 150) * 100}%` }} />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                    <span className="text-[9px] text-slate-500 uppercase block mb-1">Backlog</span>
                    <span className="text-sm font-bold text-rose-400">{state.backlog.warehouse}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                    <span className="text-[9px] text-slate-500 uppercase block mb-1">In-Transit</span>
                    <span className="text-sm font-bold text-indigo-400">{state.inTransit.toWarehouse.reduce((a, b) => a + b, 0)}</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Retail */}
            <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 relative overflow-hidden group">
              <div className="absolute top-0 right-0 p-4 opacity-10 group-hover:opacity-20 transition-opacity">
                <Store className="w-16 h-16 text-white" />
              </div>
              <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest mb-4">Retail</h3>
              <div className="space-y-4">
                <div>
                  <div className="flex justify-between text-[10px] mb-1">
                    <span className="text-slate-400">Inventory</span>
                    <span className="text-white font-mono">{state.inventory.retail}</span>
                  </div>
                  <div className="h-2 w-full bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full bg-emerald-500" style={{ width: `${(state.inventory.retail / 100) * 100}%` }} />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                    <span className="text-[9px] text-slate-500 uppercase block mb-1">Backlog</span>
                    <span className="text-sm font-bold text-rose-400">{state.backlog.retail}</span>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-800/50 border border-slate-700">
                    <span className="text-[9px] text-slate-500 uppercase block mb-1">In-Transit</span>
                    <span className="text-sm font-bold text-indigo-400">{state.inTransit.toRetail.reduce((a, b) => a + b, 0)}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Section 3: Agent Configuration */}
        <section className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-4 space-y-6">
            <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 space-y-6">
              <div className="flex items-center justify-between">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Agent Config</h3>
                <Settings2 className="w-4 h-4 text-slate-500" />
              </div>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between p-4 rounded-2xl bg-slate-800/50 border border-slate-700">
                  <span className="text-xs font-bold text-slate-300">Auto-Agent</span>
                  <button 
                    onClick={() => setAutoAgent(!autoAgent)}
                    className={cn(
                      "w-10 h-5 rounded-full transition-all relative",
                      autoAgent ? "bg-indigo-600" : "bg-slate-700"
                    )}
                  >
                    <div className={cn(
                      "absolute top-1 w-3 h-3 rounded-full bg-white transition-all",
                      autoAgent ? "right-1" : "left-1"
                    )} />
                  </button>
                </div>

                <div className="space-y-2">
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Playback Speed</span>
                  <input 
                    type="range" min="100" max="2000" step="100"
                    value={playbackSpeed}
                    onChange={(e) => setPlaybackSpeed(Number(e.target.value))}
                    className="w-full accent-indigo-600"
                  />
                  <div className="flex justify-between text-[9px] text-slate-600 font-mono">
                    <span>FAST</span>
                    <span>SLOW</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="p-8 rounded-3xl bg-indigo-500/5 border border-indigo-500/20 space-y-4">
              <h3 className="text-xs font-bold text-indigo-400 uppercase tracking-widest">Manual Override</h3>
              <div className="space-y-4">
                <div className="space-y-1">
                  <div className="flex justify-between text-[10px]">
                    <span className="text-slate-400">Factory Order</span>
                    <span className="text-indigo-400 font-mono">{manualActions.factoryToWH}</span>
                  </div>
                  <input 
                    type="range" min="0" max="100"
                    value={manualActions.factoryToWH}
                    onChange={(e) => setManualActions(prev => ({ ...prev, factoryToWH: Number(e.target.value) }))}
                    className="w-full accent-indigo-600"
                  />
                </div>
                <div className="space-y-1">
                  <div className="flex justify-between text-[10px]">
                    <span className="text-slate-400">Warehouse Order</span>
                    <span className="text-indigo-400 font-mono">{manualActions.whToRetail}</span>
                  </div>
                  <input 
                    type="range" min="0" max="100"
                    value={manualActions.whToRetail}
                    onChange={(e) => setManualActions(prev => ({ ...prev, whToRetail: Number(e.target.value) }))}
                    className="w-full accent-indigo-600"
                  />
                </div>
                <button 
                  onClick={() => handleStep(manualActions)}
                  disabled={isPlaying}
                  className="w-full py-3 rounded-xl bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white font-bold text-xs transition-all shadow-lg shadow-indigo-600/20"
                >
                  Execute Single Step
                </button>
              </div>
            </div>
          </div>

          <div className="lg:col-span-8 space-y-6">
            <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-[500px] flex flex-col">
              <div className="flex items-center justify-between mb-6">
                <h3 className="text-xs font-bold text-slate-500 uppercase tracking-widest">Inventory Dynamics</h3>
                <div className="flex gap-4">
                  <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                    <div className="w-2 h-2 rounded-full bg-indigo-500" /> Factory
                  </div>
                  <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                    <div className="w-2 h-2 rounded-full bg-violet-500" /> Warehouse
                  </div>
                  <div className="flex items-center gap-1.5 text-[10px] text-slate-400">
                    <div className="w-2 h-2 rounded-full bg-emerald-500" /> Retail
                  </div>
                </div>
              </div>
              <div className="flex-1">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={history.map(h => ({
                    week: h.week,
                    factory: h.inventory.factory,
                    warehouse: h.inventory.warehouse,
                    retail: h.inventory.retail
                  }))}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
                    <XAxis dataKey="week" hide />
                    <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 10 }} />
                    <Tooltip contentStyle={{ backgroundColor: '#0f172a', border: '1px solid #1e293b', borderRadius: '12px' }} />
                    <Area type="monotone" dataKey="factory" stroke="#6366f1" fill="#6366f1" fillOpacity={0.1} />
                    <Area type="monotone" dataKey="warehouse" stroke="#8b5cf6" fill="#8b5cf6" fillOpacity={0.1} />
                    <Area type="monotone" dataKey="retail" stroke="#10b981" fill="#10b981" fillOpacity={0.1} />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        </section>

        {/* Section 4: System Logs */}
        <section className="space-y-8">
          <div className="flex items-center gap-4">
            <div className="w-12 h-12 rounded-2xl bg-slate-800 border border-slate-700 flex items-center justify-center">
              <Terminal className="w-6 h-6 text-slate-400" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-white">System Console</h2>
              <p className="text-xs text-slate-500">Real-time event stream and logic traces</p>
            </div>
          </div>

          <div className="p-8 rounded-3xl bg-slate-900/40 border border-slate-800 h-[300px] flex flex-col overflow-hidden">
            <div className="flex-1 overflow-y-auto font-mono text-[11px] space-y-2 custom-scrollbar pr-4">
              {logs.length === 0 && <div className="text-slate-600 italic">Initializing system logs...</div>}
              {logs.map((log) => (
                <div key={log.id} className="flex gap-4 border-l-2 border-slate-800 pl-4 py-1 hover:bg-slate-800/30 transition-colors">
                  <span className="text-slate-600 shrink-0">[{log.time}]</span>
                  <span className="text-slate-300">{log.msg}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

      </main>

      {/* Footer */}
      <footer className="max-w-[1200px] mx-auto px-6 py-12 border-t border-slate-800/50 text-center">
        <div className="flex items-center justify-center gap-3 mb-4">
          <Globe className="w-6 h-6 text-indigo-500" />
          <span className="text-lg font-bold text-white">OpenEnv Flow</span>
        </div>
        <p className="text-xs text-slate-500">Powered by OpenEnv Logistics Core v1.0.0-STABLE</p>
      </footer>

      <style>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: transparent;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #1e293b;
          border-radius: 10px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #334155;
        }
      `}</style>
    </div>
  );
}
