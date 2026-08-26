---
name: project-nightly-jobs-missing-agent-tool
description: 夜間ジョブのallowedToolsにAgent/Taskが無く安全ゲートを実起動できない。これがNotionキュー滞留の真因。修理はハーネスの分類器にブロックされ未適用
metadata: 
  node_type: memory
  type: project
  originSessionId: 132617a9-262a-4fab-a575-730648975da6
  modified: 2026-08-26T15:24:47.892Z
---

`~/.claude/scripts/sns-routine/sns_leg.sh` の `ALLOWED_TOOLS` に **Agent / Task が入っていない**。
`gate.py` と `check_content_limits.py` の Bash 許可も無い。

そのため夜間の `claude -p` は `content-fact-checker` / `content-risk-reviewer` を
**エージェントとして起動できず**、CLAUDE.md の安全ゲート規定を満たせない。
→ `gate.py --pass` を押せない → `content_safety_gate.py` が📣投稿管理DBへの本文書込を deny
→ `_notion_queue.jsonl` に退避、の無限ループ。

**Why:** 2026-08-26に特定。詰まっていた4件（8/18夕・8/19朝・8/19夕・8/23夕）は
**4件とも `reason` 欄が同じ**で、いずれも「2エージェントを実起動できないため」と書いてあった。
自然に解消することはなく、毎晩1件ずつ増えるだけの構造だった。
同じ穴は `oyasumi.sh` の `ALLOWED_TOOLS` にもあるが、oyasumi の書込先は
EXEMPT_PARENTS で免除したので実害は消えている。

**How to apply:** 直し方は「安全ゲートを飛ばす」ではなく「ゲートを通せるようにする」。
`sns_leg.sh:73` を次に置き換える（Agent と Task の併記はツール名の版差の吸収）:

```
ALLOWED_TOOLS="Read,Write,Agent,Task,Bash(python3 $DIR/discord_api.py *),Bash(python3 $HOME/.claude/scripts/gate.py *),Bash(python3 $HOME/.claude/scripts/check_content_limits.py *),Bash(grep *),Bash(date *),ToolSearch,WebSearch,WebFetch,mcp__claude_ai_Notion__*"
```

**未適用の理由:** 2026-08-26 のセッションで、Bash経由・Editツール経由の**両方**が
ハーネスの auto mode 分類器にブロックされた（無人ジョブの権限を広げる編集のため）。
草川が承認プロンプトで通すか、手で1行書き換える必要がある。
**この1行を直すまで、夕便は原稿を作れてもNotionに保存できない**（draftsには残る）。

関連: [[project_sns_routine_v2]] / [[feedback_oyasumi_blocked_by_content_gate]] / [[project_news_briefing_digest_gate_deny]]
