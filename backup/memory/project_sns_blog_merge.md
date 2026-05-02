---
name: SNS＋ブログDB統合（投稿管理DBへ一本化）
description: 2026-05-03。📣SNS投稿管理DBと📝ブログ記事管理DBを統合してプラットフォーム=ブログを含むコンテンツ一本DBへ。15件転記済み・旧DBアーカイブ
type: project
originSessionId: 9a9e7ee5-7eca-4eb3-ace0-44c9502a7dc3
---
# SNS＋ブログDB統合（2026-05-03）

## 統合先
**📣 投稿管理DB（SNS＋ブログ統合）** = `collection://1bd98deb-624f-402c-aeb3-bdaa4782b389`
- DB URL: https://www.notion.so/78f40f33ae714f329cc3b00c0a36707c
- 親: 📣 コンテンツ管理ハブ

## スキーマ拡張
- ✅ プラットフォーム options に追加: **「ブログ」「YouTube Shorts」「Reels」**（既存7+新3=計10種）
- ✅ **公開URL** (url) フィールド追加
- ✅ 「投稿予定日」を「**公開予定日**」へリネーム（ブログ用語と統一）

## 移行
- 旧📝ブログ記事管理DB(`dcdf44af-`) の **15件全て** を投稿管理DBへ転記
- 各レコードのメモ末尾に `[2026-05-03 旧📝ブログ記事管理DBより統合・元ページ: <url>]` で元ページリンク保持
- 長文記事本文は元ページに残るため、メモは要約のみ（実本文は元ページ参照）

## 旧DBアーカイブ
- 旧 `dcdf44af-` を「📦 旧ブログ記事管理DB（〜2026-05-03・投稿管理DBへ統合済み）」にリネーム
- 新規書込禁止

## スキル修正
- ✅ **nichijo SKILL.md** 4箇所修正（DB認識リスト／ブログ素材R4-D／R2分類表／ブログ書込先 dcdf44af-→1bd98deb-+プラットフォーム=ブログ追加）
- ✅ **oyasumi SKILL.md** 修正（ブログ記事管理DB→投稿管理DB・公開済フィルタ調整）
- ⚠️ **未対応（軽微）**: blog-writer / blog-writer-normal / notion-saver / content-pipeline / kusakawa-voice-analyst の参照URL更新（次回触れた時に対応推奨）

## ハブページ更新
- **📣 コンテンツ管理ハブ** リライト: 統合DBの使い分け表（プラットフォーム→使うエージェント）／公開済アーカイブ別建て／旧DBは折り畳み参照
- **🌐 Notion全体地図** 対応履歴9件目に追加・コンテンツ広報セクション統合反映

## プラットフォーム選択ルール（運用）

| プラットフォーム | 用途 |
|---|---|
| ブログ | 長文（800-2500字）。blog-writer / blog-writer-normal が生成 |
| Threads / X / Instagram / Facebook / LINE | sns-content-creator が7つ同時生成 |
| YouTube / YouTube Shorts / TikTok / Reels | video-content-strategist / short-video-virality-architect |

multi_select なので、同テーマで「ブログ＋Threads＋X」など複数選択可能。
