---
name: Notionリンクは notion:// スキーム必須
description: Notionページ内に貼るNotionリンクは https://www.notion.so/ ではなく notion://www.notion.so/ で生成する。スマホ/PCとも直接アプリ起動するため
type: feedback
originSessionId: f734c400-d1a8-4b64-9f3b-5072331e4422
---
Notionページ内に他のNotionページへのリンクを貼るとき、URLは **必ず `notion://www.notion.so/...` 形式** で出力する。`https://www.notion.so/...` は使わない。

**Why:**
2026-05-01に草川から指摘。`https://www.notion.so/...` 形式だと、スマホからだとブラウザに一度飛んでしまいNotionアプリが起動しない（PC版でも一度Webページ経由になる）。`notion://` スキームならスマホ/PCとも直接Notionアプリで開く。アプリ未インストール時はWebに自動フォールバック。

**How to apply:**
- Notion MCP（mcp__claude_ai_Notion__*）でページ作成・更新時、本文中にNotionリンクを埋める場合は `notion://www.notion.so/<page-slug-or-id>` 形式で書く
- 既存ページのURLが `https://www.notion.so/xxx` なら、機械的に `notion://www.notion.so/xxx` に置換するだけでOK
- 外部URL（Google Drive・自治体サイト等）は通常通り `https://...` のまま
- 朝ダッシュボード、おやすみサマリ、タスクDB、政策候補DB、市民意見BOX、AIインタビューconfig等、横断リンクを多用する全DBに適用
- Notion内の「ページメンション（@参照）」が使える場合はそちらが最も確実だが、MCPで生のURLを書く場面では `notion://` スキームを徹底
- ohayo/oyasumi/nichijo/iken/policy-update/content-pipeline 等、Notionリンクを生成する全スキル・全エージェントに適用される横断ルール
