"use client";

import { useState } from "react";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import {
  ChevronDown,
  ChevronUp,
  Zap,
  AlertCircle,
  Lightbulb,
  Upload,
  X,
} from "lucide-react";

interface ScoreResult {
  score: number;
  matchedSkills: string[];
  matchedExperience: string[];
  matchedEducation: string[];
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
}

export default function Home() {
  const [jobDescription, setJobDescription] = useState("");
  const [userCV, setUserCV] = useState("");
  const [skillsWeight, setSkillsWeight] = useState(30);
  const [experienceWeight, setExperienceWeight] = useState(40);
  const [educationWeight, setEducationWeight] = useState(30);
  const [result, setResult] = useState<ScoreResult | null>(null);
  const [isExpanded, setIsExpanded] = useState(true);
  const [jdFileName, setJdFileName] = useState<string | null>(null);
  const [cvFileName, setCvFileName] = useState<string | null>(null);

  const handleFileUpload = async (
    file: File,
    setContent: (content: string) => void,
    setFileName: (name: string | null) => void,
  ) => {
    if (!file) return;

    try {
      const text = await file.text();
      setContent(text);
      setFileName(file.name);
    } catch (error) {
      alert(
        "Error reading file. Please ensure it is a valid text or PDF file.",
      );
      console.error("File reading error:", error);
    }
  };

  const clearFile = (
    setContent: (content: string) => void,
    setFileName: (name: string | null) => void,
  ) => {
    setContent("");
    setFileName(null);
  };

  const computeScore = async () => {
    if (!jobDescription?.trim() || !userCV?.trim()) {
      alert("Please fill in both Job Description and CV");
      return;
    }

    try {
      const formData = new FormData();
      formData.append(
        "cv_file",
        new Blob([userCV], { type: "text/plain" }),
        cvFileName || "cv.txt",
      );
      formData.append("jd_text", jobDescription);
      formData.append(
        "weights",
        JSON.stringify({
          skills: skillsWeight / 100,
          experience: experienceWeight / 100,
          education: educationWeight / 100,
        }),
      );

      const response = await fetch("http://localhost:8000/evaluate/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      console.log("Backend response:", data);

      if (!response.ok || !data.success) {
        alert(`Backend error: ${data.detail || "Unknown error"}`);
        return;
      }

      const d = data.data;

      setResult({
        score: d.score.total,
        matchedSkills: d.parsed_cv.skills || [],
        matchedExperience: [],
        matchedEducation: [],
        strengths: d.explanation.strengths || [],
        weaknesses: d.explanation.weaknesses || [],
        recommendations: [d.explanation.overall_fit],
      });
    } catch (error) {
      alert("Error connecting to backend. Make sure FastAPI is running.");
      console.error(error);
    }
  };

  const extractKeywords = (text: string) => {
    const skillKeywords = [
      "javascript",
      "typescript",
      "python",
      "react",
      "vue",
      "angular",
      "node",
      "express",
      "sql",
      "database",
      "css",
      "html",
      "git",
      "aws",
      "docker",
      "kubernetes",
      "figma",
      "design",
      "ui",
      "ux",
      "testing",
      "jest",
      "agile",
      "scrum",
      "leadership",
      "communication",
    ];
    const experienceKeywords = [
      "years",
      "years of experience",
      "worked",
      "developed",
      "led",
      "managed",
      "built",
      "created",
      "implemented",
      "designed",
      "deployed",
    ];
    const educationKeywords = [
      "bachelor",
      "master",
      "degree",
      "computer science",
      "engineering",
      "graduation",
      "university",
      "college",
      "certification",
      "bootcamp",
    ];

    const skills = skillKeywords.filter((keyword) => text.includes(keyword));
    const experience = experienceKeywords.filter((keyword) =>
      text.includes(keyword),
    );
    const education = educationKeywords.filter((keyword) =>
      text.includes(keyword),
    );
    const all = [...skills, ...experience, ...education];

    return { skills, experience, education, all };
  };

  const findMatches = (jdTerms: string[], cvTerms: string[]) => {
    return jdTerms.filter((term) =>
      cvTerms.some((cvTerm) => cvTerm.includes(term) || term.includes(cvTerm)),
    );
  };

  const generateStrengths = (
    skills: string[],
    experience: string[],
    education: string[],
  ) => {
    const strengths = [];
    if (skills.length > 0)
      strengths.push(
        `Strong match in technical skills (${skills.slice(0, 3).join(", ")})`,
      );
    if (experience.length > 0)
      strengths.push(
        "Relevant professional experience aligned with role requirements",
      );
    if (education.length > 0)
      strengths.push("Educational background matches job requirements");
    if (skills.length + experience.length + education.length === 0)
      strengths.push("CV demonstrates foundational knowledge");
    return strengths.length > 0
      ? strengths
      : ["Review alignment with job requirements"];
  };

  const generateWeaknesses = (
    jdKeywords: ReturnType<typeof extractKeywords>,
    skills: string[],
    experience: string[],
    education: string[],
  ) => {
    const weaknesses = [];
    const unmatchedSkills = jdKeywords.skills.filter(
      (s) => !skills.includes(s),
    );
    const unmatchedExperience = jdKeywords.experience.filter(
      (e) => !experience.includes(e),
    );
    const unmatchedEducation = jdKeywords.education.filter(
      (e) => !education.includes(e),
    );

    if (unmatchedSkills.length > 0)
      weaknesses.push(
        `Missing skills: ${unmatchedSkills.slice(0, 2).join(", ")}`,
      );
    if (unmatchedExperience.length > 0)
      weaknesses.push("Limited demonstration of required experience level");
    if (unmatchedEducation.length > 0)
      weaknesses.push("Educational credentials may need strengthening");
    return weaknesses.length > 0 ? weaknesses : ["Generally well-matched"];
  };

  const generateRecommendations = (weaknesses: string[]) => {
    const recommendations = [];
    if (weaknesses.some((w) => w.includes("skills"))) {
      recommendations.push(
        "Consider learning the missing technical skills through online courses or certifications",
      );
    }
    if (weaknesses.some((w) => w.includes("experience"))) {
      recommendations.push(
        "Highlight relevant project experience and volunteer work to demonstrate expertise",
      );
    }
    if (weaknesses.some((w) => w.includes("education"))) {
      recommendations.push(
        "Consider pursuing relevant certifications or advanced degrees",
      );
    }
    if (recommendations.length === 0) {
      recommendations.push(
        "Continue developing expertise in your strongest areas",
      );
      recommendations.push(
        "Maintain your technical certifications and stay updated with industry trends",
      );
    }
    return recommendations;
  };

  const getScoreColor = (score: number) => {
    if (score >= 80) return "#d4af37";
    if (score >= 60) return "#888888";
    if (score >= 40) return "#666666";
    return "#444444";
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0a0a] via-[#1a1a1a] to-[#2a2a2a] text-white p-4 md:p-8">
      {/* Header */}
      <div className="max-w-7xl mx-auto mb-12">
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold mb-2 text-white">
            CV <span className="text-accent">Arbiter</span>
          </h1>
          <p className="text-gray-400 text-lg">
            Match your qualifications against job requirements
          </p>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto">
        {/* Two Column Layout */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Left Column - Job Description */}
          <Card className="bg-gradient-to-br from-black to-[#2a2410] border-[#3a3410] hover:border-accent/50 transition-colors">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                <Zap className="w-5 h-5 text-accent" />
                Job Description
              </h2>
              {jobDescription ? (
                <div className="space-y-4">
                  <div className="bg-[#1a1a1a] border border-[#3a3410] rounded-lg p-4">
                    <p className="text-sm text-gray-400 mb-2">
                      File: {jdFileName}
                    </p>
                    <div className="bg-[#0f0f0f] rounded p-3 max-h-80 overflow-y-auto text-sm text-gray-300 whitespace-pre-wrap break-words">
                      {jobDescription}
                    </div>
                  </div>
                  <Button
                    onClick={() => clearFile(setJobDescription, setJdFileName)}
                    variant="outline"
                    className="w-full bg-[#1a1a1a] border-[#3a3410] hover:bg-[#252415] text-white"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Clear File
                  </Button>
                </div>
              ) : (
                <label className="w-full">
                  <input
                    type="file"
                    accept=".pdf,.docx,.doc,.txt"
                    onChange={(e) => {
                      if (e.target.files?.[0]) {
                        handleFileUpload(
                          e.target.files[0],
                          setJobDescription,
                          setJdFileName,
                        );
                      }
                    }}
                    className="hidden"
                  />
                  <div className="w-full min-h-96 bg-[#1a1410] border-2 border-dashed border-[#3a3410] hover:border-accent/50 rounded-lg flex flex-col items-center justify-center cursor-pointer transition-colors">
                    <Upload className="w-12 h-12 text-gray-400 mb-4" />
                    <p className="text-gray-400 text-center px-4">
                      <span className="text-accent font-semibold">
                        Click to upload
                      </span>{" "}
                      or drag and drop
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      PDF, DOCX, TXT up to 10MB
                    </p>
                  </div>
                </label>
              )}
            </div>
          </Card>

          {/* Right Column - CV */}
          <Card className="bg-gradient-to-br from-black to-[#2a2410] border-[#3a3410] hover:border-accent/50 transition-colors">
            <div className="p-6">
              <h2 className="text-xl font-bold mb-4 text-white flex items-center gap-2">
                <Lightbulb className="w-5 h-5 text-accent" />
                Your CV
              </h2>
              {userCV ? (
                <div className="space-y-4">
                  <div className="bg-[#1a1a1a] border border-[#3a3410] rounded-lg p-4">
                    <p className="text-sm text-gray-400 mb-2">
                      File: {cvFileName}
                    </p>
                    <div className="bg-[#0f0f0f] rounded p-3 max-h-80 overflow-y-auto text-sm text-gray-300 whitespace-pre-wrap break-words">
                      {userCV}
                    </div>
                  </div>
                  <Button
                    onClick={() => clearFile(setUserCV, setCvFileName)}
                    variant="outline"
                    className="w-full bg-[#1a1a1a] border-[#3a3410] hover:bg-[#252415] text-white"
                  >
                    <X className="w-4 h-4 mr-2" />
                    Clear File
                  </Button>
                </div>
              ) : (
                <label className="w-full">
                  <input
                    type="file"
                    accept=".pdf,.docx,.doc,.txt"
                    onChange={(e) => {
                      if (e.target.files?.[0]) {
                        handleFileUpload(
                          e.target.files[0],
                          setUserCV,
                          setCvFileName,
                        );
                      }
                    }}
                    className="hidden"
                  />
                  <div className="w-full min-h-96 bg-[#1a1410] border-2 border-dashed border-[#3a3410] hover:border-accent/50 rounded-lg flex flex-col items-center justify-center cursor-pointer transition-colors">
                    <Upload className="w-12 h-12 text-gray-400 mb-4" />
                    <p className="text-gray-400 text-center px-4">
                      <span className="text-accent font-semibold">
                        Click to upload
                      </span>{" "}
                      or drag and drop
                    </p>
                    <p className="text-sm text-gray-500 mt-2">
                      PDF, DOCX, TXT up to 10MB
                    </p>
                  </div>
                </label>
              )}
            </div>
          </Card>
        </div>

        {/* Controls Section */}
        <Card className="bg-gradient-to-br from-black to-[#2a2410] border-[#3a3410] mb-8">
          <div className="p-6">
            <h2 className="text-xl font-bold mb-6 text-white">
              Evaluation Weights
            </h2>

            {/* Skills Weight */}
            <div className="mb-8">
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-semibold text-gray-200">
                  Technical Skills Weight
                </label>
                <span className="text-lg font-bold text-accent">
                  {skillsWeight}%
                </span>
              </div>
              <Slider
                value={[skillsWeight]}
                onValueChange={(val) => setSkillsWeight(val[0])}
                max={100}
                step={1}
                className="w-full"
              />
            </div>

            {/* Experience Weight */}
            <div className="mb-8">
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-semibold text-gray-200">
                  Experience Weight
                </label>
                <span className="text-lg font-bold text-accent">
                  {experienceWeight}%
                </span>
              </div>
              <Slider
                value={[experienceWeight]}
                onValueChange={(val) => setExperienceWeight(val[0])}
                max={100}
                step={1}
                className="w-full"
              />
            </div>

            {/* Education Weight */}
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <label className="text-sm font-semibold text-gray-200">
                  Education Weight
                </label>
                <span className="text-lg font-bold text-accent">
                  {educationWeight}%
                </span>
              </div>
              <Slider
                value={[educationWeight]}
                onValueChange={(val) => setEducationWeight(val[0])}
                max={100}
                step={1}
                className="w-full"
              />
            </div>

            <p className="text-xs text-gray-400 mb-6">
              Total weight: {skillsWeight + experienceWeight + educationWeight}%
            </p>

            {/* Compute Button */}
            <Button
              onClick={computeScore}
              className="w-full bg-accent text-black hover:bg-accent/90 font-bold py-6 text-lg transition-all"
            >
              Compute Score
            </Button>
          </div>
        </Card>

        {/* Results Section */}
        {result && (
          <Card className="bg-gradient-to-br from-black to-[#2a2410] border-accent/30 border-2">
            <div className="p-6">
              {/* Score Display */}
              <div className="mb-8">
                <h2 className="text-2xl font-bold mb-6 text-white">
                  Match Score
                </h2>
                <div className="flex items-center justify-center mb-6">
                  <div className="relative w-48 h-48 rounded-full border-8 border-[#3a3410] flex items-center justify-center bg-[#1a1410]">
                    <div
                      className="absolute w-full h-full rounded-full border-8 border-transparent"
                      style={{
                        borderTopColor: getScoreColor(result.score),
                        borderRightColor: getScoreColor(result.score),
                      }}
                    />
                    <div className="text-center">
                      <div
                        className="text-5xl font-bold"
                        style={{ color: getScoreColor(result.score) }}
                      >
                        {result.score}
                      </div>
                      <div className="text-gray-400">out of 100</div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Collapsible Sections */}
              <div className="space-y-4">
                {/* Strengths */}
                <div className="border border-[#3a3410] rounded-lg overflow-hidden">
                  <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full p-4 bg-[#1a1410] hover:bg-[#252415] flex justify-between items-center text-left transition-colors"
                  >
                    <span className="font-bold text-accent flex items-center gap-2">
                      <Zap className="w-5 h-5" />
                      Strengths
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                  {isExpanded && (
                    <div className="p-4 bg-[#0f0f0f]">
                      <ul className="space-y-2">
                        {result.strengths.map((strength, idx) => (
                          <li key={idx} className="text-green-400 flex gap-2">
                            <span className="text-accent mt-1">✓</span>
                            {strength}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Weaknesses */}
                <div className="border border-[#3a3410] rounded-lg overflow-hidden">
                  <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full p-4 bg-[#1a1410] hover:bg-[#252415] flex justify-between items-center text-left transition-colors"
                  >
                    <span className="font-bold text-red-400 flex items-center gap-2">
                      <AlertCircle className="w-5 h-5" />
                      Weaknesses
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                  {isExpanded && (
                    <div className="p-4 bg-[#0f0f0f]">
                      <ul className="space-y-2">
                        {result.weaknesses.map((weakness, idx) => (
                          <li key={idx} className="text-red-300 flex gap-2">
                            <span className="text-red-400 mt-1">•</span>
                            {weakness}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>

                {/* Recommendations */}
                <div className="border border-[#3a3410] rounded-lg overflow-hidden">
                  <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full p-4 bg-[#1a1410] hover:bg-[#252415] flex justify-between items-center text-left transition-colors"
                  >
                    <span className="font-bold text-blue-400 flex items-center gap-2">
                      <Lightbulb className="w-5 h-5" />
                      Recommendations
                    </span>
                    {isExpanded ? (
                      <ChevronUp className="w-5 h-5" />
                    ) : (
                      <ChevronDown className="w-5 h-5" />
                    )}
                  </button>
                  {isExpanded && (
                    <div className="p-4 bg-[#0f0f0f]">
                      <ul className="space-y-2">
                        {result.recommendations.map((rec, idx) => (
                          <li key={idx} className="text-blue-300 flex gap-2">
                            <span className="text-accent mt-1">→</span>
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
