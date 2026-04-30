---
name: 📡AIインタビュー設定DB
description: 2026-04-30新設。depth-interview-kusagawa.vercel.app の AIインタビュー config を蓄積するDB。コピペ最適化の長文コードブロック構造
type: project
originSessionId: 315bc548-c970-4c44-b754-4d42e7e24a61
---
2026-04-30新設。AIインタビュー設定（config）を蓄積する専用Notion DBを構築。

**DB情報**:
- 名前: 📡 AIインタビュー設定DB
- ページID: `435f05b5d67e4daf977e8f2c86061d97`
- data_source ID: `a2396bf5-3411-408b-b3d8-b7ec01d08088`
- 親ページ: 一般質問ネタ・プラットフォーム（5daccebabef34d2ca57ecc48a12e228c）
- URL: https://app.notion.com/p/435f05b5d67e4daf977e8f2c86061d97

**プロパティ**:
- タイトル / config_id / ステータス（設計中/実行中/終了/アーカイブ）/ カテゴリ（11種MULTI_SELECT）/ 議会対象 / LLMプロバイダー / 推定時間（秒）/ 公開URL / 管理URL / 回答数 / 公開日 / 終了日 / テーマ概要

**ページ本文構造**（全長文をコードブロック化＝Notion右上1クリックコピー対応）:
- ①config_id ②タイトル ③説明 ④推定時間 ⑤LLMプロバイダー ⑥ステータス ⑦初期挨拶 ⑧ナレッジソース ⑨カスタムプロンプト ⑩LP概要 ⑪質問テーマ ⑫プライバシーノート + 質問#1〜#5（質問文＋ヒント3つ）

**Why**:
ai-interview-config-designer の出力（管理画面8〜12フィールド）を毎回ローカルファイルに散在させると再利用・履歴管理ができない。Notion DB化で①過去設定の一覧 ②配信中インタビューのステータス管理 ③回答数モニタリング ④コピペ性 を一元化。

**How to apply**:
- ai-interview-config-designer 起動時、出力後に本DBへ自動登録（agent定義の更新が必要、要対応）
- 管理画面に貼付する際は本DBのページから各コードブロックをコピー
- 一般質問ネタDBエントリと相互参照（手動リンク）

**初回エントリ**:
- 【亀山市】太陽光発電施設の適正な導入・規制条例（kameyama_taiyoukou, 2026年6月議会対象, 設計中）
- 元ネタ: https://go2senkyo.com/seijika/168135/posts/1244954
