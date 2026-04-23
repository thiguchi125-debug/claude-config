---
name: 政策アップデートシステム
description: 2026-04-23新設。週次/月次で政策候補を常時アップデートする統合システム。/policy-updateスキル＋policy-synthesizerエージェント＋🎯政策候補DB＋NotebookLM手動エクスポート連携
type: project
originSessionId: 2150a3f9-fb22-40fa-9812-abd6ab7a5a0a
---
2026-04-23新設。草川たくや（亀山市議会議員）の政策候補を、亀山市政・県政・国政・社会トレンド・市民の声・NotebookLM・過去会話・ブログ/SNSを統合分析して常時アップデートし続けるシステム。

**Why:** 情報源が散在しており「市民の心を打つ政策」を機動的に更新する仕組みが必要だった。個別の調査エージェントはあったが、統合レイヤーと承認ワークフローが未整備。

**How to apply:** 政策立案・議会準備・市民発信の起点として使う。

## システム構成

- **/policy-update スキル**: オーケストレータ（週次／月次／オンデマンド3モード）
  - パス: `~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/policy-update/SKILL.md`
- **policy-synthesizer エージェント**: 統合分析専任（Notion直接書き込みしない）
  - パス: `~/.claude/agents/policy-synthesizer.md`
  - 一次調査は kameyama-researcher / policy-researcher に委譲
- **🎯政策候補DB**: Notion
  - URL: https://www.notion.so/b9f8d42a9c364acaab1bcabcd5132c40
  - data_source_id: `6f1895ac-3373-43b8-97d7-7ee4aa2791e0`
  - 親ページ（ハブ）: https://www.notion.so/34bcf503a68f819e9159f64c519993d2
- **NotebookLM エクスポート置き場**: `~/.claude/agent-memory/policy-synthesizer/knowledge/notebooklm/`
  - 命名規則: `YYYY-MM-DD_テーマ.md`
  - バックアップ対象外（機密情報保存禁止）

## 情報源の統合軸
- 亀山市政（kameyama-researcher）
- 国政・県政・先進事例（policy-researcher）
- 市民の声（📝市民意見リストDB）
- 社会トレンド（WebSearch）
- 草川発信チャンネル: X `kusakawa_kame` / Threads `kusagawatakuya` / Instagram `kusagawatakuya` / 選挙ドットコム `168135`
- 過去会話（`~/.claude/projects/` 配下 grep）
- NotebookLM手動エクスポート

## 承認ワークフロー（必須）
草案生成 → ユーザー（草川）に5択提示（A:全件承認／B:一部承認／C:草案保留／D:修正再提示／E:保存せず） → 承認分のみDB書き込み。**AI単独での自動確定禁止**。

## 週次/月次スケジュール
`/schedule` で登録する想定（ユーザー承認後）:
- 週次: 毎週月曜 7:47 JST（差分更新）
- 月次: 毎月1日 7:57 JST（棚卸し）

スケジュール未登録でもオンデマンド手動実行は可能。
