---
name: feedback_agent_registry_partial_load
description: エージェント部分ロードの根本原因はagents/knowledge配下に入れ子生成された.claude/agent-memoryがレジストリを汚染していたこと。2026-07-02に隔離修理済み・再発監視ポイントあり
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7d0e233-9752-4f54-a171-99e2d6cec3a1
---

2026-06-02 に「.mdが実在するのにレジストリ未登録」のエージェント多数（council-material-creator / citizen-inquiry-responder / print-designer / photo-curator / policy-archive-miner / policy-synthesizer 等）を確認。**2026-07-02 に根本原因を特定し修理済み**。

**根本原因:** サブエージェントが `~/.claude/agents/knowledge/kusagawa_archive/` 配下のディレクトリをcwdにして動いた際、そこに **入れ子の `.claude/agent-memory/` を12箇所・111ファイル生成**していた。agent-memoryの.mdは frontmatter に name/description を持つため**エージェント定義としてパース・登録され**（review-achi-v8 / molcky-council-statement-misattribution 等16件が偽エージェント化）、レジストリ枠を圧迫して本物のエージェントを押し出していた。

**修理内容（2026-07-02）:**
1. 入れ子agent-memoryの中身16件（誤帰属ガード・公選法ガード等の有用メモリ）を正規の `~/.claude/agent-memory/<agent>/` へ救出コピー＋各MEMORY.mdへインデックス追記。
2. 入れ子 `.claude` ディレクトリ12箇所を `~/.claude/_trash_nested_claude_20260702/` へ隔離（確認後に削除可）。
3. あわせて不要エージェント4本削除（bug-quality-checker / skill-validator / design-doc-reviewer / video-content-strategist）・廃止スキル2本削除（council-materials-intake / council-mode-toggle）。

**Why:** `~/.claude/agents/` は再帰走査され、frontmatterにname/descriptionを持つ.mdは何でもエージェント登録される。知識アーカイブがagents/配下にある限り、サブエージェントの作業cwd次第で同じ汚染が再発しうる。

**How to apply:**
1. `Agent type not found` が再発したら、まず `find ~/.claude/agents/knowledge -type d -name .claude` で入れ子汚染を疑う。あれば中身救出→隔離→再起動。
2. Available一覧に日本語のfeedback/reference風の名前が並んでいたら汚染のサイン。
3. 月次棚卸し（task-audit時など）で上記findを1回走らせる。
4. 恒久策候補: 知識アーカイブを `~/.claude/agents/knowledge/` から `~/.claude/knowledge/` へ移す案があるが、CLAUDE.md・多数のagent定義・スキルがパスを参照しているため影響大。やるなら一括置換で別途実施。
5. 未登録agentへの即時回避策（従来通り）: general-purposeに該当.mdをReadさせて成り代わらせる。

関連: [[reference_agent_triggers]] / [[feedback_content_pipeline_agent_registration]] / [[feedback_system_closing_loops_rot]]
