---
name: project_sns_video_system_codex
description: Codex製の実写ショート動画 自動編集CLI（sns-video）をClaude Codeでも使えるよう設定（2026-09-14）。本体の場所・入口・未整備点
metadata: 
  node_type: memory
  type: project
  originSessionId: 71f9250a-6f9a-48f2-a953-874d6df382f1
  modified: 2026-09-14T06:15:29.680Z
---

Codexが2026-09-12〜14に構築した「SNS動画制作システム」（Python＋FFmpeg・テスト241件）。本体＝`~/Documents/Codex/2026-09-12/sns-sns-claude-code-sns-capcut/`（ローカルgit・main c26568a）。撮影前の準備（5文書＋カード画像＋両ゲート→awaiting_footage）と、撮影後「いつもの動画にして」で文字起こし→照合→カット→字幕→挿入画像→final.mp4＋CapCutパッケージ。

2026-09-14にClaude Code対応：`~/.claude/skills/sns-video-system/SKILL.md`（読み替え表）／本体に `CLAUDE.md` 追加（未コミット）／skill_router.py に1行／ホームCLAUDE.mdトリガー表に1行。手順の正本はCodexと共有の `.agents/skills/sns-video-system/references/`。

**Why:** Codex版は `bin/sns-video --root .` 前提・知識正本が `~/.codex`・尺45〜60秒で、Claude側ルール（尺35〜50秒・`~/.claude` 正本）とずれていた。
**How to apply:** 入口は必ず `skill-intent`。「ショート動画作って」単体は not_applicable→[[feedback_short_video_use_virality_architect_first]]の short-video-create。9/14 faster-whisper導入＋長さずれ修正で finish 実走OK（全243テスト合格）。残＝字幕の固有名詞誤り（台本ヒント方式は編集判定が壊れ不採用）・字幕の語中改行・CapCut公式連携未認証・修正は未コミット。
