import React, { useState, useEffect } from 'react';
import { 
  MessageSquare, 
  Mic, 
  MapPin, 
  TrendingUp, 
  AlertCircle, 
  CheckCircle2, 
  BarChart3, 
  Users,
  ArrowRight,
  Globe
} from 'lucide-react';

const API_BASE = 'http://localhost:8000';

// --- Components ---

const StatCard = ({ title, value, icon: Icon, color }) => (
  <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-100 flex items-center space-x-4">
    <div className={`p-3 rounded-lg ${color}`}>
      <Icon className="w-6 h-6 text-white" />
    </div>
    <div>
      <p className="text-sm text-slate-500 font-medium">{title}</p>
      <h3 className="text-2xl font-bold text-slate-800">{value}</h3>
    </div>
  </div>
);

const RecommendationCard = ({ rec }) => (
  <div className="bg-white p-6 rounded-xl shadow-md border-l-4 border-blue-600 hover:shadow-lg transition-shadow">
    <div className="flex justify-between items-start mb-4">
      <div>
        <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-1 rounded">
          {rec.category}
        </span>
        <h4 className="text-lg font-bold text-slate-800 mt-2">{rec.title}</h4>
      </div>
      <div className="text-right">
        <p className="text-xs text-slate-400">Priority Score</p>
        <p className="text-2xl font-black text-blue-600">{rec.priority_score}/100</p>
      </div>
    </div>
    <p className="text-slate-600 text-sm mb-4 leading-relaxed">{rec.justification}</p>
    <div className="grid grid-cols-2 gap-4 mb-6">
      <div className="bg-slate-50 p-3 rounded-lg">
        <p className="text-xs text-slate-400">Est. Budget</p>
        <p className="font-semibold text-slate-700">₹{rec.estimated_cost.toLocaleString()}</p>
      </div>
      <div className="bg-slate-50 p-3 rounded-lg">
        <p className="text-xs text-slate-400">Impacted Pop.</p>
        <p className="font-semibold text-slate-700">{rec.affected_population.toLocaleString()}</p>
      </div>
    </div>
    <button className="w-full py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 transition-colors flex items-center justify-center space-x-2">
      <span>Approve Project</span>
      <ArrowRight className="w-4 h-4" />
    </button>
  </div>
);

// --- Main App ---

export default function JanSunwaiDashboard() {
  const [view, setView] = useState('admin'); // 'admin' or 'citizen'
  const [recs, setRecs] = useState([]);
  const [feedbacks, setFeedbacks] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const recsRes = await fetch(`${API_BASE}/analytics/recommendations`);
      const recsData = await recsRes.json();
      setRecs(recsData);

      const feedRes = await fetch(`${API_BASE}/feedback/all`);
      const feedData = await feedRes.json();
      setFeedbacks(feedData);
    } catch (e) {
      console.error("Fetch error:", e);
    }
    setLoading(false);
  };

  if (loading) return <div className="h-screen flex items-center justify-center font-sans text-slate-500">Loading Governance Engine...</div>;

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900">
      {/* Navigation */}
      <nav className="bg-white border-b border-slate-200 px-8 py-4 flex justify-between items-center sticky top-0 z-10">
        <div className="flex items-center space-x-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Globe className="text-white w-6 h-6" />
          </div>
          <h1 className="text-xl font-black tracking-tight text-slate-800">JAN-SUNWAI <span className="text-blue-600">AI</span></h1>
        </div>
        <div className="flex bg-slate-100 p-1 rounded-lg">
          <button 
            onClick={() => setView('admin')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${view === 'admin' ? 'bg-white shadow-sm text-blue-600' : 'text-slate-500'}`}
          >
            Policy Dashboard
          </button>
          <button 
            onClick={() => setView('citizen')}
            className={`px-4 py-2 rounded-md text-sm font-medium transition-all ${view === 'citizen' ? 'bg-white shadow-sm text-blue-600' : 'text-slate-500'}`}
          >
            Citizen Portal
          </button>
        </div>
      </nav>

      <main className="p-8 max-w-7xl mx-auto">
        {view === 'admin' ? (
          <div className="space-y-8">
            {/* Header Stats */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <StatCard title="Total Feedback" value={feedbacks.length} icon={MessageSquare} color="bg-blue-500" />
              <StatCard title="Active Regions" value="12" icon={MapPin} color="bg-emerald-500" />
              <StatCard title="AI Recommendations" value={recs.length} icon={TrendingUp} color="bg-amber-500" />
              <StatCard title="Resolved Issues" value="42%" icon={CheckCircle2} color="bg-indigo-500" />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              {/* Left: AI recommendations */}
              <div className="lg:col-span-2 space-y-6">
                <div className="flex items-center justify-between">
                  <h2 className="text-2xl font-bold text-slate-800 flex items-center space-x-2">
                    <BarChart3 className="w-6 h-6 text-blue-600" />
                    <span>Priority Project Recommendations</span>
                  </h2>
                  <button onClick={fetchData} className="text-sm text-blue-600 font-medium hover:underline">Refresh Analysis</button>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {recs.map((rec, i) => <RecommendationCard key={i} rec={rec} />)}
                </div>
              </div>

              {/* Right: Live Feedback Feed */}
              <div className="bg-white rounded-xl shadow-sm border border-slate-200 p-6 h-fit">
                <h2 className="text-lg font-bold text-slate-800 mb-6 flex items-center space-x-2">
                  <Users className="w-5 h-5 text-blue-600" />
                  <span>Live Citizen Feed</span>
                </h2>
                <div className="space-y-4 overflow-y-auto max-h-[600px] pr-2">
                  {feedbacks.map((f, i) => (
                    <div key={i} className="p-4 rounded-lg bg-slate-50 border border-slate-100">
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-xs font-bold text-slate-400 uppercase">{f.pincode}</span>
                        <span className="text-[10px] text-slate-400">{new Date(f.timestamp).toLocaleTimeString()}</span>
                      </div>
                      <p className="text-sm text-slate-700 italic mb-2">"{f.original_content}"</p>
                      <p className="text-sm text-slate-600 font-medium">
                        <span className="text-slate-400 font-normal">Translated: </span>
                        {f.translated_content}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        ) : (
          /* Citizen Submission View */
          <div className="max-w-2xl mx-auto bg-white rounded-2xl shadow-xl border border-slate-200 overflow-hidden">
            <div className="bg-blue-600 p-8 text-white text-center">
              <h2 className="text-3xl font-bold mb-2">Your Voice Matters</h2>
              <p className="text-blue-100">Submit your grievances directly to the government. We support Hindi, English, Marathi, and more.</p>
            </div>
            <div className="p-8 space-y-6">
              <div className="grid grid-cols-2 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-600">Citizen ID</label>
                  <input type="text" className="w-full p-3 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="Enter ID" />
                </div>
                <div className="space-y-2">
                  <label className="text-sm font-semibold text-slate-600">Pincode</label>
                  <input type="text" className="w-full p-3 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500 outline-none" placeholder="110001" />
                </div>
              </div>
              <div className="space-y-2">
                <label className="text-sm font-semibold text-slate-600">Your Complaint</label>
                <textarea 
                  className="w-full p-3 rounded-lg border border-slate-200 focus:ring-2 focus:ring-blue-500 outline-none h-32" 
                  placeholder="Describe the issue in your local language..."
                ></textarea>
              </div>
              <div className="flex flex-col items-center p-8 border-2 border-dashed border-slate-200 rounded-xl bg-slate-50 hover:bg-slate-100 transition-colors cursor-pointer">
                <div className="bg-blue-100 p-4 rounded-full text-blue-600 mb-3">
                  <Mic className="w-8 h-8" />
                </div>
                <p className="font-bold text-slate-700">Record Voice Grievance</p>
                <p className="text-xs text-slate-400">Supported for accessibility and rural users</p>
              </div>
              <button className="w-full py-4 bg-blue-600 text-white rounded-xl font-bold text-lg hover:bg-blue-700 transition-all shadow-lg">
                Submit to Government
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
