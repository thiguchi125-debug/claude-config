---
name: Notion view-DSL のステータス型フィルタ書き込み不可
description: notion-create-view/update-view の DSL では status型プロパティのフィルタ（=/!=/IN）がサイレント失敗。CLEAR FILTERもsimpleFiltersを消せない
type: feedback
originSessionId: 9a9e7ee5-7eca-4eb3-ace0-44c9502a7dc3
---
# Notion view-DSL のステータス型フィルタ制約

## 事象（2026-05-02 ハマり）

`mcp__claude_ai_Notion__notion-create-view` / `update-view` の `configure` DSL でステータス型(status)プロパティに対するフィルタ（`=`, `!=`, `IN`）を書き込もうとすると、**エラーは出ないがフィルタが空になる**（advancedFilter: filters:[]）。

検証済みパターン（全て無効）:
- `FILTER "ステータス" = "Done"`
- `FILTER "ステータス" != "Done"`
- `FILTER "ステータス" IN ("inbox", "Wish List")`
- `FILTER "ステータス" != "Done" AND "ステータス" != "Archive"`

select型は同じ syntax で機能する（`FILTER "優先度" = "高"` は動く）。status型のみ問題。

## CLEAR FILTER の問題

DSL の `CLEAR FILTER` は **advancedFilter のみ消去** し、Notion UI で設定された **simpleFilters は消せない**。古い壊れたフィルタが残ったまま新しい advancedFilter が追加され、AND結合でビューが空になる。

## Why

**Why**: Notion API の DSL 実装が status型を完全サポートしていない仕様上の制約。

## How to apply

**How to apply**: 
1. status型でフィルタしたいビューを作る場合、**新規作成**を推奨（既存ビューの simpleFilter は CLEAR FILTER で消せない）
2. status型フィルタが必要な場合、**ユーザーにNotion UIで手動追加してもらう** indication をハブページに明記
3. 代替策：
   - ボード型ビューで `GROUP BY "ステータス"` を使い、Done/Archive列を視覚的に右端に配置（手動でカラム畳み可能）
   - sort by 期限 ASCで「過去日＝期限切れ」を上に集める
4. 壊れたsimpleFiltersを持つビューはリネームして「📦 旧○○（壊れ・削除可）」とし、ユーザーに手動削除を依頼
