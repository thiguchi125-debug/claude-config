---
name: reference-routine-unkohyo
description: 日々のClaude Codeルーティン一覧「ルーティン運行表」の正本パスと更新トリガー
metadata: 
  node_type: memory
  type: reference
  originSessionId: 132617a9-262a-4fab-a575-730648975da6
  modified: 2026-08-26T16:39:26.854Z
---

日次ルーティン（自動7本／呼べば動くもの／止めたもの／手番待ち）を1枚にまとめた運行表。

- **正本HTML**: `~/outputs/routines/routine_unkohyo.html`
- **アーティファクト**: https://claude.ai/code/artifact/b8948857-7c61-45f8-bb02-c9875920602b
  （更新は同じファイルパスを再publish、または他セッションからは `url` にこのURLを渡す。新規発行しないこと）
- **更新トリガー**: 「運行表更新して」
- 2026-08-26の簡素化を反映して作成。ジョブを増減したら [[project_sns_routine_v2]] と
  [[project_discord_channel_split]] と合わせてここも直す。

[[project_ai_env_map_notion_embed]] の作業環境マップ（スキル・エージェントの俯瞰図）とは別物。
あちらは「何があるか」、こちらは「いつ何が動くか」。

関連: [[project_nightly_jobs_missing_agent_tool]]（運行表の「手番待ち①」）／
[[project_news_briefing_digest_gate_deny]]（同②）
