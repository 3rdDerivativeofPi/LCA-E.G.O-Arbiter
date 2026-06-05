import asyncio
from services.parser import parse_jd

async def test():
    jd = """
    Chúng tôi đang tìm kiếm Lập trình viên Backend Python với hơn 3 năm kinh nghiệm.
    Kỹ năng bắt buộc: Python, FastAPI, PostgreSQL.
    Kỹ năng ưu tiên: Docker, Redis, AWS.
    Học vấn: Cử nhân Khoa học Máy tính hoặc ngành liên quan.
    Mô tả công việc: Xây dựng và duy trì các API RESTful, tối ưu hóa hiệu suất hệ thống,
    phối hợp với nhóm frontend và DevOps để triển khai sản phẩm.
    """
    result = await parse_jd(jd)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(test())