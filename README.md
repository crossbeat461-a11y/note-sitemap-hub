# note-sitemap-hub

[note @ktech_dev](https://note.com/ktech_dev) の公開記事一覧を、毎日自動で更新する。

人が読むページ: https://crossbeat461-a11y.github.io/note-sitemap-hub/  
検索エンジン用: https://crossbeat461-a11y.github.io/note-sitemap-hub/sitemap.xml

## 何をしているか

note の公開 API から全記事を取り、`index.html` と `sitemap.xml` を書き換える。GitHub Actions が毎日 1 回（UTC 18:00）動く。

note の [サイトマップ（目録）](https://note.com/ktech_dev/n/n4eb9d70dc172) には、この一覧ページへのリンクだけ置く。記事 URL を note に貼らない。

## 手動で今すぐ更新する

GitHub の Actions → **Update Sitemap** → **Run workflow**

## 作者

K-Tech Studio / 開発担当  
https://note.com/ktech_dev · https://x.com/K_Tech_Dev
