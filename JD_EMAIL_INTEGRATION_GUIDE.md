# Hướng dẫn tích hợp: JD Generation & Email Generation

> Tài liệu này dành cho FE để tích hợp 2 tính năng mới: **Tạo Mô tả Công việc (JD)** và **Soạn Email ứng viên**.
> Cả hai endpoint đều đã có sẵn implementation mẫu trong `GenerateJDTab.tsx` và `RankTab.tsx` (nhánh hiện tại) — coi đó là tài liệu tham khảo song song với guide này.

---

## 1. Tổng quan

| Tính năng | Endpoint | Method | Phụ thuộc session? |
|---|---|---|---|
| Tạo JD | `/jd/generate` | POST | Không |
| Soạn email | `/email/session/{session_id}/candidate/{candidate_id}` | POST | Có — cần session Rank đã tồn tại |

Base URL (dev): `http://localhost:8000`

Cả hai endpoint đều gọi LLM cục bộ (Qwen3 4B qua Ollama) nên **độ trễ phản hồi thường 5–20 giây**. Luôn hiển thị loading state, không để UI trông như bị treo.

---

## 2. JD Generation — `POST /jd/generate`

### Mục đích
HR điền form có cấu trúc → AI viết thành một bản JD hoàn chỉnh, có đoạn giới thiệu hấp dẫn, không phải chỉ là chép lại ghi chú của HR.

### Request

Content-Type: **`application/json`** (KHÔNG phải FormData — khác với `/evaluate/` và `/rank/session`)

```ts
interface JDGenerateRequest {
  title: string;                    // BẮT BUỘC — các field còn lại optional, để "" hoặc [] nếu không có
  company: string;
  location: string;
  work_type: string;
  required_skills: string[];        // mảng string, KHÔNG phải chuỗi phân cách bởi dấu phẩy
  preferred_skills: string[];
  experience_required: string;
  education_required: string;
  responsibilities: string;         // ghi chú thô của HR, có thể là câu ngắn gọn không hoàn chỉnh
  perks: string;                    // ghi chú thô của HR
}
```

Nếu form input là text field phân cách bằng dấu phẩy (vd: "Python, FastAPI, Docker"), nhớ `.split(",").map(s => s.trim()).filter(Boolean)` trước khi gửi.

### Response

```ts
interface JDGenerateResponse {
  success: boolean;
  data: {
    title: string;
    full_text: string;              // toàn bộ JD, có \n để xuống dòng — render với white-space: pre-wrap
    required_skills: string[];
    preferred_skills: string[];
    experience_required: string;
    education_required: string;
  };
}
```

**Lưu ý quan trọng:** `full_text` đã được backend đảm bảo luôn xuất hiện kỹ năng ưu tiên trong nội dung (server tự kiểm tra và bổ sung nếu LLM bỏ sót). Vẫn nên defensive-code phía FE — xem mục 4.

### Ví dụ fetch

```ts
const resp = await fetch(`${BACKEND_URL}/jd/generate`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title: "Kỹ sư Dữ liệu",
    company: "FinTech ABC",
    location: "TP.HCM",
    work_type: "Hybrid 3 ngày/tuần",
    required_skills: ["Python", "SQL", "Airflow"],
    preferred_skills: ["Kafka", "dbt"],
    experience_required: "Hơn 2 năm kinh nghiệm",
    education_required: "Cử nhân CNTT hoặc liên quan",
    responsibilities: "xây dựng ETL pipeline, làm việc với data warehouse",
    perks: "lương 30-45tr, bảo hiểm sức khỏe, WFH 2 ngày/tuần",
  }),
});
const { data } = await resp.json();
```

### Hành vi sau khi tạo

Theo quyết định sản phẩm hiện tại: **chỉ hiển thị + cho phép copy, KHÔNG auto-fill vào ô JD ở tab Rank.** HR tự copy-paste thủ công nếu muốn dùng JD này để tạo ranking session.

---

## 3. Email Generation — `POST /email/session/{session_id}/candidate/{candidate_id}`

### Mục đích
Soạn email mời phỏng vấn hoặc từ chối, dựa trên kết quả đánh giá của một ứng viên cụ thể trong một session Rank đã tồn tại.

### Điều kiện tiên quyết
- Phải có `session_id` hợp lệ (từ `POST /rank/session`)
- Phải có `candidate_id` hợp lệ (từ `POST /rank/session/{id}/cv`)
- Candidate đó nên đã được "explain" trước đó (gọi `POST /rank/session/{id}/explain/{candidate_id}`) — không bắt buộc về mặt kỹ thuật, nhưng UI hiện tại đặt nút soạn email bên trong panel giải thích (explanation panel), tức là user phải click vào candidate trước.

### Request

Content-Type: `application/json`

```ts
interface EmailGenerateRequest {
  email_type: "invite" | "reject";  // BẮT BUỘC — chỉ 2 giá trị này
  company_name?: string;            // optional, mặc định rỗng
  sender_name?: string;             // optional, mặc định "Bộ phận Tuyển dụng"
  interview_details?: string;       // optional — CHỈ áp dụng cho "invite", bỏ qua nếu "reject"
}
```

### Response

```ts
interface EmailGenerateResponse {
  success: boolean;
  data: {
    subject: string;
    body: string;                   // văn bản thuần (plain text), đã được strip markdown — render với white-space: pre-wrap
    type: "invite" | "reject";      // LUÔN khớp với email_type đã gửi — backend đảm bảo, không cần validate
  };
}
```

### Ví dụ fetch

```ts
const resp = await fetch(
  `${BACKEND_URL}/email/session/${sessionId}/candidate/${candidateId}`,
  {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      email_type: "invite",
      company_name: "TechViet Solutions",
      sender_name: "Phòng Nhân sự",
      interview_details: "10:00 sáng, Thứ Năm ngày 25/06, văn phòng Hà Nội",
    }),
  }
);
const { data } = await resp.json();
// data.subject, data.body, data.type
```

### ⚠️ Quan trọng — Human-in-the-loop

Đây là **bản nháp**, không bao giờ tự động gửi đi. UI phải:
- Luôn hiển thị rõ ràng đây là draft (vd: badge "EMAIL NHÁP")
- Có cảnh báo nhắc người dùng kiểm tra trước khi gửi
- Cung cấp nút Copy để HR tự paste vào email client của họ — không có tính năng "Send" trực tiếp trong scope hiện tại

### Email từ chối (reject) không chứa thông tin điểm yếu cụ thể

Đây là chủ đích thiết kế, không phải bug: backend cố tình **không đưa `weaknesses` vào prompt** khi soạn email reject, để tránh AI vô tình tiết lộ lý do từ chối chi tiết có thể gây tổn thương hoặc rủi ro pháp lý. Email reject sẽ luôn chung chung kiểu "công ty đã chọn ứng viên khác phù hợp hơn". Đừng cố hiển thị thêm lý do chi tiết ở FE cho loại email này.

---

## 4. Defensive coding phía FE (khuyến nghị)

Dù backend đã có validation/normalization, vẫn nên defensive ở FE vì model AI đôi khi không ổn định:

```ts
// Khi set state từ response, luôn có fallback:
setResult({
  title: data.data?.title || fallbackTitle,
  full_text: data.data?.full_text || "(Không có nội dung — vui lòng thử lại)",
  required_skills: Array.isArray(data.data?.required_skills) ? data.data.required_skills : [],
  preferred_skills: Array.isArray(data.data?.preferred_skills) ? data.data.preferred_skills : [],
  // ...
});
```

Không bao giờ gọi `.map()` trực tiếp trên field có thể `undefined` — luôn bọc `(arr || []).map(...)`.

---

## 5. Lỗi thường gặp & xử lý

| Tình huống | HTTP Status | Cách xử lý FE |
|---|---|---|
| Thiếu `title` khi tạo JD | 422 (Pydantic validation) | Validate phía FE trước khi gửi — `title` không được rỗng |
| `session_id` không tồn tại | 404 | Hiển thị "Session not found" — có thể do server đã restart (session lưu in-memory) |
| `candidate_id` không tồn tại | 404 | Hiển thị lỗi, gợi ý refresh leaderboard |
| `email_type` không phải "invite"/"reject" | 400 | Validate phía FE — chỉ cho phép 2 giá trị |
| LLM timeout / lỗi sinh JSON | 500 | Backend đã tự retry 1 lần trước khi trả lỗi — nếu vẫn lỗi, hiển thị "Vui lòng thử lại" và cho phép user bấm lại nút |

**Lưu ý:** session lưu in-memory, mất khi backend restart. Nếu FE thấy lỗi 404 cho session vừa tạo cách đây không lâu, khả năng cao là backend đã restart (vd: do `--reload` trong lúc dev). Không phải bug FE.

---

## 6. UI/UX đã thống nhất (tham khảo nhánh hiện tại)

- **JD Generation**: tab riêng thứ 3 ("Generate JD"), 2 cột — form bên trái, kết quả + nút Copy bên phải
- **Email Generation**: không phải trang riêng — nằm trong panel giải thích (explanation panel) của từng candidate ở tab Rank, dưới dạng 2 nút "Mời phỏng vấn" / "Từ chối", kết quả hiện ngay bên dưới trong khung có viền vàng + cảnh báo draft

Nếu thiết kế FE khác đi, vẫn giữ nguyên 2 nguyên tắc cốt lõi: (1) JD chỉ copy thủ công, không auto-fill, (2) Email luôn là draft, có cảnh báo, có nút copy, không có nút gửi tự động.
