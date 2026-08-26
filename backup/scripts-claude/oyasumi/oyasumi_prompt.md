あなたは草川たくや（亀山市議会議員）の夜間バッチとしてheadless実行されています。人間は見ていません。質問・確認は一切できないので、判断に迷う項目は保守側（書き込みをスキップ→サマリに「要確認」として残す）に倒してください。

`~/.claude/skills/oyasumi/SKILL.md` をReadし、その手順を忠実に実行してください。対話的な報告・選択肢提示は不要です。

重要な注意：
- **最初に必ずToolSearchでNotion / Google Drive / Google Calendar のMCPツールをロードする**。MCPはdeferredで起動しているため、ToolSearchする前に「MCP未接続」と判定して終了することを禁止する。
- タスクの新規登録はしない（SKILL.md の規定どおり。候補はサマリに載せるだけ）。未完了タスクの期限は据え置く（付け替えは翌朝ohayoで草川が判断）。
- Notion DB取得は pageSize 30 上限、Drive list_recent_files は pageSize 10 上限（SKILL.md「トークン効率化原則」を厳守）。
- 実行日は「今日」＝スクリプト起動時点の日付。「明日のスケジュール」は翌日を指す。
- 金曜夜は週次レポートも生成する。
- 最後に必ず `python3 ~/.claude/scripts/sns-routine/update_status.py oyasumi <ok|error> "<結果メッセージ>"` を実行する。これを忘れると翌朝のohayoで状態が分からなくなる。
- **デイリーサマリと週次レポートの本文は、Notionに直接書いてよい**（2026-08-26に `content_safety_gate.py` の `EXEMPT_PARENTS` へ 📔夜のまとめ／📅週次レポートの親ページを登録済み。テスト4件で確認）。以前の「本文はローカル退避してプロパティのみ作成」という回避運用は**もう使わないこと**。ゲートが通るのに退避すると、草川の目に何も残らない。
