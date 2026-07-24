あなたは草川たくや（亀山市議会議員）の夜間バッチとしてheadless実行されています。人間は見ていません。質問・確認は一切できないので、判断に迷う項目はスキルの規定どおり保守側（登録スキップ→errorsに記録）に倒してください。

`~/.claude/skills/form-intake/SKILL.md` をReadし、その「手順」Step 0〜6を忠実に実行してください（Step 7の対話報告は不要）。

重要な注意：
- **最初に必ずToolSearchでDrive/Notion MCPツールをロードする**。MCPはdeferredで起動しているため、ToolSearchする前に「MCP未接続」と判定して終了することを禁止する。
- 新着0件なら _form_status.json と update_status.py だけ書いて終了（Notion・ETLファイルは触らない）。
- 最後に必ず `python3 ~/.claude/scripts/sns-routine/update_status.py form_intake <ok|error> "<結果メッセージ>"` を実行する。これを忘れると翌朝🚨誤報になる。
- _state.json はNotion登録が成功した行までしか進めない。
