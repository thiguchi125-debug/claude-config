---
name: Notion内部リンクは app.notion.com 形式で書く
description: Notionページ本文に貼るNotion内部リンクは https://app.notion.com/p/<id> 形式で出力。www.notion.so よりモバイルアプリへのハンドオフが効きやすい。notion:// スキームはAPI保存時に剥がされるので使わない
type: feedback
originSessionId: f734c400-d1a8-4b64-9f3b-5072331e4422
---
Notionページ本文に他のNotionページへのリンクを貼るときは **`https://app.notion.com/p/<page-id>`** 形式で書く。`https://www.notion.so/...` は使わない。

**Why:**
2026-05-01に草川から「スマホからリンクが飛ばない／PCもWeb経由で遠回り」と指摘。当初は `notion://www.notion.so/...` deep-linkスキーム置換で対応しようとしたが、検証の結果 **Notion MCP API（update_content）はNotion内部URLを保存時に強制的に `https://app.notion.com/p/...` 形式へ正規化する**ことが判明。`notion://` を書き込んでも剥がされる。一方 `app.notion.com/p/` 形式は `www.notion.so/` より iOS/Android のNotionアプリへハンドオフが効きやすく、原タスクの意図（タップ即アプリ起動）にほぼ近い挙動をする。

**How to apply:**
- Notion MCPでページ作成・更新時、本文中のNotion内部リンクは `https://app.notion.com/p/<id>` 形式で書く（生成段階で意識する）
- `https://www.notion.so/...` 形式が混入したら、そのまま update_content で `https://app.notion.com/p/...` に置換すれば API の正規化と整合する
- `notion://` スキームは Notion 本文に書いても保存時に剥がされるので無駄。**Notion DB に保存しない外部発信物（メール本文／SNSプロフィール／印刷QRコード等）に限り** `notion://` を採用すれば deep-link として機能する
- 外部URL（Google Drive・自治体サイト・SNS等）は通常通り `https://...` のまま、置換対象外
- 既存ページ修正実績：2026-05-01に直近1週間（04-24〜05-01）作成ページ約60件を走査、6ページ14リンクを `app.notion.com/p/` 形式へ統一済み（デイリーサマリ4件・エージェントトリガー一覧・会議ハブ）
- ohayo/oyasumi/nichijo/iken/policy-update/content-pipeline 等、Notionリンクを生成する全スキル・全エージェントに適用される横断ルール
