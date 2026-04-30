---
name: 公開済アーカイブシステム
description: 2026-05-01新設。草川の真の声（公開後実テキスト）学習基盤。📚公開済アーカイブDB＋scrape.py＋oyasumi月曜分岐＋voice-analyst最優先ソース。Phase 1=ブログ/Threads/YouTube。
type: project
originSessionId: 24951467-1863-4b41-b983-d35481e730af
---
# 公開済アーカイブシステム（2026-05-01新設）

草川の発信物の **公開後の最終テキスト** をスクレイプ→Notion蓄積し、kusakawa-voice-analystの「真の声」学習素材とする基盤。下書きDB（SNS投稿管理／ブログ記事管理）は最終投稿前の版なので、投稿直前編集を反映できない問題を解消。

**Why:** 草川は投稿直前に手を入れる派。下書きDB→公開済の差分こそ「磨き上げの指紋」。voice-dna精度を一段引き上げるため、公開済テキストを最優先ソースに格上げ。

**How to apply:** voice-dna再抽出（kusakawa-voice-analyst起動）の入力は📚公開済アーカイブDBを最優先で読み、SNS/ブログDB（下書き）は副ソース扱い。新規発信物追加は自動（毎週月曜oyasumiが取得）。

## 構成

| 要素 | 値 |
|------|----|
| 📚公開済アーカイブDB（data_source） | `0ae2d907-d804-49ab-9860-b4b981d34c56` |
| DB top URL | https://app.notion.com/p/a9d670b3acec4f18bb8dabdd651f5fa9 |
| 親ページ | 📣コンテンツ管理（`34acf503-a68f-8159-b2d6-d225b637dbc1`） |
| スクレイパー | `~/.claude/scripts/published-archive/scrape.py` |
| ローカル全文JSON | `~/.claude/scripts/published-archive/output.json` |
| Notionペイロード生成 | `~/.claude/scripts/published-archive/build_notion_payload.py` |

## 取得対象（Phase 1）

| 媒体 | 取得方法 | 取得性 |
|------|---------|--------|
| ブログ | go2senkyo RSS `https://www.go2senkyo.com/seijika/168135/posts.rss` | ★完璧（10件・本文/日付/URL全取得） |
| YouTube | 公式RSS `feeds/videos.xml?channel_id=UCy_ttKLUr0q14q77wBKMNVA` | ★完璧（15件・タイトル/説明/公開日） |
| Threads | 公開HTML `https://www.threads.com/@kusagawatakuya` | △直近5-6件のみ（ログイン制限・正規表現抽出が不安定） |

## 自動化フロー（oyasumi Step 5.6・月曜のみ）

```
[月曜夜のおやすみ起動]
  → bash python3 ~/.claude/scripts/published-archive/scrape.py --since 8
  → output.jsonの各itemを既登録URLと照合
  → 新規分のみNotion create-pages（本文1900字truncate）
  → voice-DNA抽出済=falseが5件超えたら kusakawa-voice-analyst Task 起動
  → voice-dna.md更新後、対応Notionページの抽出済を一括true化
```

## DBスキーマ

| プロパティ | 型 | 用途 |
|-----------|---|------|
| タイトル | title | 投稿タイトル/動画タイトル |
| 媒体 | select | ブログ/Threads/YouTube/X/Instagram/Facebook/LINE |
| 公開URL | url | dedupeキー |
| 公開日 | date | プラットフォーム上の公開日時 |
| 本文 | rich_text | スクレイプ実テキスト先頭1900字（全文はoutput.json） |
| 元DB原稿URL | url | 対応する下書きDBページURL（手動or将来自動マッチ） |
| 差分あり | checkbox | 下書きと公開済に編集差分がある場合true |
| voice-DNA抽出済 | checkbox | analyst処理済みフラグ |
| 取得日時 | created_time | スクレイパー実行時刻 |
| 分野 | select | SNS DBと同じ10分類 |
| 文字数 | number | 短文/長文傾向分析用 |
| メモ | rich_text | 差分要因・声DNA特徴メモ |

## 初回バックフィル（2026-05-01）

過去60日間で21件（ブログ10／YouTube 11）登録済み。Threads 0件（HTML構造変化で正規表現未マッチ）→ 月曜分岐で次回再試行。

## 連携している他コンポーネント

- **oyasumiスキル** Step 5.6（月曜のみ実行・スキップロジック内蔵）
- **kusakawa-voice-analystエージェント** 最優先入力ソースとして設定済み
- **将来拡張**: 下書きDB↔公開済の差分検知で「投稿直前編集パターン」抽出

## トラブル時のチェックポイント

- scrape.py失敗 → Python 3.9系なのでtype hintsは`Optional[int]`/`List[Dict]`形式
- Threadsが0件 → HTML構造変化のため正規表現要更新（`scrape_threads`関数のpost_pattern）
- Notion登録失敗 → 本文1900字制限超過・特殊文字エスケープ
- voice-analystが起動しない → 抽出済=false件数が5件未満（閾値設定）
