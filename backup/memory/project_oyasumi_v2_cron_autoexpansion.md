---
name: oyasumi v2 (cron化＋自動展開＋仕上げ統合)
description: 2026-05-08実装。Drive/ミーティング→📝・✅DB自動展開、仕上げモード(A/B/C)統合、cron 22:00 JST化、ohayo参照源最適化。routine ID trig_01TbZU1pJDecnG4QmZKosz72
type: project
originSessionId: 7a72bdd1-81e5-4c90-bec6-61316fe9a435
---
2026-05-08 実装。oyasumi/ohayoスキルを大幅拡張し、cron化で発話不要の自動運用に切替。

## 実装内容

### oyasumi SKILL.md（新規Step）
- **Step 4.5-8**: ミーティングフォローアップ自動抽出 → ✅タスクDBへ「【未確認・自動抽出】」プレフィクスで create
- **Step 5.5-6**: Drive資料サマリの議会活用メモ自動展開 → 📝一般質問ネタDB／🎯政策候補DBへ create
- **Step 6.5**: 仕上げモード自動実行（基準a 完全保守的）
  - A: 📱モバイル下書き仕上げ — voice-dna整合90%以上のみ自動清書
  - B: 当日コンテンツ素材抽出 — 本文生成はせず素材列挙のみ
  - C: 全DB横断振分 — 確度0.8以上自動、未満は朝レビュー
- Step 6 デイリーサマリに「📝 自動抽出された質問ネタ候補」「✅ 自動抽出されたタスク候補」セクション追加
- Step 9 チャット出力に🤖自動抽出＋📝仕上げモード集計を反映

### ohayo SKILL.md（新規セクション）
- **§3-PRE**: 📔昨夜のデイリーサマリ最優先取得（fallback付き）— 朝のNotion DB直叩きをサマリ参照に置き換え、燃費100K→30〜40Kに削減
- **§3-7**: 🤖昨夜の自動抽出・仕上げモードレビュー — 📝/✅候補・📱保留・🗂未紐付け・📦素材を一覧表示
- 出力フォーマットに🤖自動抽出レビュー行を追加

### Routine（cron化）
- **ID**: `trig_01TbZU1pJDecnG4QmZKosz72`
- **名前**: oyasumi-nightly-kusagawa
- **cron**: `0 13 * * *` UTC = 毎晩 22:00 JST（実際は22:07頃にスプレッド）
- **Repo**: thiguchi125-debug/claude-config
- **MCP**: Notion / Drive / Gmail / Calendar
- **Model**: claude-sonnet-4-6
- **管理URL**: https://claude.ai/code/routines/trig_01TbZU1pJDecnG4QmZKosz72

## 「未確認」運用ルール
ステータス値に「未確認」が無いDB（タスクDB／一般質問ネタDB）では、タイトル先頭に `【未確認・自動抽出】` or `【未確認・Drive自動抽出】` プレフィクスで識別。草川承認時にプレフィクス削除＋ステータス昇格、誤抽出時はページ削除。

## トークン削減見込み
- Before: oyasumi 100K + ohayo 100K = 200K/日
- After: oyasumi 130〜150K（cron）+ ohayo 30〜40K = **160〜190K/日**（仕上げモード追加しても現状より削減）

## 既存issue（後日対応）
- **oyasumi Step 9 重複**: L1141（チャット出力）/ L1242（過去棚卸し）の2か所。後日 Step 9.5 等に改番推奨
- **claude-config repo 未sync**: 編集はローカル `~/.claude/plugins/cache/...` のみ。リモート routine の SKILL.md 取得は古い版になる可能性。プロンプト内フォールバックで新Step記載済みのため当面は動作する。手動 push or restore.sh 実行で同期推奨

## 初回手動実行
2026-05-08 23時頃、cron初回（明晩）を待たず手動runで初動テスト実施。next_run_at: 2026-05-09 22:07 JST。
