---
name: 街頭演説は「最近のテーマ＝基軸／過去の蓄積＝乗せる素材」の階層で組む
description: daily-street-speechの組立順序。今日のホットニュース・直近テーマを基軸に置き、その上に草川8年の継続的取り組みを乗せて厚みを出す
type: feedback
originSessionId: 61dbb827-601a-4546-b7ab-2c8d51a78332
---
街頭演説の組立は **「最近のテーマ＝基軸／過去の蓄積＝乗せる素材」** という明確な階層で組む。

**Why:**
- 街頭演説の用途は「**毎日の街頭で、今日のテーマを探る**」こと（ohayoや政策提案ではなく、現場で何が刺さるか試行錯誤する場）
- 鮮度が無いと聴衆が立ち止まらない（「またあの話か」になる）
- 一方で鮮度だけだと「この人本当に政策やってきたのか」感が出て薄っぺらい
- 8年の蓄積を「乗せる」ことで継続性・本気度・専門性が伝わる
- 2026-05-06に「最近のテーマに絞られているのはあえて？それとも学習不足？」のフィードバックを受け、設計意図を確認

**How to apply:**
- daily-street-speech 起動時の組立順序：
  1. **基軸選定**：今日のホットニュース（news-briefing当日分）／直近nichijo／市民意見直近 から1〜2テーマ選ぶ
  2. **アーカイブ照合（必須）**：選んだ基軸テーマに関連する草川過去発言を `grep -rl "<キーワード>" ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,05_resources,06_election}/` で **最低3件** 引く
  3. **3pillars v0参照**：`~/.claude/agents/knowledge/kusagawa_archive/04_compass/3pillars/v0_handoff.md` の柱と接続できるか確認
  4. **layering構造で組む**：
     - 30秒掴み＝今日のニュース or 直近現場（鮮度100%）
     - 本論軸1＝今日のテーマを「8年前から私はこう取り組んできた」と接続（蓄積を乗せる）
     - 本論軸2＝隣接領域に拡張（過去の継続テーマで支える）
     - 本論軸3＝希望（今日の素材→将来像）
  5. **発言根拠の引用**：本論には過去発言・過去質問・過去成果を最低3カ所、具体的に織り込む（「令和○年○月議会で〜と質問しました」「○年○月の○○計画で〜」等）
- 1本の統一フロー（feedback_street_speech_unified_flow.md）と政策分散（feedback_street_speech_topic_diversity.md）は維持
- 選挙文脈最小化（feedback_street_speech_no_election_focus.md）も維持
- 「鮮度＝足が止まる理由」「蓄積＝信頼してもらえる理由」と覚える
