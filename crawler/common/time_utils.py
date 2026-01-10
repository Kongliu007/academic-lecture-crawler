from datetime import datetime

def is_today_or_future(date_str: str) -> bool:
    """
    判断北大物理讲座时间是否为今天或未来
    支持格式：
    '2026年1月9日（星期五）15:00—16:00'
    """
    try:
        # 只取年月日部分
        date_part = date_str.split("（")[0].split(" ")[0].replace("年", "-").replace("月", "-").replace("日", "")
        lecture_date = datetime.strptime(date_part, "%Y-%m-%d").date()
        return lecture_date >= datetime.today().date()
    except Exception:
        # 出错默认返回 False
        return False
