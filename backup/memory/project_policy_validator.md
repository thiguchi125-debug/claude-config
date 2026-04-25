---
name: policy-validatorエージェント新設
description: 2026-04-25新設。EBPM 8軸検証専任。policy-synthesizer→🎯政策候補DBの間に位置するゲーティング層
type: project
originSessionId: 117eaaff-c146-4719-8294-a6baba4be080
---
2026-04-25、政策エージェント体系の最終ゲートとして policy-validator を新設。これで政策周りの完全パイプライン体制が確立。

**役割**: policy-synthesizerの出力を「いいアイデア」から「説得力ある政策」に昇格させる出荷前検証。市民・議会・メディアの厳しい視線に耐えるエビデンス・論理を保証。

**8軸EBPM検証**:
1. **エビデンス**: データソース・鮮度・出典明記
2. **他自治体実績比較**: 同規模自治体・先進事例・成功率
3. **費用試算**: 初期/運用/財源/ROI
4. **法的整合性**: 関連法令・条例・公選法
5. **過去主張連続性**: kusagawa_archive照合
6. **voice-dna整合**: 草川語彙・トーン・AIっぽさ排除
7. **KPI具体性**: 数値化・期限・測定方法
8. **反論準備**: 想定反論3-5件＋応答セット

**判定**: APPROVE / REVISE / REJECT
- APPROVE: 全軸B以上 + Critical fixゼロ + 平均B+以上
- REVISE: 1-3軸C + Critical fix 3以下 + 平均B-以上
- REJECT: D/E あり OR Critical fix 4以上 OR 法的整合性E

**4モード**:
- Standard 8軸全数
- 反論準備フォーカス（議会質問前夜）
- 対外発信物チェック（応援カード/SNS/ブログ）
- 議員提案条例草案チェック（法的整合最優先）

**Why**: 政策案の「フワッと感」を排除し、AIが提案した雛形がそのまま本番に流れないよう人間判断ゲートを必須化。voice-dna崩壊・エビデンス欠落・反論準備不足を構造的に防ぐ。

**完成した7エージェント連携**:
```
policy-archive-miner ─┐
kameyama-researcher ──┼─→ policy-synthesizer ─→ policy-validator ─→ 🎯政策候補DB
policy-researcher ────┘                              ↓
                                            council-material-creator
                                                  print-designer
                                                  sns-content-creator
                                                  speech-writer
```

**How to apply**: 
- 「政策案をEBPM検証して」「この政策案レビューして」「一般質問の前に裏付け確認」発話で起動
- /policy-update実行後の自動チェックポイントとして活用
- 応援カード/SNS/ブログの政策言及部分の事前検証にも使用
- 草川承認を経るまで本番反映しないルールを内蔵
