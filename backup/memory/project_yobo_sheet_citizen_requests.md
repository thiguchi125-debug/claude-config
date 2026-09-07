---
name: project-yobo-sheet-citizen-requests
description: 市役所対応の市民要望はGoogleスプレッドシート「市民要望管理台帳」（yobo.py）。2026-09-05稼働・ohayo §9b＋§5 Inbox棚卸し連携・Todoist13本再編済。残＝実物FB・相手先要確認3件
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
- 2026-09-05 18:16 Apps Scriptで実行済（Chrome経由・エディタは操作可）: fixStayDaysFormat（T列数値書式）＋setupSort（`sort_ledger.gs`）＝X列「並び順」非表示数式キー／完了行グレー(条件付き書式先頭)／毎時sortLedger＋ステータス・期限・報告日編集でonEditSort。並び＝回答済・報告前→受付→照会中→保留→完了、同順位は⚠先・期限昇順、完了は最終更新の新しい順。Web App(_list/_add/_update)は旧デプロイのまま＝CLI更新後の並び替えは毎時トリガー待ち
- 2026-09-05 18:34 `dashboard.gs`（setupDashboard実行済）: 先頭タブ「📱今やること」＝スマホ向け2列（No＋件名／↳次アクション｜期限＋相手先）・区分🔴相談者へ報告→🟠期限切れ→🟡進行中→⏸保留→✅完了(直近10)・台帳編集時＋毎時に再生成（onEditDashboard/buildDashboard）。台帳側は経路/連絡手段/TEL/関連リンク/旧TodoistIDを非表示・件名等を折り返し・行1列A固定
- **草川の問い（9/5夜・未回答のまま区切り）**: ①見にくい→ダッシュボードで対処、実物FB待ち ②Todoistのカテゴリ乱立を整理し台帳との使い分け＋スマホでの一次保存先＋振り分けタイミングを確立したい ③スプレッドシートが本当に最適か、独自アプリの方がよいか（動機＝市民要望には台帳が必要）
- **エディタ操作の癖**: 関数ドロップダウンは保存クリックで「setup」に戻る＋メニューが開いたまま実行すると前の関数が走る→「保存→選択→メニューが閉じたのを確認→実行」の順。コード追加はpbcopy→cmd+vが安全（typeは自動閉じ括弧で崩れる）
- 未着手: 台帳の「相手先（要確認）」3件の課名確認／**滞留日数は移行日9/5が最終更新になっているので全件0日から数え直し**（本当の滞留はTodoist時代の期限で判断）

**Why:** Todoistは担当課・回答・報告日を持てず、案件の全体像と滞留が見えない。相談者への報告漏れ防止が目的。
**How to apply:** 相談者がいて市（県・警察・自治会）と動く案件は `yobo.py add`。Todoistは草川自身の議会・政策・イベント・選挙のみ。関連 [[feedback_spreadsheet_deliverable_must_be_native_and_functional]] [[feedback_citizen_inquiry_task_registration]] [[project_todoist_task_migration]]

- 2026-09-05: Apps Script未デプロイ中の `yobo.py add` は `~/outputs/yobo-sheet/_pending.jsonl` に退避する仕様に修正（従来はtraceback）。同日夕方にURL設定済みで書込可を確認（KY-068転校手続き・KY-069健康弁当）。キューは空。以後は台帳直書き

- **2026-09-05 夜（Todoist使い分け再編・完了）**: 草川の問い②に回答。Todoist 35本→**親8本＋子5本＝13本**（新設📝議会（会期別）・空箱22本アーカイブ・中身あり子3本は🎪直下へ）。教訓＝REST `POST /projects/{id}` は parent_id を受けない→**移動は Sync API `project_move`**。親をarchiveすると子も畳まれる（unarchiveで復旧・タスク75件は無傷）。`td.py mv <id> <PJ名>` 新設（bak-20260905あり）。判定1問「終わったら誰かに報告するか？→はい＝台帳」＋一次保存先＝Todoist Inbox＋ohayo §5「Inbox棚卸し」（台帳へ／箱へ／捨てる／残す）を CLAUDE.md・OPERATIONS【B】・task-add・smart-intake 7/7b に反映。Inboxの6件は翌朝ohayoで初回棚卸し。問い③（独自アプリ可否）は未回答＝実物FBの後

- **2026-09-06 案A適用済（シート側）**: Apps Script（コード.gs 1本に全関数）へ sort_ledger/dashboard 新版＋rename_status.gs を投入し `renameStatusA` 実行→「ステータス付け替え完了: 69件」。yobo.py list で確認＝これから聞く46／返事待ち18／様子見3／相談者に報告2／完了0。旧名称はゼロ。エディタの `_add` 既定値も「これから聞く」に修正済（Web Appは旧デプロイのまま・yobo.py側が明示送信するので再デプロイ不要）。**次＝草川手番＝既存69件の一気棚卸し**（PCで台帳直編集・「これから聞く」だけフィルタして上から）→「棚卸し終わった」で食い違いを洗う。編集の癖：貼付は cmd+v 不可→monaco setValue、関数選択はマウス不可→JSで option を scrollIntoView してから座標クリック
- **台帳の実体URL（正）**: https://docs.google.com/spreadsheets/d/1-qocheanDQRcyUqsixp9EU3Qz6BltTPTbGzfl83cOJ8/edit ＝ Apps Scriptが変換生成した「市民要望管理台帳_v1」。Drive上の **xlsx `1x2Ut5GH68JZKGI9qq77aNOOjNndgXt9O` は変換元の抜け殻**（9/6に草川がこれを開いて「変わってない」と誤認）。案内するときは必ず上のURL。xlsxは9/6にゴミ箱へ（草川指示）。台帳フォルダ内は正本シート1本のみ
- **2026-09-06 17:08 追加修理（fixLayout）**: 案A適用直後、台帳タブで69件が約900行の空行の下へ押し出され「空っぽ」に見えた。真因＝「並び順」数式が空行で `""` を返し、Sheetsのsortで空文字が実データより先頭に並ぶ。修理＝空行は `"zzzz"` を返す数式に張り替え（`fix_layout.gs`・ローカル `sort_ledger.gs` も同修正）＋集計タブの値セル4件（受付/照会中/回答済・報告前/保留）を新名称へ。ログ「修理完了: 先頭行=KY-018 見出し置換=4件」。**教訓＝ソート列の数式は空行に空文字を返させない**
- 2026-09-06 17:13: 台帳の固定列を「要望内容（件名）」まで（E列・5列）に変更（草川指示・`freezeToSubject`）。ローカル dashboard.gs の setupDashboard も同値に更新
- **2026-09-07 棚卸し後の食い違い一括修正（69件更新・失敗0）**: 草川がステータス入力を完了→本体で洗い出し→AskUserQuestion 4問で決定→`yobo.call` で一括update。①期限切れ48件をステータス別に付け直し（これから聞く→9/14／返事待ち→9/19催促／相談者に報告→9/9／様子見は期限を消す。期限空の動く案件にも同ルール）②返事待ち31件の照会日を受付日で埋めた③KY-069健康弁当・KY-076コミバスは完了が入力ミス→これから聞くへ戻した④相談者に報告3件（KY-023/018/003）は回答メモ空→次アクション「回答メモを書く→相談者へ報告」期限9/9＝**草川手番**⑤返事待ちなのに「照会」文言の次アクション4件を「回答を回収」へ。残＝相手先「要確認」9件（KY-004/014/036/054/070-074）とKY-074の内容・相談者補記＝草川手番。教訓＝Todoist時代の期限は台帳へ持ち込むと全件⚠になる。棚卸し後は必ず期限の付け直しを1回挟む

- **2026-09-07 朝の残件処理（完了）**: Todoist Inboxの市民要望4件を台帳へ移行＝KY-078 さんぺいさん宅前道路（これから聞く・9/14）／KY-079 北町の木（返事待ち・催促9/20）／KY-080 前田川の竹・県部分（返事待ち・催促9/20）／KY-081 加太の道路・Instagram（これから聞く・9/14）。Todoist側4件は完了処理。相手先は4件とも「要確認」＝草川手番。**期限一括整理は草川判断で「変更なし」**：+7/+14ルールを機械適用しても02:30の付け直し（9/14／9/19）とほぼ同じで、手置きの5件（KY-016 9/30・KY-069 9/8等）を壊すだけ。+7/+14は新規登録の既定値としてのみ使う


## 2026-09-07 Todoistミラー（草川「今日やることを1箇所で見たい」）
- `~/.claude/scripts/yobo/yobo_mirror.py`＝台帳→Todoist一方向ミラー。対象＝未完了で次アクション期限が今日+3日以内／期限超過／ステータス「相談者に報告」。写し先＝🏛議員活動／🗂台帳フォロー（自動）セクション、件名「KY-xxx 件名 ｜ 次アクション」・期限＝次アクション期限。相談者名は写さない
- 起動＝`yobo.py add/update/done` の直後に自動＋毎朝ohayo§9b。状態＝`~/.config/yobo/mirror_state.json`（KY→sig,task_id）。台帳側が変われば旧を閉じて作り直し、完了・期限消去なら閉じる。Todoist側で完了しても台帳は動かない（草川の一言で yobo.py 更新→ミラーが閉じる）
- 全件写すと65件でTodoistが台帳の複製になるため3日窓にした。9/14に30件・9/19に25件の期限が固まっている（9/6案Aの一括設定）＝その週は窓に入った時点でohayoが振り直す
- 日曜改修ルールの例外＝草川の直接要望で月曜に実装（約80行）
