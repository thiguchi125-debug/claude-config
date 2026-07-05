---
name: project-photo-post-skill
description: photo-postスキル（写真＋ひとこと→投稿文・画像・動画の統合1パス）2026-07-05実装
metadata: 
  node_type: memory
  type: project
  originSessionId: 6e8fa7bf-f02d-4dcb-a8ee-2bba653fb18e
---

2026-07-05実装完了。写真1〜3枚＋ひとこと→投稿文（1〜2PF）→SNS投稿画像（1:1＋9:16・実写無加工デザイン合成・テンプレ3種=下帯型/サイドバー型/座布団型）→ショート動画（ffmpeg Ken Burns＋透過見出し＋「声を、チカラに。」エンドカード・10〜20秒9:16無音）を統合1パス生成。確認2回のみ。[[project_spark_skill]]と連携（写真つきの種→PAIRモード橋渡し）。設計正本=~/.claude/skills/photo-post/DESIGN.md。natural-design-reviewerゲート組込済（[[feedback_design_review_gate_no_skip]]）。初回実運用フィードバック待ち。

**Why:** 実運用は「画像＋ひらめき/活動記録を一緒に投稿」が基本形のため、文と画像を同じ接地・同じコピー素材から分岐させ、安全ゲート・保存を各1回に統合（燃費60〜80K）。政治家写真のAI生成改変は誤解リスクHIGHのため実写無加工＋デザイン合成方式。
**How to apply:** 写真＋ひとこと投入で提案起動。「画像だけ」で動画スキップ。優良レイアウトはdesign_system「SNSカード」昇格提案。動画エンジン=skills/photo-post/scripts/make_video.sh（-o出力 -eエンドカード -tオーバーレイ 写真1〜3枚）。

**エンドカード仕様（2026-07-05草川指示で確定）:** スローガンは「声をチカラに」または「ええやん亀山」。句読点付き「声を、チカラに。」は使わない。エンドカードには拳ポーズの透過ポートレート（skills/photo-post/assets/kusagawa_portrait.png・白背景をscripts/cutout_portrait.pyで切り抜き・胴中央は台形保護帯で明色シャツを守る）を右下配置、スローガンと名前は左のクリア緑地帯。別の本人写真に差し替える時はcutout_portrait.py再実行。
