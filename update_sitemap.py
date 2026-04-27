import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os

# 設定
RSS_URL = "https://note.com/ktech_devz/rss"
SITEMAP_FILE = "sitemap.xml"

def get_note_articles():
    try:
        # ブラウザからのアクセスを装うためのヘッダーをより強力に設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(RSS_URL, headers=headers, timeout=15)
        response.raise_for_status()
        
        # 取得した内容を解析
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item"):
            link_node = item.find("link")
            if link_node is not None and link_node.text:
                articles.append(link_node.text)
        
        print(f"RSSから {len(articles)} 件の記事を取得しました。")
        return articles
    except Exception as e:
        print(f"RSS取得エラー: {e}")
        return []

def update_sitemap(new_links):
    # 常に最新のリストで上書きする（重複を避ける）
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 取得したURLを一つずつ追加
    for link in sorted(set(new_links)):
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = link
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = today

    # 書き出し
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
    print(f"{SITEMAP_FILE} を更新しました。")

if __name__ == "__main__":
    links = get_note_articles()
    # 記事が取得できた場合のみ、中身のあるサイトマップを作る
    if links:
        update_sitemap(links)
    else:
        # 取得失敗時にファイルが空にならないよう、最低限の構造を維持
        print("記事が取得できなかったため、更新をスキップしました。")
