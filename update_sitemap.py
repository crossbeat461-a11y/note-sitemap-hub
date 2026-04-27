import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os

# あなたのnote RSS URL
RSS_URL = "https://note.com/ktech_devz/rss"
SITEMAP_FILE = "sitemap.xml"

def get_note_articles():
    try:
        # 強力なヘッダー（身分証明）を設定
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/xml, text/xml, */*',
            'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
        }
        
        print(f"Connecting to {RSS_URL}...")
        response = requests.get(RSS_URL, headers=headers, timeout=20)
        response.raise_for_status()
        
        # 取得したXMLを解析
        root = ET.fromstring(response.content)
        articles = []
        
        # noteのRSS構造（item内のlink）を抽出
        for item in root.findall(".//item"):
            link_node = item.find("link")
            if link_node is not None and link_node.text:
                articles.append(link_node.text)
        
        print(f"Found {len(articles)} articles.")
        return articles
        
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        # エラーが起きた場合は空リストを返す
        return []

def update_sitemap(new_links):
    # XMLの基本構造を作成
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = datetime.now().strftime("%Y-%m-%d")
    
    # 取得できたリンクを書き込む
    for link in sorted(set(new_links)):
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = link
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = today

    # ファイルに書き出し
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
    print(f"{SITEMAP_FILE} has been updated with {len(new_links)} links.")

if __name__ == "__main__":
    links = get_note_articles()
    # 記事が0件でも、最低限の構造を書き出す（git add エラー防止）
    update_sitemap(links)
