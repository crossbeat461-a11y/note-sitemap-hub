import xml.etree.ElementTree as ET
import requests
from datetime import datetime
import os

# 設定：あなたのnoteのRSS URL
RSS_URL = "https://note.com/ktech_devz/rss"
SITEMAP_FILE = "sitemap.xml"

def get_note_articles():
    try:
        response = requests.get(RSS_URL)
        # noteのRSSは標準的なXML形式
        root = ET.fromstring(response.content)
        articles = []
        for item in root.findall(".//item"):
            link = item.find("link").text
            articles.append(link)
        return articles
    except Exception as e:
        print(f"Error fetching RSS: {e}")
        return []

def update_sitemap(new_links):
    # 既存のサイトマップがあれば読み込む（過去記事の蓄積のため）
    existing_links = set()
    if os.path.exists(SITEMAP_FILE):
        try:
            # サイトマップの標準Namespaceに対応
            ns = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            tree = ET.parse(SITEMAP_FILE)
            root = tree.getroot()
            for loc in root.findall("ns:url/ns:loc", ns):
                existing_links.add(loc.text)
        except Exception as e:
            print(f"Error reading existing sitemap: {e}")

    # 新旧のリンクを合体（重複は自動で排除される）
    all_links = existing_links.union(set(new_links))

    # XML構造の再構築
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    
    # 常に最新の日付を付与（あるいは記事ごとの日付取得も可能ですが、まずは簡素に）
    today = datetime.now().strftime("%Y-%m-%d")
    
    for link in sorted(all_links):
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = link
        lastmod = ET.SubElement(url, "lastmod")
        lastmod.text = today

    # 書き出し
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)

if __name__ == "__main__":
    links = get_note_articles()
    if links:
        update_sitemap(links)
        print(f"Success: Sitemap updated with {len(links)} articles.")
    else:
        print("No articles found or error occurred.")