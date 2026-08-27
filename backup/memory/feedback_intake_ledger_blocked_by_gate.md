---
name: feedback-intake-ledger-blocked-by-gate
description: smart-intakeの🔖台帳行は、発信物を伴わないファイル振り分けだと安全ゲートで書き込めない。ローカル_intake_ledger.jsonlで代替する
metadata:
  type: feedback
---

smart-intake A-3 は「すべての保存の直後」に nichijo 日次ログへ 🔖台帳1行を追記せよと定める（省略禁止）。
だが**発信物を1つも作らない振り分け作業**（Desktop/Downloadsの棚卸し、ファイルのDrive配置）では、この1行が `content_safety_gate.py` に deny される。

**Why:** Notion本文への書き込みは、gate.py に指紋が記録されているかどうかだけで判定される。指紋の記録には `--pass`＝content-fact-checker と content-risk-reviewer をそのセッションで実際に通した宣言が要る。台帳行の中身が「どのファイルをどこへ動かしたか」だけで、市民向けの記述も数値も個人名も含まなくても例外はない。ファイル名に「メモ」を入れて internal 判定にしても、機械チェックが通るだけで `--pass` の要求は消えない（[[feedback_gate_kind_of_by_filename]]）。

発信物を伴う作業（動画パッケージ、ブログ）では、その成果物でゲートを通した流れで台帳行も書ける。**振り分け単体のときだけ**この壁に当たる。

**How to apply:**
- 振り分け作業の記録は `_root_intake.py` が `99_raw/_scripts/_intake_ledger.jsonl` に元パス・先パス・判定根拠つきで自動記録する。モードBの検索対象にも入っているので、**Notion台帳が無くても情報迷子にはならない**。
- Notion台帳に残したいかどうかは草川に選ばせる。2026-08-27の棚卸しでは「ローカル台帳だけでよい」を選択。
- 2エージェントを起動してまで3行を通す判断は、草川の明示指示があるときだけ。

関連：[[feedback_safety_gates_before_notion_save]]／[[feedback_gate_json_concurrent_overwrite]]
