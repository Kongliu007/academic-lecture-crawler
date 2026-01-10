from bs4 import BeautifulSoup
from common.fetch import fetch
from common.time_utils import is_today_or_future
from common.save import save_json
from urllib.parse import urljoin
import os

BASE_DOMAIN = "https://www.phy.pku.edu.cn"

# 各页面 URL 对应的类型名称
LECTURE_PAGES = {
    "物院论坛": "https://www.phy.pku.edu.cn/xshd/wylt.htm",
    "百年物理讲堂": "https://www.phy.pku.edu.cn/xshd/bnwljt.htm",
    "物理之美": "https://www.phy.pku.edu.cn/xshd/wlzm.htm",
    "博士后科学沙龙": "https://www.phy.pku.edu.cn/xshd/bshkxsl.htm",
    "学术报告-学院": "https://www.phy.pku.edu.cn/xshd/xsbg1/xy.htm",
    "学术报告-理论物理": "https://www.phy.pku.edu.cn/xshd/xsbg1/llwl1.htm",
    "学术报告-凝聚态": "https://www.phy.pku.edu.cn/xshd/xsbg1/njt1.htm",
    "学术报告-光学": "https://www.phy.pku.edu.cn/xshd/xsbg1/gx1.htm",
    "学术报告-重离子": "https://www.phy.pku.edu.cn/xshd/xsbg1/zlz1.htm",
    "学术报告-技术物理": "https://www.phy.pku.edu.cn/xshd/xsbg1/jswl1.htm",
    "学术报告-天文": "https://www.phy.pku.edu.cn/xshd/xsbg1/tw1.htm",
    "学术报告-大气海洋": "https://www.phy.pku.edu.cn/xshd/xsbg1/dqhy.htm",
    "学术报告-量子材料": "https://www.phy.pku.edu.cn/xshd/xsbg1/lzcl.htm",
    "学术报告-电镜实验室": "https://www.phy.pku.edu.cn/xshd/xsbg1/djsys.htm",
    "学术会议": "https://www.phy.pku.edu.cn/xshd/xshy.htm",
}

def parse_lecture_li(li, lecture_type):
    """解析单条 li，返回字典"""
    a_tag = li.select_one("a")
    if not a_tag:
        return None

    title = a_tag.get_text(strip=True)
    link = urljoin(BASE_DOMAIN, a_tag.get("href"))

    speaker_tag = li.select_one("p.caleander-info")
    speaker = speaker_tag.get_text(strip=True).replace("主讲人：", "") if speaker_tag else ""

    info_tags = li.select("p.caleander-info span")
    lecture_time = info_tags[0].get_text(strip=True).replace("时间：", "") if len(info_tags) > 0 else ""
    location = info_tags[1].get_text(strip=True).replace("地点：", "") if len(info_tags) > 1 else ""

    # 只抓今天及未来
    if lecture_time and is_today_or_future(lecture_time):
        return {
            "school": "pku",
            "subject": "physics",
            "type": lecture_type,
            "title": title,
            "speaker": speaker,
            "time": lecture_time,
            "location": location,
            "link": link
        }
    return None

def crawl_page(url, lecture_type):
    """爬取单个页面"""
    html = fetch(url)
    soup = BeautifulSoup(html, "lxml")
    lectures = []

    # 尝试抓 li
    for li in soup.select("ul.news-list.caleander-list li"):
        lecture = parse_lecture_li(li, lecture_type)
        if lecture:
            lectures.append(lecture)
    return lectures

def fetch_pku_physics():
    """抓取北大物理讲座"""
    all_lectures = []
    for lecture_type, url in LECTURE_PAGES.items():
        try:
            lectures = crawl_page(url, lecture_type)
            all_lectures.extend(lectures)
            print(f"{lecture_type}: {len(lectures)} lectures found")
        except Exception as e:
            print(f"Error crawling {lecture_type} ({url}): {e}")

    # 确保保存目录存在
    save_path = "data/pku"
    os.makedirs(save_path, exist_ok=True)
    save_json(all_lectures, os.path.join(save_path, "physics.json"))
    print(f"Total lectures saved: {len(all_lectures)}")
