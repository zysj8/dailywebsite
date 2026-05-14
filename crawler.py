import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup

BASE_URL = "https://www.yudou789.top"
today_str = datetime.now().strftime("%Y%m%d")
today_cn = datetime.now().strftime("%Y年%m月%d日")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Referer": BASE_URL
}

def get_latest_post_url():
    try:
        resp = requests.get(BASE_URL, headers=HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        articles = soup.find_all("h2")
        for h2 in articles:
            title = h2.get_text(strip=True)
            if today_cn in title:
                link_tag = h2.find("a", href=True)
                if link_tag:
                    href = link_tag["href"]
                    full_url = BASE_URL + href if not href.startswith("http") else href
                    return full_url
        return None
    except:
        return None

def extract_txt_link(post_url):
    if not post_url:
        return None
    try:
        resp = requests.get(post_url, headers=HEADERS, timeout=15)
        html = resp.text
        pattern = re.compile(r'https?://[^\s"]+?' + re.escape(today_str) + r'[^\s"]*?\.txt', re.IGNORECASE)
        matches = pattern.findall(html)
        return matches[0] if matches else None
    except:
        return None

def generate_html(link):
    html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>今日订阅链接</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #e4eaf5 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }}
        .card {{
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0,0,0,0.08);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            text-align: center;
        }}
        h1 {{
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }}
        .link-box {{
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 10px;
            padding: 16px;
            word-break: break-all;
            font-size: 16px;
            color: #007bff;
            margin-bottom: 20px;
        }}
        .copy-btn {{
            background: #007bff;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: 0.2s;
        }}
        .copy-btn:hover {{
            background: #0069d9;
        }}
        .error {{
            color: #dc3545;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div class="card">
        <h1>📅 {today_cn} 订阅链接</h1>
        {'<div class="link-box" id="link">' + link + '</div><button class="copy-btn" onclick="copy()">🔗 一键复制</button>' if link else '<p class="error">❌ 未获取到链接</p>'}
    </div>

    <script>
        function copy() {{
            let text = document.getElementById('link').innerText;
            navigator.clipboard.writeText(text).then(() => {{
                alert('✅ 复制成功！');
            }});
        }}
    </script>
</body>
</html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    post_url = get_latest_post_url()
    txt_link = extract_txt_link(post_url)
    generate_html(txt_link)
