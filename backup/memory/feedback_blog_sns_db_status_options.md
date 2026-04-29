---
name: ブログ／SNS DBのステータス選択肢に「下書き完成」が無い
description: ブログ記事管理DB（dcdf44af-）／SNS投稿管理DB（1bd98deb-）のステータスselectが未着手/進行中/完了の3択のみ。スキル仕様の「下書き完成」と齟齬
type: feedback
originSessionId: 5c4d4819-c63f-43f1-b3e9-ef800355d065
---
# ブログ／SNS DBのステータス選択肢ミスマッチ

3エージェント並列生成（2026-04-29）で発覚。ブログ記事管理DB（`dcdf44af-f285-499e-a6c3-08cc343fc3fa`）／SNS投稿管理DB（`1bd98deb-624f-402c-aeb3-bdaa4782b389`）の`ステータス`プロパティ選択肢が **`未着手` / `進行中` / `完了`** の3つだけで、nichijoスキル等で指定している `下書き完成` が存在しない。

**Why:** 過去のスキル設計時に独自ステータス値を仕様化したが、実DB側のselect optionsを揃えていなかった。エージェントは仕方なく `進行中` を代用しつつメモ欄に「下書き完成」と注記する運用になっている。

**How to apply:**
- 当面：エージェント側で「下書き完成」が選択肢にない場合 `進行中` を選択し、メモ欄に注記する運用を継続
- 恒久対応案：Notion側のステータスselectに `下書き完成` 選択肢を追加するか、スキル側を `進行中` 一本に書き換えるか、いずれかでスキーマと仕様を一致させる
- 関連ファイル：
  - `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/nichijo/SKILL.md`（複数箇所で「下書き完成」記述）
  - `content-pipeline` スキル
- 同種事象：分野select単一型のため「福祉/教育」併記不可、`福祉` 単一採用となるケースも併発
