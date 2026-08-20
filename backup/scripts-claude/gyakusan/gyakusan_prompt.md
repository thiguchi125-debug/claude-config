あなたは草川たくや（亀山市議会議員）の週次バッチとしてheadless実行されています。人間は見ていません。質問・確認は一切できません。

`~/.claude/skills/gyakusan/SKILL.md` をReadし、その Step1〜4 を**候補表示モード**で実行してください。

重要な注意：
- **最初に必ずToolSearchで Google Calendar / Notion のMCPツールをロードする**。MCPはdeferredで起動しているため、ToolSearchする前に「MCP未接続」と判定して終了することを禁止する。
- **Todoistへの登録は一切しない**（草川の承認前に書き込まないのが本スキルの原則）。`td.py` は既存タスクの読み取り（`week` / `list`）のみに使う。
- 提案は上位5件までに畳む。それ以上は件数だけ添える。
- 結果を `~/.claude/scripts/gyakusan/_gyakusan_status.json` に次の形で書き出す（これを翌朝以降のohayoが読む）:
  {"generated_at":"YYYY-MM-DD HH:MM","total":<総件数>,"items":[{"event":"<イベント名>","date":"YYYY-MM-DD","task":"<不足している準備タスク>","due":"YYYY-MM-DD"}],"note":"<補足・0件なら漏れなし>"}
- 漏れ0件でも `total: 0` でファイルを必ず書く（古い週の候補が残り続けるのを防ぐ）。
- 最後に必ず `python3 ~/.claude/scripts/sns-routine/update_status.py gyakusan <ok|error> "<結果メッセージ>"` を実行する。
