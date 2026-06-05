import asyncio
from services.agent import run_pipeline

async def test():
    jd = """
    Chúng tôi đang tìm kiếm Lập trình viên Backend Python với hơn 3 năm kinh nghiệm.
    Kỹ năng bắt buộc: Python, FastAPI, PostgreSQL.
    Kỹ năng ưu tiên: Docker, Redis, AWS.
    Học vấn: Cử nhân Khoa học Máy tính hoặc ngành liên quan.
    Mô tả: Xây dựng và duy trì các API RESTful, tối ưu hóa cơ sở dữ liệu,
    phối hợp với nhóm frontend để phát triển sản phẩm.
    """

    cv_text = """
    Nguyễn Thị Lan
    Lập trình viên Backend với 3 năm kinh nghiệm.
    Kỹ năng: Python, FastAPI, PostgreSQL, Git
    Kinh nghiệm: Lập trình viên Backend tại Công ty ABC (3 năm) - Xây dựng API RESTful và microservices.
    Học vấn: Cử nhân Khoa học Máy tính, Đại học Bách Khoa Hà Nội, 2021.
    """

    result = await run_pipeline(cv_text.encode(), "lan.txt", jd)

    print(f"Ứng viên: {result['candidate']}")
    print(f"Điểm tổng: {result['score']['total']}%")
    print(f"Chi tiết: {result['score']['breakdown']}")
    print(f"Đề xuất: {result['explanation']['recommendation']}")
    print(f"Điểm thiên kiến JD: {result['bias_report']['bias_score']}")
    print(f"Cảnh báo agent: {result['agent_flags']}")

asyncio.run(test())