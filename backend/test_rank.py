import asyncio
import httpx

BASE = "http://localhost:8000"

JD = """
Chúng tôi đang tìm kiếm Lập trình viên Backend Python với hơn 3 năm kinh nghiệm.
Kỹ năng bắt buộc: Python, FastAPI, PostgreSQL.
Kỹ năng ưu tiên: Docker, Redis, AWS.
Học vấn: Cử nhân Khoa học Máy tính hoặc ngành liên quan.
Mô tả: Xây dựng và duy trì các API RESTful, tối ưu hóa cơ sở dữ liệu,
phối hợp với nhóm frontend để phát triển sản phẩm.
"""

CVS = [
    ("Nguyễn Thị Lan", """
    Nguyễn Thị Lan. Kỹ năng: Python, FastAPI, PostgreSQL, Git, Docker.
    Kinh nghiệm: Lập trình viên Backend tại Công ty ABC (3 năm) - Xây dựng API RESTful.
    Học vấn: Cử nhân Khoa học Máy tính, Đại học Bách Khoa Hà Nội, 2021.
    """),
    ("Trần Văn Bình", """
    Trần Văn Bình. Kỹ năng: Java, Spring Boot, MySQL.
    Kinh nghiệm: Kỹ sư phần mềm tại Tập đoàn XYZ (2 năm) - Xây dựng microservices.
    Học vấn: Cử nhân Công nghệ Thông tin, Đại học Khoa học Tự nhiên TP.HCM, 2022.
    """),
    ("Lê Thị Châu", """
    Lê Thị Châu. Kỹ năng: Python, Django, PostgreSQL, Redis, AWS.
    Kinh nghiệm: Lập trình viên Full Stack tại Startup DEF (4 năm) - Phát triển ứng dụng web.
    Học vấn: Cử nhân Kỹ thuật Phần mềm, Đại học Đà Nẵng, 2020.
    """),
]

async def test():
    async with httpx.AsyncClient(timeout=120) as client:
        # 1. Tạo phiên làm việc
        resp = await client.post(f"{BASE}/rank/session", data={"jd_text": JD})
        session_id = resp.json()["session_id"]
        print(f"Phiên tạo thành công: {session_id}")

        # 2. Tải lên CV
        for name, cv_text in CVS:
            files = {"cv_file": (f"{name}.txt", cv_text.encode("utf-8"), "text/plain")}
            resp = await client.post(f"{BASE}/rank/session/{session_id}/cv", files=files)
            print(f"Đã tải lên: {resp.json()['name']}")

        # 3. Lấy bảng xếp hạng
        resp = await client.get(f"{BASE}/rank/session/{session_id}/rank")
        leaderboard = resp.json()["leaderboard"]
        print("\nBảng xếp hạng:")
        for c in leaderboard:
            print(f"  #{c['rank']} {c['name']}: {c['score']['total']}%")

asyncio.run(test())