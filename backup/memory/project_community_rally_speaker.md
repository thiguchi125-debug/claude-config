---
name: community-rally-speakerエージェント新設
description: 2026-04-26新設。自治会総会・地区集会の短尺アジテーション挨拶専任。speech-writerの式典・長尺フォーマル系と棲み分け
type: project
originSessionId: dd8f1b22-bf50-4c11-95a3-c7704e21c8b9
---
2026-04-26新設。自治会総会・地区集会・町内会・後援会冒頭の3〜10分短尺アジテーション挨拶を専任で担当。

**Why**：自治会総会の挨拶は「報告型」ではなく「報告＋決意＋呼びかけ」のアジテーション型がベスト、と草川が確認。speech-writer（式典・長尺フォーマル）との重複を避けつつ、地元密着の短尺アジ専任エージェントを切り出した。

**How to apply**：
- 「自治会の挨拶」「地区集会で話す」「アジテーションスピーチ」等のトリガーで起動
- 5ブロック構成（掴み30秒→柱1〜3各2分→結び1分）
- 仮想敵は「縦割り」「市境の壁」「無関心」等の構造（個人攻撃しない）
- 必ず「3つの約束」を置く
- 出力は要点版／フル原稿の2モード

**コア資産**：
- エージェント本体：~/.claude/agents/community-rally-speaker.md
- ナレッジ：~/.claude/agents/knowledge/community_speech/
  - template_5blocks.md（構成テンプレート）
  - agitation_patterns.md（アジ作法8パターン）
  - killer_phrases.md（キラーフレーズ生成パターン7型）
  - reference_examples.md（過去事例メタデータ）
  - db_reference.md（地区別関係性メモDB ID等）
- Notion DB：🗺️地区別関係性メモ（data_source_id: 520fe503-116e-4e15-96d5-ed8f2cd8bd4a）
- Notionハブ：🤝地域挨拶・スピーチ集（id: 34ecf503-a68f-810b-a7ff-de6e6e18b509）

**第1号リファレンス**：二本松自治会総会（2026-04-26）— アジ型5ブロックの完成形

**並列起動連携**：kameyama-researcher（直近市政動向）、policy-archive-miner（過去発言・約束との整合）

**棲み分けルール**：speech-writer.md 冒頭に明記済み。「自治会／地区／町内会／アジテーション」 → community-rally-speaker、「所信表明／祝辞／弔辞／基調講演／式典」 → speech-writer。
