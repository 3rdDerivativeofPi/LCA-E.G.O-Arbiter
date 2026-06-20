import { useState } from "react";
import { AlertCircle, Mail, X, Copy, Check } from "lucide-react";

const BACKEND_URL = "http://localhost:8000";

interface Candidate {
  id: string;
  name: string;
  score: { total: number; breakdown: { skills: number; experience: number; education: number } };
  rank: number;
}

interface Explanation {
  strengths: string[];
  weaknesses: string[];
  overall_fit: string;
  recommendation: string;
}

interface EmailResult {
  subject: string;
  body: string;
  type: "invite" | "reject";
}

export default function RankTab() {
  const [jdText, setJdText] = useState("");
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [cvFile, setCvFile] = useState<File | null>(null);
  const [candidates, setCandidates] = useState<{ id: string; name: string }[]>([]);
  const [leaderboard, setLeaderboard] = useState<Candidate[]>([]);
  const [explanation, setExplanation] = useState<{ id: string; data: Explanation } | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState("");

  // Email generation state
  const [emailLoading, setEmailLoading] = useState<"invite" | "reject" | null>(null);
  const [emailResult, setEmailResult] = useState<EmailResult | null>(null);
  const [emailCopied, setEmailCopied] = useState(false);

  const createSession = async () => {
    if (!jdText.trim()) return alert("Please enter a job description.");
    setIsLoading(true);
    setStatus("Parsing job description...");
    try {
      const formData = new FormData();
      formData.append("jd_text", jdText);
      const resp = await fetch(`${BACKEND_URL}/rank/session`, { method: "POST", body: formData });
      const data = await resp.json();
      setSessionId(data.session_id);
      setStatus("Session created! Now upload CVs.");
      setCandidates([]);
      setLeaderboard([]);
    } catch (err) {
      alert("Failed to create session.");
    } finally {
      setIsLoading(false);
    }
  };

  const uploadCV = async () => {
    if (!cvFile || !sessionId) return alert("Please select a CV file.");
    setIsLoading(true);
    setStatus(`Uploading ${cvFile.name}...`);
    try {
      const formData = new FormData();
      formData.append("cv_file", cvFile);
      const resp = await fetch(`${BACKEND_URL}/rank/session/${sessionId}/cv`, { method: "POST", body: formData });
      const data = await resp.json();
      setCandidates(prev => [...prev, { id: data.candidate_id, name: data.name }]);
      setStatus(`✓ ${data.name} added. Upload another or click Rank.`);
      setCvFile(null);
    } catch (err) {
      alert("Failed to upload CV.");
    } finally {
      setIsLoading(false);
    }
  };

  const getRanking = async () => {
    if (!sessionId) return;
    setIsLoading(true);
    setStatus("Ranking candidates...");
    try {
      const resp = await fetch(`${BACKEND_URL}/rank/session/${sessionId}/rank`);
      const data = await resp.json();
      setLeaderboard(data.leaderboard);
      setStatus("Done!");
    } catch (err) {
      alert("Failed to rank candidates.");
    } finally {
      setIsLoading(false);
    }
  };

  const explainCandidate = async (candidateId: string) => {
    if (!sessionId) return;
    // Reset email panel when switching candidates
    setEmailResult(null);
    setEmailCopied(false);
    setStatus("Loading explanation...");
    try {
      const resp = await fetch(`${BACKEND_URL}/rank/session/${sessionId}/explain/${candidateId}`, { method: "POST" });
      const data = await resp.json();
      setExplanation({ id: candidateId, data: data.explanation });
      setStatus("");
    } catch (err) {
      alert("Failed to load explanation.");
    }
  };

  const generateEmail = async (emailType: "invite" | "reject") => {
    if (!sessionId || !explanation) return;
    setEmailLoading(emailType);
    setEmailResult(null);
    setEmailCopied(false);
    try {
      const resp = await fetch(
        `${BACKEND_URL}/email/session/${sessionId}/candidate/${explanation.id}`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email_type: emailType }),
        }
      );
      if (!resp.ok) throw new Error("Email generation failed");
      const data = await resp.json();
      setEmailResult(data.data);
    } catch (err) {
      alert("Failed to generate email.");
      console.error(err);
    } finally {
      setEmailLoading(null);
    }
  };

  const copyEmail = async () => {
    if (!emailResult) return;
    try {
      await navigator.clipboard.writeText(`Subject: ${emailResult.subject}\n\n${emailResult.body}`);
      setEmailCopied(true);
      setTimeout(() => setEmailCopied(false), 2000);
    } catch (err) {
      alert("Could not copy. Please select and copy manually.");
    }
  };

  return (
    <div className="grid-2">
      {/* Left panel */}
      <div className="flex-col">
        <div className="card">
          <div className="label">📋 Job Description</div>
          <textarea className="textarea" placeholder="Paste job description here..."
            value={jdText} onChange={e => setJdText(e.target.value)}
            disabled={!!sessionId} />
          <button className="btn" onClick={createSession} disabled={isLoading || !!sessionId}>
            {sessionId ? "✓ Session Created" : "Create Session"}
          </button>
        </div>

        {sessionId && (
          <div className="card">
            <div className="label">📄 Upload CV</div>
            <input type="file" accept=".pdf,.doc,.docx,.txt" className="input"
              onChange={e => e.target.files?.[0] && setCvFile(e.target.files[0])} />
            {cvFile && <p className="text-green text-sm">✓ {cvFile.name}</p>}
            <button className="btn" onClick={uploadCV} disabled={isLoading || !cvFile}>
              {isLoading ? "Uploading..." : "Upload CV"}
            </button>
          </div>
        )}

        {candidates.length > 0 && (
          <div className="card">
            <div className="label">👥 Candidates ({candidates.length})</div>
            {candidates.map(c => (
              <div key={c.id} className="list-item">{c.name}</div>
            ))}
            <button className="btn" onClick={getRanking} disabled={isLoading}>
              {isLoading ? "Ranking..." : "⬆ Rank All"}
            </button>
          </div>
        )}

        {status && <p className="text-muted text-sm">{status}</p>}
      </div>

      {/* Right panel */}
      <div className="card">
        {leaderboard.length === 0 ? (
          <div className="empty-state">
            <AlertCircle size={48} style={{ marginBottom: "16px", opacity: 0.3 }} />
            <p>Leaderboard will appear here...</p>
          </div>
        ) : (
          <div>
            <div className="label label-gold" style={{ marginBottom: "16px" }}>⬆ Leaderboard</div>
            {leaderboard.map(c => (
              <div key={c.id} className="leaderboard-row" onClick={() => explainCandidate(c.id)}>
                <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
                  <span className="rank-badge">#{c.rank}</span>
                  <span style={{ fontWeight: 500 }}>{c.name}</span>
                </div>
                <div style={{ display: "flex", gap: "16px", fontSize: "13px" }}>
                  <span className="text-muted">Skills: <span className="text-gold">{c.score.breakdown.skills}%</span></span>
                  <span className="text-muted">Exp: <span className="text-gold">{c.score.breakdown.experience}%</span></span>
                  <span className="text-gold" style={{ fontWeight: "bold" }}>{c.score.total}%</span>
                </div>
              </div>
            ))}

            {explanation && (
              <div className="card-dark mt-16">
                <div className="label label-gold" style={{ marginBottom: "12px" }}>
                  💡 {leaderboard.find(c => c.id === explanation.id)?.name} — Explanation
                </div>
                <div className="grid-equal">
                  <div>
                    <div className="label label-green">Strengths</div>
                    <div className="list-green">
                      {explanation.data.strengths.map((s, i) => <div key={i} className="list-item">{s}</div>)}
                    </div>
                  </div>
                  <div>
                    <div className="label label-red">Gaps</div>
                    <div className="list-red">
                      {explanation.data.weaknesses.map((w, i) => <div key={i} className="list-item">{w}</div>)}
                    </div>
                  </div>
                </div>
                <p className="text-sm mt-8 text-muted">{explanation.data.overall_fit}</p>
                <p className="text-gold mt-8" style={{ fontWeight: "bold" }}>{explanation.data.recommendation}</p>

                {/* Email generation actions */}
                <div style={{ display: "flex", gap: "8px", marginTop: "16px" }}>
                  <button
                    className="btn-outline"
                    style={{ flex: 1, borderColor: "#4ade80", color: "#4ade80" }}
                    onClick={() => generateEmail("invite")}
                    disabled={emailLoading !== null}
                  >
                    <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "6px" }}>
                      <Mail size={14} />
                      {emailLoading === "invite" ? "Đang soạn..." : "Mời phỏng vấn"}
                    </span>
                  </button>
                  <button
                    className="btn-outline"
                    style={{ flex: 1, borderColor: "#ef4444", color: "#ef4444" }}
                    onClick={() => generateEmail("reject")}
                    disabled={emailLoading !== null}
                  >
                    <span style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: "6px" }}>
                      <Mail size={14} />
                      {emailLoading === "reject" ? "Đang soạn..." : "Từ chối"}
                    </span>
                  </button>
                </div>

                {/* Generated email preview */}
                {emailResult && (
                  <div className="card-dark mt-16" style={{ border: "1px solid #fbbf24" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "12px" }}>
                      <div className="label label-gold" style={{ marginBottom: 0 }}>
                        ✉️ Email nháp — {emailResult.type === "invite" ? "Mời phỏng vấn" : "Từ chối"}
                      </div>
                      <div style={{ display: "flex", gap: "8px" }}>
                        <button className="btn-outline" onClick={copyEmail} style={{ padding: "4px 10px", fontSize: "12px" }}>
                          {emailCopied ? (
                            <span style={{ display: "flex", alignItems: "center", gap: "4px" }}><Check size={12} /> Copied</span>
                          ) : (
                            <span style={{ display: "flex", alignItems: "center", gap: "4px" }}><Copy size={12} /> Copy</span>
                          )}
                        </button>
                        <button
                          className="btn-outline"
                          onClick={() => { setEmailResult(null); setEmailCopied(false); }}
                          style={{ padding: "4px 8px" }}
                        >
                          <X size={12} />
                        </button>
                      </div>
                    </div>
                    <div style={{ fontSize: "13px", marginBottom: "8px" }}>
                      <span className="text-muted">Tiêu đề: </span>
                      <span style={{ fontWeight: 500 }}>{emailResult.subject}</span>
                    </div>
                    <div
                      style={{
                        whiteSpace: "pre-wrap",
                        fontSize: "13px",
                        lineHeight: 1.6,
                        background: "#1a1a1a",
                        padding: "12px",
                        borderRadius: "6px",
                        color: "#ddd",
                      }}
                    >
                      {emailResult.body}
                    </div>
                    <p className="text-sm mt-8 text-muted" style={{ fontStyle: "italic" }}>
                      ⚠️ Đây là bản nháp — vui lòng kiểm tra kỹ trước khi gửi.
                    </p>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}