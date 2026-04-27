---
name: nichijo モバイル版 ＋ PC仕上げモード ＋ コンテンツ抽出モード
description: スマホ(Claude.ai)で 📱プレフィクス付き下書きを Notion 登録し、PC /nichijo 仕上げモードで深掘り調査＋上書き仕上げする2段構成。さらに2026-04-27追加で当日全情報横断のコンテンツ抽出モードあり
type: project
originSessionId: 4106fbb9-d1d3-4a51-82e0-d79536592b47
---

nichijoスキル（日次活動記録）はモバイル（Claude.aiプロジェクト）とPC（Claude Code）の2段構成で運用している。

**Why:** スマホ版Claude Codeネイティブアプリが存在せず、Claude.aiプロジェクトではサブエージェントが呼べないため、モバイルは簡易叩き台生成、PCで深掘り仕上げ、という役割分担にした。下書きが「仕上げ待ち」かどうかを機械的に判別するため、タイトル先頭 `📱 ` プレフィクスで識別する方式を採用。

## 構成ファイル
- **モバイル指示書**: `/Users/kusakawatakuya/nichijo-mobile-project-instructions.md`（Claude.aiプロジェクト「記録（日次活動ログ）」のカスタム指示にコピペする原本）
- **PC側スキル本体**: `/Users/kusakawatakuya/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/nichijo/SKILL.md`

## 3つの起動モード（PC側SKILL.md）
1. **記録モード**（既定）: 「記録：〇〇した」等で Step 1〜5 を実行
2. **仕上げモード**: 「仕上げ」「モバイル記録を仕上げて」等で起動（📱付き下書きの個別仕上げ）
3. **コンテンツ抽出モード**（2026-04-27追加）: 「今日のコンテンツ抽出」「今日のネタ全部出して」「今日まるごと抽出」等で起動。当日の活動ログ／市民意見／一般質問ネタ／ニュース／政策候補／完了タスクを横断スキャン→テーマ候補5〜10件提示→ユーザーGOサイン取得→content-pipeline委任で生成。下書きが無くてもゼロから発信ネタを発掘できる点が仕上げモードと異なる。市民相談個人情報秘匿・iJAMP転載禁止・公選法配慮を明文化済み

## 仕上げモードの動作
- 対象3DBの**専用ビュー**（タイトル starts_with `📱`）を `notion-query-database-view` で並列クエリ。`notion-search` は絵文字プレフィクスを取りこぼすため禁止（2026-04-22改修）
  - 一般質問ネタDB `📱下書き仕上げ待ち` view: `cb47d25e30b14b61b39f56254bf9432a?v=34acf503-a68f-819d-af39-000c0ba57b4d`
  - SNS投稿管理DB `📱下書き仕上げ待ち` view: `78f40f33ae714f329cc3b00c0a36707c?v=34acf503-a68f-812c-92a0-000cd78dfa77`
  - ブログ記事管理DB `📱下書き仕上げ待ち` view: `c3130352e33e49f8a3282bb546ff37f5?v=34acf503-a68f-818d-9a0d-000cffd660f9`
- ユーザーに一覧提示→番号/種類で選択
- 選択項目ごとに policy-researcher + kameyama-researcher 並列調査 → blog-writer / sns-content-creator で仕上げ版生成 → `notion-update-page` で**上書き**
- タイトルの `📱` プレフィクスは仕上げ完了時に削除（再検出防止）
- 元本文は上書きされるが Notion の版履歴から復元可能

## How to apply
- NotionのデータベースID（日次ログ f6d15ac0... / 一般質問ネタDB 42716725... / SNS 1bd98deb... / ブログ dcdf44af... / タスク 292cf503-a68f-81c6-... / 市民意見 c2c34bd8... 等）を変更した場合、PC側のSKILL.md とモバイル版指示書の両方を更新する必要がある。**タスクDBは2026-04-24に旧日次DB(b43cf503)と統合済で単一ID**
- 「仕上げ」機能が動かない場合、まず `📱` プレフィクスが正しくNotion側のタイトルに入っているか確認（モバイル側の貼付済み指示書に `📱 ` 必須の明記があるか）
- ユーザーが「スマホで記録が動かない」と言った場合、まずClaude.aiプロジェクト側のNotionコネクタ接続を疑う
- 仕上げは上書き方式。元原稿保存が必要と言われたら Notion の版履歴を案内する
