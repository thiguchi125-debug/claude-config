---
name: obsidian-vault-workflow
description: 2026-09-06導入。Obsidian(brew cask 1.13.7)＝草川の読み書き画面。議会文書の正本はvault、Notionは完成後の鏡
metadata:
  type: project
---

Obsidianを2026-09-06に導入（`brew install --cask obsidian`）。vault＝`~/Documents/ObsidianVault/`（4月13日作成の骨組みを再利用）。

- 9月議会 想定質問の正本＝`ObsidianVault/20_議会活動/2026-09_一般質問/想定質問の流れ_v7_件名1-2_注記反映.md`。drafts側の旧名はシンボリックリンク。
- vault内リンク：`20_議会活動/drafts`→drafts／`30_政策調査/research_ledger`／`10_ClaudeCode/引き継ぎメモ`→handoff/archive
- 草川の注記は行内 `#注記` タグ。`grep -n "#注記"` で拾う（「→」は本文で使用済みなので目印にしない）
- 方針の正本＝vault `10_ClaudeCode/設定/Obsidian活用方針_2026-09-06.md`

**Why:** TextEditでmdが読みにくい・書きにくい。Notionを正本にすると1回150K。
**How to apply:** 開いているファイルは上書きせず新版（v8…）で出す。草川が「注記入れた」と言ってから読む。Obsidianで直した発信物も安全ゲート再通過。関連 [[ippan-shitsumon-2026-09]]
