---
name: Notion内部リンクは mention-page タグ必須
description: Notionページ本文に他のNotionページへのリンクを書くときは普通のマークダウンリンク [text](url) ではなく <mention-page url="..."> タグを使う。markdown linkはモバイルでブラウザに飛ぶがmention-pageはアプリ内ネイティブ遷移する
type: feedback
originSessionId: f734c400-d1a8-4b64-9f3b-5072331e4422
---
Notionページ本文に他のNotionページへのリンクを書くときは、必ず以下の形式を使う：

```
<mention-page url="https://app.notion.com/p/<page-id>">ページタイトル</mention-page>
```

普通のマークダウンリンク `[text](url)` は **絶対に使わない**（モバイルでブラウザに飛ばされる）。

**Why:**
2026-05-01に3回検証してようやく真の原因判明：
1. 1回目：`https://www.notion.so/...` → `notion://www.notion.so/...` deep-link置換 → API正規化で剥がれて失敗
2. 2回目：`app.notion.com/p/...` 形式統一 → 「まだ飛ばない」
3. 3回目：マークダウン表示テキストのURL露出を修正 → 「まだ飛ばない」
4. 真の答え：**Notion enhanced-markdown仕様書 (`notion://docs/enhanced-markdown-spec`) が定義する `<mention-page url="...">タイトル</mention-page>` インライン参照タグ**

普通のマークダウンリンク `[text](https://app.notion.com/p/xxx)` はNotionモバイルアプリが「外部URL」として扱うためブラウザ経由になる。`<mention-page>` タグはサーバー側で実ページとして解決され、@-mentionと同等にアプリ内ネイティブ遷移する。仕様書も「Mentions are clickable and link to the entity」と明記。

**How to apply:**
- Notionページ本文に他のNotionページを参照するときは、**必ず `<mention-page url="https://app.notion.com/p/<id>">タイトル</mention-page>` 形式**
- 自己閉じ形式 `<mention-page url="..." />` も可（その場合Notionが自動でタイトル解決して展開）
- 普通のマークダウンリンク `[text](url)` は **Notion内部ページには絶対使わない**（外部URL専用）
- `<page url="...">` **ブロック**タグは別物（subpageを意味する）。これをmentionと混同するとページ削除・移動の破壊的操作になる。インライン参照には絶対使わない
- href部分の形式は `https://app.notion.com/p/<id>` でも `https://www.notion.so/<id>` でも可（API側で `app.notion.com` に正規化される）が、統一感のため `app.notion.com/p/` 推奨
- 外部URL（Drive・自治体・SNS・ニュース等）は普通のマークダウンリンク `[text](url)` のままでOK。`<mention-page>` はNotion内部ページ専用

**既存ページ修正実績（2026-05-01・3回目で本当の修正）:**
- 13ページ・約110リンクを `<mention-page>` 形式に変換
- 🌅朝のダッシュボード38本／📔デイリーサマリ4件43本／🗺️ナビゲーションマップ15本／🎯政策アップデートハブ4本／🎯マイスキル/エージェント一覧7本／🤝地域挨拶集1本／🗂️会議ハブ6本／📅毎日のルーティン3本
- 失敗1本：朝のダッシュボード内「三重県南海トラフ被害想定」ニュース項目（NotionのUnicode正規化バグで「市町」が異なるコードポイントとして返却され update_content の old_str マッチ失敗）

**全スキル・エージェントへの適用必須:**
ohayo / oyasumi / nichijo / iken / policy-update / content-pipeline / notion-saver / その他Notionに書き込む全スキル・全エージェントに横断適用。**新規ページ生成時は最初から `<mention-page>` 形式で書く**こと。既に普通のマークダウンリンク形式で生成してしまったら必ず `<mention-page>` に変換してから保存。
