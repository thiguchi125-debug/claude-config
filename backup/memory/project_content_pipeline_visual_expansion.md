---
name: project_content_pipeline_visual_expansion
description: content-pipelineにサムネ画像＋ショート動画生成を統合／ブログモードを自動判定化（2026-07-14）
metadata: 
  node_type: memory
  type: project
  originSessionId: 97e376e7-c2f7-4032-b185-dc004038d76e
---

2026-07-14、三寺コスモス畑ブログ制作の一連の流れ（ニュース記事URL＋写真→ブログ→安全ゲート→Notion保存→サムネ→SNS7種→インスタReel）を **content-pipeline スキルに統合拡張**（草川指示「content-pipelineを拡張」「毎回自動判定」）。

**変更点**:
1. **ステップ2-0**: ブログモードを「毎回2択質問」→**素材からの自動判定→1行提案→承認**に変更（イベント告知/活動報告=ノーマル推奨、政策論=深掘り推奨、拮抗時はノーマル既定）。
2. **新ステップ4「発信ビジュアル」**（条件付き=イベント告知/写真添付/明示指示時）: 4-A サムネ画像（**1600×900** OGP・元写真は photo-curator で自分で選び切る（2026-09-04に「先に聞く」旧ルールは廃止）・HTML/CSS→Chrome→PNG・EYES-FIRST）／4-B ショート動画（9:16 Reels・写真autorotate正立化＋コンタクト自Read→透過テキストカード→ffmpeg軽量ズーム→BG実行）／4-C 安全ゲート（ブログ流用は継承可）／4-D 保存（~/outputs/thumbnails・~/outputs/short-video）。
3. **description更新**: サムネ・ショート動画・記事URL・写真トリガー追加。
4. **新reference**: `~/.claude/skills/content-pipeline/references/visual-assets-playbook.md`（サムネ＆Reelの具体レシピ正本。ffmpegコマンド・落とし穴チェックリスト・zsh配列1始まり・BG実行・4Kズーム回避等）。

**制作実績（初回・正本サンプル）**:
- ブログ: drafts/2026-07-14_三寺コスモス畑種まきイベント_v1.md → Notion 39dcf503a68f811d9c8ee0d9f0b5f1d5
- サムネ: ~/outputs/thumbnails/2026-07-14_mitsudera_cosmos/thumb.png（1200×630）
- Reel: ~/outputs/short-video/2026-07-14_mitsudera_cosmos/（6カット・約16.5秒・9:16・草川本人IMG_9600含む）

関連: [[feedback_no_emoji_ai_smell]] （写真＋動画はphoto-postフル＋写真Read必須＝skills/photo-post/SKILL.md 📌節） [[project_nakasho_natsumatsuri_flyer]]（同・中庄町イベント系）
