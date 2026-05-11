---
name: ohayo に archive grep 連動を組み込み（v2.2）
description: 2026-05-08 草川指示「news-briefingに組むより ohayo に組むべき（耐障害性）」採用。news-briefing cron停止時もohayoがgrep連動を担保
type: feedback
originSessionId: 7e6bdb45-44e5-4890-b3d1-7774a1bce51d
---
ohayo SKILL.md に v2.2 として「🔍 過去発言連動（archive grep）」セクションを新設。

**Why（草川判断）:** 当初 news-briefing への組込みを推奨したが、草川「Cの方がいいのでは？」で再考の結果ohayoに組み込む方針に変更。理由：

1. **耐障害性**：news-briefing cron停止（2026-05-07・08連続停止と同種の事故）でも ohayo が動けば grep 連動は走る
2. **応用範囲**：ニュース以外（タスク・プロジェクト・市民意見）にも grep 連動を将来拡張可能
3. **思考フロー**：朝の人間思考「news → 自分の過去発言 → 議会活用」と一致

**How to apply:**
- ohayo起動時、🗞️今朝のニュース表示の直後に「🔍 過去発言連動」セクションを追加
- 上位3件のキーワード（5〜7字の地名・固有名詞・政策キーワード）を抽出
- `grep -l <キーワード> ~/.claude/agents/knowledge/kusagawa_archive/{01_council,02_publications,03_themes}/*.txt | head -5`
- ヒットファイルから上位2件を `grep -B1 -A4` で文脈抽出
- チャット出力のみ（Notion本文書込みなし・v2燃費方針踏襲）
- 追加トークン目安+10K（ohayo合計80K→90K前後）

**ヒット時のメリット:** 2026-05-08 実演で実証。「南海トラフ被害想定3月精緻化」ニュース → 草川がR070306で『最大3m浸水のハザードマップ予定地に庁舎は不適切』発言済を発見 → 議会活用メモが「県データ更新を機に庁舎建設地再検討を問う」という草川独自の議会戦略まで深化。
