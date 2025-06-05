## 1. 概要

* **目的**：GitHub Pages 上で動作する静的ブログシステムを、Node.js ベースの静的サイトジェネレータ（Eleventy など）を使ってビルド・公開できるようにする。
* **対象ユーザー**：技術者や個人ブロガー。
* **前提条件**：

  * GitHub アカウントを保有し、GitHub Pages 機能を利用できること。
  * Node.js（LTS 推奨版）と npm の基本操作を理解していること。
  * Markdown と Git の基本操作を理解していること。

## 2. システム構成

* **静的サイトジェネレータ**：Eleventy (11ty)
* **ビルド環境**：Node.js / npm
* **ホスティング**：GitHub Pages
* **CI/CD**：GitHub Actions
* **プログラミング言語／テンプレート**：

  * JavaScript (ES Modules / CommonJS)
  * Nunjucks（または Liquid、Handlebars、その他 Eleventy 対応のテンプレートエンジン）
  * Markdown（記事ファイル）
  * YAML（Front Matter）
  * SCSS（Sass）

## 3. ディレクトリ構成例

```
/（リポジトリルート）
├── .github/
│   └── workflows/
│       └── deploy.yml            # GitHub Actions ワークフロー
├── .eleventy.js                  # Eleventy の設定ファイル
├── package.json                  # プロジェクト定義（scripts, dependencies など）
├── package-lock.json             # 依存管理（npm による自動生成）
├── README.md                     # プロジェクト概要
├── src/
│   ├── _data/
│   │   └── navigation.json       # ナビゲーションメニュー設定
│   ├── _includes/
│   │   ├── header.njk            # ヘッダー共通パーツ
│   │   ├── footer.njk            # フッター共通パーツ
│   │   ├── sidebar.njk           # サイドバー（カテゴリ・タグ一覧）
│   │   └── social-share.njk      # SNS シェアボタンパーツ
│   ├── _layouts/
│   │   ├── base.njk               # ベースレイアウト
│   │   ├── post.njk               # 記事ページ用レイアウト
│   │   └── home.njk               # トップページ用レイアウト
│   ├── posts/
│   │   ├── 2025-06-05-first-post.md
│   │   └── 2025-06-08-second-post.md
│   ├── categories/               # カテゴリ一覧ページテンプレート（Eleventy Collections で生成可）
│   │   └── category.njk
│   ├── tags/                     # タグ一覧ページテンプレート（Eleventy Collections で生成可）
│   │   └── tag.njk
│   ├── assets/
│   │   ├── css/
│   │   │   └── style.scss        # SCSS ソース（ビルド後に style.css 生成）
│   │   ├── js/
│   │   │   └── main.js           # 必要に応じたクライアントサイドスクリプト
│   │   └── images/
│   │       └── ogp-cover.jpg     # OGP 用カバー画像など
│   ├── index.md                  # トップページ定義（Front Matter で layout: home）
│   ├── about.md                  # 固定ページ（About）
│   └── rss.xml                   # RSS フィードテンプレート
└── public/                       # ビルド成果物（Eleventy 出力先）  
```

* `src/`：ソースコードとテンプレート、記事を置く。
* `public/`：Eleventy がビルド時に生成する静的ファイルを配置するディレクトリ。GitHub Pages ではこのディレクトリを `gh-pages` ブランチにデプロイ。
* `package.json`：依存パッケージ、ビルドスクリプト、開発サーバースクリプトなどを定義。
* `.eleventy.js`：Eleventy 固有の設定（ディレクトリ指定、テンプレートエンジン設定など）。
* `.github/workflows/deploy.yml`：ビルドとデプロイを自動化する GitHub Actions ワークフロー。

## 4. Front Matter 仕様

各記事（`src/posts` 配下の Markdown ファイル）は、以下の YAML Front Matter を先頭に記述する。

```yaml
---
layout: post                  # Eleventy の layout 名
title: "記事タイトル"
date: 2025-06-05T10:30:00+09:00
categories: ["カテゴリ1", "カテゴリ2"]
tags: ["タグA", "タグB"]
description: "記事概要（SEO 用 meta description）"
thumbnail: "/assets/images/サムネイル.jpg"
draft: false
permalink: "/posts/first-post/"  # 任意でフレンドリ URL を設定
---
# ここから本文（Markdown）

本文を記述する。
```

* `layout`：Eleventy が参照するレイアウトファイル（例：`layouts/post.njk`）。
* `title`：記事タイトル。
* `date`：公開日時。ISO 8601 形式を推奨。
* `categories`：配列形式のカテゴリ名。
* `tags`：配列形式のタグ名。
* `description`：meta description 用テキスト。
* `thumbnail`：記事一覧カードや OGP で利用するサムネイル画像パス。
* `draft`：`true` の場合はビルド対象外。Eleventy の設定で `eleventyConfig.addCollection("posts", … d` 内で除外処理を行う。
* `permalink`：生成される静的ページのパスを指定。省略すると自動生成。

## 5. 機能要件

### 5.1. 必須機能

1. **記事作成・管理**

   * Markdown 形式で記事を作成する。
   * Front Matter に必要なメタ情報を記述する。
   * `draft: true` の記事はビルド時に出力しない。

2. **トップページ（記事一覧）**

   * 最新順（降順）で記事を一覧表示する。
   * 各記事カードに以下を表示：タイトル、公開日、概要（`description`）、サムネイル。
   * ページネーション対応（例：1ページあたり 10件）。
   * ページャーとして「前へ」「次へ」リンクを設置。

3. **記事詳細ページ**

   * タイトル、公開日、最終更新日（オプション）、カテゴリ、タグを表示する。
   * Markdown → HTML 変換済み本文を表示する。
   * 見出し要素に自動で ID を振り、目次（TOC）を自動生成して表示する（Eleventy のプラグインやショートコードで実装）。
   * シンタックスハイライト対応（Prism.js や Highlight.js を組み込む）。
   * SNS シェアボタンを設置（Twitter、Facebook、Hatena ブックマークなど）。
   * 前後記事リンク（「← 前の記事」「次の記事 →」）を表示する。

4. **カテゴリ・タグ一覧**

   * 全記事を収集したコレクション（`Collections`）を使い、カテゴリごとに記事一覧ページを生成する。
   * 同様にタグごとに記事一覧ページを生成する。
   * どちらもページネーション対応可能。

5. **RSS フィード**

   * サイト全体の RSS フィードを生成する（`/rss.xml`）。
   * カテゴリ別やタグ別の RSS フィードをオプションで生成可能。

6. **SEO 対策**

   * 各ページに `meta title`、`meta description` を出力する。
   * Open Graph タグ（`og:title`、`og:description`、`og:image`、`og:url`）を出力する（Eleventy のプラグインまたはテンプレート部品で実装）。
   * HTML の `<html lang="ja">` のように `lang` 属性を指定する。
   * パンくずリストを設置し、カテゴリ階層を反映して表示する。

7. **レスポンシブ対応**

   * モバイルファースト設計。
   * ブレークポイント例：

     * 320px–480px：スマホ小サイズ（1カラム）
     * 481px–768px：タブレット縦向き（1カラムまたは2カラム）
     * 769px–1024px：タブレット横向き/ノートPC（2カラム）
     * 1025px以上：デスクトップ（2カラム＋サイドバー固定）
   * モバイル時はハンバーガーメニューまたはドロワーメニュー化する。

8. **ナビゲーション**

   * サイトロゴまたはテキストロゴをクリックでトップページへ遷移する。
   * グローバルナビゲーションに固定ページ（About、Contact など）のリンクを表示する。
   * カテゴリ一覧へのドロップダウンメニューを実装する。

9. **ローカルプレビュー**

   * `npm run dev` コマンドを用意し、Eleventy のリーンビルド＋ローカルサーバー起動（Browsersync など）でプレビューできるようにする。
   * ソースを保存すると自動ビルド・自動リロードされる。

10. **GitHub Pages 連携（自動ビルド＆デプロイ）**

    * `main` ブランチにプッシュすると GitHub Actions がビルドを実行し、生成した静的ファイルを `gh-pages` ブランチにデプロイする。
    * `baseUrl` や `pathPrefix` を Eleventy 設定およびテンプレート内で適切に設定する（リポジトリ名がサブディレクトリになる場合を考慮）。
    * カスタムドメインを利用する場合、リポジトリ直下に `CNAME` ファイルを配置し、DNS 設定を行う。

### 5.2. 推奨機能（拡張項目）

1. **検索機能（クライアントサイド）**

   * Eleventy ビルド時に全記事を JSON 形式で出力し（例：`public/search_index.json`）、Lunr.js などでクライアントサイド検索を実装する。
   * 検索 UI をトップページまたはナビゲーションバーに設置し、キーワード検索に対応する。

2. **コメント機能連携**

   * GitHub Issues を利用したコメントシステム（Utterances、Giscus など）を導入可能にする。
   * Disqus などの外部コメントプラットフォームを設定できるテンプレート部品を用意する。

3. **多言語対応**

   * `src/posts/en/`、`src/posts/ja/` のように言語別ディレクトリを分けて記事を管理する。
   * `_data/` 以下に `i18n/ja.json`、`i18n/en.json` のような UI 文言ファイルを用意し、テンプレートで参照できるようにする。
   * サイトメニューに言語切替のドロップダウンを設置し、URL に言語プレフィックスを付与する（例：`/en/`、`/ja/`）。

4. **テーマ切り替え（ダークモード対応）**

   * CSS カスタムプロパティ（Variables）を利用してライト／ダークテーマを切り替えられるようにする。
   * `prefers-color-scheme` メディアクエリを使って OS の設定に追随し、初期テーマを自動選択する。
   * ユーザーが手動でテーマを切り替えるスイッチを設置する。

5. **パフォーマンス最適化**

   * 画像最適化プラグイン（例えば Eleventy-Plugin-Image）や build 時の Sharp 呼び出しで複数サイズのレスポンシブ画像を生成する。
   * CSS / JS の最小化（Minify）をビルドスクリプト内で実行し、ファイルサイズを削減する。
   * CSS / JS に対してキャッシュバスティング用のハッシュを付与する仕組みを取り入れる。

6. **PWA（プログレッシブ Web アプリ）対応**

   * `manifest.json` を生成し、アプリアイコンやテーマカラーを設定する。
   * サービスワーカーを実装し、静的ファイルをキャッシュすることでオフライン閲覧をサポートする。

7. **アーカイブ機能**

   * Eleventy の Collections 機能とテンプレートを組み合わせて、年別・月別アーカイブページを自動生成する。
   * アーカイブページでは該当年月の全記事と記事件数を一覧表示する。

8. **著者情報管理**

   * `src/_data/authors.json` に著者ごとのプロフィール情報（名前、プロフィール画像URL、SNSリンクなど）を定義する。
   * 記事 Front Matter に `author: 著者ID` を追加し、記事詳細ページで該当著者情報を表示する。
   * 著者一覧ページを自動生成し、各著者のすべての記事を一覧できるようにする。

9. **CI テスト・Lint**

   * GitHub Actions で以下のチェックを行うジョブを定義：

     * リンクチェック（`html-validate`、`eleventy-plugin-check-links` など）
     * HTML アクセシビリティチェック（`pa11y-ci`）
     * CSS Lint（`stylelint`）、JavaScript Lint（`eslint`）、Markdown Lint（`markdownlint`）
   * プルリクエスト開発フロー時に自動でこれらのチェックを実行し、エラーを検知する。

10. **セキュリティ対策**

    * CDN や外部スクリプトを読み込む場合は、SRI (`integrity` 属性) を付与して改ざんリスクを低減する。
    * HTML `<meta>` タグで Content Security Policy を指定し、外部リソースの読み込みを制限する。
    * プライバシー対策として Google Analytics や外部トラッキングを導入する場合はクッキーバナーや同意取得バナーを表示する。
    * コメント欄（Utterances／Giscus）を導入する際、リポジトリ権限設定や Issues 設定を適切に行い、不正投稿を防止する。

## 6. 詳細設計

### 6.1. package.json の例

```jsonc
{
  "name": "my-eleventy-blog",
  "version": "1.0.0",
  "description": "GitHub Pages + Eleventy で構築する静的ブログ",
  "author": "Your Name <you@example.com>",
  "license": "MIT",
  "scripts": {
    "dev": "eleventy --serve --input src --output public --watch",
    "build": "eleventy --input src --output public",
    "clean": "rimraf public",
    "lint:css": "stylelint \"src/assets/css/**/*.scss\"",
    "lint:js": "eslint \"src/assets/js/**/*.js\"",
    "lint:md": "markdownlint \"src/**/*.md\"",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d public"
  },
  "dependencies": {
    "@11ty/eleventy": "^2.0.0",
    "nunjucks": "^3.2.3",
    "sass": "^1.64.1"
  },
  "devDependencies": {
    "eslint": "^8.48.0",
    "gh-pages": "^5.0.0",
    "markdownlint": "^0.34.0",
    "pa11y-ci": "^6.2.0",
    "rimraf": "^5.0.0",
    "stylelint": "^15.14.0"
  }
}
```

* `dev`：Eleventy の開発サーバー起動（ソース `src/` → 出力 `public/`、ウォッチモード付き）。
* `build`：本番用ビルド（`src/` → `public/`）。
* `clean`：`public/` を削除してクリーンアップ。
* `lint:*`：CSS、JavaScript、Markdown の Lint チェックコマンド。
* `predeploy`：デプロイ前に実行されるビルドコマンド（GitHub Actions 内で使う）。
* `deploy`：`public/` を `gh-pages` ブランチにデプロイするコマンド。

### 6.2. Eleventy 設定（`.eleventy.js`）

```js
module.exports = function(eleventyConfig) {
  // Markdown のパース設定（必要ならカスタマイズ）
  eleventyConfig.setLibrary("md", require("markdown-it")({
    html: true,
    linkify: true,
    typographer: true
  }));

  // パス別のテンプレートエンジン指定
  eleventyConfig.setTemplateFormats(["md", "njk", "html", "liquid"]);

  // ディレクトリ構成
  return {
    dir: {
      input: "src",
      includes: "_includes",
      layouts: "_layouts",
      data: "_data",
      output: "public"
    },
    templateFormats: ["njk", "md", "html"],
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    dataTemplateEngine: "njk",
    passthroughFileCopy: true
  };
};
```

* `setLibrary("md", …)`：Markdown-it を使って Markdown をパースし、HTML 生成をカスタマイズ。
* `setTemplateFormats([...])`：Eleventy がビルド対象とするファイル拡張子を指定。
* `dir` 設定：

  * `input: "src"`：ソースコードディレクトリを `src/` にする。
  * `includes: "_includes"`：テンプレート用パーシャルを `src/_includes/` 配下に配置。
  * `layouts: "_layouts"`：レイアウトを `src/_layouts/` 配下に配置。
  * `data: "_data"`：サイト全体で参照するデータファイル（ナビゲーション、著者情報など）を `src/_data/` 配下に配置。
  * `output: "public"`：ビルド成果物を `public/` に出力。

### 6.3. テンプレート構成

#### 6.3.1. ベースレイアウト（`src/_layouts/base.njk`）

```njk
<!DOCTYPE html>
<html lang="ja">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{% if page.title %}{{ page.title }} | {% endif %}{{ site.title }}</title>
    <meta name="description" content="{% if page.description %}{{ page.description }}{% else %}{{ site.description }}{% endif %}" />
    <!-- Open Graph -->
    <meta property="og:title" content="{{ page.title | default(site.title) }}" />
    <meta property="og:description" content="{% if page.description %}{{ page.description }}{% else %}{{ site.description }}{% endif %}" />
    <meta property="og:type" content="website" />
    <meta property="og:url" content="{{ site.url }}{{ page.url }}" />
    <meta property="og:image" content="{{ site.url }}{% if page.thumbnail %}{{ page.thumbnail }}{% else %}{{ site.default_thumbnail }}{% endif %}" />
    <!-- CSS / スタイル -->
    <link rel="stylesheet" href="{{ '/assets/css/style.css' | url }}" />
    <!-- その他 head 内に必要な要素を追加 -->
  </head>
  <body>
    {% include "header.njk" %}
    <main class="container">
      {{ content | safe }}
    </main>
    {% include "footer.njk" %}
    <!-- クライアントサイド JS 読み込み -->
    <script src="{{ '/assets/js/main.js' | url }}"></script>
  </body>
</html>
```

* `<html lang="ja">`：サイト言語を日本語に設定。
* `<meta>`：SEO／OGP 用のタグを動的に出力。
* `<link rel="stylesheet">`：ビルド後の CSS を読み込む。

#### 6.3.2. ヘッダー部品（`src/_includes/header.njk`）

```njk
<header class="site-header">
  <div class="inner">
    <h1 class="site-logo">
      <a href="{{ '/' | url }}">{{ site.title }}</a>
    </h1>
    <nav class="global-nav">
      <ul>
        {% for item in navigation.main %}
          <li class="nav-item">
            {% if item.subitems %}
              <div class="dropdown">
                <a href="#">{{ item.title }}</a>
                <ul class="dropdown-menu">
                  {% for sub in item.subitems %}
                    <li><a href="{{ sub.url }}">{{ sub.title }}</a></li>
                  {% endfor %}
                </ul>
              </div>
            {% else %}
              <a href="{{ item.url }}">{{ item.title }}</a>
            {% endif %}
          </li>
        {% endfor %}
      </ul>
    </nav>
    <button class="nav-toggle" aria-label="Toggle Navigation">
      &#9776;
    </button>
  </div>
</header>
```

* `navigation.main`：`src/_data/navigation.json` の内容を参照してメニューを生成。
* モバイル時にハンバーガーメニューを表示するトグルボタンを設置。

#### 6.3.3. フッター部品（`src/_includes/footer.njk`）

```njk
<footer class="site-footer">
  <div class="inner">
    <p>&copy; {{ new Date().getFullYear() }} {{ site.author }}. All rights reserved.</p>
    <ul class="social-links">
      <li><a href="https://twitter.com/{{ site.twitter_username }}" aria-label="Twitter">Twitter</a></li>
      <li><a href="https://github.com/{{ site.github_username }}" aria-label="GitHub">GitHub</a></li>
    </ul>
  </div>
</footer>
```

* サイト運営者情報を `package.json` や `src/_data/site.json`（必要なら別途）で定義して参照。

#### 6.3.4. トップページレイアウト（`src/_layouts/home.njk`）

```njk
{% extends "base.njk" %}

{% block content %}
  <div class="post-list">
    {% for post in collections.posts | reverse | slice(0, 10) %}
      <article class="post-card">
        <a href="{{ post.url }}">
          <figure class="thumb">
            <img src="{{ post.data.thumbnail }}" alt="{{ post.data.title }}" />
          </figure>
          <div class="post-info">
            <h2>{{ post.data.title }}</h2>
            <time datetime="{{ post.date }}">{{ post.date | date("yyyy-MM-dd") }}</time>
            <p>{{ post.data.description }}</p>
          </div>
        </a>
      </article>
    {% endfor %}
  </div>
  {% if collections.posts | length > 10 %}
    <nav class="pagination">
      <a href="/page/2/" class="next">→ Older Posts</a>
    </nav>
  {% endif %}
{% endblock %}
```

* `collections.posts`：Eleventy のデフォルトコレクションで、`src/posts/*.md` から取得した記事一覧。
* `reverse`：日付が古い順にソートされている場合、最新記事を先頭にするために逆順。
* ページネーションは Eleventy の Pagination 機能でさらに細かく制御可能。

#### 6.3.5. 記事ページレイアウト（`src/_layouts/post.njk`）

```njk
{% extends "base.njk" %}

{% block content %}
  <article class="post-detail">
    <header class="post-header">
      <h1>{{ title }}</h1>
      <time datetime="{{ date }}">{{ date | date("yyyy-MM-dd") }}</time>
      {% if data.categories %}
        <ul class="categories">
          {% for cat in data.categories %}
            <li><a href="/categories/{{ cat | slug }}/">{{ cat }}</a></li>
          {% endfor %}
        </ul>
      {% endif %}
      {% if data.tags %}
        <ul class="tags">
          {% for tag in data.tags %}
            <li><a href="/tags/{{ tag | slug }}/">{{ tag }}</a></li>
          {% endfor %}
        </ul>
      {% endif %}
      {% if data.thumbnail %}
        <figure class="post-thumbnail">
          <img src="{{ data.thumbnail }}" alt="{{ title }}" />
        </figure>
      {% endif %}
    </header>

    <section class="post-content">
      {{ content | safe }}
    </section>

    <nav class="post-navigation">
      {% if pagination.previous %}
        <a href="{{ pagination.previous.url }}" class="prev">← {{ pagination.previous.data.title }}</a>
      {% endif %}
      {% if pagination.next %}
        <a href="{{ pagination.next.url }}" class="next">{{ pagination.next.data.title }} →</a>
      {% endif %}
    </nav>

    {% include "social-share.njk" %}
    {% if site.comments %}
      <div id="comments">
        <!-- Utterances や Giscus のスクリプトをここに挿入 -->
      </div>
    {% endif %}
  </article>
{% endblock %}
```

* `title`、`date`、`data.categories`、`data.tags` などは Front Matter のデータを参照。
* `pagination.previous` / `pagination.next` は Eleventy の Pagination 機能を使って前後記事を取得。
* シンタックスハイライトを行うために、`<pre><code>` ブロックは CSS／JS を別途準備。

#### 6.3.6. カテゴリ一覧レイアウト（`src/_layouts/category.njk`）

```njk
{% extends "base.njk" %}

{% block content %}
  <h1>カテゴリ: {{ category }}</h1>
  <div class="post-list">
    {% for post in collections.posts | filter(post => post.data.categories && post.data.categories.includes(category)) %}
      <article class="post-card">
        <a href="{{ post.url }}">
          <figure class="thumb">
            <img src="{{ post.data.thumbnail }}" alt="{{ post.data.title }}" />
          </figure>
          <div class="post-info">
            <h2>{{ post.data.title }}</h2>
            <time datetime="{{ post.date }}">{{ post.date | date("yyyy-MM-dd") }}</time>
            <p>{{ post.data.description }}</p>
          </div>
        </a>
      </article>
    {% endfor %}
  </div>
{% endblock %}
```

* `category` はページ作成時に Front Matter で指定する変数。
* Eleventy の Filter 機能で、対象カテゴリを含む記事のみを抽出。

#### 6.3.7. タグ一覧レイアウト（`src/_layouts/tag.njk`）

```njk
{% extends "base.njk" %}

{% block content %}
  <h1>タグ: {{ tag }}</h1>
  <div class="post-list">
    {% for post in collections.posts | filter(post => post.data.tags && post.data.tags.includes(tag)) %}
      <article class="post-card">
        <a href="{{ post.url }}">
          <figure class="thumb">
            <img src="{{ post.data.thumbnail }}" alt="{{ post.data.title }}" />
          </figure>
          <div class="post-info">
            <h2>{{ post.data.title }}</h2>
            <time datetime="{{ post.date }}">{{ post.date | date("yyyy-MM-dd") }}</time>
            <p>{{ post.data.description }}</p>
          </div>
        </a>
      </article>
    {% endfor %}
  </div>
{% endblock %}
```

* `tag` は Front Matter または Eleventy Collection のコンテキストで指定する変数。
* フィルタリングロジックはカテゴリと同様に実装。

#### 6.3.8. RSS フィードテンプレート（`src/rss.xml`）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>{{ site.title }}</title>
    <link>{{ site.url }}</link>
    <description>{{ site.description }}</description>
    {% for post in collections.posts | reverse | slice(0, 20) %}
      <item>
        <title>{{ post.data.title }}</title>
        <link>{{ site.url }}{{ post.url }}</link>
        <pubDate>{{ post.date | date("EEE, dd MMM yyyy HH:mm:ss Z") }}</pubDate>
        <description>{{ post.data.description }}</description>
      </item>
    {% endfor %}
  </channel>
</rss>
```

* 最新 20 件の記事をフィードアイテムとして出力。
* Eleventy がこのファイルをテンプレートとして処理し、ビルド後 `public/rss.xml` として生成。

### 6.4. ナビゲーション設定（`src/_data/navigation.json`）

```jsonc
{
  "main": [
    {
      "title": "Home",
      "url": "/"
    },
    {
      "title": "About",
      "url": "/about/"
    },
    {
      "title": "Categories",
      "subitems": [
        {
          "title": "Tech",
          "url": "/categories/Tech/"
        },
        {
          "title": "Eleventy",
          "url": "/categories/Eleventy/"
        }
      ]
    },
    {
      "title": "Tags",
      "subitems": [
        {
          "title": "JavaScript",
          "url": "/tags/JavaScript/"
        },
        {
          "title": "StaticSite",
          "url": "/tags/StaticSite/"
        }
      ]
    }
  ]
}
```

* `navigation.main` を Eleventy のデータとして参照し、`header.njk` でループしてメニューを生成する。
* JSON フォーマットを採用することで、JavaScript でアクセスしやすい。

## 7. 運用フロー

### 7.1. 初期セットアップ

1. **GitHub リポジトリ作成**

   * リポジトリ名を `username.github.io` にすると、プッシュするだけで Pages がルート公開される。
   * それ以外のリポジトリ名を使う場合は、GitHub Pages の設定でブランチ（通常は `gh-pages`）を公開先に指定する。

2. **ローカル環境構築**

   ```bash
   # リポジトリをクローン
   $ git clone https://github.com/username/repo-name.git
   $ cd repo-name

   # Node.js と npm がインストール済みであることを確認
   $ node -v
   $ npm -v

   # 依存パッケージをインストール
   $ npm install
   ```

3. **Eleventy プロジェクト構築**

   * `package.json` の `scripts` セクションで以下を定義しておく：

     ```jsonc
     "scripts": {
       "dev": "eleventy --serve --input src --output public --watch",
       "build": "eleventy --input src --output public",
       "clean": "rimraf public",
       "deploy": "gh-pages -d public"
     }
     ```
   * `.eleventy.js` をプロジェクトルートに作成し、先述の Eleventy 設定を記述。
   * `src/` 配下にディレクトリ構成を整備し、テンプレートファイルや記事サンプルを配置。

4. **SCSS ビルド環境構築**

   * `sass` パッケージを依存に追加済みであれば、`style.scss` を `public/assets/css/style.css` にビルドする npm スクリプトを追加しておく。例：

     ```jsonc
     "scripts": {
       "css:build": "sass src/assets/css/style.scss public/assets/css/style.css --no-source-map --style=compressed"
     }
     ```
   * Eleventy の前後フックとして `eleventyConfig.on('beforeBuild', ...)` で CSS ビルドを走らせることも可能。

5. **GitHub Actions ワークフロー作成**

   * `.github/workflows/deploy.yml` を作成し、`main` ブランチにプッシュされたらビルド → `gh-pages` にデプロイする設定を記述。

### 7.2. ローカルプレビュー

```bash
# 開発サーバー起動
$ npm run dev
```

* Eleventy が `src/` を監視しながらビルドし、Browsersync が `public/` を提供。
* `http://localhost:8080`（デフォルト）またはログに表示されるローカルURLにアクセスすると、変更内容がリアルタイムにブラウザに反映される。

### 7.3. 記事追加手順

1. `src/posts/` ディレクトリに Markdown ファイルを追加する。

   * ファイル名：`YYYY-MM-DD-slug.md` 形式を推奨。
   * Front Matter を記述し、本文を Markdown で執筆。

2. Git でコミット & プッシュ

   ```bash
   $ git add src/posts/2025-06-10-new-post.md
   $ git commit -m "Add new post: 新しい記事"
   $ git push origin main
   ```

3. GitHub Actions がトリガーされ、自動的にビルド → `gh-pages` ブランチにデプロイされる。

4. 数分以内に GitHub Pages 上のサイトが更新される。

### 7.4. 拡張機能追加の流れ

1. **検索機能を追加する場合**

   * Eleventy のコレクションから全記事のデータを JSON にまとめるファイル（例：`src/search_index.json`）を生成するテンプレートやスクリプトを用意し、`eleventyConfig.addCollection` の中でビルド時に出力。
   * フロントエンドで Lunr.js を読み込み、`search_index.json` をフェッチして全文検索 UI を実装する。

2. **コメント機能を追加する場合**

   * Utterances や Giscus を使う設定スクリプトを `src/_includes/comments.njk` のように部品化し、記事ページのテンプレートからインクルードする。
   * リポジトリ情報（owner, repo, issue term など）を設定変数として Eleventy のデータファイルで管理する。

3. **多言語対応を行う場合**

   * `src/i18n/ja.json`、`src/i18n/en.json` のように文言ファイルを用意する。
   * `src/posts/ja/`、`src/posts/en/` などに記事を分け、Eleventy の設定で各言語ディレクトリをコレクションとして扱う。
   * 言語別のビルドターゲット（例：`/ja/`、`/en/`）をルーティング設定して、テンプレート側で `lang` 属性を動的に設定する。

4. **プラグイン非対応機能を導入する場合**

   * Node.js のカスタムビルドスクリプトを `package.json` の `build` コマンドに追加し、必要な処理（画像リサイズ、CSS/JS ミニファイなど）を組み込む。
   * GitHub Actions ワークフローで `npm run build` を実行し、成果物を `gh-pages` ブランチにプッシュするように定義する。

## 8. GitHub Actions ワークフロー例（`.github/workflows/deploy.yml`）

```yaml
name: Build and Deploy Eleventy Site

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '18.x'

      - name: Install dependencies
        run: npm ci

      - name: Build CSS
        run: npm run css:build

      - name: Build Eleventy site
        run: npm run build

      - name: Deploy to GitHub Pages
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: public
          publish_branch: gh-pages
          # optional: custom domain を使う場合
          # cname: example.com
```

* `actions/checkout@v4`：リポジトリをチェックアウト。
* `actions/setup-node@v3`：Node.js 環境をセットアップ。
* `npm ci`：`package-lock.json` に基づきクリーンインストール。
* `npm run css:build`：SCSS → CSS ビルド。
* `npm run build`：Eleventy ビルド（`src/` → `public/`）。
* `peaceiris/actions-gh-pages@v4`：`public/` ディレクトリを `gh-pages` ブランチにデプロイ。
* `github_token`：`Secrets` に自動提供されるトークンを利用。

## 9. セキュリティ・運用上の注意

* **パッケージ依存管理**：`npm audit` を定期的に実行して脆弱性をチェックし、必要に応じてアップデートする。
* **外部スクリプトの SRI**：CDN から読み込む場合、可能であれば SRI（`integrity` 属性）を追加して改ざんを防止する。
* **CSP（Content Security Policy）**：`<meta http-equiv="Content-Security-Policy">` を設定し、外部リソースアクセスを制限する。
* **コメント機能の設定**：Utterances や Giscus を導入する場合、Issues や Discussion の権限を適切に設定し、不正投稿を防止する。
* **Google Analytics / トラッキング**：プライバシー保護のため、必要に応じてクッキーバナーや同意取得バナーを実装し、GDPR に対応する。

## 10. 用語定義

* **Eleventy (11ty)**：Node.js ベースの静的サイトジェネレータ。軽量かつ柔軟なテンプレートエンジンをサポートする。
* **Front Matter**：Markdown ファイル先頭に記述する YAML 形式のメタデータ。
* **テンプレートエンジン**：HTML に埋め込む変数やループ、条件分岐などを扱う仕組み。Eleventy では Nunjucks、Liquid、Handlebars など複数選択可能。
* **Collection**：Eleventy がソースディレクトリ内から収集するコンテンツのグループ。記事一覧やカテゴリ別一覧を扱う際に利用する。
* **Pagination**：コレクションをページ単位に分割して生成する機能。Eleventy の組み込み機能またはプラグインを利用する。
* **OGP (Open Graph Protocol)**：SNS でシェアされた際に表示されるタイトル・説明・画像を指定するメタタグの仕様。
* **GitHub Actions**：GitHub リポジトリ上で CI/CD ワークフローを自動化できる仕組み。

## 11. 参考情報・リンク

* [Eleventy 公式ドキュメント](https://www.11ty.dev/docs/)
* [GitHub Pages ヘルプ](https://docs.github.com/pages)
* [Nunjucks テンプレート言語リファレンス](https://mozilla.github.io/nunjucks/)
* [Sass (SCSS) 公式ドキュメント](https://sass-lang.com/documentation)
* [Eleventy Collections](https://www.11ty.dev/docs/collections/)
* [Eleventy Pagination](https://www.11ty.dev/docs/pagination/)
* [Utterances 設定ガイド](https://utteranc.es/)
* [Lunr.js 公式サイト](https://lunrjs.com/)
* [GitHub Actions ドキュメント](https://docs.github.com/actions)

以上が、Node.js（Eleventy）を用いてビルドする GitHub Pages ブログソフトの仕様書です。必要に応じて各セクションをカスタマイズし、実際の開発を進めてください。
