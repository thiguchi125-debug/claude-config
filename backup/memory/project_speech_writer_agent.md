---
name: speech-writerエージェント新設
description: 2026-04-24新設。歴代名演説の修辞知＋草川たくや voice-dna 融合の熱情的スピーチライター
type: project
originSessionId: c71e97b1-2ac0-4297-9136-ae5057fbcc67
---
草川たくや専属スピーチライターエージェント `speech-writer` を新設（2026-04-24）。

**位置づけ**：council-material-creator（一般質問）/ blog-writer / sns-content-creator では受け持たない、**フォーマルな演説・挨拶・弔辞・祝辞・所信表明・街頭演説・基調講演**の専任。

**Why**：SNS・ブログ・議会質問とは別に、「人の心を打つ熱情的かつ知性的なスピーチ」が必要な場面（後援会新年会、選挙キックオフ、式典祝辞、弔辞、党大会演説、シンポジウム基調講演など）で、歴代名演説の修辞知識と草川たくや voice-dna を融合して原稿化するため。

**How to apply**：
- トリガー：「スピーチを書いて」「演説原稿」「挨拶文」「所信表明」「祝辞」「弔辞」「年頭所感」「街頭演説」「熱い演説を作って」「名演説風に」「心を打つスピーチ」等
- 必ず voice-dna.md を事前読み込み（`~/.claude/plugins/cache/claude-plugins-official/skill-creator/unknown/skills/content-pipeline/references/voice-dna.md`）
- 参照 Canon：日本歴代首相（吉田茂・池田勇人・田中角栄・大平・中曽根・小泉・安倍・岸田）／明治（福沢諭吉・吉田松陰・新渡戸・内村）／英米欧（Lincoln・Churchill・JFK・MLK・Mandela・Obama・Reagan・Thatcher・Merkel・Zelensky）等
- 修辞ツール：Tricolon / Anaphora / Antithesis / Chiasmus / Pathos・Ethos・Logos配分 / 序破急・起承転結
- 必須入力：speech_type、duration、audience、purpose、key_message
- 出力：原稿本文＋修辞分析＋配信ノート（間・強弱・テンポ）＋代替フレーズ集
- **返却原則**：必ず全文をメッセージ本文に出力（省略・ファイル押し出し禁止。council-material-creator 失敗事例を踏襲）
- **不使用**：一般質問（→council-material-creator）、ブログ/SNS（→blog-writer/sns-content-creator）、政策調査（→policy-researcher）

**色**：red（赤＝熱情の象徴）
**model**：opus
**ファイル**：`~/.claude/agents/speech-writer.md`（365行）
