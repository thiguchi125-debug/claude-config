---
name: feedback_agent_registry_partial_load
description: セッションによっては主要エージェントが部分ロードで未登録になる。council-material-creator等が起動不可になる事象と回避策
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7d0e233-9752-4f54-a171-99e2d6cec3a1
---

2026-06-02 のセッションで、`~/.claude/agents/` に .md が**実在するのに launchable レジストリに載っていない**エージェントが多数あることを確認（Agent起動で `Agent type 'X' not found. Available agents: ...` が返って判明）。

**未登録だった主要エージェント（.mdは在る）**: council-material-creator / citizen-inquiry-responder / policy-archive-miner / policy-synthesizer / policy-validator / photo-curator / print-designer / design-director / design-doc-reviewer / design-inspiration-researcher / bug-quality-checker / skill-validator。
**逆にレジストリに紛れていた非エージェント**: feedback-giji-filename-crossed / kameyama-kansaisen-kusatsusen-facts / qa-pair-misattribution-across-questioners / rebuttal-structure-decoupled-from-teroppu / pre-election-policy-resolve-not-vote-solicitation（=memory/feedbackノートがagent扱いで登録）。

**Why:** 「.mdが在る＝起動できる」ではない。レジストリはセッション開始時に構築され、その時の読込対象次第で部分集合になる。CLAUDE.md/MEMORY.md は多数のagentが常時使える前提で書かれているため、未登録だとブログ安全ゲート（content-fact-checker→content-risk-reviewerは登録あり／但しcitizen-inquiry-responder等は未登録）・市民相談・印刷物・政策系の自動運用が無言で欠落しうる。

**How to apply:**
1. エージェント起動前提のタスクで `not found` が出たら、まず **`Agent type ... not found` のAvailable一覧で実レジストリを確認**（表示されたツール説明の「利用可能一覧」は抜粋で不正確）。
2. **正攻法の修復＝Claude Code 再起動**で `~/.claude/agents/` を再走査させ、登録され直すか確認。
3. それでも載らなければ**読込上限/設定の問題**として別途調査（registryの構築元・上限を確認）。
4. **即時回避策＝`general-purpose` エージェントに未登録agentの .md を Read させ、その指示・役割・返却原則ごと成り代わらせる**（例: council-material-creator.md を読ませて骨子生成。挙動ほぼ同等）。
5. この事象が再発するか次セッションで要確認（transientか恒常かは未確定。2026-06-02時点の観測）。

関連: [[reference_agent_triggers]] / [[feedback_content_pipeline_agent_registration]]（agentは ~/.claude/agents/ 直下配置必須＝配置は満たしているのに未登録だった点が新事象）
