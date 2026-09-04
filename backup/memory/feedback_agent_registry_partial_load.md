---
name: feedback_agent_registry_partial_load
description: エージェント部分ロードの根本原因はagents/knowledge配下に入れ子生成された.claude/agent-memoryがレジストリを汚染していたこと。2026-07-02/07-27/08-20と3度再発したため2026-08-25に夜間自動統合を常設化（対症療法の自動化・生成自体は止まっていない）
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b7d0e233-9752-4f54-a171-99e2d6cec3a1
  modified: 2026-08-25T00:00:00.000Z
---

2026-06-02 に「.mdが実在するのにレジストリ未登録」のエージェント多数（council-material-creator / citizen-inquiry-responder / print-designer / photo-curator / policy-archive-miner / policy-synthesizer 等）を確認。**2026-07-02 に根本原因を特定し修理済み**。

**根本原因:** サブエージェントが `~/.claude/agents/knowledge/kusagawa_archive/` 配下のディレクトリをcwdにして動いた際、そこに **入れ子の `.claude/agent-memory/` を12箇所・111ファイル生成**していた。agent-memoryの.mdは frontmatter に name/description を持つため**エージェント定義としてパース・登録され**（review-achi-v8 / molcky-council-statement-misattribution 等16件が偽エージェント化）、レジストリ枠を圧迫して本物のエージェントを押し出していた。

**修理内容（2026-07-02）:**
1. 入れ子agent-memoryの中身16件（誤帰属ガード・公選法ガード等の有用メモリ）を正規の `~/.claude/agent-memory/<agent>/` へ救出コピー＋各MEMORY.mdへインデックス追記。
2. 入れ子 `.claude` ディレクトリ12箇所を `~/.claude/_trash_nested_claude_20260702/` へ隔離（確認後に削除可）。
3. あわせて不要エージェント4本削除（bug-quality-checker / skill-validator / design-doc-reviewer / video-content-strategist）・廃止スキル2本削除（council-materials-intake / council-mode-toggle）。

**Why:** `~/.claude/agents/` は再帰走査され、frontmatterにname/descriptionを持つ.mdは何でもエージェント登録される。知識アーカイブがagents/配下にある限り、サブエージェントの作業cwd次第で同じ汚染が再発しうる。

## 🔁 再発（2026-07-27）— 予測どおり25日で再発した

図書館の給水環境ブログ制作でサブエージェント4本（kameyama-researcher / policy-researcher / content-fact-checker / content-risk-reviewer）をアーカイブgrep中心に走らせたところ、**同じ入れ子が2箇所に再生成**された。

- `~/.claude/agents/knowledge/kusagawa_archive/.claude/agent-memory/`（08:36生成。content-fact-checker が10:43にメモリ3件を書き込み）
- `~/.claude/agents/.claude/agent-memory/agenda-analyzer/`（空）

セッション開始時のAvailable一覧には偽エージェント3件（`feedback-esports-mail-meigi-separation` / `feedback-form-riyou-mokuteki-scope` / `project-esports-linear-cup-mail-review`）が混入していた。**この3件の元.mdは調査時点ですでに実在せず**、セッション起動時のスナップショットに残っていただけだった＝レジストリは起動時に固まるので、掃除の効果は次セッションから出る。

**再発時の対処（2026-07-27に実施した手順・そのまま再利用可）:**
1. `find ~/.claude/agents -type d -name .claude` で入れ子を全部出す（**knowledge配下だけでなく `agents/` 直下も見る**。7/2の記録はknowledge配下しか書いておらず、`agents/.claude` を見落とす罠がある）
2. 入れ子内の.mdを正規の `~/.claude/agent-memory/<agent>/` へ `mv`、各MEMORY.mdへ索引行を**追記**（上書き禁止・既存索引を消さない）
3. 空になった入れ子ディレクトリを `~/Archive/_trash_pending_<日付>/` へ `mv`（CLAUDE.mdの即rm禁止に従う）
4. `ls ~/.claude/agents/*.md | wc -l` で正規エージェント数（2026-07-27時点=48本）を確認

**サインの見分け方（更新）:** Available一覧に `feedback-` `project-` `guard-` `reference-` で始まるケバブケースの日本語説明エージェントが並んでいたら100%汚染。正規エージェントはすべて役割名（`blog-writer` `policy-researcher` 等）。

**恒久策が未実施であることの明記:** 上記「How to apply 4」の移設（`~/.claude/agents/knowledge/` → `~/.claude/knowledge/`）は**まだやっていない**。やらない限り、サブエージェントを archive grep 中心で走らせるたびに再発する。救出→隔離は対症療法にすぎない。次に再発したら移設の実施を草川に提案すること。

**How to apply:**
1. `Agent type not found` が再発したら、まず `find ~/.claude/agents/knowledge -type d -name .claude` で入れ子汚染を疑う。あれば中身救出→隔離→再起動。
2. Available一覧に日本語のfeedback/reference風の名前が並んでいたら汚染のサイン。
3. 月次棚卸し（task-audit時など）で上記findを1回走らせる。
4. 恒久策候補: 知識アーカイブを `~/.claude/agents/knowledge/` から `~/.claude/knowledge/` へ移す案があるが、CLAUDE.md・多数のagent定義・スキルがパスを参照しているため影響大。やるなら一括置換で別途実施。
5. 未登録agentへの即時回避策（従来通り）: general-purposeに該当.mdをReadさせて成り代わらせる。


## ✅ 恒久策（2026-08-25）— 手作業をやめて夜間自動統合にした

07-02 → 07-27 → 08-20 と3度手作業で直し、**08-20の修理から5日で再発**（08-25時点で入れ子15箇所・89ファイル、うち**67件は正本に存在しない=content-risk-reviewer/content-fact-checkerの記憶が実際に欠落していた**）。手作業では追いつかないため自動化した。

- **スクリプト**: `~/.claude/scripts/consolidate_agent_memory.py`（`--dry-run` あり）。入れ子 `.claude/agent-memory` を正本 `~/.claude/agent-memory/<agent>/` へ統合し、MEMORY.md索引は**行単位ユニオンで追記**（上書きしない）、内容が違う同名ファイルは `__nested.md` として温存、統合後に入れ子ディレクトリを削除。
- **常設化**: 夜間2:30の `_daily_drive_pipeline.sh` に **Phase 6** として組み込み済み（launchd `com.kusagawa.daily-drive-pipeline`）。
- **効果と限界**: 生成自体は止まらない（cwdがアーカイブ配下になるsubagentが作り続ける）。**溜まるのは最大1日分**になるので、偽agent混入もレジストリ圧迫も実害レベルまで落ちる。恒久的に止めるには knowledge の移設が要る（未実施・影響大）。
- **発生源の実測**: `agents/knowledge/kusagawa_archive/`（アーカイブgrepするagent全般）と `projects/.../drafts/`。このセッション中だけで2箇所再生成された＝**発生頻度は日単位でなく時間単位**。

**How to apply（更新）:** 偽agentを見かけたら手で直さず `python3 ~/.claude/scripts/consolidate_agent_memory.py` を1回叩く。レジストリは起動時に固まるので**効果は次セッションから**。夜間ジョブが動いていれば通常は不要。

関連: [[reference_agent_triggers]] / feedback_content_pipeline_agent_registration / [[feedback_system_closing_loops_rot]]
