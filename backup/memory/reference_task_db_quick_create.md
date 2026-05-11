---
name: ✅タスクDB クイック登録（schema fetch不要）
description: タスクDBへの新規登録時、notion-search/fetch を省略して create-pages 1発で済ませるための data_source_id とプロパティ仕様
type: reference
originSessionId: 3b5b76df-4bb0-481f-998f-4b9f8d23f55d
---
# ✅タスクDB ダイレクト登録仕様

**目的**: 単純なタスク登録で notion-search → fetch(hub) → fetch(schema) → create という4段重ねを避け、create 1発に圧縮する。

## ID

- ハブページ: `292cf503a68f802da262d7e0dab4ebf3`（プロジェクト＆タスク）
- ✅タスクDB page_id: `292cf503a68f814eafcdec9eed56f273`
- ✅タスクDB **data_source_id**: `292cf503-a68f-81c6-b9dd-000b3ffdd2ce` ← create-pagesで使う
- 🗂️プロジェクトDB data_source_id: `292cf503-a68f-81fe-bd40-000b64314f2e`

## 最小プロパティ（これだけで登録可）

```json
{
  "タスク名": "<title>",
  "ステータス": "inbox",
  "優先度": "高|中|低",
  "date:期限:start": "YYYY-MM-DD",
  "要約": "<短い要約>"
}
```

## 選択肢（暗記用）

- **ステータス**: `inbox` / `Wish List` / `Project` / `Waiting` / `Remind` / `Done` / `Archive`
- **優先度**: `低` / `中` / `高`
- **連絡ツール**: `電話` / `メール` / `フォーム` / `公式LINE` / `個人LINE` / `Instagram` / `X` / `Threads` / `その他`
- **昇格判定タグ**: `["A","B","C","D","E"]` のJSON配列

## オプション（必要時のみ）

- `相談元氏名` / `相談元連絡先` / `連絡ツール`
- `date:昇格判定日:start` ＋ `昇格判定タグ`（プロジェクト化判定時）
- `関連市民意見` / `関連政策候補` / `関連一般質問ネタ`（JSON配列のpage URL）

## **Why:**
2026-05-07、御幸公園落書きという軽量タスク登録に search＋fetch×2＋create で 3000+トークン消費。schemaは安定なので毎回取りに行くのは無駄。

## **How to apply:**
- 「タスク」「タスク登録」「〜やっておいて」等の単発タスク依頼 → 即 create-pages、schema取らない
- 関係DBへの relation を貼る等の特殊要件があるときだけ追加 fetch
- schemaが変わったと疑う事象（プロパティ名でcreateが失敗する等）が出たら、その時だけ fetch して本ファイル更新
