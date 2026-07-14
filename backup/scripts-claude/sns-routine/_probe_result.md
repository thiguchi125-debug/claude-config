# Task 3 検証記録（headless claude -p 能力検証）2026-07-14

## Step 1: headless基本実行
- `claude` 実体: `/Users/kusakawatakuya/.local/bin/claude`
- `cd ~ && claude -p "1+1の答えだけを出力せよ"` → `2` ✅

## Step 2: Notion MCP到達性
- `claude -p "mcp__claude_ai_Notion__notion-fetch で 391cf503-a68f-8191-b218-e80fdc7aedeb を取得しタイトル出力…" --allowedTools "mcp__claude_ai_Notion__notion-fetch"`
- 出力: `📥未分類インテーク` ✅

## 判定: **PATH A（headlessからNotion MCP直接書込可）**
- triage_prompt.mdのNotion直接書込が主経路。queue退避（_notion_queue.jsonl）は障害時フォールバックとして維持。
- ohayoのqueue flush手順は「queueが非空のときのみ」の軽量運用でよい（Task 6）。

## 注意
- 本検証は対話セッション由来のシェル環境で実施。launchdコンテキスト（環境変数最小）での同等動作は Task 5 Step 3 のkickstart実走で最終確認する。認証エラー時はplistのEnvironmentVariablesを拡張。
