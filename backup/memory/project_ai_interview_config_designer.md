---
name: ai-interview-config-designerエージェント新設
description: 2026-04-30新設。政策テーマ→AIインタビュー(depth interview)設定編集8フィールドを設計するエージェント。ai-interview-sns-posterの逆処理
type: project
originSessionId: 92294fb5-0fe8-4273-a419-0917a8786207
---
# ai-interview-config-designer エージェント

**新設日**: 2026-04-30
**保存先**: `~/.claude/agents/ai-interview-config-designer.md`
**model**: opus / **color**: cyan

## 役割
政策テーマを入力 → `https://depth-interview-kusagawa.vercel.app/admin/configs/<config_id>` の管理画面に貼り付けて即運用可能なAIインタビュー設定編集の全フィールド内容を生成。

**Why**: ai-interview-sns-poster は完成したインタビュー回答 → SNS化（消費側）。本エージェントは逆向きで、新規インタビューのconfig設計（生産側）。両方揃ってAIインタビュープロジェクトの双方向自動化が完成。

**How to apply**:
- 新しいテーマでAIインタビューを立てたい時 → 本エージェント
- 既に回答が集まり投稿化したい時 → ai-interview-sns-poster
- 同じ「AIインタビュー」キーワードでも用途で完全分離

## ベンチマーク
`kameyama_bukatsu`（中学校部活動の地域移行ヒアリング）の完成度を基準とする。PDF参照: `_政治に声を届ける_ AIインタビュー（プロトタイプ）.pdf`

## 設計対象8セクション
1. 基本情報（タイトル/説明/推定時間/LLM/ステータス）
2. 初期挨拶
3. ナレッジソーステキスト（**実在する亀山市文書のみ**）
4. カスタムプロンプト（インタビュワー挙動指示）
5. ランディングページ概要
6. 質問テーマ5本（広→狭の階段構成）
7. プライバシーノート
8. 質問項目3〜5本（#1は固定形式、各ヒント3行）

## 命名規則
`config_id` = `kameyama_<snake_case_keyword>`
- 既存: `kameyama_bukatsu` / `kameyama_sougoukeikaku_bousai`
- 新規例: `kameyama_kaimono` / `kameyama_akiya` / `kameyama_taiki` / `kameyama_tsugakuro`

## 必須リサーチ連携（並列起動）
- **kameyama-researcher**: 亀山市の計画名・条例・統計・担当課・既存施策
- **policy-researcher**: 国動向・他自治体先進事例3件

## 任意リサーチ連携
- **policy-archive-miner**: 草川過去発言の確認
- **📋市民意見受付BOX**(354432ec-): 既存市民意見の検索
- **🎯政策候補DB**: 既存政策候補化状況

## 禁止事項
- 架空の計画名・条例名・統計禁止（kameyama-researcher出力ベース必須）
- generic AI fluff禁止（具体的な数字・地区名・担当課名で語る）
- 個人情報引き出し禁止（属性レベル止まり）
- 誘導質問禁止（公平な中立問い）
- 公選法配慮（投票依頼・選挙質問禁止）
- 難読語禁止（CLAUDE.md feedback整合）

## トリガーワード
- 「AIインタビュー設定を作って」
- 「新しいインタビューを設計」
- 「depth interviewの設定編集」
- 「〇〇テーマでAIインタビュー作成」
- 「ai-interview-config-designer」

## ai-interview-sns-poster との関係
| 観点 | config-designer（本エージェント） | sns-poster |
|---|---|---|
| 起点 | 政策テーマ | インタビュー回答要約 |
| 出力 | インタビュー設定編集8フィールド | SNS投稿原稿＋市民意見BOX登録 |
| タイミング | インタビュー開設前 | 回答収集後 |
| 連携 | kameyama-researcher / policy-researcher | 事例DB / 市民意見BOX |

## Notion連携済み
- エージェントトリガー一覧（id:34ecf503...818a）コンテンツ生成系セクションに追記済み
- カスタムエージェント総数: 23本 → 24本
