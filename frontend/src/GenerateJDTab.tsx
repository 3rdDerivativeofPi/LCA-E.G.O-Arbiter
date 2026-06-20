import { useState } from "react";
import { FileText, Copy, Check } from "lucide-react";

const BACKEND_URL = "http://localhost:8000";

interface JDResult {
  title: string;
  full_text: string;
  required_skills: string[];
  preferred_skills: string[];
  experience_required: string;
  education_required: string;
}

const emptyForm = {
  title: "",
  company: "",
  location: "",
  work_type: "",
  required_skills: "",
  preferred_skills: "",
  experience_required: "",
  education_required: "",
  responsibilities: "",
  perks: "",
};

export default function GenerateJDTab() {
  const [form, setForm] = useState(emptyForm);
  const [result, setResult] = useState<JDResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const update = (key: keyof typeof form, value: string) =>
    setForm(prev => ({ ...prev, [key]: value }));

  const splitList = (s: string) =>
    s.split(",").map(x => x.trim()).filter(Boolean);

  const generate = async () => {
    if (!form.title.trim()) {
      alert("Vui lòng nhập tên vị trí.");
      return;
    }
    setIsLoading(true);
    setResult(null);
    setCopied(false);
    try {
      const payload = {
        title: form.title,
        company: form.company,
        location: form.location,
        work_type: form.work_type,
        required_skills: splitList(form.required_skills),
        preferred_skills: splitList(form.preferred_skills),
        experience_required: form.experience_required,
        education_required: form.education_required,
        responsibilities: form.responsibilities,
        perks: form.perks,
      };

      const resp = await fetch(`${BACKEND_URL}/jd/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!resp.ok) throw new Error("Generation failed");
      const data = await resp.json();
      const d = data.data || {};

      // Defensive defaults — backend LLM output can occasionally drop or rename fields
      setResult({
        title: d.title || form.title,
        full_text: d.full_text || "(Không có nội dung — vui lòng thử lại)",
        required_skills: Array.isArray(d.required_skills) ? d.required_skills : [],
        preferred_skills: Array.isArray(d.preferred_skills) ? d.preferred_skills : [],
        experience_required: d.experience_required || "",
        education_required: d.education_required || "",
      });
    } catch (err) {
      alert("Lỗi kết nối. Vui lòng kiểm tra backend đang chạy tại :8000");
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async () => {
    if (!result) return;
    try {
      await navigator.clipboard.writeText(result.full_text);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      alert("Không thể sao chép. Vui lòng chọn và sao chép thủ công.");
    }
  };

  return (
    <div className="grid-2">
      {/* Left panel — form */}
      <div className="flex-col">
        <div className="card">
          <div className="label">📋 Thông tin cơ bản</div>
          <input
            className="input"
            placeholder="Tên vị trí (bắt buộc) — vd: Lập trình viên Backend Python"
            value={form.title}
            onChange={e => update("title", e.target.value)}
          />
          <input
            className="input"
            placeholder="Tên công ty"
            value={form.company}
            onChange={e => update("company", e.target.value)}
          />
          <input
            className="input"
            placeholder="Địa điểm — vd: Hà Nội"
            value={form.location}
            onChange={e => update("location", e.target.value)}
          />
          <input
            className="input"
            placeholder="Hình thức làm việc — vd: Toàn thời gian, hybrid 2 ngày/tuần"
            value={form.work_type}
            onChange={e => update("work_type", e.target.value)}
          />
        </div>

        <div className="card">
          <div className="label">🛠️ Kỹ năng</div>
          <input
            className="input"
            placeholder="Kỹ năng bắt buộc (phân cách bằng dấu phẩy)"
            value={form.required_skills}
            onChange={e => update("required_skills", e.target.value)}
          />
          <input
            className="input"
            placeholder="Kỹ năng ưu tiên (phân cách bằng dấu phẩy)"
            value={form.preferred_skills}
            onChange={e => update("preferred_skills", e.target.value)}
          />
        </div>

        <div className="card">
          <div className="label">🎓 Kinh nghiệm & Học vấn</div>
          <input
            className="input"
            placeholder="Kinh nghiệm yêu cầu — vd: Hơn 3 năm kinh nghiệm"
            value={form.experience_required}
            onChange={e => update("experience_required", e.target.value)}
          />
          <input
            className="input"
            placeholder="Học vấn yêu cầu — vd: Cử nhân Khoa học Máy tính"
            value={form.education_required}
            onChange={e => update("education_required", e.target.value)}
          />
        </div>

        <div className="card">
          <div className="label">📝 Trách nhiệm & Quyền lợi</div>
          <textarea
            className="textarea"
            placeholder="Ghi chú về trách nhiệm công việc (có thể viết ngắn gọn, AI sẽ diễn đạt lại)"
            value={form.responsibilities}
            onChange={e => update("responsibilities", e.target.value)}
          />
          <textarea
            className="textarea"
            placeholder="Ghi chú về quyền lợi/phúc lợi (có thể viết ngắn gọn, AI sẽ diễn đạt lại)"
            value={form.perks}
            onChange={e => update("perks", e.target.value)}
          />
        </div>

        <button className="btn" onClick={generate} disabled={isLoading || !form.title.trim()}>
          {isLoading ? "🔄 ĐANG TẠO JD..." : "▶ TẠO MÔ TẢ CÔNG VIỆC"}
        </button>
      </div>

      {/* Right panel — result */}
      <div className="card">
        {!result ? (
          <div className="empty-state">
            <FileText size={48} style={{ marginBottom: "16px", opacity: 0.3 }} />
            <p>Mô tả công việc sẽ hiển thị ở đây...</p>
          </div>
        ) : (
          <div>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "16px" }}>
              <div className="label label-gold" style={{ marginBottom: 0 }}>📄 {result.title}</div>
              <button className="btn-outline" onClick={copyToClipboard}>
                {copied ? (
                  <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <Check size={14} /> Đã sao chép
                  </span>
                ) : (
                  <span style={{ display: "flex", alignItems: "center", gap: "6px" }}>
                    <Copy size={14} /> Sao chép
                  </span>
                )}
              </button>
            </div>

            <div className="card-dark mb-16" style={{ whiteSpace: "pre-wrap", lineHeight: 1.6, fontSize: "14px" }}>
              {result.full_text}
            </div>

            <div className="grid-equal">
              <div>
                <div className="label label-green">Kỹ năng bắt buộc</div>
                <div className="list-green">
                  {(result.required_skills || []).map((s, i) => <div key={i} className="list-item">{s}</div>)}
                </div>
              </div>
              <div>
                <div className="label label-gold">Kỹ năng ưu tiên</div>
                <div className="card-dark">
                  {(result.preferred_skills || []).map((s, i) => <div key={i} className="list-item">{s}</div>)}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}