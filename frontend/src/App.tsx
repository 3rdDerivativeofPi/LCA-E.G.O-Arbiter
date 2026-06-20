import { useState } from "react";
import { Zap } from "lucide-react";
import EvaluateTab from "./EvaluateTab";
import RankTab from "./RankTab";
import GenerateJDTab from "./GenerateJDTab";

type Tab = "evaluate" | "rank" | "generate-jd";

export default function App() {
  const [activeTab, setActiveTab] = useState<Tab>("evaluate");

  return (
    <div className="container">
      <div style={{ marginBottom: "32px" }}>
        <div className="title">
          <Zap size={28} fill="#fbbf24" /> LCA E.G.O ARBITER
        </div>
        <p className="subtitle">Automated Talent Assessment & Bias Detection</p>
      </div>

      <div className="tabs">
        <button
          className={`tab ${activeTab === "evaluate" ? "active" : ""}`}
          onClick={() => setActiveTab("evaluate")}
        >
          ▶ Evaluate
        </button>
        <button
          className={`tab ${activeTab === "rank" ? "active" : ""}`}
          onClick={() => setActiveTab("rank")}
        >
          ⬆ Rank
        </button>
        <button
          className={`tab ${activeTab === "generate-jd" ? "active" : ""}`}
          onClick={() => setActiveTab("generate-jd")}
        >
          📋 Generate JD
        </button>
      </div>

      {activeTab === "evaluate" && <EvaluateTab />}
      {activeTab === "rank" && <RankTab />}
      {activeTab === "generate-jd" && <GenerateJDTab />}
    </div>
  );
}