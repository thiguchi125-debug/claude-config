---
name: ニュースブリーフィングシステム
description: 2026-04-25構築。news-briefingスキル＋📰ニュースDB＋cron(6:00 JST)＋ohayo統合。市議会議員として知るべきニュースを6カテゴリで自動収集
type: project
originSessionId: 739c537c-6f3a-4a81-832e-643b1e774b86
---
# ニュースブリーフィングシステム

2026-04-25 構築。草川たくや（亀山市議会議員）が毎朝知っておくべきニュースを6カテゴリで自動収集し、Notion蓄積＋議会活用視点付きで提示する仕組み。

**Why:** 一般質問・SNS発信・市民相談に活用できる情報を、毎朝消費可能な形で構造化して蓄積するため。手動収集の属人化を解消し、過去ニュースの検索性も担保。

**How to apply:**
- 「ニュース教えて」「今日のニュース」「ニュースまとめて」「news-briefing」等の発話で `news-briefing` スキル起動
- 「おはよう」発話時は `ohayo` スキルが📰DBから当日分を読み込んで表示（ライブ取得しない）
- 毎朝 6:00 JST に cron で自動実行されるため、起床時にはDBに当日分が揃っている想定
- 深掘りしたいテーマがあれば「〇〇について深掘り」でモードB（詳細概要＋議会活用視点詳細）へ切り替え

## 構成要素

### 1. Notion📰ニュースDB
- DB URL: https://www.notion.so/f2eefc669dd54648bbcdacdc8afa1158
- data_source_id: `29e5c1a2-d64d-4822-81fd-0d642c3f07bc`
- プロパティ: 見出し / 日付 / カテゴリ / 関心テーマ / 情報源 / URL / 概要 / 亀山関連度 / 議会活用メモ / ステータス
- 1ニュース＝1ページ（構造化、検索可能）

### 2. 既存🗞️毎朝ニュースまとめページ（人間可読版）
- page_id: `75681023203042838ff7ed3b99b1ae2d`
- 当日のMarkdownレポート（PART 1ニュースダイジェスト形式）を追記
- 履歴を時系列で読める

### 3. news-briefing スキル
- 場所: `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/news-briefing/SKILL.md`
- モードA（軽量・デフォルト）: 6カテゴリ計5〜10件、80字要約、約1〜2分
- モードB（深掘り）: 指定カテゴリ詳細、概要300字＋議会活用メモ詳細、約2〜3分
- 6カテゴリ: 亀山市・三重県／国政・自治体／関心テーマ／全国時事／省庁発表／SNSトレンド
- 関心6テーマ: 子育て・教育・医療健康・都市計画まちづくり・防災・AI（曜日ローテ）

### 4. ohayo スキル統合
- Step 3-0 として📰ニュースDBから当日分を取得（ライブWebSearchはしない）
- 出力に「🗞️ 今朝のニュース」セクション追加
- 0件時は「⚠️ 未収集」と表示し `/news-briefing` を案内

### 5. cron 自動実行（remote routine）
- routine ID: `trig_01WXgkt4JqANvhi1YuQLGsEQ`
- スケジュール: `0 21 * * *` UTC（= 毎朝 6:00 JST）
- モデル: Claude Sonnet 4.6
- MCP: Notion 接続
- 管理URL: https://claude.ai/code/routines/trig_01WXgkt4JqANvhi1YuQLGsEQ
- プロンプトに収集ロジック全文をインライン化済み（リモートはローカルスキル参照不可のため）

## 関連DB／ページID（変更厳禁）
- 📰ニュースDB: `f2eefc669dd54648bbcdacdc8afa1158` (collection: `29e5c1a2-d64d-4822-81fd-0d642c3f07bc`)
- 🗞️毎朝ニュースまとめページ: `75681023203042838ff7ed3b99b1ae2d`
- 🌅朝のダッシュボード: `722beb9e9827421aa5dbbef67c1c4688`
