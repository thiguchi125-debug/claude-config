---
name: db-c2c34bd8-354432ec
description: 市民意見の唯一の正本はc2c34bd8（📝市民意見リスト）。旧354432ec（📦受付BOX）は廃止。書込/参照先の張替え完了記録
metadata: 
  node_type: memory
  type: feedback
  originSessionId: b1bffd68-56cd-488c-8f9a-ea845e4e5a17
---

市民意見の保存先は **📝市民意見リスト `c2c34bd8-1e16-492e-aab0-d3f497d18d4d` の一箇所のみ**。旧 **📋市民意見受付BOX `354432ec-6c3a-4a71-b649-ce53c6b74427`** は2026-05-02に廃止され、Notion上で「📦旧受付BOX（…市民意見リストへ統合済み）」に改名・アーカイブ済み。

**Why:** 2026-06-07、草川の「スマホ記録/報告会聞き取りがどこ行った」調査の派生で、354432ecがまだ生きていて孤立データを生んでいたことが判明。実態：
- 旧BOXに4件残存（#1若林データセンター/#2鈴鹿川河川敷/#3 AI#24/#4 AI#37）。#1〜#3は5/2にc2c34bd8へ移管済の重複、但し**#4「AIインタビュー#37 部活動地域移行」は廃止後の2026-05-23に新規登録された真の孤立データ**だった（→2026-06-07にc2c34bd8 [378cf503-a68f-811c-919b-c98224706472] へ移管救済）。
- 原因＝ライブのagent/skillが旧IDをWRITE/QUERY先として参照し続けていた。特に **ai-interview-sns-poster** がAIインタビュー由来の市民の声を354432ecへ書き込んでいた（#4漏れの犯人）。

**How to apply:**
- 市民意見の新規登録・検索は常に `c2c34bd8-`。`354432ec-` へは二度と書かない。
- フィールド名はc2c34bd8スキーマ：`件名(title)/相談者（氏名等）/分類タグ(multi)/受付日(date)/経路/緊急度/地区/担当課/意見内容/次アクション/対応メモ/匿名/関連タスク`。**対応状況(status)は廃止済で存在しない**（旧354432ecには有った）。タスク化は「関連タスク」relationでタスクDBへ抽出。
- 2026-06-07に張替え済のファイル：`ai-interview-sns-poster.md`(登録先+マッピング)／`ai-interview-config-designer.md`(クエリ)／`citizen-voice-analyst.md`(ソース)／`daily-content-generator/SKILL.md`(2箇所)。iken/nichijo本体は元々c2c34bd8で正常。
- **未処理の軽微ドリフト**: iken SKILL.md の description/overview(3・8行)が表示テキスト上「📋市民意見受付BOX(354432ec-)」のまま（plugins cacheでHARD BLOCKの可能性・本体ロジックは正常）。スキルピッカー表示のみの問題。直すなら claude-config 側ソースで。
- 旧354432ec DB自体の物理削除はNotion MCPに削除ツールが無く不可。消すならNotion UIで手動Trash（全4件はc2c34bd8に重複済・書込元も断ったため削除は無害）。但しアーカイブ放置でも実害なし。
- 旧2層モデルを記した [[市民意見受付BOX-ikenスキル]]（project_form_intake_db.md）は本一本化で上書き済み。正は [[市民意見DB再設計-永続ログタスク抽出モデル-2026-05-02]]（project_iken_db_redesign.md）。
