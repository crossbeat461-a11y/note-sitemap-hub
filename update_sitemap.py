import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os
import time

# 設定
RSS_URL = "https://note.com/ktech_devz/rss"
SITEMAP_FILE = "sitemap.xml"

def get_note_articles():
    # noteのセキュリティを回避するため、本物のブラウザに近い情報を送ります
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept': 'application/rss+xml, application/xml, text/xml, */*',
    }
    
    try:
        print(f"Connecting to RSS...")
        response = requests.get(RSS_URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        # XMLを解析
        root = ET.fromstring(response.content)
        articles = []
        
        # itemタグ内のlinkをすべて探す
        for item in root.findall(".//item"):
            link = item.find("link").text
            if link:
                articles.append(link)
        
        print(f"取得できたURL数: {len(articles)}")
        return articles

    except Exception as e:
        print(f"取得エラー発生: {e}")
        return []

def update_sitemap(new_links):
    # XMLの骨組み作成
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # 【最重要】もし1件も取れなくても、強制的に1行ダミーを入れる
    # これにより「常に変更がある」とGitに思わせ、上書きを強制します
    today = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if not new_links:
        # 記事が取れなかった時のためのバックアップURL
        new_links = ["https://note.com/ktech_devz"]

    for link in sorted(set(new_links)):
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = link
        lastmod = ET.SubElement(url, "lastmod")
        # 秒まで入れることで、必ずファイルに「差分」を作ります
        lastmod.text = datetime.now().strftime("%Y-%m-%d")

    # ファイル書き出し
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
    print(f"完了: {SITEMAP_FILE} を作成しました。")

if __name__ == "__main__":
    links = get_note_articles()
    update_sitemap(links)
