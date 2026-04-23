---
name: claude-config バックアップリポジトリ
description: Claude Code CLIの設定・エージェント・スキル・記憶のGitHubバックアップ場所と復元手順
type: reference
originSessionId: bf1df9e4-cd8d-4fb1-9849-3b3df682f40d
---
Claude Code CLIの引き継ぎ用リポジトリ: https://github.com/thiguchi125-debug/claude-config (private)

**場所**: `~/claude-config/`

**自動同期**: `~/.claude/settings.json` のStop hookで、セッション終了毎に `scripts/sync-to-git.sh` が走り GitHub へ auto push。

**バックアップ対象** (`backup/` 配下):
- `agents/` — カスタムエージェント
- `commands/` — slash commands
- `settings/` — settings.json, settings.local.json
- `memory/` — MEMORY.md と記憶ファイル群
- `skills/` — ohayo, nichijo, content-pipeline 等カスタムスキル
- `plugins-meta/` — installed_plugins.json

**新PC復元手順**:
1. `npm install -g @anthropic-ai/claude-code` && `claude` で認証
2. `git clone https://github.com/thiguchi125-debug/claude-config.git ~/claude-config`
3. `~/claude-config/scripts/restore.sh`

**手動同期**: `~/claude-config/scripts/sync-to-git.sh`

詳細は `~/claude-config/README.md`。
