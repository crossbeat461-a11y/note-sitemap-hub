import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os

# 設定：RSS URL（末尾に /rss がついているか再確認）
RSS_URL = "https://note.com/ktech_devz/rss"
SITEMAP_FILE = "sitemap.xml"

def get_note_articles():
    try:
        # ユーザーエージェントを設定して拒否を防ぐ
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(RSS_URL, headers=headers)
        response.raise_for_status()
        
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item"):
            link = item.find("link").text
            if link:
                articles.append(link)
        return articles
    except Exception as e:
        print(f"RSS取得エラー: {e}")
        return []

def update_sitemap(new_links):
    # 既存のリンクを保持
    existing_links = set()
    if os.path.exists(SITEMAP_FILE) and os.path.getsize(SITEMAP_FILE) > 0:
        try:
            ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            tree = ET.parse(SITEMAP_FILE)
            for loc in tree.getroot().findall("ns:url/ns:loc", ns):
                existing_links.add(loc.text)
        except:
            pass

    # 全リンクを統合
    all_links = existing_links.union(set(new_links))
    
    # 【重要】もし記事が0件でも、空のXML構造を必ず作る
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    today = datetime.now().strftime("%Y-%m-%d")
    
    for link in sorted(all_links):
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = link
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = today

    # ファイルを書き出す（これで git add が失敗しなくなります）
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)
    print(f"{SITEMAP_FILE} を作成しました。リンク数: {len(all_links)}")

if __name__ == "__main__":
    links = get_note_articles()
    # 取得できなくても、空のサイトマップを作るために実行する
    update_sitemap(links)
