---
name: kameyama-researcherエージェント新設
description: 亀山市ローカル調査専用エージェント。content-pipeline Step 1.5 / council-material-creator / citizen-inquiry-responder / nichijo から呼ばれる
type: project
originSessionId: aa31d0d4-8756-43b8-95ca-4230415f6438
---
2026-04-23 に `~/.claude/agents/kameyama-researcher.md` を新設。亀山市公式サイト・議会会議録検索・総合計画・予算書・三重県施策を調査する専任ロールを、policy-researcher から切り出した。

**Why:** content-pipeline の Step 1.5 が `kameyama-researcher` を subagent_type で参照していたが、エージェント本体は未作成だった（`content-pipeline/agents/kameyama-researcher.md` はプレイブック止まり）。亀山市固有の一次情報源・組織・過去議論への当たりを、policy-researcher（国・他自治体担当）から分離することで、並列調査が成立する。

## How to apply
- 亀山市特化の情報が必要な場合（現状確認・担当課特定・議会履歴・予算規模・条例確認）は **kameyama-researcher** を起動
- 国・他自治体・統計ベンチマークが必要な場合は **policy-researcher**
- 両方必要な場面（content-pipeline Step 1.5、一般質問準備）では **並列起動**
- 添付資料（PDF・スキャン・テキスト）は `/Users/kusakawatakuya/.claude/agent-memory/kameyama-researcher/knowledge/` に置く。エージェントは `knowledge_index.md` で索引管理
- エージェント固有メモリは `/Users/kusakawatakuya/.claude/agent-memory/kameyama-researcher/` 配下（policy-researcher の亀山市固有project memoryとは棲み分け：本エージェントは調査ノウハウ・一次情報源・資料indexが中心）

## 連携関係
- content-pipeline（Step 1.5 / Step 0-2）... policy-researcher と並列起動
- council-material-creator ... 出力を一般質問原稿の素材に投入
- citizen-inquiry-responder ... 担当課・既存施策の裏取りに利用
- nichijo ... 一般質問ネタ抽出時の即時裏取り
- ohayo ... 議会スケジュール確認（必要時のみ）

## 成果物の自動保存（2026-04-23 追加）
単発呼出・council-material-creator・citizen-inquiry-responder から呼ばれた場合、調査レポートを以下に自動保存する（content-pipeline からのJSON返却時はスキップ）：
- ローカル: `/Users/kusakawatakuya/Documents/kameyama-research/YYYY-MM-DD_{テーマ}_亀山市調査レポート.md`
- Notion 一般質問ネタDB
  - 親ページ: 一般質問ネタ・プラットフォーム（page_id: `5daccebabef34d2ca57ecc48a12e228c`）
  - データソース: `42716725-fece-497f-9782-705076539de4`
  - 重複チェック必須（既存なら追記更新）
  - プロパティ: ネタ名／分野／優先度／ネタ元／担当課（想定）／対象（定例会/時期）／次アクション／状況=調査中
