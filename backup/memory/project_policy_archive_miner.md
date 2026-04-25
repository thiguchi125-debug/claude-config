---
name: policy-archive-minerエージェント新設
description: 2026-04-25新設。草川たくやの過去8年発言・主張を議事録/ブログ/SNS/紙物から横断抽出し、テーマ別×時系列×論点別に構造化する歴史アーカイブ専任
type: project
originSessionId: 117eaaff-c146-4719-8294-a6baba4be080
---
2026-04-25、政策検討の上流に**過去アーカイブ層**を追加。policy-synthesizer（統合）の前段で必要なデータ層。

**役割**: 「過去8年で草川は何を言ってきたか」を、議事録・ブログ・SNS・紙物・nichijo・speech-writer出力を横断スキャンして体系化する。policy-researcher（外部）の自己側カウンターパート。

**保存先**: `~/.claude/agents/knowledge/kusagawa_archive/`
- `INDEX.md` - 全テーマ索引
- `themes/{テーマ}.md` - 主要主張/論点別/時系列進化/ギャップ分析/policy-synthesizer向けフィード
- `raw/` - 元データ抜粋（議事録/ブログ/SNS/チラシOCR）

**初回試運転（2026-04-25）**: 子育て・教育テーマでドラフト作成完了
- 主要主張5本抽出（「制度があっても使いにくければ届かない」等）
- 7論点（誰でも通園/産後ケア/オンライン化/施設再編/着替問題/部活動移行/5無料化）
- 一貫性スコアA、未触れ領域10件特定（学童質・特支・不登校・教員働き方・ヤングケアラー等）
- 短期/中期/長期の政策案候補を policy-synthesizer 向けに整理

**Why**: 「政策の質を上げる」には、新しい外部情報だけでなく**自己アーカイブの再活用**が必須。過去8年の主張連続性・進化軌跡をベースに、ギャップを国政・他自治体先進例で埋める二段構えにする。

**How to apply**:
- 政策3本柱の中身を詰める時 → 該当テーマファイル参照
- 「草川の過去発言を集めて」「アーカイブ抽出」「未触れトピック教えて」「voice-dna一貫性チェック」発話 → policy-archive-miner起動
- /policy-update の input source として組み込み

**6エージェント連携**:
```
policy-archive-miner（草川過去）
        +
kameyama-researcher（亀山市公式）
        +
policy-researcher（国政/他自治体）
        ↓
policy-synthesizer（統合→政策候補）
        ↓
policy-validator（EBPM検証, 将来作成予定）
        ↓
🎯政策候補DB（Notion）
```

**今後の課題**:
1. 議会会議録本文の体系的取込（kameyama-researcher経由）
2. 過去チラシのOCR取込ルート確立
3. policy-validator エージェント新設（EBPMチェック専任）
4. 暮らし・福祉、まちづくり・経済テーマファイルの構築
