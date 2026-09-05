---
name: project-yobo-sheet-citizen-requests
description: 市役所対応の市民要望はGoogleスプレッドシート「市民要望管理台帳」（yobo.py add/update/alert/flush）。2026-09-05稼働・ohayo §9b連携済。残＝T列書式(fix_format.gs)・相手先要確認3件
metadata:
  type: project
---
2026-09-05、草川の指示「市役所対応の市民要望系タスクはTodoistでなく基本的に全てGoogleスプレッドシートで管理」で着手。確認済み判断＝①既存Todoistの市民相談タスクは全部台帳へ移しTodoist側は完了処理 ②相談者氏名は書く（置き場00_名簿・個人情報）③1行＝1案件 ④Apps Script Web Appを草川がデプロイ。

**状態（2026-09-05）**
- 作成済: `~/outputs/yobo-sheet/市民要望管理台帳_v1.xlsx`（67案件・Todoist 75件分・台帳/相手先マスタ/集計/使い方の4タブ・入力規則・色分け・滞留日数と要対応⚠の数式）→ Drive `草川たくや 議会質問アーカイブ/日常資料アーカイブ/00_名簿・個人情報/` に配置
- 作成済: `~/outputs/yobo-sheet/yobo_webapp.gs`（doPost add/update/list＋onEdit最終更新）・`SETUP_AppsScript.md`（草川手順書）・`~/.claude/scripts/yobo/yobo.py`（CLI）・`close_todoist.sh`（移行76件の完了処理）・`build_sheet.py`/`migration_rows.py`（再生成用）
- ルール反映済: CLAUDE.md／OPERATIONS.md【B】例外節／GUARDRAILS【6】／iken／citizen-inquiry-responder／smart-intake 7b／task-add
- **稼働開始 2026-09-05 17:15**: ネイティブ台帳 https://docs.google.com/spreadsheets/d/1-qocheanDQRcyUqsixp9EU3Qz6BltTPTbGzfl83cOJ8/edit ／Apps Script（スタンドアロン・`yobo_standalone_READY.gs`・Drive APIサービスv3有効・setup()でxlsx→Sheets変換＋onEditStampトリガー設置） https://script.google.com/home/projects/199z75WAAzo5wT8Pl9BumQxmKIm-xTZ1JZfxFnOKo-3y34c-DuaPrvD2I/edit ／Web App URLと合言葉は `~/.config/yobo/config.json`。`yobo.py list` 67件疎通OK・Todoist 76件は完了処理済（close_todoist.sh）。
- **Chromeの罠**: Google Sheets画面はclaude-in-chromeの computer/screenshot/javascript が「Cannot access a chrome-extension:// URL of different extension」で全滅（別拡張のiframe）。Apps Scriptエディタ・example.comは動く。Sheets操作はApps Script経由で行う。サブエージェントからのブラウザ操作は権限分類器でdeny→本体で実行
- 既知の表示不具合: 台帳T列「滞留日数」が日付書式で表示される（数値は正しい・⚠判定は正常）。Apps Scriptで setNumberFormat("0") を当てれば直る
- 2026-09-05 夜: ohayo §9b新設（`yobo.py alert`＝⚠をステータス別3段で圧縮表示・勝手にステータスを動かさない）／`yobo.py flush`（退避キュー再投入・KY-068健康弁当を投入済）／滞留日数はyobo.py側で受付日・照会日・回答日・最終更新の最大から再計算（T列の日付書式に依存しない）。Todoist「〇〇地区 市民相談」5本アーカイブ済（昼生・南部・井田川・御幸・神辺）。
- 未着手: T列書式＝草川が `~/outputs/yobo-sheet/fix_format.gs` の fixStayDaysFormat() をApps Scriptエディタで1回実行（再デプロイ不要）／台帳の「相手先（要確認）」3件の課名確認／**滞留日数は移行日9/5が最終更新になっているので全件0日から数え直し**（本当の滞留はTodoist時代の期限で判断）

**Why:** Todoistは担当課・回答・報告日を持てず、案件の全体像と滞留が見えない。相談者への報告漏れ防止が目的。
**How to apply:** 相談者がいて市（県・警察・自治会）と動く案件は `yobo.py add`。Todoistは草川自身の議会・政策・イベント・選挙のみ。関連 [[feedback_spreadsheet_deliverable_must_be_native_and_functional]] [[feedback_citizen_inquiry_task_registration]] [[project_todoist_task_migration]]

- 2026-09-05: Apps Script未デプロイ中の `yobo.py add` は `~/outputs/yobo-sheet/_pending.jsonl` に退避する仕様に修正（従来はtraceback）。同日夕方にURL設定済みで書込可を確認（KY-068転校手続き・KY-069健康弁当）。キューは空。以後は台帳直書き
