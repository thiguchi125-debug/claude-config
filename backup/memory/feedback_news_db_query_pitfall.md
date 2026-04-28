---
name: ニュースDBクエリの落とし穴
description: ohayoスキルでニュース取得が無検出になる事故の再発防止。data_source_url の database/data_source 取り違えと query="ニュース" の0件失敗
type: feedback
originSessionId: bc6c839a-70c7-4247-b018-ea1016d5220e
---
ohayoスキル実行時、本日分のニュースが「未収集」と誤判定される事故が2026-04-29朝に発生した。

**Why**: 過去の対応:
1. `notion-search query="ニュース"` を叩いたが、**ニュース見出しに「ニュース」の語がなく0件**返却された（セマンティック検索の空回り）
2. `data_source_url: collection://f2eefc66-fa30-4f57-...` を渡したが、これは**database top-level ID**であり data source ID ではないため `Invalid Data Source URL` エラー
3. cronは正常に走っており、本日分8件（亀山関連度★5「自然と太陽光発電調和条例6月議会提出」含む）が収集済みだった

**How to apply**:
- ニュースDB取得は **必ず view_url 直接指定で notion-query-database-view を使う**：
  `https://www.notion.so/f2eefc669dd54648bbcdacdc8afa1158?v=9d34f9a4-2bc1-4381-a31b-8f8c8ac719e2`
- collection IDの正しい値:
  - ✅ `29e5c1a2-d64d-4822-81fd-0d642c3f07bc` (data source / collection)
  - ❌ `f2eefc66-fa30-4f57-8bba-3a1e57e4fe5a` (database top-level、data_source_url には使えない)
- notion-search の query 引数には意味のある単語を入れない（`"."` か空クエリ）
- 「0件」と判定する前に、必ず **view_url 直叩き** で全件取得→ローカルで日付フィルタを試す
- ohayo SKILL.md (Step 3-0) は2026-04-29に修正済み（事故事例も明記）
