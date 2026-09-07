---
name: open-md-in-obsidian-not-notion
description: vault内の.mdを `open` で開くとNotionアプリが立ち上がる。Obsidianで開くには obs_open.sh（obsidian://URI）を使う
metadata:
  type: feedback
---

Mac の .md 既定アプリは Notion。`open <file>.md` は Notion で開いてしまう（2026-09-06 に発生・草川「いやnotionで開かれた 改善を」）。

**Why:** 議会文書の正本は Obsidian vault（[[project_obsidian_vault_workflow]]）。Notionで開くと注記が正本に入らない。

**How to apply:** vault内ファイルを開く指示は `~/.claude/scripts/obs_open.sh <path>`（obsidian://open?vault=ObsidianVault&file=<相対パスURLエンコード>）。`open` や `open -e` は使わない。

**2026-09-07追記（窓が無いと開かない）**: Obsidianが常駐したまま窓だけ閉じられていると `obsidian://open` は何も起きない。手順は ①`osascript -e 'tell application "Obsidian" to activate'` → ②`count windows of process "Obsidian"` が0なら quit→`open -a Obsidian`→5秒待つ → ③URIで開く → ④`name of windows` にファイル名が出たことを確認してから「開いた」と言う。obs_open.sh へのこの組み込みは@日曜改修。
