---
name: project_token_efficiency_overhaul_2026-09-05
description: "2026-09-05 燃費改善。実測で主因3つ（[1m]窓で文脈>200Kが本体51%／fact-checker 1本5.5M／自動ジョブ1回15M）を特定し設定・agent・ジョブを改修。効果測定は9/19に token_report.py で前後比較"
metadata: 
  node_type: memory
  type: project
  originSessionId: 2cf90bb1-7b55-4239-b25b-3e63a0b29c05
  modified: 2026-09-04T23:10:42.738Z
---

# トークン燃費改善（2026-09-05）

**実測（8/22〜9/4）**: 4,931M／35,388呼出。本体2,764Mのうち文脈>200Kの呼出が51%（`claude-fable-5-1[1m]` で988Kまで伸びた）。サブ2,194M＝44%（fact-checker 549M・100本・平均50回、general-purpose 792M の大半は孫起動）。夕方SNS便376M＋ニュース便219M＝12%。

**やった改修**
- settings.json: model を `claude-fable-5-1`（200K窓）へ。swift-lspプラグイン停止。バックアップ `settings.json.bak-20260905`
- `hooks/context_budget_notice.py` 閾値 100K/140K/170K→以降50Kごと
- CLAUDE.md トークン節約節を5行に圧縮、詳細は OPERATIONS.md【G】へ（バックアップ `~/.claude/CLAUDE.md.bak-20260905`）
- content-fact-checker.md に「予算と台帳」節（取得15回上限・Agent禁止・`verified_claims` 入力・台帳追記）
- 新設 `agents/knowledge/fact_ledger/verified_facts.tsv`（検証済み主張の台帳。fact-checkerが先にgrep）
- notion-saver.md に予算節（notion-fetch は最大1回・30回で打ち切り）
- `news_briefing.sh` に `--model claude-sonnet-5 --max-turns 60`／`sns_leg.sh` に `--max-turns 60`

**未着手の提案（草川判断）**: superpowersプラグイン停止／content-risk-reviewer の MEMORY.md 41KB圧縮／MEMORY.md 完了案件の退避／effortLevel medium／ゲート統合（短文SNSは fact+risk 1本）

**Why:** 「大したことしていないのに上限」の正体は、長い文脈で毎回全量を払い直す構造と、ゲート1本が調査エージェント並みに動く構造だった。
**How to apply:** 9/19頃に `python3 ~/.claude/scripts/token_report.py 14 09-05` で前後比較。fact-checkerの1本あたり呼出が20回以下、文脈>200Kの割合が0に近いことを確認。悪化していれば settings.json.bak から戻す。関連 [[project_token_reduction_2026-08-20]] [[feedback_token_report_blind_to_subagents]]
