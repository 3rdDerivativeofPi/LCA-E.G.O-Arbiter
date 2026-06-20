import asyncio
from services.email_generator import generate_email

CV = {
    "name": "Nguyễn Thị Lan",
    "summary": "Lập trình viên Backend với 3 năm kinh nghiệm xây dựng REST APIs và microservices.",
    "skills": ["Python", "FastAPI", "PostgreSQL", "Git", "Docker"],
    "experience": [{
        "title": "Lập trình viên Backend",
        "company": "Công ty ABC",
        "duration": "3 năm",
        "description": "Xây dựng API RESTful và microservices"
    }],
    "education": [{
        "degree": "Cử nhân Khoa học Máy tính",
        "institution": "Đại học Bách Khoa Hà Nội",
        "year": "2021"
    }],
}

JD = {
    "title": "Lập trình viên Backend Python",
    "required_skills": ["Python", "FastAPI", "PostgreSQL"],
    "preferred_skills": ["Docker", "Redis"],
    "experience_required": "Hơn 3 năm kinh nghiệm",
    "education_required": "Cử nhân Khoa học Máy tính",
}

SCORE = {
    "total": 88.5,
    "breakdown": {"skills": 92.4, "experience": 85.8, "education": 80.0},
}

EXPLANATION = {
    "strengths": [
        "Kinh nghiệm trực tiếp với đúng bộ công nghệ yêu cầu (Python, FastAPI, PostgreSQL)",
        "Đã có kinh nghiệm triển khai dịch vụ bằng Docker",
        "Nền tảng học vấn phù hợp với vị trí",
    ],
    "weaknesses": [
        "Chưa thể hiện kinh nghiệm với Redis hoặc AWS",
        "Số năm kinh nghiệm ở mức tối thiểu yêu cầu",
    ],
    "overall_fit": "Ứng viên phù hợp tốt với vị trí, đáp ứng đầy đủ các yêu cầu cốt lõi.",
    "recommendation": "Rất phù hợp",
}


async def test_invite():
    print("=" * 50)
    print("EMAIL MỜI PHỎNG VẤN")
    print("=" * 50)
    result = await generate_email(
        email_type="invite",
        cv=CV,
        jd=JD,
        score=SCORE,
        explanation=EXPLANATION,
        company_name="TechViet Solutions",
        sender_name="Phòng Nhân sự",
        interview_details="10:00 sáng, Thứ Năm ngày 25/06/2026, tại văn phòng Hà Nội (hoặc qua Google Meet nếu cần)",
    )
    print(f"\nSubject: {result.get('subject')}")
    print(f"\nBody:\n{result.get('body')}")
    print(f"\nType: {result.get('type')}")


async def test_reject():
    print("\n" + "=" * 50)
    print("EMAIL TỪ CHỐI")
    print("=" * 50)
    result = await generate_email(
        email_type="reject",
        cv=CV,
        jd=JD,
        score=SCORE,
        explanation=EXPLANATION,
        company_name="TechViet Solutions",
        sender_name="Phòng Nhân sự",
    )
    print(f"\nSubject: {result.get('subject')}")
    print(f"\nBody:\n{result.get('body')}")
    print(f"\nType: {result.get('type')}")

    # Sanity check: reject email should not leak specific weaknesses
    body_lower = result.get("body", "").lower()
    leaked_terms = ["redis", "aws", "tối thiểu"]
    leaks = [t for t in leaked_terms if t in body_lower]
    if leaks:
        print(f"\n⚠️  WARNING: reject email may have leaked weakness details: {leaks}")
    else:
        print("\n✓ No specific weakness details leaked into reject email.")


async def main():
    await test_invite()
    await test_reject()

asyncio.run(main())