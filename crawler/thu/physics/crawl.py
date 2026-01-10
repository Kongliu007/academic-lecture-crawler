from bs4 import BeautifulSoup
from common.fetch import fetch
from common.time_utils import is_today_or_future
from common.save import save_json
from urllib.parse import urljoin
import os
import re

BASE_DOMAIN = "https://www.phys.tsinghua.edu.cn"

# 各页面 URL 对应类型名称
LECTURE_PAGES = {
    "物理系讲座": "https://www.phys.tsinghua.edu.cn/xwyhd/xshd.htm",
    # 如果后续有更多分类页面可以加在这里
}

def parse_lecture_li(li, lecture_type):
    """解析单条 li，返回字典"""
    # 日期
    date_div = li.select_one("div.lb-ul-date")
    if not date_div:
        return None
    year_month_match = re.search(r"(\d{4}-\d{2})", date_div.get_text(strip=True))
    day_tag = date_div.find("span")
    day = day_tag.get_text(strip=True) if day_tag else "01"
    lecture_time_str = f"{year_month_match.group(1)}-{day}" if year_month_match else None

    # 只抓今天及未来
    if not lecture_time_str or not is_today_or_future(lecture_time_str):
        return None

    # 标题和链接
    title_tag = li.select_one("div.lb-ul-tt a")
    title = title_tag.get_text(strip=True) if title_tag else ""
    link = urljoin(BASE_DOMAIN, title_tag.get("href")) if title_tag else ""

    # 详情文本
    detail_ul = li.select_one("ul.lb-ul-p")
    detail_text = detail_ul.get_text(strip=True) if detail_ul else ""

    # 提取报告人、具体时间、地点
    speaker_match = re.search(r"报\s*告\s*人[:：]([\u4e00-\u9fa5a-zA-Z0-9\s,.-]+)", detail_text)
    speaker = speaker_match.group(1).strip() if speaker_match else ""

    time_match = re.search(r"报告时间[:：]([\d年月日()：: \-]+)", detail_text)
    lecture_time = time_match.group(1).strip() if time_match else lecture_time_str

    location_match = re.search(r"报告地点[:：]([\u4e00-\u9fa5A-Za-z0-9\s]+)", detail_text)
    location = location_match.group(1).strip() if location_match else ""

    return {
        "school": "thu",
        "subject": "physics",
        "type": lecture_type,
        "title": title,
        "speaker": speaker,
        "time": lecture_time,
        "location": location,
        "link": link
    }

def crawl_page(url, lecture_type):
    """爬取单个页面"""
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    lectures = []

    for li in soup.select("ul.lb-ul li"):
        lecture = parse_lecture_li(li, lecture_type)
        if lecture:
            lectures.append(lecture)
    return lectures

def fetch_thu_physics():
    """抓取清华物理讲座"""
    all_lectures = []
    for lecture_type, url in LECTURE_PAGES.items():
        try:
            lectures = crawl_page(url, lecture_type)
            all_lectures.extend(lectures)
            print(f"{lecture_type}: {len(lectures)} lectures found")
        except Exception as e:
            print(f"Error crawling {lecture_type} ({url}): {e}")

    # 确保保存目录存在
    save_path = "data/thu"
    os.makedirs(save_path, exist_ok=True)
    save_json(all_lectures, os.path.join(save_path, "physics.json"))
    print(f"Total lectures saved: {len(all_lectures)}")
