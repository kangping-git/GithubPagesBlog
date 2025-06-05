# GitHub Pages ブログソフト仕様書

## 1. 概要

* **目的**：GitHub Pages 上で動作する静的ブログシステムを提供し、Markdown 形式の記事作成だけで自動的にサイトがビルド・公開されることを実現する。
* **対象ユーザー**：技術者や個人ブロガー。
* **前提条件**：

  * GitHub アカウントを保有し、GitHub Pages 機能を利用できること。
  * Markdown と Git の基本操作を理解していること。

## 2. システム構成

* **静的サイトジェネレータ**：Jekyll（GitHub Pages 標準対応）
* **ビルド環境**：GitHub Actions（必要に応じて、例えばプラグイン非対応機能を利用する場合）
* **ホスティング**：GitHub Pages
* **プログラミング言語・フレームワーク**：

  * HTML / CSS / JavaScript（フロントエンド）
  * Liquid テンプレート（Jekyll）
  * YAML（フロントマター、\_config.yml）
  * SCSS（Sass）

## 3. ディレクトリ構成

```
/（リポジトリルート）
├── .github/
│   └── workflows/
│       └── gh-pages.yml          # GitHub Actions ワークフロー（任意）
├── _config.yml                   # Jekyll 設定ファイル
├── _data/
│   └── navigation.yml            # ナビゲーションメニュー設定
├── _drafts/                      # 下書き記事（フロントマターで draft: true のみ出力）
│   └── YYYY-MM-DD-draft-example.md
├── _includes/                    
│   ├── header.html               # ヘッダー共通パーツ
│   ├── footer.html               # フッター共通パーツ
│   ├── sidebar.html              # サイドバー（カテゴリ・タグ一覧）
│   └── social-share.html         # SNS シェアボタンパーツ
├── _layouts/                     
│   ├── default.html              # ページ共通レイアウト
│   └── post.html                 # 記事ページ専用レイアウト
├── _posts/                       
│   ├── YYYY-MM-DD-first-post.md  # 記事ファイル
│   └── YYYY-MM-DD-second-post.md
├── assets/
│   ├── css/
│   │   └── style.scss            # SCSS ソース（ビルド後に style.css 生成）
│   ├── js/
│   │   └── main.js               # 必要に応じたクライアントサイドスクリプト
│   └── images/
│       └── ogp-cover.jpg         # OGP 用カバー画像など
├── categories/                   # カテゴリ別一覧ページ（手動 or プラグイン生成）
│   └── tech.html
├── tags/                         # タグ別一覧ページ（手動 or プラグイン生成）
│   └── jekyll.html
├── index.html                    # トップページ（レイアウト：home / default）
├── about.md                      # 固定ページ（About）
├── rss.xml                       # RSS フィード用テンプレート
└── README.md                     
```

## 4. フロントマター仕様

各記事（`_posts` 配下の Markdown ファイル）は、以下の YAML フロントマターを先頭に記述する。

```yaml
---
layout: post
title: "記事タイトル"
date: 2025-06-05 10:30:00 +0900
categories: ["カテゴリ1", "カテゴリ2"]
tags: ["タグA", "タグB"]
description: "記事概要（SEO 用 meta description）"
thumbnail: "/assets/images/サムネイル.jpg"
draft: false
---
# ここから本文（Markdown）

本文を記述する。
```

* `layout`：使用するレイアウト名（例：`post`、`page`、`home` など）
* `title`：記事タイトル
* `date`：公開日時（ISO 8601 形式またはタイムゾーン指定）
* `categories`：配列形式のカテゴリ名
* `tags`：配列形式のタグ名
* `description`：meta description 用テキスト
* `thumbnail`：記事一覧カードや OGP で利用するサムネイル画像パス
* `draft`：`true` の場合、ビルド時に公開されない（ローカルプレビューのみ）

## 5. 機能要件

### 5.1. 必須機能

1. **記事作成・管理**

   * Markdown 形式で記事を作成
   * フロントマターに必要なメタ情報を記述
   * `draft: true` を指定した下書き記事はローカルプレビュー時のみ表示

2. **トップページ（記事一覧）**

   * 最新順（降順）で記事を一覧表示
   * 記事カードに以下を表示：タイトル、公開日、概要 (`description`)、サムネイル
   * ページネーション対応（1ページあたり 10 件など）
   * ページャーとして「前へ」「次へ」リンクを設置

3. **記事詳細ページ**

   * タイトル、公開日、最終更新日（オプション）、カテゴリ、タグを表示
   * Markdown → HTML 変換済み本文を表示
   * 見出し要素に自動で ID を振り、目次（TOC）を自動生成して表示
   * シンタックスハイライト対応 (`<pre><code>` ブロック)
   * SNS シェアボタンを設置（Twitter、Facebook、Hatena ブックマークなど）
   * 前後記事リンク（「← 前の記事」「次の記事 →」）を表示

4. **カテゴリ・タグ一覧**

   * 各カテゴリごとに記事一覧ページを生成
   * 各タグごとに記事一覧ページを生成
   * どちらもページネーション対応（必要に応じて）

5. **RSS フィード**

   * サイト全体の RSS フィードを生成 (`/feed.xml`)
   * カテゴリ別 RSS フィードやタグ別 RSS フィードをオプションで生成可能

6. **SEO 対策**

   * 各ページに `meta title`、`meta description` を出力
   * Open Graph タグ (`og:title`、`og:description`、`og:image`、`og:url` など) を出力
   * `lang` 属性を HTML に指定（例：日本語サイトなら `lang="ja"`）
   * パンくずリストを設置（カテゴリ階層を反映）

7. **レスポンシブ対応**

   * モバイルファースト設計
   * ブレークポイント例：

     * 320px–480px：スマホ小サイズ（1カラム）
     * 481px–768px：タブレット縦向き（1カラム or 2カラム）
     * 769px–1024px：タブレット横向き / ノートPC（2カラム）
     * 1025px 以上：デスクトップ（2カラム＋サイドバー固定）
   * ハンバーガーメニューまたはドロワーメニューを採用（モバイル時）

8. **ナビゲーション**

   * サイトロゴまたはテキストロゴをクリックでトップページへ遷移
   * グローバルナビゲーションに固定ページ（About、Contact など）のリンクを表示
   * カテゴリ一覧へのドロップダウンメニューを実装

9. **ローカルプレビュー**

   * `bundle exec jekyll serve --livereload` コマンドでローカルサーバーを起動
   * コードや Markdown を変更すると自動でページをリロードし、内容を反映

10. **GitHub Pages 連携（自動ビルド）**

    * リポジトリの `main` または `master` ブランチにコミットすると GitHub Pages 側で自動ビルド
    * `baseurl` や `url` を `_config.yml` で適切に設定
    * カスタムドメインを利用する場合、リポジトリ直下に `CNAME` ファイルを配置し、DNS 設定を行う

### 5.2. 推奨機能（拡張機能）

1. **検索機能（クライアントサイド）**

   * Lunr.js や Algolia などを使った全文検索
   * GitHub Actions ビルド時に全記事のインデックスを JSON ファイルとして生成（例：`search_index.json`）
   * クライアント側でキーワード検索し、リストを動的に表示

2. **コメント機能連携**

   * GitHub Issues を利用したコメントシステム（Utterances、Giscus など）を導入可能
   * Disqus を埋め込むオプション

3. **多言語対応**

   * 記事ごとに言語別ディレクトリを分ける（例：`_posts/ja/`、`_posts/en/` など）
   * サイトメニューに言語切り替えを実装
   * `_data/` 配下に言語別文言ファイルを用意し、テンプレートに埋め込む

4. **テーマ切り替え（ダークモード対応）**

   * CSS カスタムプロパティ（Variables）を利用してライト／ダークテーマを切り替え
   * `prefers-color-scheme` メディアクエリを活用し、OS 設定に追随
   * ユーザーが手動でテーマを切り替えるトグルを設置

5. **パフォーマンス最適化**

   * 画像最適化プラグイン（`jekyll-picture-tag` など）を使い、複数サイズのレスポンシブ画像を生成
   * 生成された HTML に対して CSS / JS の最小化（Minify）
   * CSS / JS ファイルにハッシュを付与し、ブラウザキャッシュを有効化

6. **PWA（プログレッシブ Web アプリ）対応**

   * `manifest.json` を生成し、アイコンやテーマカラーを設定
   * サービスワーカーを実装し、オフラインキャッシュをサポート

7. **アーカイブ機能**

   * 年別・月別アーカイブページを自動生成
   * それぞれのアーカイブに記事件数とリンクを表示
   * `_config.yml` でアーカイブ設定を行い、必要に応じて `jekyll-archives` プラグインを利用

8. **著者情報管理**

   * `_data/authors.yml` に著者情報を定義（名前、プロフィール画像、SNS リンクなど）
   * 記事のフロントマターに `author: 著者ID` を追加
   * 記事詳細ページで該当著者の情報を表示し、著者一覧ページを生成

9. **CI テスト・Lint**

   * GitHub Actions で以下を実行するワークフローを定義：

     * リンクチェック（`htmlproofer`）
     * アクセシビリティチェック（`pa11y-ci`）
     * CSS Lint（`stylelint`）、Markdown Lint（`markdownlint`）
   * プルリクエスト時に自動でチェックを実行し、エラーを検知

10. **セキュリティ対策**

    * 外部スクリプト読み込み時に SRI (`integrity` 属性) を設定
    * `Content-Security-Policy` を HTML の `<meta>` で適切に設定し、外部リソースアクセスを制限
    * クッキーバナーを表示し、アナリティクスなどの同意取得を実装

## 6. 詳細設計

### 6.1. `_config.yml` 設定例

```yaml
# サイト基本情報
title: "My GitHub Pages Blog"
description: "GitHub Pages + Jekyll で構築したブログ"
url: "https://username.github.io"
baseurl: ""                # サブディレクトリ利用時は "/my-blog" など

# Markdown とパーマリンク
markdown: kramdown
permalink: /:categories/:year/:month/:day/:title.html

# プラグイン
plugins:
  - jekyll-feed           # RSS
  - jekyll-sitemap        # sitemap.xml
  - jekyll-seo-tag        # SEO タグ生成
  - jekyll-paginate       # ページネーション
  # - jekyll-archives     # 年・月・カテゴリ・タグのアーカイブ（必要に応じて）

# ページネーション設定
paginate: 10
paginate_path: "/page/:num/"

# ソーシャル情報
author: "Your Name"
email: "you@example.com"
twitter_username: "your_twitter"
github_username: "username"

# 配置先ブランチ設定（GitHub Pages 設定側で明示的に gh-pages などを指定する場合）
# publish_branch: gh-pages  （GitHub Actions でデプロイする場合に利用）
```

### 6.2. テンプレート構成

#### 6.2.1. 共通レイアウト（`_layouts/default.html`）

* `<head>`：

  * `<meta charset="UTF-8">`
  * `<meta name="viewport" content="width=device-width, initial-scale=1">`
  * `<title>{{ page.title }} | {{ site.title }}</title>`
  * `<meta name="description" content="{{ page.description | default: site.description }}">`
  * SEO / Open Graph タグ（`{% seo %}` を利用）
  * CSS 読み込み：`<link rel="stylesheet" href="{{ '/assets/css/style.css' | relative_url }}">`
  * 必要に応じてフォントやアイコン（例：Google Fonts）の読み込み

* `<body>`：

  1. **ヘッダー部**（`_includes/header.html` をインクルード）

     * サイトロゴ or サイトタイトル
     * グローバルナビゲーション（固定ページ・カテゴリ一覧へのリンク）
     * モバイル時はハンバーガーメニュー化
  2. **メインコンテンツ**

     * 2カラム構成（メイン記事エリア + サイドバー）
     * モバイル時は 1カラム表示
  3. **フッター部**（`_includes/footer.html` をインクルード）

     * 著作権表示
     * SNS リンク
     * ページ最下部に戻るボタン

#### 6.2.2. 記事レイアウト（`_layouts/post.html`）

* フロントマターに指定された `thumbnail` を `<figure><img>` で表示
* タイトル：`<h1>{{ page.title }}</h1>`
* 投稿日：`<time datetime="{{ page.date | date_to_xmlschema }}">{{ page.date | date: "%Y-%m-%d" }}</time>`
* カテゴリ：`{% for cat in page.categories %}<a href="{{ '/categories/' | append: cat | append: '.html' | relative_url }}">{{ cat }}</a>{% if forloop.last == false %}, {% endif %}{% endfor %}`
* タグ：`{% for tag in page.tags %}<a href="{{ '/tags/' | append: tag | append: '.html' | relative_url }}">{{ tag }}</a>{% if forloop.last == false %}, {% endif %}{% endfor %}`
* 目次生成：JavaScript で `<h2>`～`<h4>` に自動で ID を振り、目次用 `<nav>` 要素内にリストを生成
* 本文表示：`{{ content }}`
* シンタックスハイライト：`{% highlight lang %}` ブロックまたは Prism.js / Highlight.js を読み込み
* SNS シェアボタン：`{% include social-share.html %}`
* 前後記事へのリンク：

  ```liquid
  {% if page.previous %}
    <a href="{{ page.previous.url | relative_url }}">← {{ page.previous.title }}</a>
  {% endif %}
  {% if page.next %}
    <a href="{{ page.next.url | relative_url }}">{{ page.next.title }} →</a>
  {% endif %}
  ```
* コメント欄：Utterances や Giscus のスクリプトを `<div id="comments"></div>` に挿入

#### 6.2.3. トップページレイアウト（`_layouts/home.html` または `index.html`）

* `_config.yml` の `paginate` 設定を利用して、最新記事を `paginator.posts` でループ表示
* 記事カード構成：

  * サムネイル (`post.thumbnail`)
  * タイトル：`<a href="{{ post.url | relative_url }}">{{ post.title }}</a>`
  * 日付：`<time>{{ post.date | date: "%Y-%m-%d" }}</time>`
  * 概要：`{{ post.description }}`
* ページネーション表示：

  ```liquid
  <ul class="pagination">
    {% if paginator.previous_page %}
      <li><a href="{{ paginator.previous_page_path | relative_url }}">← Newer</a></li>
    {% endif %}
    {% if paginator.next_page %}
      <li><a href="{{ paginator.next_page_path | relative_url }}">Older →</a></li>
    {% endif %}
  </ul>
  ```

#### 6.2.4. カテゴリページ（例：`categories/tech.html`）

* フロントマター：

  ```yaml
  ---
  layout: default
  title: "カテゴリ: Tech"
  category: "Tech"
  ---
  ```
* ページ本文で以下をループ：

  ```liquid
  {% assign posts_in_category = site.categories[page.category] %}
  {% for post in posts_in_category %}
    <article>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <time>{{ post.date | date: "%Y-%m-%d" }}</time>
      <p>{{ post.description }}</p>
    </article>
  {% endfor %}
  ```

#### 6.2.5. タグページ（例：`tags/jekyll.html`）

* フロントマター：

  ```yaml
  ---
  layout: default
  title: "タグ: Jekyll"
  tag: "Jekyll"
  ---
  ```
* ページ本文で以下をループ：

  ```liquid
  {% assign posts_with_tag = site.tags[page.tag] %}
  {% for post in posts_with_tag %}
    <article>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title }}</a></h2>
      <time>{{ post.date | date: "%Y-%m-%d" }}</time>
      <p>{{ post.description }}</p>
    </article>
  {% endfor %}
  ```

#### 6.2.6. RSS フィードテンプレート（`rss.xml`）

* Jekyll プラグイン `jekyll-feed` を利用して自動生成
* 生成後 `/feed.xml` で公開される

### 6.3. ナビゲーション設定（`_data/navigation.yml`）

```yaml
main:
  - title: "Home"
    url: "/"
  - title: "About"
    url: "/about.html"
  - title: "Categories"
    subitems:
      - title: "Tech"
        url: "/categories/Tech.html"
      - title: "Jekyll"
        url: "/categories/Jekyll.html"
  - title: "Tags"
    subitems:
      - title: "GitHub Pages"
        url: "/tags/GitHub%20Pages.html"
      - title: "静的サイト"
        url: "/tags/静的サイト.html"
```

* レイアウト内で `navigation.yml` をループし、ドロップダウン付きメニューを生成
* モバイル時はハンバーガーアイコンをクリックすると展開

## 7. 運用フロー

### 7.1. 初期セットアップ

1. GitHub でリポジトリを作成

   * リポジトリ名が `username.github.io` の場合、`main` ブランチをそのまま GitHub Pages に公開
   * それ以外の場合は、`gh-pages` ブランチを公開先に設定
2. ローカル環境にリポジトリをクローン
3. Jekyll プロジェクトを初期化（または手動でディレクトリ構成を作成）

   ```bash
   $ jekyll new . --force
   ```
4. `_config.yml` を編集し、サイト情報やプラグインを設定
5. `_layouts`／`_includes`／`assets`／`_posts` を自分好みに整備
6. CSS（SCSS）を記述し、`assets/css/style.scss` にメインスタイルを準備

### 7.2. ローカルプレビュー

```bash
$ bundle install           # Gemfile を利用している場合
$ bundle exec jekyll serve --livereload
# または
$ jekyll serve --livereload
```

* `http://localhost:4000` にアクセスし、変更をリアルタイムに確認

### 7.3. 記事追加手順

1. `_posts/` 配下に Markdown ファイルを作成

   * ファイル名：`YYYY-MM-DD-スラグ.md`
   * フロントマターを記述し、本文を Markdown で執筆
2. Git でコミット & プッシュ

   ```bash
   $ git add _posts/YYYY-MM-DD-new-post.md
   $ git commit -m "Add new post: 記事タイトル"
   $ git push origin main
   ```
3. GitHub Pages が自動ビルドを実行し、数分以内にサイトが更新される

### 7.4. 拡張機能追加の流れ

1. **検索機能を追加する場合**

   * GitHub Actions でビルド時に全記事を JSON 形式で出力（`search_index.json` を生成）
   * Lunr.js をサイトに組み込み、検索 UI を実装
2. **コメント機能を追加する場合**

   * Utterances または Giscus の設定方法を確認
   * リポジトリ名・リポジトリ所有者・Issue 作成先などを指定してスクリプトタグを追加
3. **多言語対応を行う場合**

   * `_posts/ja/`、`_posts/en/` のように記事ディレクトリを分割
   * 各言語で `_layouts`・`_includes`・`assets/lang/` を分けて管理
   * サイト全体に「言語切替」メニューを設置
4. **プラグイン非対応機能を導入する場合**

   * GitHub Actions でカスタムビルドを行い、成果物を `gh-pages` ブランチへデプロイ
   * `.github/workflows/gh-pages.yml` を用意し、必要なビルドコマンドを記述

## 8. セキュリティ・運用上の注意

* **プラグイン制限**：GitHub Pages 公式ビルドではサポート外のプラグインがあるため、必要な場合は GitHub Actions でビルド → デプロイする。
* **外部リソースの SRI**：CDN や外部スクリプトを読み込む際は、`integrity` 属性を指定して改ざんリスクを低減。
* **CSP 設定**：可能であれば HTML `<meta>` で Content Security Policy を指定し、外部スクリプト／スタイルの読み込みを制限。
* **GDPR 対応**：Google Analytics や外部トラッキングを導入する場合は、クッキーバナーや同意取得バナーの設置を検討。
* **コメント欄の権限設定**：Utterances や Giscus 利用時、Issue への不正投稿を防ぐためにリポジトリ権限設定を適切に行う。

## 9. 用語定義

* **記事（Post）**：Markdown ファイル形式で執筆されるコンテンツ単位。
* **フロントマター**：Markdown ファイル冒頭に定義する YAML 形式のメタデータ。
* **レイアウト（Layout）**：共通ヘッダー・フッターや CSS を含むテンプレート HTML。
* **Include**：レイアウト内で再利用可能なパーツ HTML (例：ヘッダー、フッターなど) を分割して管理。
* **パージネーション（Pagination）**：記事一覧を複数ページに分割して表示する仕組み。
* **OGP (Open Graph Protocol)**：SNS でシェアした際に表示されるタイトル・説明・画像を指定するメタタグ。
* **RSS フィード**：サイトの新着記事情報を配信する XML 形式のデータ。

## 10. 参考情報・リンク

* [Jekyll 公式ドキュメント](https://jekyllrb.com/docs/)
* [GitHub Pages ヘルプ](https://docs.github.com/en/pages)
* [Liquid テンプレート言語リファレンス](https://shopify.github.io/liquid/)
* [Jekyll Plugins 一覧](https://jekyllrb.com/docs/plugins/)
* [Utterances 設定ガイド](https://utteranc.es/)
* [Lunr.js 公式サイト](https://lunrjs.com/)
* [GitHub Actions ドキュメント](https://docs.github.com/en/actions)

---

以上が、GitHub Pages 上で動作するブログソフトの仕様書になります。必要に応じて各セクションをカスタマイズし、実際の開発を進めてください。
