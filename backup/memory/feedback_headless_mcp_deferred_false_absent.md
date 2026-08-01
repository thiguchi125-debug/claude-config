---
name: feedback-headless-mcp-deferred-false-absent
description: headless（launchd/cron）のclaude -pではMCPツールがdeferredで起動し、ToolSearchを知らないジョブが「MCP未接続」と誤判定して黙って不発になる
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a2163459-aad0-42a4-9cca-adfaf85f812d
  modified: 2026-08-01T20:06:19.202Z
---

launchd等の headless `claude -p` 実行では、`--allowedTools` にツールパターンを複数並べるとMCPツール（`mcp__claude_ai_Notion__*` 等）が **deferred（スキーマ未ロード）** で起動する。ジョブのプロンプトに ToolSearch の指示が無いと、モデルは「Notion MCP不在／未接続」と誤判定し、正しく捏造を拒否した結果**成果物ゼロで rc=0 完了**する。ログ上は "ok" なので気づけない。

**Why:** 2026-07-17にSNS便の候補メニューが4回連続不発（7/15夕・7/16夕・7/17朝・7/17夕）。`claude mcp list` は常時 ✔ Connected、launchd環境の実測プローブでも `NOTION_OK`。犯人はMCPの接続ではなく **deferred状態の誤読** だった。実測: `--allowedTools "mcp__claude_ai_Notion__*"` 単独＝EAGER／`Read,Write,Bash(...),mcp__claude_ai_Notion__*`＝**DEFERRED**。ツール登録数が閾値を超えると遅延ロードに切り替わる。

**How to apply:**
- headlessジョブでMCPを使うなら **`--allowedTools` に `ToolSearch` を必ず含める**（無いとロード自体できない）。
- プロンプト冒頭に「deferredは未接続ではない。ToolSearchでロードしてから使う。試す前に未接続と判定するのを禁止」を明記する（sns-routineの `leg_*.md` / `pack_prompt.md` / `triage_prompt.md` / `video_stage_prompt.md` に実装済み）。
- 「MCP未接続」を報告するジョブを見たら、まずこれを疑う。再認証や接続設定をいじる前に、launchd環境で `claude -p` プローブを1本流して EAGER/DEFERRED を判定する。
- 同型の落とし穴: 定時ジョブが「材料が無い」と言って rc=0 で終わるとき、材料が本当に無いのか **読めていないだけ** なのかを必ず区別する（[[feedback_system_closing_loops_rot]] の「締め工程が腐る」の一種）。

**逆パターンもある（2026-08-02実測）:** ToolSearch自体は使えるのに、MCPツールが**1本も登録されていない**夜がある。夜間triageで `select:mcp__claude_ai_Notion__notion-fetch,...` も keyword検索 `+notion` も両方 "No matching deferred tools found" を返し、deferred一覧の中身が `CronCreate/WebFetch/TaskCreate/...` の20本のみでMCPがゼロだった。この場合は**本物の不在**なので、ToolSearchを何度も叩き直さずに queue フォールバック（`_notion_queue.jsonl`）へ即座に降りてよい。判定手順は「①exact `select:` ②keyword ③deferred一覧にMCPが1本でもあるか」の3点確認。①だけの空振りで不在と断定しない（そこが7/17の事故）。

**同夜に form-intake でも再現＋容疑者(2026-08-02 03:59):** 夜間 form-intake も全く同じ「MCPゼロ登録」に当たった（ToolSearch6回＝exact `select:` ＋ `+notion` / `+drive` / キーワード4種、すべて空振り）。**相関する唯一の異常が discordプラグイン**で、`claude mcp list` は claude.ai系5本すべて ✔ Connected なのに `plugin:discord:discord` だけ「connection timed out after 30000ms」で ✘、セッション起動時のsystem-reminderでも discord だけが "still connecting" 表示だった。→ **ローカルpluginのMCPサーバが起動ハングすると、セッションのMCP初期化を巻き込んで claude.ai系サーバのツール登録が丸ごと落ちる**疑い（未確定・要検証）。夜間ジョブが原因不明の「MCP不在」で連続するなら、再認証より先に `~/.claude/plugins/cache/claude-plugins-official/discord/` を一時無効化して切り分ける。この夜の form-intake は SKILL.md 規定どおり state 未更新（S1=48/S2=212/S3=148 据え置き）・Notion/ETL書き込みゼロで終了しており、取りこぼしは無い（翌夜または手動「フォーム取り込んで」で拾い直せる）。

関連: [[project_sns_routine_v2]] / [[project_form_intake_nightly]] / [[feedback_agent_tools_frontmatter_breaks]]（ツール喪失→捏造報告という同系統の事故）
