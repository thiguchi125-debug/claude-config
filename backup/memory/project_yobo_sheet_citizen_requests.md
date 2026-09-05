---
name: project-yobo-sheet-citizen-requests
description: 市役所対応の市民要望タスクをTodoistからGoogleスプレッドシート「市民要望管理台帳」へ移行（2026-09-05）。草川手番＝ネイティブ化＋Apps Scriptデプロイ→config保存→Todoist完了処理
metadata:
  type: project
---
2026-09-05、草川の指示「市役所対応の市民要望系タスクはTodoistでなく基本的に全てGoogleスプレッドシートで管理」で着手。確認済み判断＝①既存Todoistの市民相談タスクは全部台帳へ移しTodoist側は完了処理 ②相談者氏名は書く（置き場00_名簿・個人情報）③1行＝1案件 ④Apps Script Web Appを草川がデプロイ。

**状態（2026-09-05）**
- 作成済: `~/outputs/yobo-sheet/市民要望管理台帳_v1.xlsx`（67案件・Todoist 75件分・台帳/相手先マスタ/集計/使い方の4タブ・入力規則・色分け・滞留日数と要対応⚠の数式）→ Drive `草川たくや 議会質問アーカイブ/日常資料アーカイブ/00_名簿・個人情報/` に配置
- 作成済: `~/outputs/yobo-sheet/yobo_webapp.gs`（doPost add/update/list＋onEdit最終更新）・`SETUP_AppsScript.md`（草川手順書）・`~/.claude/scripts/yobo/yobo.py`（CLI）・`close_todoist.sh`（移行76件の完了処理）・`build_sheet.py`/`migration_rows.py`（再生成用）
- ルール反映済: CLAUDE.md／OPERATIONS.md【B】例外節／GUARDRAILS【6】／iken／citizen-inquiry-responder／smart-intake 7b／task-add
- **草川手番**: ①xlsxを「Googleスプレッドシートとして保存」②Apps Script貼付→ウェブアプリデプロイ③URLと合言葉をClaudeへ → `~/.config/yobo/config.json` に保存 → `yobo.py list --alert` で疎通 → `bash close_todoist.sh`
- 未着手: ohayo朝ブリーフで台帳の⚠一覧を読む（yobo.py稼働後）／Todoist「〇〇地区 市民相談」PJ7本の空箱をアーカイブ／台帳の「相手先（要確認）」3件の課名確認

**Why:** Todoistは担当課・回答・報告日を持てず、案件の全体像と滞留が見えない。相談者への報告漏れ防止が目的。
**How to apply:** 相談者がいて市（県・警察・自治会）と動く案件は `yobo.py add`。Todoistは草川自身の議会・政策・イベント・選挙のみ。関連 [[feedback_spreadsheet_deliverable_must_be_native_and_functional]] [[feedback_citizen_inquiry_task_registration]] [[project_todoist_task_migration]]
