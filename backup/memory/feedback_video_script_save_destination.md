---
name: 動画原稿の保存先は📣SNS投稿管理DB
description: video-content-strategistが生成するショート動画原稿（YouTube Shorts/TikTok/Reels）は今後すべて📣SNS投稿管理DB(78f40f33-)に統一保存。専用動画DBは作らない
type: feedback
originSessionId: f42f962f-311d-4042-9ba8-7db4e5594d95
---
# ルール

video-content-strategistエージェント（および任意の動画原稿生成）が出力したショート動画原稿・YouTube長尺台本は、**今後すべて 📣SNS投稿管理DB（78f40f33-ae71-4f32-9cc3-b00c0a36707c / data_source_id: 1bd98deb-624f-402c-aeb3-bdaa4782b389）に統一保存**する。

## Why
2026-05-01に草川から「Notion 📣SNS投稿管理DB　今後も統一」と明示指示。動画専用DBを作らず既存SNSハブに集約することで、横展開（IG/Threads/X）と動画台本を1箇所で管理できる。プラットフォーム多選択で動画系（YouTube/TikTok）と静止画系（Instagram/Facebook/Threads/X/LINE）を同じ管理粒度で扱う方針。

## How to apply

### 保存テンプレ（プロパティ）
- **投稿タイトル**: 先頭に🎬絵文字＋【ショート動画】or【YouTube長尺】を付与（例: `🎬【ショート動画】亀山版デジタル地域通貨を提言`）
- **ステータス**: 下書き段階は「進行中」（DBに「下書き完成」選択肢がない既知制約に従う）
- **プラットフォーム** (multi_select): 想定する動画PFを全部チェック（例: `["YouTube", "TikTok", "Instagram"]`）
- **分野**: 元テーマに合わせて選択（行政/福祉/子育て/教育/防災/産業/交通/環境/都市計画/その他）
- **ネタ元**: 議会/委員会・日次活動・市民相談・行政資料・SNS/新聞のいずれか
- **メモ**: 元素材URL、バージョン構成（60秒/30秒/90秒等）、fact-check/risk-review判定
- **アイコン**: 🎬

### 保存内容（content）
- メタ情報（元素材・URL・想定視聴者・目的・トーン・CTA・voice-dna軸）
- 安全ゲート判定（fact-checker / risk-reviewer 結果）
- カット表（秒数 / 画 / トーク / テロップ / 補足）
- バージョン違い（30秒/60秒/90秒など）
- タイトル案・サムネ案・ハッシュタグ群
- 横展開メモ（ブログ・Threads・X・IG）
- アンチ想定＋返信案
- 撮影前チェックリスト
- リサーチソース

### 動画専用DBは作らない
- 「動画台本DB」「YouTubeチャンネル管理DB」等の新設は提案しない
- 既存📣SNS投稿管理DBで統一。プラットフォーム属性で動画/静止画を区別

### 関連ハブ
- 親ページ: 📣 コンテンツ管理 (34acf503-a68f-8159-b2d6-d225b637dbc1)
