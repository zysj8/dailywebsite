import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = "https://www.yudou789.top"
today_str = datetime.now().strftime("%Y%m%d")
today_cn = datetime.now().strftime("%Y年%m月%d日")

# 伪装浏览器请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}

def get_latest_post_url():
    """从首页找到当天日期的文章链接"""
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        # 遍历所有文章链接，匹配标题中的日期
        for a in soup.find_all("a", href=True):
            title = a.get("title", "")
            if today_cn in title:
                return BASE_URL + a["href"] if not a["href"].startswith("http") else a["href"]

        # 如果没找到当天的文章，返回 None
        return None
    except Exception as e:
        print(f"获取文章链接失败: {e}")
        return None

def extract_txt_link(post_url):
    """从文章源码中提取含 today_str 的 .txt 链接"""
    if not post_url:
        return None
    try:
        resp = requests.get(post_url, headers=HEADERS, timeout=10)
        resp.raise_for_status()
        html = resp.text

        # 匹配含 YYYYMMDD 且以 .txt 结尾的链接
        pattern = re.compile(r'https?://[^\s"]+?' + re.escape(today_str) + r'[^\s"]*?\.txt', re.IGNORECASE)
        matches = pattern.findall(html)

        return matches[0] if matches else None
    except Exception as e:
        print(f"爬取文章失败: {e}")
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
        body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background: #f5f5f5; }}
        .card {{ background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 800px; margin: 0 auto; }}
        .link {{ font-size: 18px; color: #007bff; word-break: break-all; margin-top: 20px; }}
        .error {{ color: #dc3545; font-size: 18px; margin-top: 20px; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>今日（{today_cn}）节点订阅链接</h1>
        {f'<p class="link">✅ {link}</p>' if link else '<p class="error">❌ 未找到今日链接，请稍后重试</p>'}
    </div>
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
