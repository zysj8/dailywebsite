import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

# 目标网站
BASE_URL = "https://www.yudou789.top"
# 今天的日期字符串，格式 YYYYMMDD
today_str = datetime.now().strftime("%Y%m%d")
# 今天的日期中文格式，用于匹配标题（例如 "2026年05月14日"）
today_cn = datetime.now().strftime("%Y年%m月%d日")

def get_latest_post_url():
    """获取今天发布的第一篇文章链接"""
    # 这里简化处理，先直接访问已知的今天文章链接
    # 实际你可以先爬取首页，找到标题含 today_cn 的文章链接
    return f"{BASE_URL}/885.html"  # 示例：你可以改成动态获取

def extract_txt_link(post_url):
    """从文章源码中提取含 today_str 的 .txt 链接"""
    try:
        resp = requests.get(post_url, timeout=10)
        resp.raise_for_status()
        html = resp.text

        # 正则匹配：http/https开头，包含 today_str，以 .txt 结尾的链接
        pattern = re.compile(r'https?://[^\s"]+?' + re.escape(today_str) + r'[^\s"]*?\.txt', re.IGNORECASE)
        matches = pattern.findall(html)

        if matches:
            return matches[0]  # 返回第一个匹配到的链接
        else:
            return None
    except Exception as e:
        print(f"爬取出错: {e}")
        return None

def generate_html(link):
    """生成展示链接的静态页面"""
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>今日节点链接</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; }}
        .link {{ font-size: 18px; color: #007bff; word-break: break-all; }}
    </style>
</head>
<body>
    <h1>今日（{today_cn}）节点订阅链接</h1>
    {f'<p class="link">{link}</p>' if link else '<p style="color:red">未找到链接</p>'}
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    post_url = get_latest_post_url()
    txt_link = extract_txt_link(post_url)
    generate_html(txt_link)
    print("脚本运行完成，已生成 index.html")
