---
name: project_toben_tracker
description: 答弁・約束トラッカー＋実績コンパイラー（toben-tracker）と意見書・要望書ドラフター（ikensho-drafter）の構築記録（2026-07-08）
metadata: 
  node_type: memory
  type: project
  originSessionId: a7b8d821-7fc1-4265-bff8-9f4453960fc6
---

2026-07-08構築。設計書=~/claude-config/docs/specs/2026-07-08-toben-tracker-ikensho-design.md（同日commit済）。

**toben-tracker**（agent）: 市答弁の約束を台帳化→回収→実績化。台帳正本=`kusagawa_archive/07_commitments/ledger.json`（スキーマ=同SCHEMA.md・Notionミラーは閲覧用）。4モード=①抽出（草川＋市答弁ペアのみ）②回収チェック③Todoist連携（承認後td.py）④実績コンパイル（3形式＋未発信ギャップ一覧・fact-checker必須・attribution誤帰属ガード）。

**SNS実査は毎回伺い必須（草川指示・恒久）**: Instagram/Threads/XのChrome実査は実行のたびに明示承認を取る。無断でログイン済みセッションに触らない。読み取り専用。

**ikensho-drafter**（agent）: 99条議会意見書＋市への要望書。様式知識=`agents/knowledge/ikensho/ikensho_yoshiki.md`。名義整理→アーカイブ接地→安全ゲート→txt納品。

**kickoff連携**: general-question-prep SKILL.mdにStep 4.5追加（ledger.jsonから今会期の回収候補を自動提示）。

バックフィル: kusagawa_only議事録30本（8年分）から並列抽出→草川一括承認→台帳投入。**ローカル欠落会期=2023-12（R05-12）・2024-03/06/09（R06-03/06/09）**——Driveから取得すれば追補可能。

関連: [[feedback_system_closing_loops_rot]] [[feedback_giji_kusagawa_response_only]] [[feedback_no_other_council_members_names]]
