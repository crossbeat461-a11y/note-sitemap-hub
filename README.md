# note-sitemap-hub

note（@ktech_devz）の更新を自動検知し、独自ドメイン上で `sitemap.xml` を生成・蓄積するオートメーション・ハブです。

## 概要
noteの標準RSSフィードの制限（最大50件）を補完し、過去記事を含む全インデックスをGoogle Search Console等へ提供することを目的としています。
GitHub Actions を利用し、1日1回、サーバーレスで自動更新されます。

## システム構成
- **Runtime:** Python 3.x
- **Automation:** GitHub Actions (Scheduled workflow)
- **Data Source:** note RSS Feed
- **Output:** `sitemap.xml`

## 運用ポリシー
本プロジェクトは「本質主義」に基づき、過度な装飾を排し、データの整合性と自動化の継続性を重視して運用しています。
生成されたサイトマップは、以下の独自ドメイン配下で公開されています。
[あなたの独自ドメインURL]/sitemap.xml

## 作者
**Kimura Shigeru**
- CRM Administrator / EC Operations Manager
- note: https://note.com/ktech_devz
- X: https://x.com/K_Tech_Dev
