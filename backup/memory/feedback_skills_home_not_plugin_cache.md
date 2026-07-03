---
name: feedback_skills_home_not_plugin_cache
description: 自作スキルの正規置き場は ~/.claude/skills/ のみ。plugins/cache配下は自動更新で消える（2026-07-03に8スキル消失事故）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 76e686fa-e5c3-46f0-b94d-eb9f6ed4e813
---

# 自作スキルは ~/.claude/skills/ に置く（plugins cache 禁止）

2026-07-03 16:07〜16:34、自作8スキル（ohayo/oyasumi/nichijo/news-briefing/iken/drive-intake/task-audit/content-pipeline）が消失。原因は skill-creator プラグインの cache ディレクトリ（`~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/`）に自作スキルを同居させていたところ、**マーケットプレイスのプラグイン自動更新が cache を公式版で丸ごと上書き**したこと。プラグイン更新は全プラグイン一斉・繰り返し走る（installed_plugins.json の lastUpdated が毎日動く）ため、cache に置く限り再発は確実。

**Why:** cache はその名の通り揮発領域。ディレクトリが存在したまま中身だけ抉られたため、backup の `rsync --delete` が消失を鏡写しし、backup HEAD まで消えた（claude-config git 履歴 `41ab43b` から復旧できたのは git のおかげ）。

**How to apply:**
- 自作スキルの新規作成・復元先は必ず `~/.claude/skills/<name>/SKILL.md`。plugins/cache 配下には何も置かない。
- 2026-07-04 復旧完了: 8スキルを `~/.claude/skills/` に移設（計17スキル）。nichijo の `skill-creator:content-pipeline` 参照は `content-pipeline` に、content-pipeline 内の voice-dna 参照は正本 `04_compass/voice-dna.md` に修正済み。
- `sync-to-git.sh` は `~/.claude/skills/` を同期＋**ガット検知ガード**（SKILL.md が10個未満なら同期スキップ＆警告＝スキル消失の疑い）。`restore.sh` も `~/.claude/skills/` へ復元。
- スキル消失を疑ったら: `cd ~/claude-config && git log --oneline -- backup/skills` で消える直前のコミットを特定し `git archive <sha> backup/skills | tar -x` で取り出す。

関連: [[reference_claude_config_backup]] / [[feedback_system_closing_loops_rot]]
