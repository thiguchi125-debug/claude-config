---
name: reference_speech_to_drive_smartphone
description: 2026選挙の演説原稿・手元メモをvaultからスマホ用Googleドキュメントにして専用Driveフォルダへ送る仕組み（speech_to_drive.py＋Drive MCP）
metadata:
  type: reference
---
2026-10-17 構築。呼び方＝「〇〇をスマホに送って」。

**置き場**：マイドライブ「🗳2026選挙/01_演説原稿」（2026-10-18に旧「2026選挙_演説原稿（スマホ用）」を移設・名前変更、IDは同じ）id `1Rm_mIT3ieiCn8c4zoSlBmbkZuLF0VvP3`／同「旧版」id `17zVZK_X2_2HYbYxVL7_tU2qzdRoBznqH`。`_root_intake.py` の PROTECTED_DIRS は「🗳2026選挙」で保護（そもそも直下のフォルダは動かさない実装）。

**手順（Claudeが行う）**
1. `python3 ~/.claude/scripts/speech_to_drive.py build <vaultのmd>` → タイトル（例「10-18 出陣式挨拶 v2」）・HTMLパス・move_to_old をJSONで出す。要旨節を先頭へ・裏方節（出典/切り出し/講演由来/動画/つながり等）と「状態:」行を除外。`--all` で全部入り。
2. Drive MCP `create_file`（title, textContent=HTML, contentMimeType=`text/html`, parentId=フォルダid）→Googleドキュメントに変換される。
3. move_to_old があれば `update_file(fileId, parentId=旧版id)`。削除・上書きはしない（[[feedback_never_overwrite_delivered_drive_file]]）。warningが出たら同名既存＝別名で作る。
4. `speech_to_drive.py record <md> --id <新id>` → 台帳 `~/.claude/scripts/speech_to_drive_ledger.json` 更新・URL出力。

**なぜMCP経由か**：Pythonから使えるGoogle API認証がこのMacに無い（yoboはApps Script・Sheet専用、googleapiclient未導入、rclone未設定）。完全自動化するならOAuthクライアント作成かApps Script WebAppの新設が必要＝草川判断。
**検証済み**：HTMLの inline font-size はDocsで保持される（ODTエクスポートで本文16pt・見出し19/22ptを確認）。見出し・太字・番号リスト・改行も崩れない。
使い方メモ＝vault `10_ClaudeCode/設定/演説原稿をスマホへ送る手順.md`。

**2026-10-18 改定**：草川「スマホだと死ぬほど読みにくいし修正しにくい」→ 既定を**読み上げ専用の薄い版**（【要旨】【本文】だけの普通の文字・text/plainで送る）に変更。見出し・太字付きの旧形式は `--rich`。直しはスマホでせず会話に貼るか、build時にvaultの原稿の隣へ自動で置かれる `<原稿>_読み上げ.md`（同じ薄い版）に #注記 を書いてもらう（既存なら上書きしない）。
