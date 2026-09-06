---
name: open-md-in-obsidian-not-notion
description: vault内の.mdを `open` で開くとNotionアプリが立ち上がる。Obsidianで開くには obs_open.sh（obsidian://URI）を使う
metadata:
  type: feedback
---

Mac の .md 既定アプリは Notion。`open <file>.md` は Notion で開いてしまう（2026-09-06 に発生・草川「いやnotionで開かれた 改善を」）。

**Why:** 議会文書の正本は Obsidian vault（[[project_obsidian_vault_workflow]]）。Notionで開くと注記が正本に入らない。

**How to apply:** vault内ファイルを開く指示は `~/.claude/scripts/obs_open.sh <path>`（obsidian://open?vault=ObsidianVault&file=<相対パスURLエンコード>）。`open` や `open -e` は使わない。
