---
name: feedback_general_question_architect_agent
description: 一般質問設計の専任エージェント general-question-architect を新設（2026-06-02）。意味ある一般質問を時間内に構築する規律をコード化
metadata: 
  node_type: memory
  type: feedback
  originSessionId: aacc0097-07d8-4744-b796-012cd6720635
---

**新設エージェント `general-question-architect`**（`~/.claude/agents/general-question-architect.md`・2026-06-02新設）。

**Why**：6月議会一般質問prepで、質問構築の"効く部分"（協定の既決返球封じ・報告返球封じ・重複排除・時間圧の武器化）が毎回草川の対話指摘頼みで、既存エージェント（counter-argument-simulator＝想定答弁準備／council-material-creator＝原稿化／bill-scrutiny-architect＝議案質疑）に「限られた時間内で"意味のある一般質問そのもの"を設計する専任」が無かった。草川「エージェントが機能してない。意味のある一般質問を限られた時間内で構築できるエージェントが必要」（2026-06-02 直接指示）。

**How to apply**：
- bill-scrutiny-architect の一般質問版。トリガー：「一般質問を設計」「意味のある一般質問」「時間内に収まる質問」「逃げられない質問にして」「重複を排除して」「45分に収めて」「報告返球を封じて」等。
- 6つのオーナーシップ：①5価値フィルター ②**時間バジェットエンジン**（答弁込み45分逆算・1往復1仕事・撤退ライン）③**逃げ封じ設計**（既決返球/報告返球/検討中逃げ/デリケート逃げを「先に認めてから刺す」で封じる＋時間圧の武器化）④重複排除＆流れ（1往復1仕事・再質問階段）⑤既決チェック（協定/可決議案/現況報告/計画/過去答弁と照合）⑥市民翻訳・アーカイブ/voice整合。
- 出力＝一般質問設計書（全7セクション：45分の地図／既決チェック／中項目設計〈話す〉骨子付／重複排除ログ／時間検算／逃げ封じカード集／通告書要旨）。
- 後工程＝counter-argument-simulator（想定答弁3パターン）／council-material-creator（原稿化）／content-fact-checker→content-risk-reviewer。
- **登録の注意**（[[feedback_agent_registry_partial_load]]）：新設.mdは作成セッション中はAgentツール一覧に未登録＝再起動で登録。それまではgeneral-purposeに.mdを読ませて代走可（6月議会prepでは代走で実適用＝89K tokens・一次資料10回照合で②③系を本格再設計し新問題4件を掘り当てた実績あり）。

関連：[[project_ippan_shitsumon_2026-06_resume]]（初適用案件）／[[feedback_ippan_shitsumon_theme_priority]]（テーマ選定）。
