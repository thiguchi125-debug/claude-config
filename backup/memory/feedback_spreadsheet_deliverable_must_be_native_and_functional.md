---
name: feedback-spreadsheet-deliverable-must-be-native-and-functional
description: 「スプレッドシートで管理したい」＝ネイティブGoogleスプレッドシート＋運用機能まで。CSVをDriveに置くのは納品ではない
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a8a4c6b6-7f0f-49d2-ac05-764d02aae063
  modified: 2026-08-26T14:25:19.315Z
---

草川が「**スプレッドシートで管理したい**」と言ったら、求めているのは
**①ネイティブのGoogleスプレッドシート（開いてすぐ編集・自動保存できる状態）**
**②管理表として機能すること**（数式・入力規則・色分け・集計）の2つ。

2026-08-26の後援会管理表で、CSVをDriveフォルダに置いただけで「保存しました」と報告し、
「よくわからん / googleスプレッドシートに保存できたのか / ウグイス管理表みたいに機能的なのがいい」と差し戻された。

**Why:** DriveにCSVを置いてもDrive上ではCSVアイコンのままで、開いても素の一覧。
「保存先が正しいこと」と「草川が使えること」は別物で、草川が見ているのは後者だけ。
xlsxのままDriveに置いた場合も、プレビュー画面は読み取り専用なので「編集が保存されない」事故になる。

**How to apply:**
- 納品形は **ネイティブGoogleスプレッドシート**。xlsxのままDriveに置いて終わりにしない。
  MCPコネクタにSheets書込APIが無いので、xlsxを置く→草川が「ファイル→Googleスプレッドシートとして保存」を
  1回押す、が現状の唯一の経路。**その1クリックが必要なことを渡す時に必ず言う**（黙って渡さない）。
  ※ ネイティブ化すると以後こちらから一括更新できなくなる。作り直しは別名xlsxで渡す。
- xlsxの base64 を Drive `create_file` に直接渡す経路は**使えない**。
  35KBのxlsx＝base64 46KBがpersisted-outputに逃げてツール引数に貼れない。Drive同期フォルダ経由が確実。
- 機能面の最低ライン（openpyxlで作れる）：
  1行目固定・オートフィルタ・入力規則のプルダウン・ステータス別の行色分け・
  「要対応」を数式で自動判定・集計ダッシュボードのタブ・**記録を1行足すと名簿側が自動更新される導線**。
- 生データのCSVは「再生成用の控え」として残してよいが、どれを開けばいいかを1行で明示する。

関連: [[feedback_never_overwrite_delivered_drive_file]] [[project_koenkai_roster_two_systems]]
