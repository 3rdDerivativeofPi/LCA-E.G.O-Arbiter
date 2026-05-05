import { useState } from "react";
import { AlertCircle, CheckCircle2, ShieldAlert } from "lucide-react";

const BACKEND_URL = "http://localhost:8000";

interface EvaluateResult {
  candidate: string;
  score: {
    overall: number;
    breakdown: { skills: number; experience: number; education: number };
  };
  explanation: { strengths: string[]; weaknesses: string[]; overall_fit: string; recommendation: string };
  bias_report: { bias_score: number; flags: Array<{ phrase: string; issue: string; suggestion: string }>; overall_assessment: string };
}

export default function EvaluateTab() {
  const [jdText, setJdText] = useState("");
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [weights, setWeights] = useState({ skills: 50, experience: 30, education: 20 });
  const [result, setResult] = useState<EvaluateResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const computeScore = async () => {
    if (!cvFile || !jdText.trim()) {
      alert("Please upload a CV and enter a job description.");
      return;
    }
    setIsLoading(true);
    setResult(null);
    try {
      const formData = new FormData();
      formData.append("cv_file", cvFile);
      formData.append("jd_text", jdText);
      formData.append("weights", JSON.stringify({
        skills: weights.skills / 100,
        experience: weights.experience / 100,
        education: weights.education / 100,
      }));

      const resp = await fetch(`${BACKEND_URL}/evaluate/`, { method: "POST", body: formData });
      if (!resp.ok) throw new Error("Analysis failed");
      const data = await resp.json();
      const d = data.data;

      setResult({
        candidate: d.candidate,
        score: {
          overall: Math.round(d.score.total),
          breakdown: d.score.breakdown,
        },
        explanation: d.explanation,
        bias_report: d.bias_report,
      });
    } catch (err) {
      alert("Connection error. Ensure backend is running at :8000");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="grid-2">
      {/* Left panel */}
      <div className="flex-col">
        <div className="card">
          <div className="label">📄 Candidate CV</div>
          <input type="file" accept=".pdf,.doc,.docx,.txt" className="input"
            onChange={e => e.target.files?.[0] && setCvFile(e.target.files[0])} />
          {cvFile && <p className="text-green text-sm">✓ {cvFile.name}</p>}
        </div>

        <div className="card">
          <div className="label">📋 Job Description</div>
          <textarea className="textarea" placeholder="Paste job description here..."
            value={jdText} onChange={e => setJdText(e.target.value)} />
        </div>

        <div className="card">
          <div className="label">⚙️ Weight Calibration</div>
          {Object.entries(weights).map(([key, val]) => (
            <div key={key} style={{ marginBottom: "16px" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: "12px", marginBottom: "6px", textTransform: "capitalize" }}>
                <span>{key}</span>
                <span className="text-gold">{val}%</span>
              </div>
              <input type="range" min="0" max="100" className="slider" value={val}
                onChange={e => setWeights({ ...weights, [key]: parseInt(e.target.value) })} />
            </div>
          ))}
        </div>

        <button className="btn" onClick={computeScore} disabled={isLoading || !cvFile || !jdText.trim()}>
          {isLoading ? "🔄 PROCESSING..." : "▶ EXECUTE ANALYSIS"}
        </button>
      </div>

      {/* Right panel */}
      <div className="card">
        {!result ? (
          <div className="empty-state">
            <AlertCircle size={48} style={{ marginBottom: "16px", opacity: 0.3 }} />
            <p>Awaiting analysis input...</p>
          </div>
        ) : (
          <div>
            <div className="grid-equal mb-16">
              <div className="card-dark score-card">
                <div className="score-value">{result.score.overall}%</div>
                <div className="score-label">Overall Match</div>
              </div>
              <div className="card-dark score-card">
                <div className="score-value" style={{ color: result.bias_report.bias_score > 50 ? "#ef4444" : "#4ade80" }}>
                  {result.bias_report.bias_score}/100
                </div>
                <div className="score-label">Bias Score</div>
              </div>
            </div>

            <div className="grid-equal mb-16">
              <div className="card-dark score-card">
                <div className="score-value">{result.score.breakdown.skills}%</div>
                <div className="score-label">Skills</div>
              </div>
              <div className="card-dark score-card">
                <div className="score-value">{result.score.breakdown.experience}%</div>
                <div className="score-label">Experience</div>
              </div>
            </div>

            <div className="card-dark mb-16">
              <div className="label label-gold">💡 Recommendation</div>
              <p className="mt-8">{result.explanation.recommendation}</p>
            </div>

            <div className="grid-equal mb-16">
              <div>
                <div className="label label-green" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <CheckCircle2 size={14} /> Strengths
                </div>
                <div className="list-green">
                  {result.explanation.strengths.map((s, i) => <div key={i} className="list-item">{s}</div>)}
                </div>
              </div>
              <div>
                <div className="label label-red" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                  <ShieldAlert size={14} /> Gaps
                </div>
                <div className="list-red">
                  {result.explanation.weaknesses.map((w, i) => <div key={i} className="list-item">{w}</div>)}
                </div>
              </div>
            </div>

            <div className="card-dark">
              <div className="label label-gold" style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                <ShieldAlert size={14} /> JD Bias Audit
              </div>
              <p className="text-sm mt-8 mb-16" style={{ color: "#ddd" }}>{result.bias_report.overall_assessment}</p>
              {result.bias_report.flags.map((f, i) => (
                <div key={i} style={{ marginBottom: "8px", padding: "8px", background: "#1a1a1a", borderRadius: "4px", fontSize: "12px" }}>
                  <span className="text-red">"{f.phrase}"</span> → <span className="text-green" style={{ fontStyle: "italic" }}>Try: {f.suggestion}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}