export interface ParsedCV {
  name: string;
  summary: string;
  skills: string[];
  experience: Array<{
    title: string;
    company: string;
    duration: string;
    description: string;
  }>;
  education: Array<{
    degree: string;
    institution: string;
    year: string;
  }>;
}

export interface ParsedJD {
  title: string;
  summary: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_required: string;
  education_required: string;
}

export interface ScoreResult {
  candidate: string;
  score: {
    overall: number;
    breakdown: {
      skills: number;
      experience: number;
      education: number;
    };
    details: {
      skills: { matched: string[] };
      experience: { matched_titles: string[] };
      education: { matched_degrees: string[] };
    };
  };
  explanation: {
    strengths: string[];
    weaknesses: string[];
    overall_fit: string;
    recommendation: string;
  };
  bias_report: {
    bias_score: number;
    flags: Array<{ phrase: string; issue: string; suggestion: string }>;
    overall_assessment: string;
    improved_excerpt: string;
  };
  agent_flags: string[];
}

export interface AnalysisWeights {
  skills: number;
  experience: number;
  education: number;
}