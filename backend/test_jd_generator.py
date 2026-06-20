import asyncio
from services.jd_generator import generate_jd

async def test():
    fields = {
        "title": "Lập trình viên Backend Python",
        "company": "TechViet Solutions",
        "location": "Hà Nội",
        "work_type": "Toàn thời gian, làm việc tại văn phòng (hybrid 2 ngày/tuần)",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "REST APIs", "Git"],
        "preferred_skills": ["Docker", "Redis", "AWS", "CI/CD"],
        "experience_required": "Hơn 3 năm kinh nghiệm phát triển backend",
        "education_required": "Cử nhân Khoa học Máy tính hoặc ngành liên quan",
        "responsibilities": (
            "thiết kế API, làm việc với DB, tối ưu performance, "
            "code review, mentor junior, họp với PM hàng tuần"
        ),
        "perks": (
            "lương 25-35tr, thưởng tháng 13, bảo hiểm sức khỏe cao cấp, "
            "20 ngày nghỉ phép, laptop công ty cấp, du lịch công ty hàng năm"
        ),
    }

    result = await generate_jd(fields)

    import json
    print("=== RAW RESULT (for debugging) ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print()

    print("=== TITLE ===")
    print(result.get("title"))
    print("\n=== FULL TEXT ===")
    print(result.get("full_text"))
    print("\n=== REQUIRED SKILLS ===")
    print(result.get("required_skills"))
    print("\n=== PREFERRED SKILLS ===")
    print(result.get("preferred_skills"))
    print("\n=== EXPERIENCE REQUIRED ===")
    print(result.get("experience_required"))
    print("\n=== EDUCATION REQUIRED ===")
    print(result.get("education_required"))

asyncio.run(test())