import { useState } from "react";
import { Zap, AlertCircle, CheckCircle2, ShieldAlert } from "lucide-react";

const BACKEND_URL = "http://localhost:8000";

interface ScoreResult {
  candidate: string;
  score: {
    overall: number;
    breakdown: { skills: number; experience: number; education: number };
    details: {
      skills: { matched: string[] };
      experience: { matched_titles: string[] };
      education: { matched_degrees: string[] };
    };
  };
  explanation: { strengths: string[]; weaknesses: string[]; overall_fit: string; recommendation: string };
  bias_report: { bias_score: number; flags: Array<{ phrase: string; issue: string; suggestion: string }>; overall_assessment: string };
  agent_flags: string[];
}

export default function App() {
  const [jobDescription, setJobDescription] = useState<string>("");
  const [result, setResult] = useState<ScoreResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [weights, setWeights] = useState({ skills: 30, experience: 40, education: 30 });

  const handleCvUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setCvFile(e.target.files[0]);
  };

  const computeScore = async () => {
    if (!cvFile || !jobDescription.trim()) {
      alert("Please upload CV and enter job description.");
      return;
    }

    setIsLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("cv_file", cvFile);
      formData.append("jd_text", jobDescription);
      formData.append("weights", JSON.stringify(weights));

      const response = await fetch(`${BACKEND_URL}/evaluate/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Analysis failed");

      const data = await response.json();
      setResult({
        candidate: data.data.candidate,
        score: {
          overall: data.data.score.total,
          breakdown: data.data.score.breakdown,
          details: data.data.score.details || { skills: { matched: [] }, experience: { matched_titles: [] }, education: { matched_degrees: [] } }
        },
        explanation: data.data.explanation,
        bias_report: data.data.bias_report,
        agent_flags: data.data.agent_flags,
      });
    } catch (error) {
      alert("Connection error. Ensure backend is running at :8000");
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const styles = {
    container: { background: '#0a0a0a', color: '#fff', minHeight: '100vh', padding: '40px 20px', fontFamily: 'system-ui, -apple-system, sans-serif' },
    header: { maxWidth: '1200px', margin: '0 auto', marginBottom: '40px' },
    title: { fontSize: '36px', fontWeight: 'bold', color: '#fbbf24', marginBottom: '8px', display: 'flex', alignItems: 'center', gap: '12px' },
    subtitle: { color: '#999', fontSize: '14px', fontStyle: 'italic' },
    main: { maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '32px' },
    section: { background: '#1a1a1a', border: '1px solid #333', borderRadius: '12px', padding: '24px' },
    label: { fontSize: '12px', fontWeight: 'bold', color: '#999', textTransform: 'uppercase', marginBottom: '12px', letterSpacing: '0.5px' },
    input: { width: '100%', padding: '12px', background: '#2a2a2a', border: '1px solid #333', borderRadius: '8px', color: '#fff', fontSize: '14px', marginBottom: '16px', boxSizing: 'border-box' },
    textarea: { width: '100%', padding: '12px', background: '#2a2a2a', border: '1px solid #333', borderRadius: '8px', color: '#fff', fontSize: '14px', minHeight: '120px', marginBottom: '16px', boxSizing: 'border-box', fontFamily: 'inherit', resize: 'vertical' },
    slider: { width: '100%', accentColor: '#fbbf24', marginBottom: '12px' },
    button: { width: '100%', padding: '12px 24px', background: '#fbbf24', color: '#000', fontWeight: 'bold', border: 'none', borderRadius: '8px', cursor: 'pointer', fontSize: '14px', marginTop: '16px' },
    buttonDisabled: { opacity: '0.5', cursor: 'not-allowed' },
    scoreGrid: { display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '24px' },
    scoreCard: { background: '#2a2a2a', border: '1px solid #333', borderRadius: '8px', padding: '16px', textAlign: 'center' },
    scoreValue: { fontSize: '32px', fontWeight: 'bold', color: '#fbbf24', marginBottom: '8px' },
    scoreLabel: { fontSize: '12px', color: '#999', textTransform: 'uppercase' },
    strengthsList: { background: '#0f3a0f', border: '1px solid #333', borderRadius: '8px', padding: '16px' },
    weaknessesList: { background: '#3a0f0f', border: '1px solid #333', borderRadius: '8px', padding: '16px' },
    listItem: { padding: '8px', marginBottom: '8px', background: '#1a1a1a', borderRadius: '4px', fontSize: '13px', borderLeft: '3px solid #fbbf24' },
  };

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div style={styles.title}>
          <Zap size={28} fill="#fbbf24" /> LCA E.G.O ARBITER
        </div>
        <p style={styles.subtitle}>Automated Talent Assessment & Bias Detection</p>
      </div>

      <div style={styles.main}>
        {/* Left Panel: Input */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          <div style={styles.section}>
            <div style={styles.label}>📄 Candidate CV</div>
            <input type="file" accept=".pdf,.doc,.docx,.txt" onChange={handleCvUpload} style={{ ...styles.input, marginBottom: '8px' }} />
            {cvFile && <p style={{ fontSize: '12px', color: '#4ade80' }}>✓ {cvFile.name}</p>}
          </div>

          <div style={styles.section}>
            <div style={styles.label}>📋 Job Description</div>
            <textarea value={jobDescription} onChange={(e) => setJobDescription(e.target.value)} placeholder="Paste job description here..." style={styles.textarea} />
          </div>

          <div style={styles.section}>
            <div style={styles.label}>⚙️ Weight Calibration</div>
            {Object.entries(weights).map(([key, val]) => (
              <div key={key} style={{ marginBottom: '16px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', marginBottom: '6px', textTransform: 'capitalize' }}>
                  <span>{key}</span>
                  <span style={{ color: '#fbbf24' }}>{val}%</span>
                </div>
                <input type="range" min="0" max="100" value={val} onChange={(e) => setWeights({ ...weights, [key]: parseInt(e.target.value) })} style={styles.slider} />
              </div>
            ))}
          </div>

          <button onClick={computeScore} disabled={isLoading || !cvFile || !jobDescription.trim()} style={{ ...styles.button, ...(isLoading || !cvFile || !jobDescription.trim() ? styles.buttonDisabled : {}) }}>
            {isLoading ? "🔄 PROCESSING..." : "▶ EXECUTE ANALYSIS"}
          </button>
        </div>

        {/* Right Panel: Output */}
        <div style={styles.section}>
          {!result ? (
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '400px', color: '#666' }}>
              <AlertCircle size={48} style={{ marginBottom: '16px', opacity: 0.3 }} />
              <p>Awaiting analysis input...</p>
            </div>
          ) : (
            <div style={{ animation: 'fadeIn 0.5s ease-in' }}>
              {/* Overall Score */}
              <div style={styles.scoreGrid}>
                <div style={styles.scoreCard}>
                  <div style={styles.scoreValue}>{result.score.overall.toFixed(1)}%</div>
                  <div style={styles.scoreLabel}>Overall Match</div>
                </div>
                <div style={styles.scoreCard}>
                  <div style={{ ...styles.scoreValue, color: result.bias_report.bias_score > 50 ? '#ef4444' : '#4ade80' }}>
                    {result.bias_report.bias_score}/100
                  </div>
                  <div style={styles.scoreLabel}>Bias Score</div>
                </div>
              </div>

              {/* Breakdown */}
              <div style={styles.scoreGrid}>
                <div style={styles.scoreCard}>
                  <div style={styles.scoreValue}>{result.score.breakdown.skills}%</div>
                  <div style={styles.scoreLabel}>Skills Match</div>
                </div>
                <div style={styles.scoreCard}>
                  <div style={styles.scoreValue}>{result.score.breakdown.experience}%</div>
                  <div style={styles.scoreLabel}>Experience</div>
                </div>
              </div>

              {/* Recommendation */}
              <div style={{ ...styles.scoreCard, marginBottom: '16px' }}>
                <div style={styles.label}>💡 Recommendation</div>
                <p style={{ marginTop: '8px', fontSize: '14px' }}>{result.explanation.recommendation}</p>
              </div>

              {/* Insights */}
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px', marginBottom: '16px' }}>
                <div>
                  <div style={{ ...styles.label, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px', color: '#4ade80' }}>
                    <CheckCircle2 size={14} /> Strengths
                  </div>
                  <div style={styles.strengthsList}>
                    {result.explanation.strengths.map((s, i) => (
                      <div key={i} style={styles.listItem}>
                        {s}
                      </div>
                    ))}
                  </div>
                </div>
                <div>
                  <div style={{ ...styles.label, marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px', color: '#ef4444' }}>
                    <ShieldAlert size={14} /> Gaps
                  </div>
                  <div style={styles.weaknessesList}>
                    {result.explanation.weaknesses.map((w, i) => (
                      <div key={i} style={styles.listItem}>
                        {w}
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Bias Report */}
              <div style={{ ...styles.scoreCard, borderColor: result.bias_report.bias_score > 50 ? '#7f1d1d' : '#1e3a1e' }}>
                <div style={{ ...styles.label, color: '#fbbf24', marginBottom: '12px', display: 'flex', alignItems: 'center', gap: '6px' }}>
                  <ShieldAlert size={14} /> JD Bias Audit
                </div>
                <p style={{ fontSize: '13px', marginBottom: '12px', color: '#ddd' }}>{result.bias_report.overall_assessment}</p>
                {result.bias_report.flags.length > 0 && (
                  <div style={{ fontSize: '12px', color: '#999' }}>
                    {result.bias_report.flags.map((f, i) => (
                      <div key={i} style={{ marginBottom: '8px', padding: '8px', background: '#1a1a1a', borderRadius: '4px' }}>
                        <span style={{ color: '#ef4444' }}>"{f.phrase}"</span> → <span style={{ color: '#4ade80', fontStyle: 'italic' }}>Try: {f.suggestion}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}