# note-sitemap-hub

[note @ktech_dev](https://note.com/ktech_dev) の公開記事一覧を、毎日自動で更新する。

人が読むページ（note に貼る URL）: https://k-tech-lab.vercel.app/notes/  
データ正本: https://crossbeat461-a11y.github.io/note-sitemap-hub/  
検索エンジン用: https://crossbeat461-a11y.github.io/note-sitemap-hub/sitemap.xml

## 何をしているか

note の公開 API から全記事を取り、`index.html`・`notes.json`・`sitemap.xml` を書き換える。GitHub Actions が毎日 1 回（UTC 18:00）動く。Homepage の一覧ページは `notes.json` を読んで表示する。

note の [サイトマップ（目録）](https://note.com/ktech_dev/n/n4eb9d70dc172) には、Homepage の一覧（`https://k-tech-lab.vercel.app/notes/`）だけ置く。GitHub Pages の URL は note のカード画像と相性が悪い。

## 手動で今すぐ更新する

GitHub の Actions → **Update Sitemap** → **Run workflow**

## 作者

K-Tech Studio / 開発担当  
https://note.com/ktech_dev · https://x.com/K_Tech_Dev
