---
name: feedback_bill_scrutiny_scriptwriter_agent
description: 議案質疑/一般質問の本番原稿化を仕組み化。新agent bill-scrutiny-scriptwriter＋共通craftファイル＋council-material-creator底上げ
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 44f1e63d-ceae-4780-833e-e2b5e09eb5f0
---

議案質疑の本番原稿づくり（2026-06 太陽光条例で本人OK＝成功）を、将来も再現できるよう仕組み化した。

**Why:** 太陽光条例の議案質疑本番原稿が"うまくいった方"で、その職人技を毎回ゼロから再発明していた。既存 bill-scrutiny-architect は「どの質疑を残すか」の設計書で止まり、演壇で読める本番原稿（凡例二層／タイムテーブル＋優先度マーカー／読み上げ散文／🔁条件付き返し／🔒想定答弁テーブル／★先制封じ／根拠弾／答弁回収シート）の craft が資産化されていなかった。一般質問側の council-material-creator も同8技法を持っていなかった。

**How to apply:**
- **共通craft**（議場本番原稿の8普遍技法）＝ `~/.claude/agents/knowledge/kusagawa_archive/01_council/_templates/honban_genko_craft_v1.md`。議案質疑・一般質問の**両方が読む土台**。
- **ゴールド見本**（実証済み）＝ 同フォルダ `GOLD_太陽光条例_議案質疑本番原稿.md`。毎回この型を模倣。
- **新agent** `bill-scrutiny-scriptwriter`（議案質疑の原稿化／council-material-creatorの議案質疑版）。トリガー「議案質疑の本番原稿作って」「議案質疑を原稿化」「答弁込み◯分に組んで」「太陽光みたいな質疑原稿にして」等。設計=architect→原稿化=scriptwriter→戦闘準備=counter-argument-simulator の分業。
- **council-material-creator** の一般質問原稿セクションも同craft＋一般質問の作法（提案/要望/決意は堂々と＝議案質疑とは逆／既決・報告返球封じ／答弁込み45分）で底上げ済み。
- **作法差分**：議案質疑＝意見表明は討論NG→受け/締めは短く（議長注意回避）。一般質問＝提案を厚く。共通craft §9 に明記。
- **注意**：新agentは [[feedback_agent_registry_partial_load]] によりCC再起動まで未登録の可能性。`Agent type not found`時はgeneral-purposeに bill-scrutiny-scriptwriter.md を読ませて成り代わらせる。
- 関連：[[feedback_general_question_architect_agent]]（一般質問設計の専任agent）。設計→原稿化の前後関係。
