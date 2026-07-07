# 答弁・約束台帳 スキーマ（ledger.json 正本定義）

> 正本はこのディレクトリの `ledger.json`。Notionミラーは閲覧用コピーであり編集禁止。
> 書込は toben-tracker エージェント経由・草川承認後のみ。手編集する場合は last_updated を更新すること。

## レコード構造（records[] の1要素 = 1約束）

```json
{
  "id": "R0706-01",
  "session": "R07-06",
  "date": "2025-06-17",
  "theme": "部活動地域移行",
  "question_summary": "草川の質問要旨（1〜2文）",
  "commitment_quote": "市答弁の原文引用。要約でなく逐語。",
  "quote_source": {
    "file": "01_council/2025-06_R0706_本会議議事録_kusagawa.txt",
    "locator": "該当箇所の目印（ページ・前後の語句など）"
  },
  "respondent": "教育長",
  "type": "検討約束",
  "status": "未回収",
  "due_hint": "2026-03議会",
  "evidence": [
    { "date": "2026-03-15", "what": "R8当初予算に◯◯費として計上", "source": "R8予算書 p.XX" }
  ],
  "attribution": {
    "is_kusagawa_origin": true,
    "note": "誤帰属ガード。他議員質疑由来・市の自発施策の場合は必ずここに明記し、実績集では草川起点として扱わない。"
  },
  "todoist_task_id": null,
  "published": ["blog:2026-04-01", "instagram"],
  "notes": ""
}
```

## フィールド規約

| フィールド | 規約 |
|---|---|
| id | `<会期>-<連番2桁>`（例 R0706-01）。会期表記は R0X0Y（令和X年Y月議会）、平成は H30 等 |
| type | `検討約束` / `実施約束` / `調査約束` / `数字約束`（数値・期日を明言）/ `ゼロ回答` の5値のみ |
| status | `未回収` / `進行中` / `実現` / `一部実現` / `停滞` / `後退` の6値のみ |
| commitment_quote | **逐語引用必須**。議事録からコピペし、語尾も変えない。実績集・議会だより等の下流はこの引用だけを使う |
| due_hint | 自由記述だが「YYYY-MM議会」「R◯予算」「◯◯計画改定」のいずれかの形を推奨（kickoff連携のマッチングに使う） |
| attribution | 実績コンパイル時の最重要ガード。is_kusagawa_origin=false のレコードは実績集に載せない（比較材料として使う場合は「市の施策」等の中立表記） |
| published | 発信済みチャネルの記録。`blog:日付` / `sns投稿管理DBのタイトル` / `チラシ名` 等。空配列=未発信（=発信ネタ候補） |

## 下流の締め工程

- **回収**: status=未回収/進行中 かつ due_hint が今会期・今年度予算に一致 → general-question-prep kickoff が自動提示
- **Todoist**: 登録は必ず「候補提示→草川承認→td.py add」。登録後 todoist_task_id を書き戻す
- **実績集**: status=実現/一部実現 かつ is_kusagawa_origin=true のみ。published が空のものは「未発信実績」としてギャップ一覧に出す
