#!/usr/bin/env python3
"""note 公開APIから全記事を取り、一覧HTMLと sitemap.xml を作る。"""

from __future__ import annotations

import html
import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CREATOR = "ktech_dev"
TZ = ZoneInfo("Asia/Tokyo")
UA = "K-Tech-Studio-NoteIndex/1.0 (+https://k-tech-lab.vercel.app/)"
NOTE_HOME = f"https://note.com/{CREATOR}"
HOMEPAGE = "https://k-tech-lab.vercel.app/"
PAGE_URL = "https://crossbeat461-a11y.github.io/note-sitemap-hub/"
OG_IMAGE = f"{PAGE_URL}ogp.jpg"
SITEMAP_FILE = Path("sitemap.xml")
INDEX_FILE = Path("index.html")


def http_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=45) as res:
        return json.load(res)


def fetch_all_notes() -> list[dict]:
    notes: list[dict] = []
    page = 1
    while page <= 40:
        data = http_json(
            f"https://note.com/api/v2/creators/{CREATOR}/contents?kind=note&page={page}"
        )
        batch = data.get("data", {}).get("contents") or []
        if not batch:
            break
        notes.extend(batch)
        page += 1
    return notes


def normalize(notes: list[dict]) -> list[dict]:
    rows = []
    seen: set[str] = set()
    for n in notes:
        if n.get("status") and n.get("status") != "published":
            continue
        key = n.get("key") or ""
        url = n.get("noteUrl") or (f"{NOTE_HOME}/n/{key}" if key else "")
        if not url or url in seen:
            continue
        seen.add(url)
        pub = n.get("publishAt") or ""
        rows.append(
            {
                "title": n.get("name") or url,
                "url": url,
                "publish_at": pub,
                "date": pub[:10] if pub else "",
            }
        )
    rows.sort(key=lambda r: r["publish_at"] or "", reverse=True)
    return rows


def write_sitemap(rows: list[dict]) -> None:
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
    home = ET.SubElement(urlset, "url")
    ET.SubElement(home, "loc").text = NOTE_HOME
    if rows:
        ET.SubElement(home, "lastmod").text = rows[0]["date"] or datetime.now(TZ).strftime("%Y-%m-%d")

    for row in rows:
        url = ET.SubElement(urlset, "url")
        ET.SubElement(url, "loc").text = row["url"]
        if row["date"]:
            ET.SubElement(url, "lastmod").text = row["date"]

    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(SITEMAP_FILE, encoding="utf-8", xml_declaration=True)


def write_index(rows: list[dict], generated: str) -> None:
    items = []
    for row in rows:
        title = html.escape(row["title"])
        url = html.escape(row["url"], quote=True)
        date = html.escape(row["date"] or "----")
        items.append(
            f'      <li><time datetime="{date}">{date}</time> '
            f'<a href="{url}">{title}</a></li>'
        )
    body = "\n".join(items) if items else "      <li>記事を取得できませんでした。</li>"
    page = f"""<!DOCTYPE html>
<html lang="ja" prefix="og: http://ogp.me/ns#">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>K-Tech Studio — note 全記事一覧</title>
  <meta name="description" content="note @ktech_dev の公開記事一覧。毎日自動更新。">
  <meta property="og:title" content="K-Tech Studio — note 全記事一覧">
  <meta property="og:description" content="note @ktech_dev の公開記事一覧。毎日自動更新。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{PAGE_URL}">
  <meta property="og:locale" content="ja_JP">
  <meta property="og:site_name" content="K-Tech Studio">
  <meta property="og:image" content="{OG_IMAGE}">
  <meta property="og:image:secure_url" content="{OG_IMAGE}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="K-Tech Studio">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="K-Tech Studio — note 全記事一覧">
  <meta name="twitter:description" content="note @ktech_dev の公開記事一覧。毎日自動更新。">
  <meta name="twitter:image" content="{OG_IMAGE}">
  <meta name="note:card" content="summary_large_image">
  <link rel="image_src" href="{OG_IMAGE}">
  <style>
    :root {{ color-scheme: light dark; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Hiragino Sans", sans-serif;
      max-width: 42rem;
      margin: 2rem auto;
      padding: 0 1.25rem 3rem;
      line-height: 1.6;
    }}
    h1 {{ font-size: 1.35rem; font-weight: 650; }}
    .meta {{ color: #666; font-size: 0.9rem; }}
    ol {{ padding-left: 1.25rem; }}
    li {{ margin: 0.45rem 0; }}
    time {{ display: inline-block; width: 7.2em; color: #666; font-variant-numeric: tabular-nums; }}
    a {{ color: inherit; }}
    footer {{ margin-top: 2.5rem; font-size: 0.9rem; }}
  </style>
</head>
<body>
  <h1>note 全記事一覧</h1>
  <p class="meta">K-Tech Studio / 開発担当　{len(rows)}件　最終更新 {html.escape(generated)}</p>
  <p>このページは毎日自動で更新されます。note の目録記事から開いてください。</p>
  <ol>
{body}
  </ol>
  <footer>
    <a href="{NOTE_HOME}">note</a>
    · <a href="{HOMEPAGE}">Homepage</a>
    · <a href="./sitemap.xml">sitemap.xml</a>
  </footer>
</body>
</html>
"""
    INDEX_FILE.write_text(page, encoding="utf-8")


def main() -> None:
    raw = fetch_all_notes()
    rows = normalize(raw)
    generated = datetime.now(TZ).strftime("%Y-%m-%d %H:%M JST")
    print(f"取得: {len(raw)}件 / 公開一覧: {len(rows)}件")
    if not rows:
        raise SystemExit("記事が0件のため、古い一覧を上書きしません。")
    write_sitemap(rows)
    write_index(rows, generated)
    print(f"更新: {INDEX_FILE} / {SITEMAP_FILE}")


if __name__ == "__main__":
    main()
