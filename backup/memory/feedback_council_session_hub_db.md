---
name: feedback-council-session-hub-db
description: 議会会期ハブDB（2026-05-12新設）の参照情報。/general-question-prep スキルで毎回使う
metadata: 
  node_type: memory
  type: reference
  originSessionId: f32b30c7-d45f-483d-b26a-fc1fc9466c58
---

# 🏛 議会会期ハブDB 参照

- DB page URL: https://www.notion.so/61bebeba2d814946bf8d817cd9dd3fcf
- data_source_id: collection://16842e7f-f34f-4242-a68c-fb59efcc2bc1
- 作成日: 2026-05-12
- 親ページ: 🗂️会議ハブ (a247fd5d-56da-4acd-b9db-3ad97cec6a12)
- 用途: 年4回の議会会期管理（kickoff/research/interview/draft/review/完了の6フェーズ）
- 主要relation: 📝一般質問ネタDB（テーマ枠）／🗂️プロジェクトDB（関連プロジェクト）
- スキーマ詳細: specs/council-session-hub-db-schema.md
- 注: 「フェーズ」プロパティはSELECT型で実装（STATUS型はDDLで初期オプション設定不可のため）
