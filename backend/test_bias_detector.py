import asyncio
from services.bias_detector import detect_bias

async def test():
    jd = """
    Chúng tôi đang tìm kiếm một "siêu nhân" lập trình trẻ trung, năng động.
    Ứng viên phải có hơn 10 năm kinh nghiệm với React (ra mắt năm 2013).
    Anh ấy cần có khả năng làm việc dưới áp lực cao trong môi trường startup.
    Bắt buộc có bằng Thạc sĩ Khoa học Máy tính.
    Ưu tiên người nói tiếng Anh như tiếng mẹ đẻ.
    Độ tuổi từ 22 đến 30.
    """

    result = await detect_bias(jd)
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))

asyncio.run(test())